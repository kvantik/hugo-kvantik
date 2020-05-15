
function draw2d(points){
  var data = []
  points.forEach(function (pi, i){
    pi.forEach(function (pj, j){
      if (pj>0){
        data.push({
          'x':i,
          'y':j,
          'v':pj,
        })
      }
    })
  
  var canvas = document.getElementById('plot');
  var ctx = canvas.getContext("2d");

  var scale = 1;

  var size = 30;
  var heatmapColor = d3.scale.linear()
    .domain([d3.min(data, function(d) { return d.v; }), d3.max(data, function(d) { return d.v; })])
    .range(["#6363FF",  "#FF6364"]);
  canvas.width = size * scale;
  canvas.height = size * scale;

  data.forEach(function (d) {
    ctx.fillStyle = heatmapColor(d.v);
    ctx.fillRect(d.x * scale, d.y * scale, (d.x + 1) * scale, (d.y + 1) * scale);
  });  
}
