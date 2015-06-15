from django.db import models

class Interval_pFive(models.Model):
    name = models.CharField(max_length=5)
    bit_rate = models.IntegerField()
    pdr_1 = models.FloatField()
    pdr_2 = models.FloatField()
    pdr_3 = models.FloatField()
    pdr_4 = models.FloatField()
    pdr_5 = models.FloatField()
    pdr_6 = models.FloatField()
    pdr_7 = models.FloatField()
    pdr_8 = models.FloatField()
    pdr_9 = models.FloatField()
    pdr_10 = models.FloatField()
    pdr_11 = models.FloatField()
    pdr_12 = models.FloatField()
    pdr_13 = models.FloatField()
    pdr_14 = models.FloatField()
    pdr_15 = models.FloatField()
    pdr_16 = models.FloatField()
    pdr_17 = models.FloatField()

    def __str__(self):
        return self.name

class Interval_One(models.Model):
    name = models.CharField(max_length=5)
    bit_rate = models.IntegerField()
    pdr_1 = models.FloatField()
    pdr_2 = models.FloatField()
    pdr_3 = models.FloatField()
    pdr_4 = models.FloatField()
    pdr_5 = models.FloatField()
    pdr_6 = models.FloatField()
    pdr_7 = models.FloatField()
    pdr_8 = models.FloatField()

    def __str__(self):
        return self.name

class Interval_Two(models.Model):
    name = models.CharField(max_length=5)
    bit_rate = models.IntegerField()
    pdr_1 = models.FloatField()
    pdr_2 = models.FloatField()
    pdr_3 = models.FloatField()
    pdr_4 = models.FloatField()

    def __str__(self):
        return self.name



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
    #8 more each float field represents an updat at time name

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