'''
author: Savvas

made: June 2015
'''

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, Context, loader

from .models import *
from .forms import *
import random
import math

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
                
                # if no algorithm is entered, don't send a list of feedback nodes
                if fb_algorithm == 'NONE':
                    c = RequestContext(request, {
                        'intervalList': interv_list,
                        'interval': time_interval,
                        'form': form                       
                    })
                    
                    return render(request, 'multicast_simulator/index.html', c) 

                # if an algorithm is entered, send a list of feedback nodes
                else:
                    fb_list = runFeedbackAlg(fb_algorithm, time_interval, k, br, dist, all_nodes)

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

                if fb_algorithm == 'NONE':
                    c = RequestContext(request, {
                        'intervalList': interv_list,
                        'interval': time_interval,
                        'form': form                       
                    })

                    return render(request, 'multicast_simulator/index.html', c) 

                else:
                    fb_list = runFeedbackAlg(fb_algorithm, time_interval, k, br, dist, all_nodes)

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

                if fb_algorithm == 'NONE':
                    c = RequestContext(request, {
                        'intervalList': interv_list,
                        'interval': time_interval,
                        'form': form                       
                    })

                    return render(request, 'multicast_simulator/index.html', c) 

                else:
                    fb_list = runFeedbackAlg(fb_algorithm, time_interval, k, br, dist, all_nodes)

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

def create_interv_list(timeInt, bitRate, allNodes):
    # 'slides' is the number of updates for the interval
    slides = int((8/timeInt)) 
    # create list containing six lists, each containing 20 lists with 20 elements each
    interv_list = [[[0 for c in range(20)] for b in range(20)] for a in range(slides)]

    z = 0
    while(z < slides):
        for node in allNodes:
            num = z + 1
            # get the corresponding pdr value for the slide (each node has exactly the same pdr values as slides)
            pdr_val = getattr(node, 'pdr_' + str(num))
            
            # each node name is formatted as such: '1-1', '1-2', ... 
            # split at '-' to get the x and y coordinates on test bed
            arr = node.name.split('-')
            x = int(arr[0])-1 
            y = int(arr[1])-1
            interv_list[z][x][y] = float("{0:.2f}".format(pdr_val * 100)) # insert in master array, format as %
        z = z + 1
    
    return interv_list

def runFeedbackAlg(func_name, time_interval, k, br, dist, nodes):
    if func_name == 'RAND':
        return k_Random(br, time_interval, k, nodes)
    elif func_name == 'WORST':
        return k_Worst(br, time_interval, k, nodes)
    else:
        return amuse(br, time_interval, dist, nodes)

# randomly choose k nodes with any pdr's (other than 0) as the feedback nodes
def k_Random(br, interv, k, all_nodes):
    slides = int((8/interv)) 
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

# choose k nodes with the lowest pdr's as the feedback nodes
def k_Worst(br, interv, k, all_nodes):
    slides = int((8/interv)) 
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

# amuse algorithm for choosing feedback nodes
def amuse(br, interv, d, all_nodes):
    slides = int((8/interv)) 
    ret_arr = [[[0 for c in range(20)] for b in range(20)] for a in range(slides)]
    s = all_nodes
    
    count = 1
    while(count <= slides):
        num = str(count)
        # order in ascending fashion by pdr for that specific slide
        s = s.order_by('pdr_' + num)
        worst = s[0]
        arr_worst = worst.name.split('-')
        x_w = int(arr[0])
        y_w = int(arr[1])



        count = count + 1
    return ret_arr

# distance formula
def calc_distance(x1, x2, y1, y2):
    return math.sqrt((math.pow((x1-x2),2) + math.pow((y1-y2),2)))

