'''
author: Savvas

made: June 2015
'''

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, Context, loader
from .models import *
from .forms import *
import random
import math
import json

# global variables for rate adaption algorithm
br_list = [6, 9, 12, 18, 24, 36, 48, 54]
A_t_list = []
M_t_list = []
curr_interval = -1
curr_rate = 6
window = 0
change_time = 0  
ref_time = 0

def index(request):

    # if post request:
    if request.method == 'POST':
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

        # data from front-end
        data = json.loads(request.body)
        interv_count = int(data[u'count'])
        time_interval = float(data[u'updateInterval'])
        dist = int(data[u'dist'])
        k = int(data[u'k'])
        fb_algorithm = str(data[u'Algorithm'])
        br = int(data[u'b_rate']) 
        h_low = data[u'H_low']
        w_min = data[u'W_min']
        w_max = data[u'W_max']
        delta = data[u'Delta']
        user_A_max = data[u'A_max']
        threshold_time = data[u'time']
    
        if time_interval == .5:

            all_nodes = Interval_pFive.objects.filter(bit_rate=br).values_list('pdr_' + str(interv_count), 'name').order_by('pdr_' + str(interv_count))
            A_max = calc_A_max(all_nodes)
            print "A_max: " + str(A_max)
            ret_slide = create_ret_slide(interv_count, br, all_nodes)
            
            # if user enters feed-back algorithm
            if fb_algorithm != 'NONE':
                
                fb_info = run_feedback_alg(fb_algorithm, interv_count, k, dist, all_nodes)
                # new request --> update the current time interval
                global curr_interval
                curr_interval = curr_interval + 1
                # 2d array, noting location of the feed-back nodes
                fb_slide = fb_info['ret_slide']
                # list of tuples, representing feed-back nodes (pdr value, X-Y)
                fb_data = fb_info['fb_list']
                
                # run rate adaptation
                new_rate = adapt_rate(h_low, delta, w_min, w_max, fb_data, threshold_time, A_max)

                print "new_rate: " + str(new_rate)
                resp_data = {'pdr_set': ret_slide, 'feedback_set': fb_slide, 'bit_rate': new_rate}
                # send to front-end
                return JsonResponse(resp_data)

            # no feed-back algorithm entered
            else: 
                
                # list of 0's 
                fb_slide = [[0 for z in range(20)] for y in range(20)]
                resp_data = {'pdr_set': ret_slide, 'feedback_set': fb_slide, 'bit_rate': br}
                return JsonResponse(resp_data)

        elif time_interval == 1:

            all_nodes = Interval_One.objects.filter(bit_rate=br).values_list('pdr_' + str(interv_count), 'name').order_by('pdr_' + str(interv_count))
            A_max = calc_A_max(all_nodes)
            ret_slide = create_ret_slide(interv_count, br, all_nodes)
            
            if fb_algorithm != 'NONE':
                
                fb_info = run_feedback_alg(fb_algorithm, interv_count, k, dist, all_nodes)
                global curr_interval
                curr_interval = curr_interval + 1
                fb_slide = fb_info['ret_slide']
                fb_data = fb_info['fb_list']
                # run rate adaptation
                new_rate = adapt_rate(h_low, delta, w_min, w_max, fb_data, threshold_time, A_max)

                print "new_rate: " + str(new_rate)
                resp_data = {'pdr_set': ret_slide, 'feedback_set': fb_slide, 'bit_rate': new_rate}
                return JsonResponse(resp_data)

            else: 
                
                # list of 0's 
                fb_slide = [[0 for z in range(20)] for y in range(20)]
                resp_data = {'pdr_set': ret_slide, 'feedback_set': fb_slide, 'bit_rate': br}
                return JsonResponse(resp_data)

        # time_interval == 2:
        else:

            all_nodes = Interval_Two.objects.filter(bit_rate=br).values_list('pdr_' + str(interv_count), 'name').order_by('pdr_' + str(interv_count))
            A_max = calc_A_max(all_nodes)
            ret_slide = create_ret_slide(interv_count, br, all_nodes)
            
            if fb_algorithm != 'NONE':
                
                fb_info = run_feedback_alg(fb_algorithm, interv_count, k, dist, all_nodes)
                global curr_interval
                curr_interval = curr_interval + 1
                fb_slide = fb_info['ret_slide']
                fb_data = fb_info['fb_list']
                # run rate adaptation
                new_rate = adapt_rate(h_low, delta, w_min, w_max, fb_data, threshold_time, A_max)

                print "new_rate: " + str(new_rate)
                resp_data = {'pdr_set': ret_slide, 'feedback_set': fb_slide, 'bit_rate': new_rate}
                return JsonResponse(resp_data)

            else: 
                
                # list of 0's 
                fb_slide = [[0 for z in range(20)] for y in range(20)]
                resp_data = {'pdr_set': ret_slide, 'feedback_set': fb_slide, 'bit_rate': br}
                return JsonResponse(resp_data)
            
