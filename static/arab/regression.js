// modified version of https://bl.ocks.org/mph006/e225e45e044dcf89c222
var parentId = "#graph-wrapper";
var animDuration = 1000;
var margin = {top: 20, right: 50, bottom: 60, left: 130};

var width = $(parentId).width() - margin.left - margin.right,
    height = $(parentId).height()  - margin.top - margin.bottom;

var xScale = d3.scale.linear()
    .range([0,width]);

var yScale = d3.scale.linear()
    .range([height, 0]);

var line = d3.svg.line();

var xAxis = d3.svg.axis()
    .scale(xScale)
    .tickSize(-height)
    .tickPadding(8)
    .tickFormat(d3.round)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(yScale)
    .tickSize(-width)
    .tickPadding(8)
    .tickFormat(d3.round)
    .orient("left");

var svg = d3.select(parentId).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .attr("id","svg-parent")
    .append("g")
      .attr("id","graph-plane")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + (height) + ")")
    .call(xAxis);

svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate("  +0+ ",0)")
    .call(yAxis);

svg.append("path")
    .attr("class","trendline")
    .attr("stroke-width", 1)
    .style("stroke","steelblue")
    .style("fill","none");

svg.append("text")
            .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
            .attr("transform", "translate("+ (-50) +","+(height/2)+")rotate(-90)")  // text is drawn off the screen top left, move down and out and rotate
            .text("год выпуска по Григорианскому календарю");

svg.append("text")
            .attr("text-anchor", "middle")  // this makes it easy to centre the text as the transform is applied to the anchor
           .attr("transform", "translate("+ (width/2) +","+(height+40)+")")
            .text("год выпуска по арабскому календарю");

function getDimensions(coins){
  var returnX=[];
  var returnY=[];
  var returnPairs = [];
  coins.forEach(function(d){
    let a = parseInt(d['Арабский']);
    let g = parseInt(d['Григорианский']);
    var pair = {x: a,y: g};
    returnPairs.push(pair);
    returnX.push(a);
    returnY.push(g);
  });
  return {x:returnX,y:returnY,pairs:returnPairs};
}

function updateTitle(x,y){
  var title = d3.select("#title").text("Линейная регрессия: годы выпуска монет по арабскому и Григорианскому календарям");
}

// returns slope, intercept and r-square of the line
//Pulled from http://bl.ocks.org/benvandyke/8459843
function leastSquares(xSeries, ySeries) {
  var reduceSumFunc = function(prev, cur) { return prev + cur; };
  
  var xBar = xSeries.reduce(reduceSumFunc) * 1.0 / xSeries.length;
  var yBar = ySeries.reduce(reduceSumFunc) * 1.0 / ySeries.length;

  var ssXX = xSeries.map(function(d) { return Math.pow(d - xBar, 2); })
    .reduce(reduceSumFunc);
  
  var ssYY = ySeries.map(function(d) { return Math.pow(d - yBar, 2); })
    .reduce(reduceSumFunc);
    
  var ssXY = xSeries.map(function(d, i) { return (d - xBar) * (ySeries[i] - yBar); })
    .reduce(reduceSumFunc);
    
  var slope = ssXY / ssXX;
  var intercept = yBar - (xBar * slope);
  var rSquare = Math.pow(ssXY, 2) / (ssXX * ssYY);
  
  return [slope, intercept, rSquare];
}
//http://snipplr.com/view/37687/random-number-float-generator/
function randomFloatBetween(minValue,maxValue,precision){
    if(typeof(precision) == 'undefined'){
        precision = 2;
    }
    return parseFloat(Math.min(minValue + (Math.random() * (maxValue - minValue)),maxValue).toFixed(precision));
}

//"draw" the line with many points respecting the calculated equation
function calculateLineData(leastSquares,xRange,iterations){
  var returnData = [];
  for(var i=0; i<iterations; i++){
    var randomX = randomFloatBetween(xRange[0],xRange[1]);
    returnData.push({
      xVal:randomX,
      yVal: (randomX*leastSquares[0])+leastSquares[1]
    });
  }
  return returnData;
}

function updateChart(){

  updateTitle("Арабские монеты: график годов");
  //Fetch data
    var table = document.querySelector("table");
    var allcoins  = parseTable(table);
    coins = allcoins.filter(function(x){ return x['✔']=='✔'});
    if (coins.length<2) {coins = [allcoins[0],allcoins[1]]; }
    //console.log(coins);
    //return;
    var records = getDimensions(coins);
  // console.log('records', records)

  //Reset scale
  yScale.domain(d3.extent(records.y));
  xScale.domain(d3.extent(records.x));

  //re-assign data (or assign new data)
  var selectedCircles = d3.select("#graph-plane")
                          .selectAll(".circles")
                          .data(records.pairs)

  //give a transition on the existing elements
  selectedCircles
    .transition().duration(animDuration)
    .attr("transform",function(d){return "translate("+xScale(d.x)+","+yScale(d.y)+")";})
    .style("fill","steelblue");

  //Append any new elements and transition them as well
  selectedCircles.enter()
                .append("circle")
                .attr("class","circles")
                .attr("r",5)
                .style("fill","steelblue")
                .transition().duration(animDuration)
                .attr("transform",function(d){return "translate("+xScale(d.x)+","+yScale(d.y)+")";});

  //Remove any dom elements which are no longer data bound
  selectedCircles.exit().remove();
                  
  //Update Axes
  d3.select(parentId).select(".x.axis").transition().duration(animDuration).call(xAxis);
  d3.select(parentId).select(".y.axis").transition().duration(animDuration).call(yAxis);

  //Update Regression
  line.x(function(d) { return xScale(d.xVal); })
      .y(function(d) { return yScale(d.yVal); });

  var leastSquaresCoeff = leastSquares(records.x, records.y);
  var lineData = calculateLineData(leastSquaresCoeff,d3.extent(records.x),200);

  var trendline = d3.selectAll(".trendline")
                        .transition().delay(1000).duration(500)
                        .attr("d",line(lineData));

  d3.select("#equation").text( 
      "Уравнение прямой: y="+leastSquaresCoeff[0].toFixed(2)+"x"+((leastSquaresCoeff[1].toFixed(2)<0)?"":"+")+
          leastSquaresCoeff[1].toFixed(2)+",   год переселения: "+
          Math.floor(leastSquaresCoeff[1].toFixed(2))
  );
}

$( document ).ready(function() {
  updateChart();
        $("#coins").tablesorter(); 
});

$( 'tbody' ).on( 'click', 'td:first-child', function() {
    $( this ).parent().toggleClass( 'unchecked' );
    if ($( this ).parent().hasClass('unchecked')) {
    $( this ).html('&#10005;')    
    } else {
    $( this ).html('&#10004;')
    }
    updateChart();
});


/*$( 'thead' ).on( 'click', 'th:first-child', function() {
    $('td:first-child').trigger('click');    
    updateChart();
});*/
