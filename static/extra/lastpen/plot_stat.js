

function plot_stat(){
var trace1 = {
  x: last_dice,
  marker: {
    color: "rgba(255, 100, 102, 0.7)", 
     line: {
      color:  "rgba(255, 100, 102, 1)", 
      width: 1
    }
  },  
  xbins: {
    end: 6.5, 
    size: 1, 
    start: 0.5,
  },
//  tickformat: ',d',
  opacity: 0.5, 
  type: "histogram", 
  name: "последние броски",
};
var trace11 = {
  x: prelast_dice,
  marker: {
    color: "rgba(255, 100, 102, 0.7)", 
     line: {
      color:  "rgba(255, 100, 102, 1)", 
      width: 1
    }
  },  
  xbins: {
    end: 6.5, 
    size: 1, 
    start: 0.5,
  },
//  tickformat: ',d',
  opacity: 0.5, 
  type: "histogram", 
  name: "предпоследние броски",
};
var trace2 = {
  x: sums,
  marker: {
    color: "rgba(40, 200, 102, 0.7)", 
     line: {
      color:  "rgba(40, 200, 102, 1)", 
      width: 1
    }
  },  
  opacity: 0.5, 
  type: 'histogram',
  name: 'суммы',
};
// may add left-to-right animation https://plot.ly/javascript/filled-area-animation/
var layout1 = {
  bargap: 0.05, 
  bargroupgap: 0.2, 
  barmode: "overlay", 
  title: "Распределение последних бросков", 
  xaxis: {
    tickvals: [1,2,3,4,5,6],
    fixedrange: true,
    },
};
var layout11 = {
  bargap: 0.05, 
  bargroupgap: 0.2, 
  barmode: "overlay", 
  title: "Распределение предпоследних бросков", 
  xaxis: {
    tickvals: [1,2,3,4,5,6],
    fixedrange: true,
    },
};
var layout2 = {
  bargap: 0.05, 
  bargroupgap: 0.2, 
  barmode: "overlay", 
  title: "Распределение сумм", 
  xaxis: {
    tickvals: [100,101,102,103,104,105],
    fixedrange: true,
  },
};
Plotly.newPlot('plot3', [trace1], layout1);
Plotly.newPlot('plot3.1', [trace11], layout11);
Plotly.newPlot('plot4', [trace2], layout2);
}

