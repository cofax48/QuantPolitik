var aPITOUSE = 'http://www.quantpolitik.com/';
//var aPITOUSE = 'http://localhost:5000/';
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
  d3.json(aPITOUSE + 'api/QP_Score', function(error, incomingData) {
    for (var i in _.range(198)) {if (whole_data.length == 198) {mapDraw()}
    else {
      whole_data.push({Country_Name:incomingData[0][i]["Country_Name"], id:incomingData[0][i]["Iso3"], value:incomingData[0][i][column_to_use]});};
  }
      });
  function mapDraw() {

  var width = 850, height = 400;

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
            {offset: "25%", color: "#23d7b1"},
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
      var div = d3.select("body").append("div")
          .attr("class", "tooltip")
          .style("opacity", .5);

      mainGroup
          .selectAll("path")
          .data(countries)
          .on("mouseover", function (p) {
                    div.transition()
                        .duration(200)
                        .style("opacity", .9);
                    div	.html(country_value_and_iso[p.id])
                        .style("left", (d3.event.pageX) + "px")
                        .style("top", (d3.event.pageY) + "px");
                    console.log("yaooooooo");
                    var num = country_value_and_iso[p.id]
                    div.html(country_name_and_iso[p.id] + "'s QP Score:" + "<br/>" + num.toFixed(2));
              d3.select(this).style("stroke-opacity", 1.0);
          })
          .on("mouseout", function () {
              d3.select(this).style("stroke-opacity", 0.0);
          })
          .on("click", function(p) { //This triggers the country data section
            var CountryName = country_name_and_iso[p.id];
            CountryDataDisplay(CountryName);
          });//ONCLick
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


}//ONLOAD

