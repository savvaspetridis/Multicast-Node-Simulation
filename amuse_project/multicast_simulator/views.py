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

            # if time interval is .5 seconds created 17 updates (slides) (should be 16)
            if time_interval == 0.5:

                # get all nodes with the corresponding bit rate entered
                all_nodes = Interval_pFive.objects.filter(bit_rate=br)
                interv_list = create_interv_list(time_interval, br, all_nodes)

                # if k_random algorithm for feedback node selection is chosen ... 
                if(fb_algorithm == 'RAND'):
                    fb_list = k_Random(time_interval, k)

                # if k_worst algorithm for feedback node selection is chosen ...
                if(fb_algorithm == 'WORST'):
                    fb_list = k_Worst(br, time_interval, k)

                # if amuse algorithm for feedback node selection is chosen ...
                # if(fb_algorithm == 'AMUSE'):

                c = RequestContext(request, {
                        # 'fbList': fb_list,
                        'intervalList': interv_list,
                        'interval': time_interval,
                        'form': form                       
                    })
                
                return render(request, 'multicast_simulator/index.html', c) 
    
            if time_interval == 1:
                all_nodes = Interval_One.objects.filter(bit_rate=br)
                interv_list = create_interv_list(time_interval, br, all_nodes)

                c = RequestContext(request, {
                        'intervalList': interv_list,
                        'interval': time_interval,
                        'form': form                       
                    })
                
                return render(request, 'multicast_simulator/index.html', c) 
    
            if time_interval == 2: 
                all_nodes = Interval_Two.objects.filter(bit_rate=br)
                interv_list = create_interv_list(time_interval, br, all_nodes)


                c = RequestContext(request, {
                        'intervalList': interv_list,
                        'interval': time_interval,
                        'form': form                       
                    })
                
                return render(request, 'multicast_simulator/index.html', c) 
    
    # if not a POST request:             
    else:
        form = SimulationForm()

    # return render(request, 'multicast_simulator/index.html', {'form': form})
    return render(request, 'multicast_simulator/start.html', {'form': form})

def k_Random(interv, k):
    slides = int((10/interv)-4) 
    ret_arr = [[[0 for z in range(slides)] for y in range(20)] for x in range(20)]
    upper_bound = 19 # 20 nodes for both x and y direction
    fbNum = k 
    random.seed()
    
    z = 0
    for z in range(slides):
        j = 0
        for j in range(fbNum):
            x = random.randint(0, upper_bound)
            y = random.randint(0, upper_bound)
            ret_arr[x][y][z] = 1

    return ret_arr

def k_Worst(br, interv, k):
    slides = int((10/interv)-4) 
    print("slides: " + str(slides))
    ret_arr = [[[0 for c in range(slides)] for b in range(20)] for a in range(20)]
    all_nodes = Interval_pFive.objects.filter(bit_rate=br)
    
    count = 1
    while(count <= slides):
        num = str(count)
        print(num)
        s = all_nodes.order_by('pdr_' + num)
        s = s[:k]
        for node in s:
            arr = node.name.split('-')
            print(arr)
            x = int(arr[0])-1
            print('x: ' + str(x)) 
            y = int(arr[1])-1
            print('y: ' + str(y))
            z = int(num)-1
            print('z: ' + str(z))
            ret_arr[x][y][z] = 1
        count = count + 1

    return ret_arr

def create_interv_list(timeInt, bitRate, allNodes):
    slides = int((8/timeInt)) 
    interv_list = [[[0 for c in range(20)] for b in range(20)] for a in range(slides)]

    z = 0
    while(z < slides):
        for node in allNodes:
            num = z + 1
            print('z: ' + str(z))
            print('num: ' + str(num))
            pdr_val = getattr(node, 'pdr_' + str(num))
            arr = node.name.split('-')
            x = int(arr[0])-1 
            y = int(arr[1])-1
            interv_list[z][x][y] = float("{0:.2f}".format(pdr_val * 100))
        z = z + 1
    
    return interv_list