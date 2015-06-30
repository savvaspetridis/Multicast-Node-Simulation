from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, Context, loader
# from django.utils import simplejson

#from .models import *
#from .forms import *
import random
import math
import json
def calc_distance(x1, x2, y1, y2):
    return math.sqrt((math.pow((x1-x2),2) + math.pow((y1-y2),2)))

random.seed()


ret_slide = [[0 for y in range(20)] for x in range(20)]
num = 0.5

s = []

count = 0

while count < 170:
	s.append(int(random.random()*10))
	count = count + 1

s.sort()

xVals = []

count = 0

while count < 170:
	xVals.append(int(random.random()*10))
	count = count + 1

yVals = []

count = 0
d = 10

while count < 170:
	yVals.append(int(random.random()*10))
	count = count + 1




while len(s) != 0:
    # print "while " + str(s.count())
    worst = s.pop()
    # arr_worst = worst.name.split('-')
    # get x and y coordinates of worst node
    xVal = xVals.pop()
    yVal = yVals.pop()

    xVal = xVal % 10
    print 
    yVal = yVal % 10
    print "xVal : yVal" + " " + str(xVal) + " " + str(yVal) 
    print "#####################################################"

    # x_offsetPlus = x_w + d
    ret_slide[xVal][yVal] = 1
    pDR = s.pop()
    #print " check x and Y vals "+ str(xVals.pop()) + " " + str(yVals.pop())
    # go through the rest of the nodes
    count = 0
    while count < len(s):

        # get its x and y coordinates
        # arr = node.name.split('-')
        x = xVals[count]
        
        y = yVals[count]
        print "x : y" + " " + str(x) + " " + str(y)

        # calculate distance using their coordinates // distance formula
        # d = 20
        calc_dist =  calc_distance(xVal, x, yVal, y) # calc_distance(x_w, x2, y_w, y2)
        print "distance " + str(calc_dist)
        count = count + 1
        # if input distance is greater than or equal to the calculated distance
        if d >= calc_dist:
            # remove this particular node (it is within D)
            s.pop()
            xVals.pop()
            yVals.pop()
            # simulate O(n) operation inside for loop
            for val in xVals:
            	val = val * 1.5

print ret_slide




