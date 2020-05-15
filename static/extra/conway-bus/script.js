var bmax = 40;

function product(array){
  let p=1
  for (var i of array){
    p = p*i
  };
  return p;
}

function obj2str(o){
  return Object.keys(o).map(function(k){return k+": "+o[k]}).join(', ')
}

function emptydiv(div){
    while (div.firstChild) {
    div.removeChild(div.lastChild);
  }
}


function abc() {
  let min_child_age = 2;
  let max_age = 300;
  let points2 = Array.from(Array(max_age+1), _ => Array(bmax+1).fill(0));
  for (let b = 1; b <= bmax; b++) {
    for (let bc_diff = 0; bc_diff < b; bc_diff++){
      let c = b - bc_diff;
      let n = b - min_child_age*c;
      if (n<1) continue;

      for (let zs of zs1(n)){
        if (zs.length > c) continue;
        for (let i=0; i<c;i++){
          zs[i] = i<zs.length ? zs[i]+ min_child_age : min_child_age
        };
        let a = product(zs);
        if (a>max_age) continue;
        //console.log(zs);
        if (points2[a][bc_diff] == 0) points2[a][bc_diff] = new Array();
        points2[a][bc_diff].push([a, b, c, zs])
      };
    };
      
  }
  return points2;
};

let points2d = abc();

let B_start = 20;

var slider_options = {
    start: [B_start],
    step: 1,
    connect: true,
    range: {
        'min': 1,
        'max': bmax,
    },
    tooltips: true,
    pips: {
        mode: 'steps',
        stepped: true,
        filter: function(value, type){return value%20?(value%5?0:2):1},
    },
    margin: 0,
    format: wNumb({
        decimals: 0
    }),
}



function tooltip(solutions){
  let combined_by_b = Object();
  solutions.forEach(function(s){
    let b = s[1];
    if(!combined_by_b[b]) combined_by_b[b] = new Array();
    combined_by_b[b].push(s[3])
  });
  //console.log(combined_by_b);
  return 'B='+Object.keys(combined_by_b).map(function(b){
    //console.log(b);
    return ''+b+': '+combined_by_b[b].map(arr => '['+arr.join(',')+']').join('; ')
  }).join('; B=');
}


function chart_datasets(b_max){
  var data = []  
  points2d.forEach(function (row, a){
    row.forEach(function (solutions, d){
      if (solutions==0) return;
      solutions = solutions.filter(sol => sol[1]<b_max)
      if (solutions.length==0) return;
      data.push({
          'x':d,
          'y':a,
          'v':solutions.length,
          'r':solutions.length*5,
      })
      
  })});
  
  return [{
            label: '1',
            data: data.filter(d => d.v==1),
            "backgroundColor":"rgb(70, 70, 70)"
        },{
            label: '2',
            data: data.filter(d => d.v==2),
            "backgroundColor":"rgb(255, 0, 100)"
        },{
            label: '3 и больше',
            data: data.filter(d => d.v>2),
            "backgroundColor":"rgb(0, 255, 100)"
        }]
  
}

function draw2d(b_max){  
  emptydiv('heatmap');
  var canvas = document.getElementById('heatmap');
  var ctx = canvas.getContext("2d");

  var scatterChart = new Chart(ctx, {
    type: 'scatter',
    data: {
        datasets: chart_datasets(b_max)
    },
    options: {
        scales: {
            xAxes: [{
                type: 'linear',
                position: 'bottom'
            }]
        },
        tooltips: {
          callbacks: {
            label: function(tooltipItem, data){
              //console.log(data);
              //console.log(tooltipItem);
              var item = data.datasets[tooltipItem.datasetIndex]['data'][tooltipItem.index];
              var solutions = points2d[item.y][item.x];
              //console.log(item);
              //console.log(points2d[+item.y]);
              //console.log(solutions);
              return tooltip(solutions);
              
            }
          }
        }
    }
  });
  return scatterChart;
}

let sliderB = document.getElementById('sliderB');  
noUiSlider.create(sliderB, slider_options);

var chart = draw2d(B_start);

sliderB.noUiSlider.on('update', function (values, handle) {
  var maxb = values[handle];
  chart.data.datasets = chart_datasets(maxb)
  chart.update();
});
