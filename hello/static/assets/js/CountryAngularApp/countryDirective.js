QPCountryAngular.directive('countryAngular', function(){
  function link(scope, element, attr){
    scope.$watch('data', function(data){
      //Removs previous intializations of th SVG
      d3.select("svg#GraphCountryD3").selectAll("*").remove();

      var clientWidth = d3.select("svg#GraphCountryD3")._groups["0"]["0"].clientWidth; //Gets the width of svg container
      //Use the margin convention practice
      var margin = {top: 10, right: 0, bottom: 0, left: 25}
        , width = clientWidth
        , height = window.innerHeight - margin.top - margin.bottom; // Use the window's height

      // parse the date / time
      var parseDate = d3.timeParse("%B-%d-%Y");

      //Converts month names into numbers
      function getMonthFromString(mon){
      return new Date(Date.parse(mon +" 1, 2012")).getMonth()
      };

      //Gets the data from my API and formats it
      var wholeData = [{date:'Mon Feb 29 2016 00:00:00 GMT-0400 (EDT)', value:35}];
      for (day in data) {
        var dayToUse = String(day.slice(-7,-5));
        var yearToUse = String(day.slice(-4));
        var monthToUse = String(getMonthFromString(day.slice(0,-8)));
        var dateForData = new Date(yearToUse, monthToUse, dayToUse);
        wholeData.push({date:dateForData, value:Number(+data[day].slice(0,5))});
      };

      //filters out my placeHolder of the leap day in 2016
      wholeData = wholeData.slice(1,);

      //Sorts my data array by date
      wholeData.sort(function(a,b) {
          return new Date(a.date).getTime() - new Date(b.date).getTime()
      });

      //determines if my data has populated the array (if three variables are in the array it builds the graph)
      if (wholeData.length > 3){

        //Converts my date time figures from strings into the proper format for d3
        var minYear = String(wholeData[1]["date"]).slice(11,15);
        var minMonth = String(getMonthFromString(String(wholeData[1]["date"]).slice(4,7)));
        var minDay = String(Number(String(wholeData[1]["date"]).slice(8,10)) - 1);
        var mindate = new Date(minYear, minMonth, minDay);
        var maxYear = String(wholeData.slice(-1)[0]["date"]).slice(11,15);
        var maxMonth = String(getMonthFromString(String(wholeData.slice(-1)[0]["date"]).slice(4,7)));
        var maxDay = String(wholeData.slice(-1)[0]["date"]).slice(8,10);
        var maxdate = new Date(maxYear, maxMonth, maxDay);

        //X scale will use the date
        var xScale = d3.scaleTime()
          .domain([mindate, maxdate])
          .range([0, width]);


        //Figures out the lowest valu and the highest value of data range
        var maxNumber = d3.max(wholeData, function(d) { return d["value"]; });
        var minNumber = d3.min(wholeData, function(d) { return d["value"]; });

        console.log(maxNumber, minNumber);

        //Adds buffer to top of graph based on highest number

        //Adds buffer to bottom of range determines if the lowest num is neg and then applis buffer
        function MaxNeg(maxNumber) {if (maxNumber <= 1) {
          var tempMax = maxNumber / .85;
          var difference = tempMax - maxNumber;
          var newMax = maxNumber - difference
          return {newMax}
        } else if (maxNumber > 1) {
          var newMax = maxNumber * 1.25;
          if (newMax > 200) {
            var newMax = 200;
            return {newMax}
          }
          else {
          return {newMax}}}};
        function MinNeg(minNumber) {if (minNumber <= 1) {
          var newMin = minNumber / .75;
          if (newMin < -200) {
            newMin = -200;
            return {newMin}
          } else {
          return {newMin}
        }} else if (minNumber > 1) {
          var newMin = minNumber * .75;
          return {newMin}}};
        var NewminNumber = Number(MinNeg(minNumber)["newMin"]);
        var NewmaxNumber = Number(MaxNeg(maxNumber)["newMax"]);

        //Y scale figures out the highst and lowest numbers to draw the range
        var yScale = d3.scaleLinear()
            .domain([NewminNumber, NewmaxNumber])
            .range([height, 0]); // output

        // Adds the SVG to the page
        var svg = d3.select("svg#GraphCountryD3")
            .attr("width", width)
            .attr("height", height + margin.top + margin.bottom)
            .attr("preserveAspectRatio", "xMinYMin meet")
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        // Calls the x axis in a group tag
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(xScale)); // Create an axis component with d3.axisBottom

        // Calls the y axis in a group tag
        svg.append("g")
            .attr("class", "y axis")
            .call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft

        // D3's line generator
        var line = d3.line()
            .x(function(d) { return xScale(d.date); })
            .y(function(d) { return yScale(d.value); })
            .curve(d3.curveMonotoneX); // apply smoothing to the line

        // Appends styling
        svg.append("g")
          .append("text")
            .attr("fill", "#000")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", "0.71em")
            .attr("text-anchor", "end")
            .text("QP Score");

        //Builds the graph
          svg.append("path")
              .datum(wholeData)
              .attr("fill", "none")
              .attr("stroke", "steelblue")
              .attr("stroke-linejoin", "round")
              .attr("stroke-linecap", "round")
              .attr("stroke-width", 1.5)
              .attr("d", line);

          svg
          .on("mouseover", console.log("yay"));

            };//Data length longer than three
    }, true); // Watcher
  }//Link function
  return {
    link: link,
    restrict: 'E',
    scope: { data: '=' }
  }
});