function createDataViz() {

  var data_table_names = ["QP Score", "Business Relations", "Country Profile", "Trade Relations", "Security", "Cultural Diffusion", "Governmental Perspective", "Presidential Exchange", "UN", "Prestige", "Sec State Bureaucratic Exchange"];

  var buttonCreator = d3.select("#controls").selectAll("button.name")
  .data(data_table_names).enter()
  .append("button")
  .on("click", function(d) {
    mapDrawFromButton(d);
    onchange(d);
  })
  .html(function(d) {return d;});

  function mapDrawFromButton (selectValue) {
    if (selectValue === "Security") {CategoryMapDraw("Security_SCORE");}
    else if (selectValue === "QP Score") {CategoryMapDraw("QP_Score");}
    else if (selectValue === "Country Profile") {CategoryMapDraw("CProfile_SCORE");}
    else if (selectValue === "Business Relations") {CategoryMapDraw("BR_SCORE");}
    else if (selectValue === "Trade Relations") {CategoryMapDraw("Trade_SCORE");}
    else if (selectValue === "Cultural Diffusion") {CategoryMapDraw("CD_SCORE");}
    else if (selectValue === "Governmental Perspective") {CategoryMapDraw("GP_SCORE");}
    else if (selectValue === "Presidential Exchange") {CategoryMapDraw("Presidential_SCORE");}
    else if (selectValue === "UN") {CategoryMapDraw("UN");}
    else if (selectValue === "Prestige") {CategoryMapDraw("Prestige_SCORE");}
    else if (selectValue === "Sec State Bureaucratic Exchange") {CategoryMapDraw("Sec_State_SCORE");}
    else {return selectValue;}
  }

  function onchange(selectValue) {
    console.log(selectValue);
    var new_select = selectValue.replace(" ", "_");
    console.log(new_select);
    d3.json(aPITOUSE + 'api/' + new_select, function(error, incomingData) {
      incomingData = incomingData[0];

    var table_name = incomingData;
    var all_data_for_map = incomingData;
    var whole_data = [table_name[30], table_name[188], table_name[60], table_name[64], table_name[81], table_name[187], table_name[144], table_name[35]];

    //THIS REMOVES ANY PREVIOUS INITIALIZATION
    d3.select("div#qpBubbles").selectAll("*").remove();//Removes prevoius BubbleChart svg canvas
    d3.select("svg#qpBarChart").selectAll("*").remove();//Removes prevoius BarChart svg canvas
    //d3.select("svg#ChoroplethMap").selectAll("*").remove();//Removes prevoius ChoroplethMap svg canvas
    d3.select("select.select").remove();
    d3.select("div.databox").remove();
    d3.select("div.textarea").remove();
    d3.selectAll("div.tooltip").remove();

    for (i in whole_data) {
    var dataKeys = d3.keys(all_data_for_map[i]).filter(function(el) {
      if (el === "Country_Name") {console.log("yay1")}
      else if (el === "Iso3") {console.log("yay2")}
      else if (el === "Economic Freedom Raw 2016 Score") {}
      else if (el === "Change in Yearly Score from 2015") {}
      else if (el === "Change in Property Rights from 2015") {}
      else if (el === "Change in Fiscal Freedom from 2015") {}
      else if (el === "Change in Trade Freedom from 2015") {}
      else if (el === "Change in Government Spending from 2015") {}
      else if (el === "Change in Business Freedom from 2015") {}
      else if (el === "Change in Labor Freedom from 2015") {}
      else if (el === "Change in Monetary Freedom from 2015") {}
      else if (el === "Change in Investment Freedom from 2015") {}
      else if (el === "Change in Financial Freedom from 2015") {}
      else if (el === "Exports from the United States in 2014") {}
      else if (el === "Imports to the United States in 2014") {}
      else if (el === "Trade Balance with the United States in 2014") {}
      else if (el === "Exports from the United States in 2013") {}
      else if (el === "Imports to the United States in 2013") {}
      else if (el === "Trade Balance with the United States in 2013") {}
      else if (el === "Exports from the United States in 2012") {}
      else if (el === "Imports to the United States in 2012") {}
      else if (el === "Trade Balance with the United States in 2012") {}
      else if (el === "Exports from the United States in 2011") {}
      else if (el === "Imports to the United States in 2011") {}
      else if (el === "Trade Balance with the United States in 2011") {}
      else if (el === "Exports from the United States in 2010") {}
      else if (el === "Imports to the United States in 2010") {}
      else if (el === "updated_on") {}
      else if (el === "Trade Balance with the United States in 2010") {}
      else if (el === "Exports from the United States in 2009") {}
      else if (el === "Imports to the United States in 2009") {}
      else if (el === "Trade Balance with the United States in 2009") {}
      else {return el;}
      });
    }



    function countryClick(d) {
      d3.selectAll("td.data").data()
    }


    var dropdownbox = d3.select('div#reportrange.pull-right').append("div")
                    .attr("class", "textarea");
        dropdownbox.html("<br>" + "Pull the Dropdown Menu to Explore Each of the Category's Data Variables!" + "<br>")

    var select = d3.select('div#reportrange.pull-right')
      .append('select')
        .attr('class','select')
        .on('change', function(d) {
          qpChoroplethMapMaker.mapButtonClick(d);
        });

    var options = select
      .selectAll('div#dashboard_graph')
      .data(dataKeys).enter()
      .append('option')
      .on("click", function(d) {
        console.log(d),
        qpChoroplethMapMaker.mapButtonClick(d);
      })
      .html(function (d) { return d; });


      //////////////////////////////////////////////////////////////////
      ////
      ////    ChoroplethMap ChoroplethMap ChoroplethMap ChoroplethMap
      ////
      //////////////////////////////////////////////////////////////////

      function qpChoroplethMapMaker() {

        var width = 850, height = 350;

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
                d3.selectAll("div.tooltip").remove();
                d3.selectAll("div.dropdownbox").remove();
                d3.selectAll("databox").remove();

                svg.transition().duration(200);

                var datapoint = d3.select('select.select').property('value');

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
                    {offset: "25%", color: "#23d7b1"},
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
                  var div = d3.select("body").append("div")
                      .attr("class", "tooltip")
                      .style("opacity", .9);

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
                                var num = country_value_and_iso[p.id];
                                div.html(country_name_and_iso[p.id] + "'s " + datapoint + "<br/>" + num.toFixed(2));
                          d3.select(this).style("stroke-opacity", 1.0);
                      })
                      .on("mouseout", function () {
                          d3.select(this).style("stroke-opacity", 0.0);
                      })
                      .on("click", function(p) { //This triggers the country data section
                        var CountryName = country_name_and_iso[p.id];
                        CountryDataDisplay(CountryName);
                      });//ONCLick
                        /* What i want in viz
                        Country Name,
                        QP Score
                        Country Flag,
                        Map,
                        Quick Facts: Capital, Language, FreedomHouseRanking, Population, GDP, HDI, FDI
                        Headline Scores for Each Section
                        */

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

function CountryDataDisplay(CountryName) {
console.log(CountryName);
d3.selectAll("div.databox").remove();
d3.json(aPITOUSE + 'api/ByCountry/' + CountryName, function(error, incomingData) {
  var databox = d3.select("div#CountryInfoboxDisplay").append("div")
                  .attr("class", "databox");
  var country_name = incomingData[0]["Country Name"];
  var qpScore = incomingData[1]["QP_Score"];
  var population = incomingData[2]["Population in Millions"];
  var gdp = incomingData[3]["GDP"];
  var gdpperCapita = incomingData[4]["GDP per Capita"];
  var hdi = incomingData[5]["HDI"];
  var size = incomingData[6]["Size"];


  console.log(incomingData)
  console.log(country_name, qpScore);
  databox.html("Quick Facts about " + country_name + "<br>" +
               "QP Score: " + qpScore + "<br>" +
               "Population (In Millions): " + population + "<br>" +
               "GDP (In Billions): " + gdp + "<br>" +
               "GDP Per Capita: " + gdpperCapita + "<br>" +
               "Human Development Index: " + hdi + "<br>" +
               "Size: " + size + " km" + "<br>"
             );


})//D3json
}//CountryDataDisplay

createDataViz();
onLoad();

function CategoryMapDraw(categoryScore) {
  d3.select("svg#ChoroplethMap").selectAll("*").remove();//Removes prevoius ChoroplethMap svg canvas
  d3.select("select.select").remove();
  d3.select("div.databox").remove();
  d3.select("div.textarea").remove();
  d3.selectAll("div.tooltip").remove();
  d3.selectAll("div.Newtooltip").remove();

  //http://localhost:5000/api/QP_Score
  var whole_data = [{Country_Name:'placeHolder', value:0}];
  d3.json(aPITOUSE + 'api/' + categoryScore, function(error, incomingData) {
    for (var i in _.range(198)) {if (whole_data.length == 198) {mapDraw()}
    else {
      whole_data.push({Country_Name:incomingData[0][i]["Country_Name"], id:incomingData[0][i]["Iso3"], value:incomingData[0][i][column_to_use]});};
  }
      });
  function mapDraw() {

  var width = 850, height = 400;

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
            {offset: "25%", color: "#23d7b1"},
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
          .text("Colored Scale for " + categoryScore);

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
        var div = d3.select("body").append("div")
            .attr("class", "Newtooltip")
            .style("opacity", .9);

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
                      var num = country_value_and_iso[p.id];
                      div.html(country_name_and_iso[p.id] + "'s " + categoryScore + "<br/>" + num.toFixed(2));
                d3.select(this).style("stroke-opacity", 1.0);
            })
            .on("mouseout", function () {
                d3.select(this).style("stroke-opacity", 0.0);
            })
            .on("click", function(p) { //This triggers the country data section
              var CountryName = country_name_and_iso[p.id];
              CountryDataDisplay(CountryName);
            });//ONCLick
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

  mapDraw();
}//ONLOAD
