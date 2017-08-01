angular.module('app', ['ngRoute', 'ngSanitize', '7minWorkout']).
config(function ($routeProvider, $sceDelegateProvider) {
  $routeProvider.when('/start', {
    templateUrl: '../static/assets/js/7MinuteWorkOut/partials/start.html'
  });
  //accessible under http://<hostname>/index.html#/start
  $routeProvider.when('/workout', {
    templateUrl: '../static/assets/js/7MinuteWorkOut/partials/workout.html',
    controller: 'WorkoutController'
  });
  $routeProvider.when('/finish', {
    templateUrl: '../static/assets/js/7MinuteWorkOut/partials/finish.html'
  });
  $routeProvider.otherwise({
    redirectTo: '/start'
  });
  $sceDelegateProvider.resourceUrlWhitelist([
    // Allow same origin resource loads.
    'self',
    'http://*.youtube.com/**']);
});

angular.module('7minWorkout', []);
//angular.module('7minWorkout', []); // creates a new module
//angular.module('7minWorkout'); //get an existing module
