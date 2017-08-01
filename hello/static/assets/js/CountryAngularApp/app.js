angular.module('app', ['ngRoute', 'ngSanitize', 'CountryAngularApp']).
config(function ($routeProvider, $sceDelegateProvider) {
  $routeProvider.when('/start', {
    templateUrl: '../static/assets/js/CountryAngularApp/partials/start.html',
    controller: 'CountryDataController'
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
