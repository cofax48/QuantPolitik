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

function onLoad() {

  //http://localhost:5000/api/QP_Score
  var whole_data = [{Country_Name:'placeHolder', value:0}];
  d3.json('http://www.quantpolitik.com/api/QP_Score', function(error, incomingData) {
    for (var i in _.range(198)) {if (whole_data.length == 198) {mapDraw(), qpBarChart()}
    else {
      whole_data.push({Country_Name:incomingData[0][i]["Country_Name"], id:incomingData[0][i]["Iso3"], value:incomingData[0][i][column_to_use]});};
  }
      });
  function mapDraw() {

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

      var minValue = d3.min(whole_data, function(d) {
            return parseFloat(d.value);})

      var color_domain = [minValue,maxValue];
      var colorQuantize = d3.scale.quantize()
          .domain(color_domain)
          .range(["#d7191c", "#d7411c", "#e76818", "#e79018", "#f29e2e", "#f9ad57", "#f9d057", "#f9dc8c", "#ffeb8c",
          "#ffeb8c", "#c7eb9d", "#90eb9d", "#00ccbc", "#00a6ca", "#0060ca", "#0006ca"]);

          //////////////////////////////////////////////////////////////////
          ////
          ////    Legend Legend Legend Legend Legend Legend Legend Legend
          ////
          //////////////////////////////////////////////////////////////////

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
            {offset: "0%", color: "#0006ca"},
            {offset: "6.25%", color: "#0060ca"},
            {offset: "12.5%", color: "#00a6ca"},
            {offset: "18.75%", color: "#00ccbc"},
            {offset: "25%", color: "#00ccbc"},
            {offset: "32.25%", color: "#48eb9d"},
            {offset: "37.5%", color: "#90eb9d"},
            {offset: "43.75%", color: "#c7eb9d"},
            {offset: "50%", color: "#ffeb8c"},
            {offset: "56.25%", color: "#f9dc8c"},
            {offset: "62.5%", color: "#f9d057"},
            {offset: "68.75%", color: "#f9ad57"},
            {offset: "75%", color: "#f29e2e"},
            {offset: "82.25%", color: "#e79018"},
            {offset: "87.5%", color: "#e76818"},
            {offset: "93.75%", color: "#d7411c"},
            {offset: "100%", color: "#d7191c"}
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
                          .domain([minValue,maxValue]);

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

  function qpBarChart() {

    var margin = {top: 20, right: 30, bottom: 40, left: 30},
        width = 960 - margin.left - margin.right,
        height = 5000 - margin.top - margin.bottom;

    var x = d3.scale.linear()
        .range([0, width]);

    var y = d3.scale.ordinal()
        .rangeRoundBands([0, height], 0.1);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .tickSize(0)
        .tickPadding(6);

    var svgbar = d3.select("svg#qpBarChart")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


      x.domain(d3.extent(whole_data, function(d) { return d.value; })).nice();
      y.domain(whole_data.map(function(d) { return d.Country_Name; }));


      svgbar.selectAll(".bar")
          .data(whole_data)
        .enter().append("rect")
          .attr("class", function(d) { return "bar bar--" + (d.value < 0 ? "negative" : "positive"); })
          .attr("x", function(d) { return x(Math.min(0, d.value)); })
          .attr("y", function(d) { return y(d.Country_Name); })
          .attr("width", function(d) { return Math.abs(x(d.value) - x(0)); })
          .attr("height", y.rangeBand());

      svgbar.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis);

      svgbar.append("g")
          .attr("class", "y axis")
          .attr("transform", "translate(" + x(0) + ",0)")
          .call(yAxis);


    function type(d) {
      d.value = +d.value;
      return d;
    }

    }//qpBarChart

qpBarChart();

}//ONLOAD

