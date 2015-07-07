var app = angular.module('app', []).config(function($httpProvider) {
$httpProvider.defaults.xsrfCookieName = 'csrftoken';
$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
app.controller('theController', ['$scope', '$interval', '$http', '$templateCache', 
	function($scope, $interval, $http, $templateCache){

		
		//{% endverbatim %}

		// get double array of node objects returned by django

		//won't keep this

		//var dataDump = {{intervalList}};
		
		//this serves as the counter for the controller and it is updated every interval
		$scope.i = 1;
		$scope.totalTime = 0; 



		// will be calculaed by django 
		$scope.Interval = [];
		$scope.COUNTER = $scope.totalTime;
		$scope.classSelectors;
		$scope.intervalCount = 0.5;
		$scope.bit_rate = 6;
		$scope.bit_rate_update = $scope.bit_rate;
		$scope.numSlides = (8.0 / $scope.intervalCount);


		// will be calculated at each interval by django
		$scope.feedbackNodes = [];
		$scope.showBitRate = true;
		$scope.showK = true;
		$scope.showDistance = false;
		$scope.algorithms = ['NONE', 'WORST', 'RAND', 'AMUSE'];
		$scope.k_nodes = 6;
		$scope.distance = 1;



		// django puts this here
		$scope.my ={option : 'NONE'};
		//$scope.method = 'JSONP';
		$scope.url = '/update';


		var promise;


		$scope.play = function()
		{
			if( angular.isDefined(promise))
				return;

			promise = $interval(function(){
				$scope.fetch();


				//$scope.Interval; // set the interval equal to the ith index in the dataDump variable

				
				var currVals = $scope.Interval;
				if(currVals == null)
				{
					console.log("hello");
				}
				var intervalColors = [];
				//var currFeed = $scope.feedbackNodes;
				$scope.check();
				$scope.COUNTER = $scope.totalTime;

				/*
					
					The last thing you need to do to add a color is to add an if-else
					condition at the bottom of the nested foroop (see location of comment in code) in this format:

						if(currVals[j][l] <= someValue && currVals[j][l] > anotherValue) // or if(currVals[j][l] == someValue)
						{
							nodeColorBooleans.push(true);
						}
						else
						{
							nodeColorBooleans.push(false);
						}

					If you want to change the ranges just update the values


				*/

				for(var j = 0; j < $scope.Interval.length; j++)
				{
					var areaColors = [];
					var checkArray = $scope.Interval[j];
					for(var l = 0; l < checkArray.length; l++)
					{
						var nodeColorBooleans = [];

						if($scope.feedbackNodes[j][l] == 1)
						{
							nodeColorBooleans.push(true);
						}
						else
						{
							nodeColorBooleans.push(false);
						}

						
						if (currVals[j][l] == 0.0)
						{
							nodeColorBooleans.push(true);
						}
						else
						{
							nodeColorBooleans.push(false);
						}

						if (currVals[j][l] <= 50.0 && currVals[j][l] > 25.0)
						{
							nodeColorBooleans.push(true);
						}
						else
						{
							nodeColorBooleans.push(false);
						}

						if (currVals[j][l] <= 75.0 && currVals[j][l] > 50.0)
						{
							nodeColorBooleans.push(true);
						}
						else
						{
							nodeColorBooleans.push(false);
						}

						if (currVals[j][l] > 75.0)
						{
							nodeColorBooleans.push(true);
						}
						else
						{
							nodeColorBooleans.push(false);
						}
						if (currVals[j][l] < 0)
						{
							nodeColorBooleans.push(true);
						}
						else
						{
							nodeColorBooleans.push(false);
						}
						if(currVals[j][l] == -100.0) // or if(currVals[j][l] == someValue)
						{
							nodeColorBooleans.push(true);
						}
						else
						{
							nodeColorBooleans.push(false);
						}
						if(currVals[j][l] <= 25.0 && currVals[j][l] > 0.0) // or if(currVals[j][l] == someValue)
						{
							nodeColorBooleans.push(true);
						}
						else
						{
							nodeColorBooleans.push(false);
						}


						// add any new if-else conditionals (as described above) here

						areaColors.push(nodeColorBooleans);
						
					}
					intervalColors.push(areaColors);
				}
				$scope.classSelectors = intervalColors;	
				
				$scope.i = $scope.i+ 1;
				$scope.totalTime = $scope.totalTime + 1;

				
				if($scope.i == $scope.numSlides +1 || $scope.bit_rate != $scope.bit_rate_update)
				{
					$scope.i = 1;
				}

				$scope.bit_rate = $scope.bit_rate_update;

					
			}, $scope.intervalCount * 1000);
	};
			
	$scope.stop = function(){
		$interval.cancel(promise);
		promise = undefined;
	};

	$scope.check = function()
	{
		if($scope.my.option == 'NONE')
			{
				$scope.showBitRate = true;
				//$scope.showK = false;
				//$scope.showDistance = false

			}
			else
			{
				$scope.showBitRate = false;
			}

			if($scope.my.option == 'RAND' || $scope.my.option == 'WORST')
			{
				$scope.showK = true;
				$scope.showDistance = false;
			}
			else
			{
				$scope.showK = false;
			}

			if($scope.my.option == 'AMUSE')
			{
				$scope.showDistance = true;
				//$scope.showK = false;
			}
			else
			{
				$scope.showDistance = false;
			}
	};

	$scope.fetch = function(){

		$http.post($scope.url, {
			updateInterval: $scope.intervalCount,
			Algorithm: $scope.my.option,
			count: $scope.i,
			b_rate: $scope.bit_rate_update,
			k: $scope.k_nodes,
			dist: $scope.distance,
		}).
		success(function(data, status, headers, config){
			$scope.Interval = data.pdr_set;
			//test this after you know interval works
			$scope.feedbackNodes = data.feedback_set;
			$scope.bit_rate_update = data.bit_rate;
		}).
		error(function(data, status)
		{
			$scope.Interval = [0,0, 0];
			$scope.feedbackNode = [];
			console.log("here");


		});
		
	};


	//$scope.play();
}]);