angular.module('app', ['ngRoute', '7minWorkout']).
config(function ($routeProvider) {
  $routeProvider.when('/start', {
    templateUrl: 'partials/start.html'
  });
  //accessible under http://<hostname>/index.html#/start
  $routeProvider.when('/workout', {
    templateUrl: 'partials/workout.html',
    controller: 'WorkoutController'
  });
  $routeProvider.when('/finish', {
    templateUrl: 'partials/finish.html'
  });
  $routeProvider.otherwise({
    redirectTo: '/start'
  });
});

angular.module('7minWorkout', []);
//angular.module('7minWorkout', []); // creates a new module
//angular.module('7minWorkout'); //get an existing module
