angular.module('app', ['ngRoute', '7minWorkout']).
config(function ($routeProvider) {
  $routeProvider.when('/start', {
    templateUrl: '../templates/partials/start.html'
  });
  //accessible under http://<hostname>/index.html#/start
  $routeProvider.when('/workout', {
    templateUrl: '../templates/partials/workout.html',
    controller: 'WorkoutController'
  });
  $routeProvider.when('/finish', {
    templateUrl: '../templates/partials/finish.html'
  });
  $routeProvider.otherwise({
    redirectTo: '../templates/partials/start'
  });
});

angular.module('7minWorkout', []);
//angular.module('7minWorkout', []); // creates a new module
//angular.module('7minWorkout'); //get an existing module