function createDataViz() {

  var data_table_names = ["QP_Score", "UN", "Trade_Relations", "Security", "Business_Relations", "Country_Profile", "Cultural_Diffusion", "Governmental_Perspective", "Presidential_Exchange", "Prestige", "Sec_State_Bureaucratic_Exchange"];

  var select = d3.select('div#reportrange.pull-right')
    .append('select')
    	.attr('class','select')
      .on('change',onchange);

  var options = select
    .selectAll('div#dashboard_graph')
  	.data(data_table_names).enter()
  	.append('option')
    .on("click", onchange)
  	.html(function (d) { return d; });

  function onchange() {
  	var selectValue = d3.select('select.select').property('value');
    d3.json('http://localhost:5000/api/' + selectValue, function(error, incomingData) {
      incomingData = incomingData[0];

    var table_name = incomingData;
    var all_data_for_map = incomingData;
    var whole_data = [table_name[30], table_name[188], table_name[60], table_name[64], table_name[81], table_name[187], table_name[144], table_name[35]];

    //THIS REMOVES ANY PREVIOUS INITIALIZATION
    d3.select("div#qpBubbles").selectAll("*").remove();//Removes prevoius BubbleChart svg canvas
    d3.select("svg#qpBarChart").selectAll("*").remove();//Removes prevoius BarChart svg canvas
    d3.select("svg#ChoroplethMap").selectAll("*").remove();//Removes prevoius ChoroplethMap svg canvas
    d3.select("#controls").selectAll("*").remove();

    for (i in whole_data) {
    var dataKeys = d3.keys(all_data_for_map[i]).filter(function(el) {return el;});
    }
      /*
      else if (el === "Iso3") {}
      else if (el === "Economic Freedom Raw 2016 Score") {}
      else if (el === "Change in Yearly Score from 2015") {}
      else if (el === "Change in Property Rights from 2015") {}
      else if (el === "Change in Fiscal Freedom from 2015") {}
      else if (el === "Change in Government Spending from 2015") {}
      else if (el === "Change in Business Freedom from 2015") {}
      else if (el === "Change in Labor Freedom from 2015") {}
      else if (el === "Change in Monetary Freedom from 2015") {}
      else if (el === "Change in Investment Freedom from 2015") {}
      else if (el === "Change in Financial Freedom from 2015") {}
      else if (el === "Iso3") {}
      else if (el === "Iso3") {}
      else if (el === "Iso3") {}
      else if (el === "Iso3") {}
      else if (el === "Iso3") {}
      else if (el === "Iso3") {}
      else if (el === "Iso3") {}
      else if (el === "Iso3") {}
      else if (el === "Iso3") {}
      else if (el === "Iso3") {}
      else if (el === "Iso3") {}
      else if (el === "Iso3") {}
      else {return el;}

      if (el === "Country_Name") {console.log("yay1")};
      else if (el === "Iso3") {console.log("yay2")};
      else {return el;}
      */



    function countryClick(d) {
      d3.selectAll("td.data").data()
    }


    var buttonCreator = d3.select("#controls").selectAll("button.name")
    .data(dataKeys).enter()
    .append("button")
    .on("click", function(d) {
      qpBubbles.bubbleButtonClick(d);
      qpBarChart.barButtonClick(d);
      qpChoroplethMapMaker.mapButtonClick(d);
    })
    .html(function(d) {return d;});

    //////////////////////////////////////////////////////////////////
    ////
    ////    BubbleChart BubbleChart BubbleChart BubbleChart
    ////
    //////////////////////////////////////////////////////////////////

    function qpBubbles(){
      qpBubbles.bubbleButtonClick = bubbleButtonClick;
      var qpSVG = d3.select("div#qpBubbles").append("svg")
          .attr({ width: 600, height: 400 })
          .style({ border: "lightgray solid", "stroke-width": "1px" })
          .append("g")
          .attr("id", "BubbleG")
          .attr("transform", "translate(50,300)")
          .selectAll("g")
          .data(whole_data)
          .enter()
          .append("g")
          .attr("class", "overallG")
          .attr("transform",
            function (d,i) {return "translate(" + (i * 50) + ", 0)"}
          );

      var BubbleChart = d3.selectAll("g.overallG");

      BubbleChart
        .append("circle").attr("r", 0)
        .transition()
        .delay(function(d,i) {return i * 100})
        .duration(500)
        .attr("r", 40)
        .transition()
        .duration(500)
        .attr("r", 20)
        .style("stroke", "black")
        .style("stroke-width", "1px");

      BubbleChart
        .append("text")
        .style("text-anchor", "middle")
        .attr("y", 30)
        .style("font-size", "10px")
        .text(function(d) {return d.Country_Name;});

      function bubbleButtonClick(datapoint) {
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
          d3.selectAll("g.overallG").select("circle").transition().duration(1000)
            .style("fill", function(p) {
              return colorQuantize(p[datapoint]);
            }).attr("r", function(p) {
              return radiusScale(p[datapoint]);
            });

          BubbleChart
          .data(whole_data)
          .select("circle")
          .on("mouseover", function(p) {
                div.transition()
                    .duration(200)
                    .style("opacity", .9);
                div	.html(p[datapoint])
                    .style("left", (d3.event.pageX) + "px")
                    .style("top", (d3.event.pageY - 28) + "px");
                div.html(datapoint + ":" + "<br/>" + p[datapoint]);
                })
        .on("mouseout", function(p) {
            div.transition()
                .duration(500)
                .style("opacity", 0);
        })
      }//ButtonClick

    }//qpBubbles

    qpBubbles();

  //////////////////////////////////////////////////////////////////
  ////
  ////    BarChart BarChartBarChartBarChartBarChartBarChartBarChart
  ////
  //////////////////////////////////////////////////////////////////

    function qpBarChart() {
      qpBarChart.barButtonClick = barButtonClick;
      //This creates the Bar Graph
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


        };//ButtonClick

      }//qpBarChart

      qpBarChart();

      //////////////////////////////////////////////////////////////////
      ////
      ////    ChoroplethMap ChoroplethMap ChoroplethMap ChoroplethMap
      ////
      //////////////////////////////////////////////////////////////////

      function qpChoroplethMapMaker() {

        var width = 1600, height = 840;

        var zoom = d3.behavior.zoom()
            .scaleExtent([1, 5])
            .on("zoom", moveAndZoom);

        var svg = d3.select("svg#ChoroplethMap")
            .attr({ width: width, height: height })
            .call(zoom);

        var projection = d3.geo.mercator();
        var path = d3.geo.path().projection(projection);

        var url = 'https://gist.githubusercontent.com/d3byex/65a128a9a499f7f0b37d/raw/176771c2f08dbd3431009ae27bef9b2f2fb56e36/world-110m.json';

        d3.json(url, function (error, world) {
            var countries = topojson.feature(world, world.objects.countries).features;
            var neighbors = topojson.neighbors(world.objects.countries.geometries);

            qpChoroplethMapMaker.mapButtonClick = mapButtonClick;

              function mapButtonClick(datapoint) {
                d3.select("svg#ChoroplethMap").selectAll("*").remove();//Removes prevoius ChoroplethMap svg canvas
                svg.transition().duration(200);

                console.log("stuff");

                var mainGroup = svg.append("g");
                mainGroup.style({ stroke: "white", "stroke-width": "2px", "stroke-opacity": 0.0 });

                  var country_value_and_iso = {};
                  incomingData.forEach(function(d) {
                    country_value_and_iso[d["Iso3"]] = +d[datapoint];
                    country_value_and_iso[d.Country_Name] = +d.id;
                  });
                  var country_name_and_iso = {};
                  incomingData.forEach(function(d) {
                    country_name_and_iso[d["Iso3"]] = d.Country_Name;
                  });

                  var maxValue = d3.max(all_data_for_map, function(d) {
                    return parseFloat(d[datapoint]);});

                  var minValue = d3.min(all_data_for_map, function(d) {
                        return parseFloat(d[datapoint]);})

                  var color_domain = [minValue,maxValue];
                  var colorQuantize = d3.scale.quantize()
                      .domain(color_domain)
                      .range(["#d7191c", "#d7411c", "#e76818", "#e79018", "#f29e2e", "#f9ad57", "#f9d057", "#f9dc8c", "#ffeb8c",
                      "#ffeb8c", "#c7eb9d", "#90eb9d", "#00ccbc", "#00a6ca", "#0060ca", "#0006ca"]);

                  //////////////////////////////////////////////////////////////////
                  ////
                  ////    Legend Legend Legend Legend Legend Legend Legend Legend
                  ////
                  //////////////////////////////////////////////////////////////////

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
                    {offset: "0%", color: "#0006ca"},
                    {offset: "6.25%", color: "#0060ca"},
                    {offset: "12.5%", color: "#00a6ca"},
                    {offset: "18.75%", color: "#00ccbc"},
                    {offset: "25%", color: "#00ccbc"},
                    {offset: "32.25%", color: "#48eb9d"},
                    {offset: "37.5%", color: "#90eb9d"},
                    {offset: "43.75%", color: "#c7eb9d"},
                    {offset: "50%", color: "#ffeb8c"},
                    {offset: "56.25%", color: "#f9dc8c"},
                    {offset: "62.5%", color: "#f9d057"},
                    {offset: "68.75%", color: "#f9ad57"},
                    {offset: "75%", color: "#f29e2e"},
                    {offset: "82.25%", color: "#e79018"},
                    {offset: "87.5%", color: "#e76818"},
                    {offset: "93.75%", color: "#d7411c"},
                    {offset: "100%", color: "#d7191c"}
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
                                  .domain([minValue,maxValue]);

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
                  .text("Colored Scale for " + datapoint);

                  ///////////////////////////////////////////////////////////
                  ///End Legend End Legend End Legend End Legend End Legend
                  ///////////////////////////////////////////////////////////

                  //Coloring of the world
                  mainGroup.selectAll("path", "countries")
                      .data(countries)
                      .enter().append("path").transition().duration(1000)
                      .attr("d", path)
                      .style("fill", function (d) {
                          return colorQuantize(country_value_and_iso[d.id]);});

                  // Define the div for the tooltip
                  var div = d3.select("svg#ChoroplethMap").append("div")
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
                                div.html(country_name_and_iso[p.id] + ":" + "<br/>" + country_value_and_iso[p.id]);
                          d3.select(this).style("stroke-opacity", 1.0);
                      });
                  mainGroup.selectAll("path")
                      .on("mouseout", function () {
                          d3.select(this).style("stroke-opacity", 0.0);
                          });

                }//ButtonClick
              });//d3json


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
        }//Move and zoom
      }//ChoroplethMapMaker
      qpChoroplethMapMaker();



})};


};

createDataViz();
onLoad();
