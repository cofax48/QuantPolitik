(function(whole_data) {

var whole_data = [];
d3.json('http://www.quantpolitik.com/api/QP_Score', function(error, incomingData) {
  var today = new Date();
  var dd = today.getDate();
  var monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
  ];
  var mm = today.getMonth(); //January is 0!
  var month_name = monthNames[mm]
  var yyyy = today.getFullYear();
  if(dd<10) {dd='0'+dd}
  if(mm<10) {mm='0'+mm}
  today = month_name+'-'+dd+'-'+yyyy;
  var column_to_use = today;
  console.log(today);
  for (var i in _.range(198)) {if (whole_data.length == 197) {mapDraw()}
  else {
    whole_data.push({Country_Name:incomingData[0][i]["Country_Name"], id:incomingData[0][i]["Iso3"], value:incomingData[0][i][column_to_use]});};
}
    });
function mapDraw() {
console.log('yayyyyy');

var width = 1600, height = 840;

var zoom = d3.behavior.zoom()
    .scaleExtent([1, 5])
    .on("zoom", moveAndZoom);

var svg = d3.select("svg#ChoroplethMap")
    .attr({ width: width, height: height })
    .call(zoom);
var mainGroup = svg.append("g");
mainGroup.style({ stroke: "white", "stroke-width": "2px", "stroke-opacity": 0.0 });

var projection = d3.geo.mercator();
var path = d3.geo.path().projection(projection);

var url = 'https://gist.githubusercontent.com/d3byex/65a128a9a499f7f0b37d/raw/176771c2f08dbd3431009ae27bef9b2f2fb56e36/world-110m.json';

d3.json(url, function (error, world) {
    var countries = topojson.feature(world, world.objects.countries).features;
    var neighbors = topojson.neighbors(world.objects.countries.geometries);

    var country_value_and_iso = {};
    whole_data.forEach(function(d) {
      country_value_and_iso[d.id] = +d.value;
      country_value_and_iso[d.Country_Name] = +d.id;
    });
    var country_name_and_iso = {};
    whole_data.forEach(function(d) {
      country_name_and_iso[d.id] = d.Country_Name;
    });


    var maxValue = d3.max(whole_data, function(d) {
      return parseFloat(d.value);})
    var color_domain = [0,maxValue];
    var colorQuantize = d3.scale.quantize()
        .domain(color_domain)
        .range(["#2c7bb6", "#00a6ca","#00ccbc","#90eb9d","#ffff8c","#f9d057","#f29e2e","#e76818","#d7191c"]);

        //////////////////////////////////////////////////////////////////
        ////
        ////    Legend Legend Legend Legend Legend Legend Legend Legend
        ////
        //////////////////////////////////////////////////////////////////
        console.log('65', whole_data);

        var legendWidth = 140, legendHeight = 400;
        var key = d3.select("svg#ChoroplethMap").append("svg")
                     .attr("width", legendWidth)
                     .attr("height", legendHeight);

        //Append a linearGradient element to the defs
        var legend = key.append("defs").append("svg:linearGradient")
                          .attr("id", "gradient")
                          .attr("x1", "100%")
                          .attr("y1", "0%")
                          .attr("x2", "100%")
                          .attr("y2", "100%")
                          .attr("spreadMethod", "pad");

      //set the color for the beggining
      legend.selectAll("stop")
      .attr("offset", "0%")
      .data([
          {offset: "0%", color: "#d7191c"},
          {offset: "12.5%", color: "#e76818"},
          {offset: "25%", color: "#f29e2e"},
          {offset: "37.5%", color: "#f9d057"},
          {offset: "50%", color: "#ffff8c"},
          {offset: "62.5%", color: "#90eb9d"},
          {offset: "75%", color: "#00ccbc"},
          {offset: "87.5%", color: "#00a6ca"},
          {offset: "100%", color: "#2c7bb6"}
        ])
        .enter().append("stop")
        .attr("offset", function(d) { return d.offset; })
        .attr("stop-color", function(d) { return d.color; })
        .attr("stop-opacity", 1);

        //Draw the rectangle and fill with gradient
        key.append("rect")
          .attr("id", "legendRect")
          .attr("width", legendWidth - 100)
          .attr("height", legendHeight -100)
          .style("fill", "url(#gradient)")
          .attr("transform", "translate(0,90)");

        var legendY = d3.scale.linear()
                        .range([300, 0])
                        .domain([0,maxValue]);

        var yAxis = d3.svg.axis()
                      .scale(legendY)
                      .orient("right");

        key
        .append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(41,90)")
        .call(yAxis).append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 50)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Colored Scale for QuantPolitik");

        ///////////////////////////////////////////////////////////
        ///End Legend End Legend End Legend End Legend End Legend
        ///////////////////////////////////////////////////////////


    //Coloring of the world
    mainGroup.selectAll("path", "countries")
        .data(countries)
        .enter().append("path")
        .attr("d", path)
        .style("fill", function (d) {
            return colorQuantize(country_value_and_iso[d.id]);});

    // Define the div for the tooltip
    var div = d3.select(".box .image.featured").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    mainGroup
        .selectAll("path")
        .data(countries)
        .on("mouseover", function (p) {
                  div.transition()
                      .duration(200)
                      .style("opacity", .9);
                  div	.html(country_value_and_iso[p.id])
                      .style("left", (d3.event.pageX) + "px")
                      .style("top", (d3.event.pageY - 28) + "px");
                  div.html(country_name_and_iso[p.id] + " 's QuantPolitik Score:" + "<br/>" + country_value_and_iso[p.id]);
            d3.select(this).style("stroke-opacity", 1.0);
        });
    mainGroup.selectAll("path")
        .on("mouseout", function () {
            d3.select(this).style("stroke-opacity", 0.0);
        });
});

function moveAndZoom() {
    var t = d3.event.translate;
    var s = d3.event.scale;

    var x = Math.min(
        (width / height) * (s - 1),
        Math.max(width * (1 - s), t[0]));

    var h = height / 4;
    var y = Math.min(
        h * (s - 1) + h * s,
        Math.max(height * (1 - s) - h * s, t[1]));

    mainGroup.style("stroke-width", ((1 / s) * 2) + "px");
    mainGroup.attr('transform', 'translate(' + x + ',' + y + ')scale(' + s + ')');
}
}//MapDraw
}(window.qpcore = window.qpcore || {}));
