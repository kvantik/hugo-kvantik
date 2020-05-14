var slider_options = {
    start: [1, 20],
    step: 1,
    connect: true,
    range: {
        'min': 1,
        'max': 100,
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

var sliders = ['sliderA','sliderB','sliderC']

sliders.forEach(function(value) {
  let slider = document.getElementById(value);  
  let slider_max = document.getElementById(value+'-max');
  let slider_min = document.getElementById(value+'-min');
  
  noUiSlider.create(slider, slider_options);
  
  slider.noUiSlider.on('update', function (values, handle) {
    var val = values[handle];
    if (handle) {
        slider_max.value = val;
    } else {
        slider_min.value = val;
    }
  });

  slider_max.addEventListener('change', function () {
    slider.noUiSlider.set([null, this.value]);
  });
  slider_min.addEventListener('change', function () {
    slider.noUiSlider.set([this.value, null]);
  });
});

document.getElementById('sliderA').noUiSlider.set([null,100]);

function get_abc() {
  let slider_get = function(value){
    return document.getElementById('slider'+value).noUiSlider.get()
  };
  return {'A':slider_get('A'),'B':slider_get('B'),'C':slider_get('C')}
}

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

function answers_abc() {
  let div = document.getElementById('answers');
  let units_allowed = document.querySelector('#units').checked;
  let abc = get_abc()
  let min_value = units_allowed? 1:2 ;
  
  while (div.firstChild) {
    div.removeChild(div.lastChild);
  }
  
  let single_a = []
  
  for (let b = abc['B'][0]; b <= abc['B'][1]; b++) {
      for (let c = abc['C'][0]; c <= abc['C'][1]; c++) {
        let n = b - min_value*c;
        if(n<1) continue;
        let ages = new Object;

        for (let zs of zs1(n)){
          if (zs.length > c) continue;
          for (let i=0; i<c;i++){
            zs[i] = i<zs.length ? zs[i]+min_value : min_value
          };
          let a=product(zs);
          if(abc['A'][0]<=a && a<=abc['A'][1]){
            if (a in ages) ages[a].push(zs);
            else ages[a]= [zs];
          };
        };
        ages_keys = Object.keys(ages);
        if (ages_keys.length<1) continue;
        let div_bc = document.createElement("div");
        div.appendChild(div_bc);
        multiple_decompositions = ages_keys.filter(p => ages[p].length > 1)
        
        if (multiple_decompositions.length == 1){
          a = multiple_decompositions[0]
          single_a.push({'возраст':a, 'номер автобуса':b, 'детей':c,'возрасты детей':ages[a]})
        }
          
        
        let div_bc_p = document.createElement("p");
        div_bc.appendChild(div_bc_p);
        div_bc_p.textContent = 'Автобус №'+b+'; '+c+' детей; '+multiple_decompositions.length+' возрастов с несколькими вариантами'
        div_bc_p.textContent += multiple_decompositions.length>0? ', а именно: '+multiple_decompositions.join(', '):' '
        div_bc_p.textContent += 'вот варианты для возможных возрастов:'
        for (a in ages){
          let div_abc = document.createElement("div");
          div_bc.appendChild(div_abc);
          div_abc.textContent = 'варианты для возраста '+a+':\n' +ages[a].join('\n')
        }
  
  
  }};

  let div_sum = document.getElementById('summary');
  div_sum.textContent = 'Подходящие варианты, где для данных номера автобуса и количества детей существует единственный возраст папы с несколькими вариантами для возрастов детей:'
  for (var triple of single_a){
    let p = document.createElement("p");
    div_sum.appendChild(p);
    p.textContent = obj2str(triple);
  }
  
};