def create_ret_slide(count, bitRate, allNodes):
    
    print "in create_ret_slide method!"
    # create list containing six lists, each containing 20 lists with 20 elements each
    ret_slide = [[0 for y in range(20)] for x in range(20)]

    # each node representation is a tuple: (PDR value, X-Y)
    for node in allNodes:
        pdr_val = node[0]
            
        # each node name is formatted as such: '1-1', '1-2', ... 
        # split at '-' to get the x and y coordinates on test bed
        arr = node[1].split('-')
        x = int(arr[0])-1 
        y = int(arr[1])-1
        ret_slide[x][y] = float("{0:.2f}".format(pdr_val * 100)) # insert in master array, format as %
    
    return ret_slide

def run_feedback_alg(func_name, count, k, dist, nodes):
    
    if func_name == 'RAND':
        return k_random(k, nodes, count)
    elif func_name == 'WORST':
        return k_worst(k, nodes, count)
    else:
        return amuse(dist, nodes, count)

def k_random(k, all_nodes, interv_count):
    
    num = str(interv_count)
    ret_slide = [[0 for y in range(20)] for x in range(20)]
    fb_nodes = []
    random.seed()
    end = all_nodes.count()-1

    count = 0
    while count < k:
        index = random.randint(0, end)
        rand_node = all_nodes[index]
        pdr_val = rand_node[0]
        if pdr_val > 0:
            fb_nodes.append(rand_node)
            arr = rand_node[1].split('-')
            x = int(arr[0])-1
            y = int(arr[1])-1
            ret_slide[x][y] = 1
            count = count + 1

    return {'ret_slide': ret_slide, 'fb_list': fb_nodes}

def k_worst(k, all_nodes, interv_count):
    
    ret_slide = [[0 for y in range(20)] for x in range(20)]
    fb_nodes = []
    num = str(interv_count)

    count = 0
    for node in all_nodes:
        pdr_val = node[0]
        if pdr_val > 0:
            fb_nodes.append(node)
            arr = node[1].split('-')
            x = int(arr[0])-1
            y = int(arr[1])-1
            ret_slide[x][y] = 1
            count = count + 1
            if count == k:
                break

    return {'ret_slide': ret_slide, 'fb_list': fb_nodes}

def create_amuse_list(ordered_list, n):
    node_list = []
    i = 0
    for node in ordered_list:
        pdr_val = node[0]
        if pdr_val > 0:
            node_list.append(node)
            i = i + 1
    return node_list

def amuse(d, all_nodes, interv_count):

    ret_slide = [[0 for y in range(20)] for x in range(20)]
    # initialize fb_node list
    fb_nodes = []
    num = str(interv_count)
    s = list(all_nodes)
    # remove nodes without information
    s = create_amuse_list(s, num)

    while len(s) != 0:

        # get worst node
        worst = str(s[0][1])
        # add it to feed-back node list
        fb_nodes.append(s[0])
        # remove worst node
        del s[0]
        # get x and y coordinates of worst node
        arr_worst = worst.split('-')
        x_w = int(arr_worst[0])
        y_w = int(arr_worst[1])
        # note feed-back node in grid
        ret_slide[x_w - 1][y_w - 1] = 1
        
        current_length_s = len(s)
        i = 0
        del_nodes = []
        # go through every other node:
        while i < current_length_s:
            # get its pdr value
            pdr_val = float("{0:.2f}".format(s[i][0] * 100))
            # get its x and y coordinates
            node = str(s[i][1])
            arr = node.split('-')
            x2 = int(arr[0])
            y2 = int(arr[1])
            # check if node is abnormal:
            if pdr_val < 85: 
                # if so, make this node a feed-back node
                # note feed-back node in grid
                ret_slide[x2 - 1][y2 - 1] = 1
                # add to feed-back node list
                fb_nodes.append(s[i])
                # add to delete node list
                del_nodes.append(i)
            # if not abnormal, check distance:
            else: 
                # calculate distance using their coordinates // distance formula
                calc_dist = calc_distance(x_w, x2, y_w, y2)
                # if input distance is greater than or equal to the calculated distance
                if d >= calc_dist:
                    # remove this particular node (it is within D) -- add to delete node list
                    del_nodes.append(i)
            i = i + 1

        # iterate through del_nodes list and delete nodes
        while len(del_nodes) > 0:
            index = del_nodes.pop()
            del s[index]

    return {'ret_slide': ret_slide, 'fb_list': fb_nodes}


