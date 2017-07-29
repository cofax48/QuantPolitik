angular.module('app', ['ngRoute', '7minWorkout']).
config(function ($routeProvider) {
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
});

angular.module('7minWorkout', []);
//angular.module('7minWorkout', []); // creates a new module
//angular.module('7minWorkout'); //get an existing module
