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

            print "here"

            # all_nodes = Interval_pFive.objects.values_list('pdr_' + interv_count, bit_rate=br)
            # all_nodes = Interval_pFive.objects.filter(bit_rate=br).values_list('pdr_' + str(interv_count), 'name').order_by('pdr_' + str(interv_count))
            all_nodes = Interval_pFive.objects.filter(bit_rate=br).values_list('pdr_' + str(interv_count), 'name')
            print "made it"
            print all_nodes
            # all_nodes = Interval_pFive.objects.filter(bit_rate=br)
            ret_slide = create_ret_slide(interv_count, br, all_nodes)
            fb_nodes = run_feedback_alg(fb_algorithm, interv_count, k, dist, all_nodes)
            resp_data = {'pdr_set': ret_slide, 'feedback_set': fb_nodes, 'bit_rate': br}
            return JsonResponse(resp_data)

        elif time_interval == 1:

            # all_nodes = Interval_One.objects.filter(bit_rate=br)
            all_nodes = Interval_One.objects.filter(bit_rate=br).values_list('pdr_' + str(interv_count), 'name').order_by('pdr_' + str(interv_count))
            ret_slide = create_ret_slide(interv_count, br, all_nodes)
            fb_nodes = run_feedback_alg(fb_algorithm, interv_count, k, dist, all_nodes)
            resp_data = {'pdr_set': ret_slide, 'feedback_set': fb_nodes, 'bit_rate': br}
            return JsonResponse(resp_data)

        else:

            # all_nodes = Interval_Two.objects.filter(bit_rate=br)
            all_nodes = Interval_Two.objects.filter(bit_rate=br).values_list('pdr_' + str(interv_count), 'name').order_by('pdr_' + str(interv_count))
            ret_slide = create_ret_slide(interv_count, br, all_nodes)
            fb_nodes = run_feedback_alg(fb_algorithm, interv_count, k, dist, all_nodes)
            response = JsonResponse({'pdr_set': ret_slide, 'feedback_set': fb_nodes, 'bit_rate': br})
            return response
            
def create_ret_slide(count, bitRate, allNodes):
    
    print "in create_ret_slide method!"
    # create list containing six lists, each containing 20 lists with 20 elements each
    ret_slide = [[0 for y in range(20)] for x in range(20)]

    for node in allNodes:
        pdr_val = node[0]
        # print(pdr_val)
            
        # each node name is formatted as such: '1-1', '1-2', ... 
        # split at '-' to get the x and y coordinates on test bed
        arr = node[1].split('-')
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
        # pdr_val = getattr(rand_node, 'pdr_' + num)
        pdr_val = rand_node[0]
        print "rand pdr val: " + str(pdr_val)
        if pdr_val > 0:
            # arr = rand_node.name.split('-')
            arr = rand_node[1].split('-')
            x = int(arr[0])-1
            y = int(arr[1])-1
            ret_slide[x][y] = 1
            count = count + 1

    return ret_slide

def k_worst(k, all_nodes, interv_count):
    
    ret_slide = [[0 for y in range(20)] for x in range(20)]
    num = str(interv_count)
    # s = all_nodes.order_by('pdr_' + num)
    count = 0
    for node in all_nodes:
        # pdr_val = getattr(node, 'pdr_' + num)
        pdr_val = node[0]
        if pdr_val > 0:
            # arr = node.name.split('-')
            arr = node[1].split('-')
            x = int(arr[0])-1
            y = int(arr[1])-1
            ret_slide[x][y] = 1
            count = count + 1
            if count == k:
                break

    return ret_slide


'''
def amuse(d, all_nodes, interv_count):

    ret_slide = [[0 for y in range(20)] for x in range(20)]
    num = str(interv_count)
    s = all_nodes
    s = s.order_by('pdr_' + num)

    print "not done"

    for node in s:
        pdr_val = getattr(node, 'pdr_' + num)
        name = str(node.name)


    create_amuse_list(s, num)

    





    print "done"
    return ret_slide
'''

def create_amuse_list(ordered_list, n):
    
    node_list = [0 for x in range(ordered_list.count())]
    i = 0
    for node in ordered_list:
        # pdr_val = self.__dict__.get(node, 'pdr_' + n)
        pdr_val = getattr(node, 'pdr_' + n)
        # pdr_val = 1
        '''
        node_list[i] = str(node.name)
        i = i + 1
        '''

        if pdr_val > 0:
            node_list[i] = str(node.name)
            i = i + 1
        else: 
            del node_list[i]

    '''
    i = 0
    while i < len(node_list):
        if node_list[i] == 'X':
            del node_list[i]
        i = i + 1
    '''

    # print node_list
    return node_list



def amuse(d, all_nodes, interv_count):

    ret_slide = [[0 for y in range(20)] for x in range(20)]
    num = str(interv_count)
    s = list(all_nodes)

    # s = s.order_by('pdr_' + num)
    # s.sort()

    print "list ordered"
    # s = create_amuse_list(s, num)

    print "list made"

    while len(s) != 0:
        print('length: ' + str(len(s)))
        # get worst node
        # worst = s.pop()

        worst = s[0][1]
        print "got worst"
        del s[0]
        print "deleted worst"


        print("worst: " + worst)
        # remove worst node from list
        
        arr_worst = worst.split('-')
        # get x and y coordinates of worst node
        x_w = int(arr_worst[0])
        y_w = int(arr_worst[1])
        # note feed-back node in grid
        ret_slide[x_w][y_w] = 1

        i = 0
        while i < len(s):
            # print "here"

            # get its x and y coordinates
            node = s[i][1]
            arr = node.split('-')
            x2 = int(arr[0])
            y2 = int(arr[1])
            # calculate distance using their coordinates // distance formula
            calc_dist = calc_distance(x_w, x2, y_w, y2)
            # if input distance is greater than or equal to the calculated distance
            if d >= calc_dist:
                # remove this particular node (it is within D)
                del s[i]
            i = i + 1
        print('length: ' + str(len(s)))
    print "returned!"
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
