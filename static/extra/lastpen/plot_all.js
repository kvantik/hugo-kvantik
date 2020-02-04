

function plot_all(){
var trace1 = {
  x: throws,
  y: last_dice,
  marker: {
    color: "rgba(255, 100, 102, 0.7)", 
     line: {
      color:  "rgba(255, 100, 102, 1)", 
      width: 1
    }
  },  
  opacity: 0.5, 
  type: "bar", 
  name: "последние броски",
};
var trace2 = {
  x: throws,
  y: sums,
  yaxis: 'y2',
  marker: {
    color: "rgba(40, 200, 102, 0.7)", 
     line: {
      color:  "rgba(40, 200, 102, 1)", 
      width: 1
    }
  },  
  opacity: 0.5, 
  type: 'bar',
  name: 'суммы',
};
// may add left-to-right animation https://plot.ly/javascript/filled-area-animation/
var data = [trace1, trace2];
var layout = {
  bargap: 0.05, 
  bargroupgap: 0.2, 
  barmode: "overlay", 
  title: "Все серии бросков", 
  xaxis: {title: "Номер броска"}, 
  yaxis: {
    title: "Последний бросок",
    range: [0, 6],    
    },
  yaxis2: {
    title: 'Сумма',
    titlefont: {color: 'rgb(148, 103, 189)'},
    tickfont: {color: 'rgb(148, 103, 189)'},
    overlaying: 'y',
    side: 'right',
    range: [100, 106],
  },
};
Plotly.newPlot('plot2', data, layout);
}

