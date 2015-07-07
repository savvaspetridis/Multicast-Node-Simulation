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

        return render(request, 'multicast_simulator/index.html', {'form': form})


def get_ret_slide(request):

    if request.method == 'POST':

        data = json.loads(request.body)
        interv_count = int(data[u'count'])
        print "interv_count: " + str(interv_count)
        time_interval = float(data[u'updateInterval'])
        dist = int(data[u'dist'])
        k = int(data[u'k'])
        fb_algorithm = str(data[u'Algorithm'])
        br = int(data[u'b_rate'])

        if time_interval == .5:

            all_nodes = Interval_pFive.objects.filter(bit_rate=br)
            ret_slide = create_ret_slide(interv_count, br, all_nodes)
            fb_nodes = run_feedback_alg(fb_algorithm, interv_count, k, dist, all_nodes)
            resp_data = {'pdr_set': ret_slide, 'feedback_set': fb_nodes, 'bit_rate': br}
            return JsonResponse(resp_data)

        elif time_interval == 1:

            all_nodes = Interval_One.objects.filter(bit_rate=br)
            ret_slide = create_ret_slide(interv_count, br, all_nodes)
            fb_nodes = run_feedback_alg(fb_algorithm, interv_count, k, dist, all_nodes)
            resp_data = {'pdr_set': ret_slide, 'feedback_set': fb_nodes, 'bit_rate': br}
            return JsonResponse(resp_data)

        else:

            all_nodes = Interval_Two.objects.filter(bit_rate=br)
            ret_slide = create_ret_slide(interv_count, br, all_nodes)
            fb_nodes = run_feedback_alg(fb_algorithm, interv_count, k, dist, all_nodes)
            response = JsonResponse({'pdr_set': ret_slide, 'feedback_set': fb_nodes, 'bit_rate': br})
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
    
    if func_name == 'NONE':
        ret_arr = [[0 for z in range(20)] for y in range(20)]
        return ret_arr
    elif func_name == 'RAND':
        return k_random(k, nodes, count)
    elif func_name == 'WORST':
        return k_worst(k, nodes, count)
    else:
        return amuse(dist, nodes, count)

def k_random(k, all_nodes, interv_count):
    
    num = str(interv_count)
    ret_slide = [[0 for y in range(20)] for x in range(20)]
    random.seed()
    end = all_nodes.count()-1

    count = 0
    while count < k:
        index = random.randint(0, end)
        rand_node = all_nodes[index]
        pdr_val = getattr(rand_node, 'pdr_' + num)
        if pdr_val > 0:
            arr = rand_node.name.split('-')
            x = int(arr[0])-1
            y = int(arr[1])-1
            ret_slide[x][y] = 1
            count = count + 1

    return ret_slide

def k_worst(k, all_nodes, interv_count):
    
    ret_slide = [[0 for y in range(20)] for x in range(20)]
    num = str(interv_count)
    s = all_nodes.order_by('pdr_' + num)
    count = 0
    for node in s:
        pdr_val = getattr(node, 'pdr_' + num)
        if pdr_val > 0:
            print(str(pdr_val))
            arr = node.name.split('-')
            x = int(arr[0])-1
            y = int(arr[1])-1
            ret_slide[x][y] = 1
            count = count + 1
            if count == k:
                break

    return ret_slide

def amuse(d, all_nodes, interv_count):
    
    ret_slide = [[0 for y in range(20)] for x in range(20)]
    num = str(interv_count)
    s = all_nodes
    print "order start"
    s = s.order_by('pdr_' + num)
    print "order end"

    while s.count() != 0:
        print "enter while loop of count"
        worst = s[0]
        print "while loop 1"
        arr_worst = worst.name.split('-')
        print "while loop 2"
        # get x and y coordinates of worst node
        x_w = int(arr_worst[0])
        print "while loop 3"
        y_w = int(arr_worst[1])
      

        ret_slide[x_w][y_w] = 1
        print "while loop 5"
        s = s.exclude(name=worst.name)
        print "while loop 6"
        # go through the rest of the nodes
        print "enter for loop (for rest of nodes)"
        iteration = 0
        for node in s:
            print "count: " + str(iteration)

            # get its x and y coordinates
            arr = node.name.split('-')
            x2 = int(arr[0])
            y2 = int(arr[1])
            # calculate distance using their coordinates // distance formula
            calc_dist = calc_distance(x_w, x2, y_w, y2)
            # if input distance is greater than or equal to the calculated distance
            if d >= calc_dist:
                # remove this particular node (it is within D)
                print "exclude begin"
                s = s.exclude(name=node.name)
                print "exclude end"
            iteration = iteration + 1
    print "returned!!"
    return ret_slide


# main rate adaption algorithm
def adapt_rate(lowest_rate, w_min, interv_count):
    rate = lowest_rate
    window = w_min
    change_time = interv_count
    ref_time = interv_count




'''
# window size determination
def get_window_size():

# rate decision
def get_rate(): 
'''


# distance formula
def calc_distance(x1, x2, y1, y2):
    return math.sqrt((math.pow((x1-x2),2) + math.pow((y1-y2),2)))
