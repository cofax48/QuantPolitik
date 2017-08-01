/* Contorllers */

angular.module('CountryAngularApp')
  .controller('CountryDataController', ['$scope', '$interval', '$location', '$http', function ($scope, $interval, $location, $http) {
    function DataAcquisition(args) {
      var CountryList = [];
      $http.get('http://localhost:5000/api/Business_Relations').
      success(function(CountryData, status, headers, config) {
        var yao = CountryData[0];
        for (i in yao) {
          console.log(yao[i].Country_Name);
          CName = yao[i].Country_Name;
          CountryList.push({"CountryName" : CName});
        }
      }).
      error(function(data, status, headers, config) {
        // log error
      });
      console.log(CountryList);
      $scope.CountryData = CountryList;
      this.CountryName = $scope.CountryData;
    }

    function AllTheData(args) {
      this.CountryName = args.Country_Name;
      this.Fiscal_Freedom = args.Fiscal_Freedom;
      this.Remittances = args.Remittances;
      //this.image = args.image;
  }

  var init = function () {
    DataAcquisition();
  };

init();
}]);
