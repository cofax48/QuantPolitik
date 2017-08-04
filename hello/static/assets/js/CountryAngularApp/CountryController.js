/* Contorllers */

angular.module('CountryAngularApp')
  .controller('CountryDataController', ['$scope', '$interval', '$location', '$http', function ($scope, $interval, $location, $http) {

    //This gets a list of all countries being used and pupulates the initial
    //dropdown menu for the user to choose which country they want to display
    $scope.CountryToUse = null;
    function CountryNameListAcquisition() {
      var CountryList = [];
      $http.get('http://localhost:5000/country_name_list').
      success(function(CountryData, status, headers, config) {
        var yao = CountryData[0];
        for (i in yao) {
          CName = yao[i].Country_Name;
          CountryList.push({"CountryName" : CName});
        }
      }).
      error(function(data, status, headers, config) {
        console.log(data);
        // log error
      });


      //Takes the users chosen country and runs an api request to data
      //arranged by country. This data is used to populate tables and
      //info in the Angular view
      $scope.CountrySelectValue = function(item) {
        graph_draw(item);
        console.log(item);
        $http.get('http://localhost:5000/api/ByCountry/' + item).
        success(function(CountryData, status, headers, config) {
          $scope.CountryNameBeingPassed = CountryData[0]["Country Name"];
          $scope.QPScoreBeingPassed = CountryData[1]["QP_Score"];
          $scope.PopulationBeingPassed = CountryData[2]["Population in Millions"];
          $scope.GDPBeingPassed = CountryData[3]["GDP"];
          $scope.GDPPerCapitaBeingPassed = CountryData[4]["GDP per Capita"];
          $scope.HDIBeingPassed = CountryData[5]["HDI"];
          $scope.SizeBeingPassed = CountryData[6]["Size"];
          $scope.PresidentialScoreBeingPassed = CountryData[7]["Presidential_SCORE2"];
          $scope.PrestigeScoreBeingPassed = CountryData[8]["Prestige_SCORE2"];
          $scope.GPScoreBeingPassed = CountryData[9]["GP_SCORE2"];
          $scope.CDScoreBeingPassed = CountryData[10]["CD_SCORE2"];
          $scope.SecurityScoreBeingPassed = CountryData[11]["Security_SCORE2"];
          $scope.SecStateScoreBeingPassed = CountryData[12]["Sec_State_SCORE2"];
          $scope.CProfileScoreBeingPassed = CountryData[13]["CProfile_SCORE2"];
          $scope.BRScoreBeingPassed = CountryData[14]["BR_SCORE2"];
          $scope.TradeScoreBeingPassed = CountryData[15]["Trade_SCORE2"];

          $scope.CountryDataBeingPassed = CountryData;
        }).
        error(function(data, status, headers, config) {
          console.log(data);
        });
      };

      $scope.CountryList = CountryList;
      $scope.CountryData = CountryList;
    }

    function graph_draw(item) {

      // Get the data
      $http.get("http://localhost:5000/api/" + item + "/QP_SCORE2").
        success(function(data, status, headers, config) {
          // set the dimensions and margins of the graph
          var margin = {top: 20, right: 20, bottom: 30, left: 50},
              width = 960 - margin.left - margin.right,
              height = 500 - margin.top - margin.bottom;

          // parse the date / time
          var parseDate = d3.timeParse("%d-%b-%y");

          // set the ranges
          var x = d3.scaleTime().range([0, width]);
          var y = d3.scaleLinear().range([height, 0]);

          // append the svg obgect to the body of the page
          // appends a 'group' element to 'svg'
          // moves the 'group' element to the top left margin
          var svg = d3.select("svg-holder")
              .attr("width", width + margin.left + margin.right)
              .attr("height", height + margin.top + margin.bottom)
            .append("g")
              .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");


          var all_the_data = data[0];
          for (day in all_the_data) {
            date = parseDate(day);
            close = +all_the_data[day];
          }

          // define the line
          var valueline = d3.line()
              .x(function(all_the_data) { return x(d); })
              .y(function(all_the_data) { return y(data[d]); });

          // Scale the range of the data
          x.domain(d3.extent(all_the_data, function(d) { console.log(d); return d; }));
          y.domain([0, d3.max(all_the_data, function(d) { console.log(d); return data[d]; })]);

          // Add the valueline path.
          svg.append("path")
              .data([all_the_data])
              .attr("class", "line")
              .attr("d", valueline);

          // Add the X Axis
          svg.append("g")
              .attr("transform", "translate(0," + height + ")")
              .call(d3.axisBottom(x));

          // Add the Y Axis
          svg.append("g")
              .call(d3.axisLeft(y));

        }).
        error(function(data, status, headers, config) {
          console.log(data);
        });
      }

  var init = function () {
    CountryNameListAcquisition();
  };

init();
}]);