# main rate adaption algorithm
def adapt_rate(h_low, delta, w_min, w_max, fb_data, threshold_time, A_max):

    global window
    global curr_interval
    global curr_rate
    global A_t_list
    global M_t_list
    global change_time
    global ref_time

    rate = curr_rate
    if curr_interval == 0:
        window = w_min

    A_t = 0
    M_t = 0

    '''
    print fb_data
    print "A_t_list: "
    print A_t_list
    print "M_t_list: "
    print M_t_list
    '''

    # calculate A_t and M_t: 
    count = 0
    for fb_node in fb_data:
        '''
        print "Node #" + str(count) 
        '''
        pdr_val = float("{0:.2f}".format(fb_node[0] * 100))
        if pdr_val < h_low - delta:
            A_t = A_t + 1
            '''
            print "1. pdr_val < h_low - delta"
            print "pdr_val: " + str(pdr_val) + " h_low: " + str(h_low) + " delta: " + str(delta)
            print "A_t added!"
            '''

        if pdr_val > h_low - delta and pdr_val < 98: 
            M_t = M_t + 1
            '''
            print "2. pdr_val > h_low"
            print "pdr_val: " + str(pdr_val) + " h_low: " + str(h_low)
            print "M_t added!"
            '''
        count = count + 1

    A_t_list.insert(0, A_t)
    M_t_list.insert(0, M_t)

    # get new calculated bit rate:
    rate_info = get_rate(rate, A_max)

    action = rate_info['action']
    new_rate = rate_info['rate']
    curr_rate = new_rate
    # change_time = rate_info['change_time']
    # alter window
    window = get_window_size(action, window, w_max, threshold_time, w_min)

    return new_rate

# rate decision
def get_rate(rate, A_max): 

    global change_time
    global curr_interval
    global M_t_list
    global A_t_list
    global br_list
    global window
    # 0 == hold, 1 == increase, -1 == decrease
    action = 0
    
    print "** curr_interval: " + str(curr_interval) + ", change_time: " + str(change_time) + ", window: " + str(window)
    if (curr_interval - change_time) > window:
        can_decrease = True
        can_increase = True
        i = 0
        while i < window: 
            A_t = A_t_list[i]
            M_t = M_t_list[i]
            if A_t < A_max:
                can_decrease = False
            
            '''
            print "A_t: " + str(A_t) + ", M_t: " + str(M_t) + ", A_max: " + str(A_max)
            print "A_t + M_t = " + str(A_t + M_t)
            '''

            if A_t + M_t > A_max:
                can_increase = False
            i = i + 1
        print can_increase
        if (can_decrease == True) and rate > br_list[0]:
            # get next lower rate
            rate = get_next_rate(rate, 0) 
            # action is to decrease
            action = -1 
            change_time = curr_interval
        if (can_increase == True) and rate < br_list[7]:
            rate = get_next_rate(rate, 1)
            action = 1
            change_time = curr_interval

    return {'rate': rate, 'action': action}

def get_next_rate(bit_rate, direction):
    global br_list
    index = 0
    # find in br_list the current bit rate
    for i in range(0, len(br_list)): 
        if bit_rate == br_list[i]:
            index = i
    # if getting lower rate
    if direction == 0:
        # return bit rate that is one left in the list (lower)
        return br_list[index-1]
    # if getting higher rate
    else:
        # return bit rate that is one right in the list (higher)
        return br_list[index+1]

# window size determination
def get_window_size(action, window, w_max, threshold_time, w_min):
    global ref_time
    global curr_interval

    # decrease
    if action == -1:
        window = min(w_max, 2 * window)
        ref_time = curr_interval
    # increase
    elif action == 1:
        ref_time = curr_interval
    # hold
    elif ((curr_interval - ref_time) > threshold_time) and (action == 0):
        window = max(w_min, window - 1)
        ref_time = curr_interval

    # return {'window': window, 'ref_time': ref_time} 
    return window

# gets A_max value
def calc_A_max(all_nodes):
    active_node_count = 0
    for node in all_nodes:
        pdr_val = node[0]
        if pdr_val > 0:
            active_node_count = active_node_count + 1
    # A_max should be 5% of the total active node count
    A_max = round(active_node_count * .05)
    return A_max

# distance formula
def calc_distance(x1, x2, y1, y2):
    return math.sqrt((math.pow((x1-x2),2) + math.pow((y1-y2),2)))
