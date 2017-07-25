angular.module('app',[])
.controller('GuessTheNumberController', GuessTheNumberController);
//This controller function enables the creation of a nw $scope, which is tied into the ng-app tag in the view-within the <body> in this case
function GuessTheNumberController($scope) {
  $scope.verifyGuess = function () {
    $scope.deviation = $scope.original - $scope.guess;
    $scope.noOfTries = $scope.noOfTries + 1;
    console.log($scope);
  }
  $scope.initializeGame=function() {
    $scope.noOfTries = 0;
    $scope.original = Math.floor((Math.random() * 1000) + 1);
    $scope.guess = null;
    $scope.deviation = null;
  }
  $scope.initializeGame();
}

//Within HTML

// outputs the value of a property
//{{property}}

//outputs the result of boolean comparison ternary operator
//{{ property1 >=0?'positive': 'negative' }}

//call testMethod() and output the return value
//{{testMethod()}}

//asign value returned by testMethod() to x. Creates "x" on scope if not available. Empty output
//{{x=testMethod()}}

//calls testMethod() and testMethod2() and assign return values to x and y. Empty output
//{{x=testMethod();y=testMethod2()}}
