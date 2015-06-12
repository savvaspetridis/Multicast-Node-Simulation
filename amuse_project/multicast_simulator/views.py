# Savvas
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import *

def index(request):
    # user will input bit-rate and update time interval --> if bite-rate = 6 and time interval = .5 ...
    # nodes not present --> 0!
    br = 6
    time_interval = .5 
    if time_interval == .5:
        # get all nodes with the corresponding bit rate and update interval
        
        n1_arr = [[0 for x in range(20)] for x in range(20)]
        n2_arr = [[0 for x in range(20)] for x in range(20)]
        n3_arr = [[0 for x in range(20)] for x in range(20)]
        n4_arr = [[0 for x in range(20)] for x in range(20)]
        n5_arr = [[0 for x in range(20)] for x in range(20)]
        n6_arr = [[0 for x in range(20)] for x in range(20)]
        n7_arr = [[0 for x in range(20)] for x in range(20)]
        n8_arr = [[0 for x in range(20)] for x in range(20)]
        n9_arr = [[0 for x in range(20)] for x in range(20)]
        n10_arr = [[0 for x in range(20)] for x in range(20)]
        n11_arr = [[0 for x in range(20)] for x in range(20)]
        n12_arr = [[0 for x in range(20)] for x in range(20)]
        n13_arr = [[0 for x in range(20)] for x in range(20)]
        n14_arr = [[0 for x in range(20)] for x in range(20)]
        n15_arr = [[0 for x in range(20)] for x in range(20)]
        n16_arr = [[0 for x in range(20)] for x in range(20)]
        n17_arr = [[0 for x in range(20)] for x in range(20)]

        all_nodes = Interval_pFive.objects.filter(bit_rate=br)
        
        for node in all_nodes:
            arr = node.name.split('-')
            x = int(arr[0])-1 
            y = int(arr[1])-1
            n1_arr[x][y] = node.pdr_1
            n2_arr[x][y] = node.pdr_2
            n3_arr[x][y] = node.pdr_3
            n4_arr[x][y] = node.pdr_4
            n5_arr[x][y] = node.pdr_5
            n6_arr[x][y] = node.pdr_6
            n7_arr[x][y] = node.pdr_7
            n8_arr[x][y] = node.pdr_8
            n9_arr[x][y] = node.pdr_9
            n10_arr[x][y] = node.pdr_10
            n11_arr[x][y] = node.pdr_11
            n12_arr[x][y] = node.pdr_12
            n13_arr[x][y] = node.pdr_13
            n14_arr[x][y] = node.pdr_14
            n15_arr[x][y] = node.pdr_15
            n16_arr[x][y] = node.pdr_16
            n17_arr[x][y] = node.pdr_17

        i = 0
        j = 0 

        for i in range(20):
            for j in range(20):
                if n1_arr[i][j] == None:
                    n1_arr[i][j] = 0
                if n2_arr[i][j] == None:
                    n2_arr[i][j] = 0
                if n3_arr[i][j] == None:
                    n3_arr[i][j] = 0
                if n4_arr[i][j] == None:
                    n4_arr[i][j] = 0
                if n5_arr[i][j] == None:
                    n5_arr[i][j] = 0
                if n6_arr[i][j] == None:
                    n6_arr[i][j] = 0
                if n7_arr[i][j] == None:
                    n7_arr[i][j] = 0
                if n8_arr[i][j] == None:
                    n8_arr[i][j] = 0
                if n9_arr[i][j] == None:
                    n9_arr[i][j] = 0
                if n10_arr[i][j] == None:
                    n10_arr[i][j] = 0
                if n11_arr[i][j] == None:
                    n11_arr[i][j] = 0
                if n12_arr[i][j] == None:
                    n12_arr[i][j] = 0
                if n13_arr[i][j] == None:
                    n13_arr[i][j] = 0
                if n14_arr[i][j] == None:
                    n14_arr[i][j] = 0
                if n15_arr[i][j] == None:
                    n15_arr[i][j] = 0
                if n16_arr[i][j] == None:
                    n16_arr[i][j] = 0 
                if n17_arr[i][j] == None:
                    n17_arr[i][j] = 0


    interv_list = [n1_arr, n2_arr, n3_arr, n4_arr, n5_arr, n6_arr, n7_arr, n8_arr, n9_arr, n10_arr, n11_arr, n12_arr, n13_arr, n14_arr, n15_arr, n16_arr, n17_arr]  
    # if time_interval = 1:
    # if time_interval = 2: 

    return render(request, 'multicast_simulator/index.html', {'intervalList': interv_list})


'''
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('multicast_simulator/index.html')
    context = RequestContext(request, {
        'latest_question_list': latest_question_list,
    })
    return HttpResponse(template.render(context))

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
'''
