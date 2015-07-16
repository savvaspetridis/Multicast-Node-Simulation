from django.db import models

class Packet_List(models.Model):
    name = models.CharField(max_length=5)
    bit_rate = models.IntegerField()
    packets = models.TextField()
    exp_name = models.TextField()
    # date_of_exp = models.Datemax_indexField()

    def __str__(self):
        return self.name


class Interval_pFive(models.Model):
    name = models.CharField(max_length=5)
    bit_rate = models.IntegerField()
    packets_recieved = models.ForeignKey(Packet_List)
    pdr_1 = models.FloatField()
    pdr_1_max_index = models.IntegerField()
    pdr_2 = models.FloatField()
    pdr_2_max_index = models.IntegerField()
    pdr_3 = models.FloatField()
    pdr_3_max_index = models.IntegerField()
    pdr_4 = models.FloatField()
    pdr_4_max_index = models.IntegerField()
    pdr_5 = models.FloatField()
    pdr_5_max_index = models.IntegerField()
    pdr_6 = models.FloatField()
    pdr_6_max_index = models.IntegerField()
    pdr_7 = models.FloatField()
    pdr_7_max_index = models.IntegerField()
    pdr_8 = models.FloatField()
    pdr_8_max_index = models.IntegerField()
    pdr_9 = models.FloatField()
    pdr_9_max_index = models.IntegerField()
    pdr_10 = models.FloatField()
    pdr_10_max_index = models.IntegerField()
    pdr_11 = models.FloatField()
    pdr_11_max_index = models.IntegerField()
    pdr_12 = models.FloatField()
    pdr_12_max_index = models.IntegerField()
    pdr_13 = models.FloatField()
    pdr_13_max_index = models.IntegerField()
    pdr_14 = models.FloatField()
    pdr_14_max_index = models.IntegerField()
    pdr_15 = models.FloatField()
    pdr_15_max_index = models.IntegerField()
    pdr_16 = models.FloatField()
    pdr_16_max_index = models.IntegerField()
    exp_name = models.TextField()
    is_access_point = models.BooleanField()
    
    


    def __str__(self):
        return self.name

class Interval_One(models.Model):
    name = models.CharField(max_length=5)
    bit_rate = models.IntegerField()
    packets_recieved = models.ForeignKey(Packet_List)
    pdr_1 = models.FloatField()
    pdr_1_max_index = models.IntegerField()
    pdr_2 = models.FloatField()
    pdr_2_max_index = models.IntegerField()
    pdr_3 = models.FloatField()
    pdr_3_max_index = models.IntegerField()
    pdr_4 = models.FloatField()
    pdr_4_max_index = models.IntegerField()
    pdr_5 = models.FloatField()
    pdr_5_max_index = models.IntegerField()
    pdr_6 = models.FloatField()
    pdr_6_max_index = models.IntegerField()
    pdr_7 = models.FloatField()
    pdr_7_max_index = models.IntegerField()
    pdr_8 = models.FloatField()
    pdr_8_max_index = models.IntegerField()
    exp_name = models.TextField()
    is_access_point = models.BooleanField()
 

    def __str__(self):
        return self.name

class Interval_Two(models.Model):
    name = models.CharField(max_length=5)
    bit_rate = models.IntegerField()
    packets_recieved = models.ForeignKey(Packet_List)
    pdr_1 = models.FloatField()
    pdr_1_max_index = models.IntegerField()
    pdr_2 = models.FloatField()
    pdr_2_max_index = models.IntegerField()
    pdr_3 = models.FloatField()
    pdr_3_max_index = models.IntegerField()
    pdr_4 = models.FloatField()
    pdr_4_max_index = models.IntegerField()
    exp_name = models.TextField()
    is_access_point = models.BooleanField()

    def __str__(self):
        return self.name

# test





'''
class Node(models.Models):
    id = models.primaryKey()
    b6 = models.foreignKey(bitrate6)
    b9
    b12

# Raphael

class Node(models.Models):
    name = 
    bitRate = 
    update_,5
    update_1
    update_2



class bitrate6(models.Model):
    upates_1_sec = models.foreignKey(update1)
    update_2_sec = models.foreignKey(update2)
    #8 more each float field represents an updat at max_index name

class Interval62000(models.Model):

class update1(models.Model):
    one = 
    two = 
    three =
    eight = 

class update2(models.Model)

class update(models.Model)
# 10 for update 1

class update_point_five 


class Interval_point_five(models.Model):
    name = models.foreign.....
    bitrate = 
    val1 = 
    val2 = 
    val3 =
    ... val 17
Node -> bitrates -> updates

Noide -> updates -> bitrates

whatever makes more sense
'''