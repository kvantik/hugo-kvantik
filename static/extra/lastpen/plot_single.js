

function plot_single(results){
var trace1 = {
  x: results.i,
  y: results.dice,
  marker: {
    color: "rgba(255, 100, 102, 0.7)", 
     line: {
      color:  "rgba(255, 100, 102, 1)", 
      width: 1
    }
  },  
  opacity: 0.5, 
  type: "bar", 
  name: "броски",
};
var trace2 = {
  x: results.i,
  y: results.sum,
  yaxis: 'y2',
  marker: {
    color: "rgba(40, 200, 102, 0.7)", 
     line: {
      color:  "rgba(40, 200, 102, 1)", 
      width: 1
    }
  },  
  opacity: 0.5, 
  type: 'scatter',
  name: 'сумма',
};
// may add left-to-right animation https://plot.ly/javascript/filled-area-animation/
var data = [trace1, trace2];
var layout = {
  bargap: 0.05, 
  bargroupgap: 0.2, 
  barmode: "overlay", 
  title: "Броски кубика", 
  xaxis: {
    title: "Номер броска",
    fixedrange: true,
    }, 
  yaxis: {
    title: "Выпавшее число",
    fixedrange: true,
    },
  yaxis2: {
    title: 'Сумма',
    titlefont: {color: 'rgb(148, 103, 189)'},
    tickfont: {color: 'rgb(148, 103, 189)'},
    overlaying: 'y',
    side: 'right',
    fixedrange: true,
  },
};
Plotly.newPlot('plot1', data, layout);
}

plot_single({i:[1,2,3],dice:[0,0,0],sum:[0,0,0]});

