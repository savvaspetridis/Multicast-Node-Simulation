'''
author: Savvas

made: June 2015
'''

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, Context, loader
# from django.utils import simplejson

from .models import *
from .forms import *
import random
import math
import json


def index(request):

    # if post request:
    if request.method == 'POST':
        print "index method"
        form = SimulationForm(request.POST)

        # check if the input is valid:
        if form.is_valid(): 

            # get entered br, time_interval, fb_algorithm, k, and distance (for amuse)
            br = form.cleaned_data['bitRate']
            time_interval = form.cleaned_data['updateInterval']
            fb_algorithm = form.cleaned_data['fbNodeAlg']
            k = form.cleaned_data['k']
            dist = form.cleaned_data['d']

            c = RequestContext(request, {
                    'k': k,
                    'dist': dist,
                    'bit_rate': br,
                    'interval': time_interval,
                    'alg': fb_algorithm,
                    'form': form,                       
                })
                
            return render(request, 'multicast_simulator/index.html', c) 
    else:
        form = SimulationForm()

        return render(request, 'multicast_simulator/start.html', {'form': form})


def get_ret_slide(request):

    print "get_ret_slide"
    # if request.is_ajax():
    if request.method == 'POST':

        data = json.loads(request.body)

        print data
        interv_count = int(data[u'count'])
        time_interval = float(data[u'updateInterval'])
        dist = int(data[u'dist'])
        k = int(data[u'k'])
        fb_algorithm = str(data[u'Algorithm'])
        print str(fb_algorithm)
        br = int(data[u'b_rate'])

        if time_interval == .5:

            print '??'

            all_nodes = Interval_pFive.objects.filter(bit_rate=br)
            ret_slide = create_ret_slide(interv_count, br, all_nodes)
            fb_nodes = run_feedback_alg(fb_algorithm, interv_count, k, dist, all_nodes)

            print 'maybe?'

            resp_data = {'pdr_set': 'ret_slide', 'feedback_set': 'fb_nodes', 'bit_rate': 'br'}
            return JsonResponse(resp_data)

        elif time_interval == 1:

            all_nodes = Interval_One.objects.filter(bit_rate=br)
            ret_slide = create_ret_slide(interv_count, br, all_nodes)
            fb_nodes = run_feedback_alg(fb_algorithm, interv_count, k, dist, all_nodes)

            resp_data = {'pdr_set': 'ret_slide', 'feedback_set': 'fb_nodes', 'bit_rate': 'br'}
            return JsonResponse(resp_data)

        #if time_interval == 2: 
        else:

            print "step 1"
            all_nodes = Interval_Two.objects.filter(bit_rate=br)
            print "step 2"
            print str(interv_count)
            print str(br)
            print str(all_nodes)

            ret_slide = create_ret_slide(interv_count, br, all_nodes)
            print "step 3"
            fb_nodes = run_feedback_alg(fb_algorithm, interv_count, k, dist, all_nodes)
            print "step 4"

            # resp_data = {'pdr_set': 'ret_slide', 'feedback_set': 'fb_nodes', 'bit_rate': 'br'}
            response = JsonResponse({'pdr_set': ret_slide, 'feedback_set': fb_nodes, 'bit_rate': br})
            print response
            print "step 5"
            return response
            
            


def create_ret_slide(count, bitRate, allNodes):
    print "in create_ret_slide method!"
    # create list containing six lists, each containing 20 lists with 20 elements each
    ret_slide = [[0 for y in range(20)] for x in range(20)]

    for node in allNodes:
        pdr_val = getattr(node, 'pdr_' + str(count))
            
        # each node name is formatted as such: '1-1', '1-2', ... 
        # split at '-' to get the x and y coordinates on test bed
        arr = node.name.split('-')
        x = int(arr[0])-1 
        y = int(arr[1])-1
        ret_slide[x][y] = float("{0:.2f}".format(pdr_val * 100)) # insert in master array, format as %
    
    return ret_slide

def run_feedback_alg(func_name, count, k, dist, nodes):
    print "in run_feedback_alg method!"
    print func_name
    # slides = int((8/time_interval))
    if func_name == 'NONE':
        print "func name is NONE!"
        ret_arr = [[0 for z in range(20)] for y in range(20)]
        return ret_arr
    elif func_name == 'RAND':
        return k_random(k, nodes)
    elif func_name == 'WORST':
        return k_worst(k, nodes, count)
    else:
        return amuse(dist, nodes, count)

def k_random(k, all_nodes):
    ret_slide = [[0 for y in range(20)] for x in range(20)]
    random.seed()

    j = 0
    while j < k:
        index = random.randint(0, end)
        arr = all_nodes[index].name.split('-')
        x = int(arr[0])-1
        y = int(arr[1])-1
        ret_slide[x][y] = 1
        j = j + 1

    return ret_slide

def k_worst(k, all_nodes, interv_count):
    
    ret_slide = [[0 for y in range(20)] for x in range(20)]
    num = str(interv_count)
    s = all_nodes.order_by('pdr_' + num)
    s = s[:k]
    for node in s:
        arr = node.name.split('-')
        x = int(arr[0])-1
        y = int(arr[1])-1
        ret_slide[x][y] = 1

    return ret_slide

