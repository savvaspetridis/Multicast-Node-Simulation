
var app = angular.module('app', ['chart.js'] ).config(function($httpProvider) {
$httpProvider.defaults.xsrfCookieName = 'csrftoken';
$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
app.controller('theController', ['$scope', '$interval', '$http', '$templateCache', function($scope, $interval, $http, $templateCache)
{
	

	

	// get double array of node objects returned by django

	//won't keep this

	//var dataDump = {{intervalList}};
	
	//this serves as the counter for the controller and it is updated every interval
	$scope.i = 1;
	$scope.totalTime = 0;

	// for bit rates graph
	$scope.bit_rates_wrapper = []; 
	$scope.bit_rates_graph = [];		
	$scope.bit_rates_wrapper.push($scope.bit_rates_graph);
	$scope.times_graph =[];
	$scope.series_bit_rate = ['bit-rate vs. time (seconds)',];

	// for throughput graph		
	$scope.throughput_wrapper = [];
	$scope.throughput_graph = [];
	$scope.throughput_wrapper.push($scope.throughput_graph);
	$scope.series_throughput = ['throughput (megabits) vs. time (seconds)',];

	$scope.showGraphs = false;


	// for min max avg node statistics
	$scope.minNode;
	$scope.maxNode;
	$scope.avgNode;

	// for other user input
	$scope.H = 88;
	$scope.Delta = 3;
	$scope.W_min = 4;
	$scope.W_max = 16;
	$scope.windowTime = 20;
	$scope.A_max = 5;

	// this is for the throughput calculation
	$scope.throughput = 0;
	$scope.throughput_new =0;
	$scope.throughput_org = 0;




	// will be calculaed by django 
	$scope.Interval;
	$scope.intervalBuffer = [];
	$scope.COUNTER = $scope.totalTime;
	$scope.classSelectors;
	$scope.intervalCount = 0.5;
	$scope.bit_rate = 6;
	$scope.bit_rate_update = $scope.bit_rate;
	$scope.numSlides = (8.0 / $scope.intervalCount);


	// will be calculated at each interval by django
	$scope.feedbackNodes = [];
	$scope.showUpdate = true;
	$scope.showBitRate = true;
	$scope.showK = false;
	$scope.showDistance = false;
	$scope.algorithms = ['NONE', 'WORST', 'RAND', 'AMUSE'];
	$scope.k_nodes = 6;
	$scope.distance = 6;



	// django puts this here
	$scope.my ={option : 'NONE'};
	//$scope.method = 'JSONP';
	$scope.url = '/update';

	$scope.options = {
			animation : false,
	}


	var promise;


	$scope.play = function()
	{
		if( angular.isDefined(promise))
			return;
		$scope.showUpdate = false;

		$scope.run_calculations();

		



		promise = $interval($scope.run_calculations, $scope.intervalCount * 1000);
	};

	$scope.run_calculations = function()
	{
		$scope.fetch();

		$scope.numSlides = (8.0 / $scope.intervalCount);
		


		// for min max avg node statistics
		$scope.minNode = 100.0;
		$scope.maxNode = 0.0;
		$scope.avgNode = 0.0;


		//$scope.Interval; // set the interval equal to the ith index in the dataDump variable

		
		var currVals = $scope.intervalBuffer;
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

		$scope.avgCheck = 0;
		




		for(var j = 0; j < $scope.intervalBuffer.length; j++)
		{
			var areaColors = [];
			var checkArray = $scope.intervalBuffer[j];
			for(var l = 0; l < checkArray.length; l++)
			{
				var nodeColorBooleans = [];

				if($scope.feedbackNodes[j][l] == 1) // green dotted line 
				{
					nodeColorBooleans.push(true);

				}
				else
				{
					nodeColorBooleans.push(false);
				}
				if($scope.feedbackNodes[j][l] == -1) //Fuscia 
				{
					nodeColorBooleans.push(true);

				}
				else
				{
					nodeColorBooleans.push(false);
				}

				if (currVals[j][l] <= 50.0 && currVals[j][l] > 25.0) // orange
				{
					nodeColorBooleans.push(true);
				}
				else
				{
					nodeColorBooleans.push(false);
				}

				if (currVals[j][l] <= 75.0 && currVals[j][l] > 50.0) // yellow
				{
					nodeColorBooleans.push(true);
				}
				else
				{
					nodeColorBooleans.push(false);
				}

				if (currVals[j][l] > 75.0) // green
				{
					nodeColorBooleans.push(true);
				}
				else
				{
					nodeColorBooleans.push(false);
				}

				if(currVals[j][l] == -100.0) // black
				{
					nodeColorBooleans.push(true);
					$scope.avgCheck = $scope.avgCheck + 1;
				}
				else
				{
					nodeColorBooleans.push(false);
				}
				if (currVals[j][l] == 0.0) // grey
				{
					nodeColorBooleans.push(true);
				}
				else
				{
					nodeColorBooleans.push(false);
				}
				if(currVals[j][l] <= 25.0 && currVals[j][l] > 0.0) // red
				{
					nodeColorBooleans.push(true);
				}
				else
				{
					nodeColorBooleans.push(false);
				}



				// add any new if-else conditionals (as described above) here

				areaColors.push(nodeColorBooleans);

				if(currVals[j][l] > $scope.maxNode)
				{
					$scope.maxNode = currVals[j][l];

				}
				if(currVals[j][l] < $scope.minNode && currVals[j][l] > 0.0)
				{
					$scope.minNode = currVals[j][l];
				}
				if(currVals[j][l] > 0.0)
				{
					$scope.avgCheck = $scope.avgCheck + 1;
					$scope.avgNode = $scope.avgNode + currVals[j][l];
				}
				
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


		// add bit rate info to graph
		$scope.times_graph.push($scope.COUNTER * $scope.intervalCount);
		if($scope.times_graph.length > 120)
		{
			$scope.times_graph.shift();
		}
		$scope.bit_rates_wrapper[0].push($scope.bit_rate_update);

		if($scope.bit_rates_wrapper[0].length >120)
		{
			$scope.bit_rates_wrapper[0].shift();
		}

		if($scope.throughput_new <= $scope.throughput_org)
		{
			$scope.throughput_org = 0;
		}

		$scope.throughput += $scope.throughput_new - $scope.throughput_org;

		$scope.throughput_org = $scope.throughput_new;

		$scope.throughput_wrapper[0].push($scope.throughput);

		if($scope.throughput_wrapper[0].length >120)
		{
			$scope.throughput_wrapper[0].shift();
		}

		$scope.bit_rate = $scope.bit_rate_update;

		$scope.avgNode = $scope.avgNode / $scope.avgCheck;

		$scope.Interval = $scope.intervalBuffer;
		$scope.showGraphs = true;



	}
			
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
			H_low: $scope.H,
			Delta: $scope.Delta,
			W_min: $scope.W_min,
			W_max: $scope.W_max,
			time: $scope.windowTime,
			A_max: $scope.A_max
		}).
		success(function(data, status, headers, config){
			$scope.intervalBuffer = data.pdr_set;
			//test this after you know interval works
			$scope.feedbackNodes = data.feedback_set;
			$scope.bit_rate_update = data.bit_rate;
			$scope.throughput_new = data.throughput;

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

