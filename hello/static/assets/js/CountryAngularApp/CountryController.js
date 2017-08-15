// set aPITOUSE according to local or production variable
var aPITOUSE = 'http://www.quantpolitik.com/';
//var aPITOUSE = 'http://localhost:5000/';

/* Contorllers */

angular.module('CountryAngularApp')
  .controller('CountryDataController', ['$scope', '$interval', '$location', '$http', function ($scope, $interval, $location, $http) {

    //This gets a list of all countries being used and pupulates the initial
    //dropdown menu for the user to choose which country they want to display
    $scope.CountryToUse = null;
    function CountryNameListAcquisition() {
      var CountryList = [];
      $http.get(aPITOUSE + 'country_name_list').
      success(function(CountryData, status, headers, config) {
        var yao = CountryData[0];
        for (i in yao) {
          CName = yao[i].Country_Name;
          CountryList.push({"CountryName" : CName});
        }
      }).
      error(function(data, status, headers, config) {
        console.log(data);// log error
      });

      //Takes the users chosen country and runs an api request to data
      //arranged by country. This data is used to populate tables and
      //info in the Angular view
      $scope.CountrySelectValue = function(countryNameChosen) {
        getDataWithNameChosen(countryNameChosen);
      };

      //This is the Country name list from which the user can choose
      $scope.CountryData = CountryList;
      $scope.Afghanistan = 'Afghanistan';
    }
    function getDataWithNameChosen(countryNameChosen) {
      $scope.$watch('countryNameChosen', function() {
        console.log(countryNameChosen);
        countryGraphAPI(countryNameChosen);

        ////////////////////////////////////////////////////////////////////////
        /// API Call to get Data for Bar Graph
        ////////////////////////////////////////////////////////////////////////
        $http.get(aPITOUSE + "api/" + countryNameChosen + "/QP_SCORE2").
          success(function(data, status, headers, config) {
            console.log(data[0]);
            $scope.countryGraphAPIData = data[0];
          }).
            error(function(data, status, headers, config) {
              console.log(data);
            });

        ////////////////////////////////////////////////////////////////////////
        /// API Call to get Data for Interpolation of variables on start.html
        ////////////////////////////////////////////////////////////////////////
        $http.get(aPITOUSE + 'api/ByCountry/' + countryNameChosen).
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
    });
  }

  function countryGraphAPI(countryNameChosen) {
    countryNameChosen = countryNameChosen.replace(' ', '%20');
    countryNameChosen = countryNameChosen.replace(' ', '%20');

    ////////////////////////////////////////////////////////////////////////
    /// Embeded Twitter API that loads according to the country slected
    ////////////////////////////////////////////////////////////////////////
    var twitterUrlToReturn = countryTweetUrlArray[countryNameChosen];
    //Clears existing canvas
    d3.select("div#twitter-container").selectAll("*").remove();
    if (twitterUrlToReturn) {
      d3.select("div#twitter-container").html('<a class="twitter-timeline" href="https://twitter.com/' + countryTweetUrlArray[countryNameChosen] +'" data-theme="dark" data-height="800">Tweets by ' + countryNameChosen + '</a> <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>');
      twttr.widgets.load()
    }
    else {
          d3.select("div#twitter-container").html('<a class="twitter-timeline" href="https://twitter.com/StateDept" data-theme="dark" data-height="800">Tweets by USEmbArgentina</a> <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>');
          twttr.widgets.load();
        }
  }

//Populates The dropdown menu with country names and the twitter feed
  var starter = function () {
    CountryNameListAcquisition();
    countryGraphAPI('Afghanistan');
  };
starter();

//Ugly hack to get Afghanistan to load as default variable on load
//Afghanistan is passed from "data-ng-init="init('Afghanistan')" next to ng-controller on DataByCountry html
$scope.init = function(countryNameChosen) {
  $http.get(aPITOUSE + 'api/ByCountry/' + countryNameChosen).
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
  $http.get(aPITOUSE + "api/" + countryNameChosen + "/QP_SCORE2").
  success(function(data, status, headers, config) {
    console.log(data[0]);
    $scope.countryGraphAPIData = data[0];
  }).
    error(function(data, status, headers, config) {
      console.log(data);
    });
  }
}]);
