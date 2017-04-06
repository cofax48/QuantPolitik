var qpSVG = d3.select("svg#qpBarChart")
    .attr({ width: '75%', height: '35%' })
    .style({ border: "lightgray solid", "stroke-width": "1px" })
    .append("g")
    .attr("id", "BarChart")
    .attr("transform", "translate(50,100)") //This determines where the bar graph is
    .selectAll("g")
    .data(whole_data)
    .enter()
    .append("g")
    .attr("class", "BarG") //This determines the tag for the Bar Graph
    .attr("transform",
      function (d,i) {return "translate(" + (i * 50) + ", 0)"} //This determines how far away each datapoint is
    );


    var BarGraph = d3.selectAll("g.BarG");
    BarGraph
      .append("rect")
      .transition()
      .delay(function(d,i) {return i * 100})
      .duration(500)
      .attr("height", 40)
      .transition()
      .duration(300)
      .attr("height", 20)
      .attr("width", 10)
      .style("stroke", "black")
      .style("fill", "pink")
      .style("stroke-width", "1px");

      BarGraph
        .append("text")
        .style("text-anchor", "middle")
        .attr("y", -10)
        .style("font-size", "10px")
        .text(function(d) {return d.Country_Name;}); //This sets the Text

    function barButtonClick(datapoint) {

      // Define the div for the tooltip
      var div = d3.select("body").append("div")
          .attr("class", "tooltip")
          .style("opacity", 0);

      var maxValue = d3.max(whole_data, function(d) {
        return parseFloat(d[datapoint]);
      });
      var colorQuantize = d3.scale.quantize()
        .domain([0,maxValue]).range(colorbrewer.Greens[5]);
      console.log(colorQuantize);
      var radiusScale = d3.scale.linear()
        .domain([0,maxValue]).range([2,30]);
      var yScale = d3.scale.linear()
        .domain([0,maxValue]).range([0,100]);
      d3.selectAll("g.BarG").select("rect").transition().duration(1000)
        .style("fill", function(p) {
          return colorQuantize(p[datapoint]);
        }).attr("height", function(p) {
          return yScale(p[datapoint]);
        });

    BarGraph
    .data(whole_data)
    .select("rect")
    .on("mouseover", function(p) {
          div.transition()
              .duration(200)
              .style("opacity", .9);
          div.html(p[datapoint])
              .style("left", (d3.event.pageX) + "px")
              .style("top", (d3.event.pageY - 28) + "px");
          div.html(datapoint + ":" + "<br/>" + p[datapoint]);
          })
  .on("mouseout", function(p) {
      div.transition()
          .duration(500)
          .style("opacity", 0);
    })
