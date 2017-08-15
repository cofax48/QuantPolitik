/*Initialization of MY Quantpolitik Angular App */
var QPCountryAngular = angular.module('app', ['ngRoute', 'ngSanitize', 'CountryAngularApp']).
config(function ($routeProvider, $sceDelegateProvider) {
  $routeProvider.when('/App', {
    templateUrl: '../static/assets/js/CountryAngularApp/partials/start.html',
    controller: 'CountryDataController'
  })
  //Specify links and routing to rest of the website from the angular app
  .when("/", {
    templateUrl: '../templates/index.html'
  })
  .when("/TheAlgorithm", {
    templateUrl: '../templates/TheAlgorithm.html'
  })
  .when("/about", {
    templateUrl: '../templates/about.html'
  })
  .when("/TheTech", {
    templateUrl: '../templates/TheTech.html'
  })
  .when("/AreasofAnalysis", {
    templateUrl: '../templates/areaOfAnalysis.html'
  })
  .when("/BureaucraticExchange", {
    templateUrl: '../templates/BureaucraticExchange.html'
  })
  .when("/BusinessRelations", {
    templateUrl: '../templates/BusinessRelations.html'
  })
  .when("/CountryProfile", {
    templateUrl: '../templates/CountryProfile.html'
  })
  .when("/CulturalDiffusion", {
    templateUrl: '../templates/CulturalDiffusion.html'
  })
  .when("/GovernmentalPerspective", {
    templateUrl: '../templates/GovernmentalPerspective.html'
  })
  .when("/Prestige", {
    templateUrl: '../templates/Prestige.html'
  })
  .when("/Security", {
    templateUrl: '../templates/Security.html'
  })
  .when("/TradeRelations", {
    templateUrl: '../templates/TradeRelations.html'
  })
  .when("/datadashboard", {
    templateUrl: '../templates/dataDashBoard.html'
  });
  $routeProvider.otherwise({
  redirectTo: '/start'
  });
  $sceDelegateProvider.resourceUrlWhitelist([
  // Allow same origin resource loads.
  'self',
  'http://*.quantpolitik.com/**']);
});

angular.module('CountryAngularApp', []);