def amuse(d, all_nodes, interv_count):
    ret_slide = [[0 for y in range(20)] for x in range(20)]
    num = str(interv_count)
    s = all_nodes
    s = s.order_by('pdr_' + num)

    while s.count() != 0:
        worst = s[0]
        arr_worst = worst.name.split('-')
        # get x and y coordinates of worst node
        x_w = int(arr_worst[0])
        y_w = int(arr_worst[1])
        ret_slide[x_w][y_w] = 1
        s = s.exclude(name=worst.name)
        # go through the rest of the nodes
        for node in s:
            # get its x and y coordinates
            arr = node.name.split('-')
            x2 = int(arr[0])
            y2 = int(arr[1])
            # calculate distance using their coordinates // distance formula
            calc_dist = calc_distance(x_w, x2, y_w, y2)
            # if input distance is greater than or equal to the calculated distance
            if d >= calc_dist:
                # remove this particular node (it is within D)
                s = s.exclude(name=node.name)

    return ret_slide


# distance formula
def calc_distance(x1, x2, y1, y2):
    return math.sqrt((math.pow((x1-x2),2) + math.pow((y1-y2),2)))

'''
def index(request):
    
    # if user inputs data: 
    if request.method == 'POST':
        form = SimulationForm(request.POST)

        # check if valid input 
        if form.is_valid():
            
            # extrapolate entered bit rate, update interval, and feedback node selection algorithm from form
            br = form.cleaned_data['bitRate']
            time_interval = form.cleaned_data['updateInterval']
            fb_algorithm = form.cleaned_data['fbNodeAlg']
            k = form.cleaned_data['k']
            dist = form.cleaned_data['d']
            
            # if the update time is 1/2 seconds
            if time_interval == 0.5:

                # get all nodes with the corresponding bit rate entered
                all_nodes = Interval_pFive.objects.filter(bit_rate=br)
                interv_list = create_interv_list(time_interval, br, all_nodes)
                
               
                fb_list = run_feedback_alg(fb_algorithm, time_interval, k, br, dist, all_nodes)

                c = RequestContext(request, {
                    'fbList': fb_list,
                    'intervalList': interv_list,
                    'interval': time_interval,
                    'form': form                       
                })
                
                return render(request, 'multicast_simulator/index.html', c) 
    
            if time_interval == 1:
                all_nodes = Interval_One.objects.filter(bit_rate=br)
                interv_list = create_interv_list(time_interval, br, all_nodes)

                fb_list = run_feedback_alg(fb_algorithm, time_interval, k, br, dist, all_nodes)

                c = RequestContext(request, {
                    'fbList': fb_list,
                    'intervalList': interv_list,
                    'interval': time_interval,
                    'form': form                       
                })
                
                return render(request, 'multicast_simulator/index.html', c) 
    
            if time_interval == 2: 
                all_nodes = Interval_Two.objects.filter(bit_rate=br)
                interv_list = create_interv_list(time_interval, br, all_nodes)

                fb_list = run_feedback_alg(fb_algorithm, time_interval, k, br, dist, all_nodes)

                c = RequestContext(request, {
                    'fbList': fb_list,
                    'intervalList': interv_list,
                    'interval': time_interval,
                    'form': form                       
                })
                
                return render(request, 'multicast_simulator/index.html', c) 
    
    # if not a POST request:             
    else:
        form = SimulationForm()

    return render(request, 'multicast_simulator/start.html', {'form': form})
'''

'''
def k_random(br, slides, k, all_nodes):
    ret_arr = [[[0 for z in range(20)] for y in range(20)] for x in range(slides)]
    random.seed()
    end = all_nodes.count()-1
    
    z = 0
    while(z < slides):
        j = 0
        while(j < k):
            index = random.randint(0, end)
            arr = all_nodes[index].name.split('-')
            x = int(arr[0])-1
            y = int(arr[1])-1
            ret_arr[z][x][y] = 1
            j = j + 1
        z = z + 1

    return ret_arr
'''
'''
# choose k nodes with the lowest pdr's as the feedback nodes
def k_worst(br, slides, k, all_nodes):
    ret_arr = [[[0 for c in range(20)] for b in range(20)] for a in range(slides)]
    
    count = 1
    while(count <= slides):
        num = str(count)
        # order in ascending fashion by pdr for that specific slide
        s = all_nodes.order_by('pdr_' + num)
        s = s[:k]
        for node in s:
            arr = node.name.split('-')
            x = int(arr[0])-1
            y = int(arr[1])-1
            z = int(num)-1
            ret_arr[z][x][y] = 1 # '1' means it is a feedback node, '0' means it is not
        count = count + 1

    return ret_arr
'''

'''
# amuse algorithm for choosing feedback nodes
def amuse(br, slides, d, all_nodes):
    ret_arr = [[[0 for c in range(20)] for b in range(20)] for a in range(slides)]
    s = all_nodes
    count = 1
    while count <= slides:
        s = all_nodes
        # num is used to delineate which pdr value to take
        num = str(count)
        # order in ascending fashion by pdr for that specific slide
        s = s.order_by('pdr_' + num)
        # while list of all 'active' nodes != 0
        while s.count() != 0:
            # node with worst pdr is the first node
            worst = s[0]
            arr_worst = worst.name.split('-')
            # get x and y coordinates of worst node
            x_w = int(arr_worst[0])
            y_w = int(arr_worst[1])
            ret_arr[count-1][x_w-1][y_w-1] = 1
            s = s.exclude(name=worst.name)
            # go through the rest of the nodes
            for node in s:
                # get its x and y coordinates
                arr = node.name.split('-')
                x2 = int(arr[0])
                y2 = int(arr[1])
                # calculate distance using their coordinates // distance formula
                calc_dist = calc_distance(x_w, x2, y_w, y2)
                # if input distance is greater than or equal to the calculated distance
                if d >= calc_dist:
                    # remove this particular node (it is within D)
                    s = s.exclude(name=node.name)
            # remove current 'worst' node, so it is not chosen again
        count = count + 1
    return ret_arr
'''



