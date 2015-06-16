'''
Raphael

This script generates the average packets recieved over a given set of intervals for some bit-rate

'''


# Import Python modules
import socket
import struct
import dpkt
import sys
import os
import glob
import time
import psycopg2
from datetime import datetime


path = sys.argv[1]
MBPS = sys.argv[2]
MBPS = sys.argv[2]
Month = sys.argv[3]
Day = sys.argv[4]
Year = sys.argv[5]
hour = sys.argv[6]
minute = sys.argv[7]
second =sys.argv[8]
offset = sys.argv[9]
calcDate = datetime(int(Year), int(Month), int(Day), int(minute), int(second), 0)
dayOfWeek = calcDate.weekday()
dayOfYear = calcDate.day


counter = 10

selectIntervals = []



while counter < len(sys.argv):
	selectIntervals.append(float(sys.argv[counter]))
	counter = counter + 1

# print selectIntervals




# Raphael

# for a database if it's set up

'''



conn = psycopg2.connect(database="test", user="postgres", password="wko845", host="127.0.0.1", port="5432")
# print "Opened database successfully"
cur = conn.cursor()

'''


# read the times from timefile
#timefile = open('Logs_test/times.txt', 'r') 
#Can try using this method, does not work on my computer
'''
timefile=open('C:/Users/Craig/Documents/ColumbiaFall2012/alcatel lucent project/Logs10_11_full/times.txt','r')
lines = timefile.read().splitlines()
print lines[0]
print lines[1]

time1 = time.strptime(lines[0], "%a %b  %d %H:%M:%S %Z %Y")
time2 = time.strptime(lines[1], "%a %b  %d %H:%M:%S %Z %Y")
timefile.close()

starttime=time.mktime(time1)
endtime=time.mktime(time2)
'''
#Time is in format (year, month, day, hour, min, sec, day of week 0 is mon 1 is tuesday ... , day of year, dst=1 or non dst=0)
#starttime=time.mktime((2015,01,06,12,42,23,1,6,0))
#endtime=time.mktime((2015,01,06,12,42,33,1,6,0))
try:
	starttime=time.mktime((int(Year), int(Month), int(Day), int(hour), int(minute), int(second), dayOfWeek, dayOfYear, 0))
except:
	starttime=time.mktime((int(Year), int(Month), int(Day), int(hour), int(minute), int(second), dayOfWeek, dayOfYear, 1))
endtime = starttime + float(offset) + 0.1

# print str(starttime) + " " + str(endtime)
x_data=[]
y_data=[]
totalBytesData=[]
CaptureTimeData=[]
averagePhyThroughputData=[]
x_send=[]
y_send=[]
DataSent=[]
TimeSent=[] 
ThroughputSent=[]
PacketsMissed=[]
initPacket=""
finalPacket=""
initframe=""
finalframe=""
totalCount=0


# Raphael

# here we're going to create an array of floats containing the relative times and payloads of the packets sent [BUILD-OUT]

TimesSent = []

# here we're going to store an array of the sender's payloads

PayloadsSender = []





for infile in glob.glob( os.path.join(path, '*.pcap') ):
	
	a=[]
	a=infile.split('bcast_data_rcvd_')
	b=infile.split('bcast_data_sent_')
	if len(b)>1:
		saveflg=0
		if len(b)>1:
			x=b[1].split('-')
		if len(a)>1:
			x=a[1].split('-')
		y=x[1].split('.pcap')
		x=x[0]
		y=y[0]
		
		# Open pcap file
		pcapFile = open(infile,"rb")

		# Initialize pcap file iterator
		pcapReader = dpkt.pcap.Reader(pcapFile)
		
		# Initialize total number of bytes on wire
		totalBytes = 0
		
		# Initialize frame counter
		frameCounter = 1
		
		# Loop through all frames in pcap file
	        Missed = ""
		try:
			cnt=0
			for ts, buf in pcapReader:
				if ts>starttime and ts<endtime:
					cnt=cnt+1
					#print cnt
					if (frameCounter == 1):
					
					# This is the first frame in the pcap file
					# Save initial timestamp value
						initialTs = ts
						data = buffer(buf,72,4)
						data2 = data[::-1]
						packetCounter = struct.unpack("@B",data2[0])[0] * 256 + struct.unpack("@B",data2[1])[0]
						initPacket=packetCounter
					# Calculate bytes on wire for this frame
					length = len(buf)

                                        data = buffer(buf,72,4)
					data2 = data[::-1]
					
					packetCounter = struct.unpack("@B",data2[0])[0] * 256 + struct.unpack("@B",data2[1])[0]
					
					PayloadsSender.append(packetCounter)
					TimesSent.append(ts-starttime)


					finalPacket=packetCounter
					if (frameCounter == 1):
						frameCounter = packetCounter
						initframe=frameCounter
					'''
					elif (frameCounter != packetCounter):
						while (frameCounter != packetCounter):
						   Missed = Missed + str(frameCounter) + " "
						   #print Missed
						   frameCounter = frameCounter + 1
					'''
					# Save current timestamp value
					currentTs = ts

					 
					# Raphael

					#TimeSent.append(new [or whatever the python syntax is] pack(packCounter, currentTS-initialTS)) or currentTS-starttime
					TotalCount = cnt

					
				
					# Update frame counter
					frameCounter = frameCounter + 1
					finalframe=frameCounter
		except dpkt.dpkt.NeedData:

			# shouldn't need to touch anything from here
		
			# Current frame is broken
			
			# Calculate capture time (s)
			captureTime = currentTs - initialTs
	
		if saveflg==0 and len(a)>1:
			saveflg=1
			x_data.append(x)
			y_data.append(y)
			PacketsMissed.append(Missed)
			
		if saveflg==0 and len(b)>1:
				
			x_send.append(x)
			y_send.append(y)
			PacketsMissed.append(Missed)
		
		# Close pcap file
		pcapFile.close

#we need to get these right






# get data
database = []

#toSend= "'INSERT INTO " + str(MBPS) + "mbps (Node, " 
sentData = []
sentData.append("1-1")
'''
count = 0
while count < TotalCount:
	toSend += "recieved# " + str(count) + ", "
	count = count + 1;
toSend = toSend[:-1] #to remove last comma
'''
count = 0
# toSend += "VALUES (1.1, "
while count < TotalCount:
	sentData.append(True) 
	count = count + 1
# toSend = toSend[:-1] #to remove last comma
# toSend += ");"
# curr.execute('toSend') 
# print(toSend)




#start and end time given from output of calcualte Bytes Sender Seq Numbers
startframe=initPacket
endframe=finalPacket
###


x_data=[]
y_data=[]
totalBytesData=[]
CaptureTimeData=[]
averagePhyThroughputData=[]
x_send=[]
y_send=[]
DataSent=[]
TimeSent=[] 
ThroughputSent=[]
for infile in glob.glob( os.path.join(path, '*.pcap') ):
	# print infile

	# list of booleans recieved and not recieved
	got = []



	
	a=[]
	b=[]
	#print "current file is: " + infile	
	a=infile.split('bcast_data_rcvd_')
	b=infile.split('bcast_data_sent_')
	
	if len(b) > 1:
		continue	
	

	# Raphael

	# This is to store the node number for the database



	nodeKeyTemp=a[1].split('.pcap')
	nodeKey=nodeKeyTemp[0]
	# print nodeKey
	got.append(nodeKey)

	# This is to store the timestamp objects recieved
	Node = []

	# This is to store the payloads:
	PayloadsReciever = []	

	if len(a)>1 or len(b)>1:
		saveflg=0

		if len(b)>1:
			x=b[1].split('-')

		if len(a)>1:
			x=a[1].split('-')

		y=x[1].split('.pcap')
		x=x[0]
		y=y[0]
		
		# Open pcap file
		pcapFile = open(infile,"rb")
		dataaval=0
		# Initialize pcap file iterator
		try:
			pcapReader = dpkt.pcap.Reader(pcapFile)
			dataaval=1
		except:
			# print "no data"
			dataaval=0
		# Initialize total number of bytes on wire
		totalBytes = 0
		currentTs=0
		initialTs=0
		#print pcapReader
		# Initialize frame counter
		frameCounter = 1
		
		# Loop through all frames in pcap file
		if dataaval==1:
			try:
				mostrecentpacket=0
				
				for ts, buf in pcapReader:
					try:
						data = buffer(buf,72,4)
						data2 = data[::-1]
						packetCounter = struct.unpack("@B",data2[0])[0] * 256 + struct.unpack("@B",data2[1])[0]
					except:
						# print "index out of range"
						noPrint = 0
						packetCounter = -1
					#print packetCounter

					if ((packetCounter>=startframe and packetCounter<=endframe and startframe<endframe) or ((packetCounter>=startframe or packetCounter<=endframe) and startframe>endframe)) and ts>(starttime-1) and ts<(endtime+1):
						if (frameCounter == 1):
						
						# This is the first frame in the pcap file
						# Save initial timestamp value
							initialTs = ts
							#print "Intial time " + str(ts)
							#print "Initial Packet Counter " + str(packetCounter)
							
						mostrecentpacket=packetCounter	
						# Calculate bytes on wire for this frame
						length = len(buf)

				
						
						# Raphael
						PayloadsReciever.append(packetCounter)

						
						
						# Update total number of bytes on wire
						totalBytes = totalBytes + len(buf)
					
						# Save current timestamp value
						currentTs = ts

						# Raphael: save timestamp
						Node.append(currentTs-initialTs)


					
						# Update frame counter
						frameCounter = frameCounter + 1
				#print "Most recent packet " + str(mostrecentpacket)
			except dpkt.dpkt.NeedData:
				#print here
			
				# Current frame is broken
			
				# Calculate capture time (s)
				
				captureTime = currentTs - initialTs
			
				# Calculate average PHY throughput (Kbps)
				
				if captureTime==0:
					averagePhyThroughput=0
				else:
					averagePhyThroughput = ((totalBytes * 8) / captureTime) / 1000
				if saveflg==0 and len(a)>1:
					saveflg=1
					x_data.append(x)
					y_data.append(y)
					totalBytesData.append(totalBytes)
					CaptureTimeData.append(captureTime)
					averagePhyThroughputData.append(averagePhyThroughput)
					# Print statistics
				if saveflg==0 and len(b)>1:
					
					x_send.append(str(x))
					y_send.append(str(y))
					DataSent.append(str(totalBytes))
					TimeSent.append(str(captureTime))
					ThroughputSent.append(str(averagePhyThroughput))
				PayloadsReciever.append(-1)
			
				# Close pcap file
				#pcapFile.close
			
				# Exit
				#sys.exit(0)
			
			count = 1
			for pack in Node:
				# toSend += "recieved# " + str(count) + ", "
				count = count + 1;
			# toSend = toSend[:-1] #to remove last comma
			# toSend += "VALUES (" + nodeKey + ", "
			counter = 0
			sender = 0
			# print str(len(PayloadsSender))
			# print str(len(PayloadsReciever))
			'''
			if counter == 0 :
				print PayloadsSender
				print PayloadsReciever
			'''
			while counter < len(PayloadsSender) :
				if(sender == len(PayloadsReciever)):
					break
				if(PayloadsSender[counter] == PayloadsReciever[sender]):
					got.append(True) 
					sender = sender + 1
					counter = counter + 1
				else :
					got.append(False)
					counter = counter + 1
			database.append(got)
			pcapFile.close
			#curr.execute('toSend')


# list of intervals 

doubleTimeCount = []
for interval in selectIntervals:
	counters = 0
	stopPac = []
	tSub1 = interval
	for time in TimesSent: 
		if time < tSub1:
			counters = counters + 1
		else:
			tSub1 += interval
			stopPac.append(counters)
			counters = counters + 1
	doubleTimeCount.append(stopPac)
	


# create triple matrix, with each list of double matrixes represents an update interval,
# each double matrix holds lists corresponding to each node with the average packets recieved at each 
# time interval 



doubleTimeCounter = 0
avgAllIntervals = []
for inter in selectIntervals:
	tSub1 = doubleTimeCount[doubleTimeCounter]
	avgValsTimeInterval =[]
	isSender = 0
	for singleNode in database:
		
		if isSender == 0:
			isSender = isSender + 1
			continue
		
		#toSend = "INSERT INTO " + str(MBPS) + str(inter) + " VALUES ("
		avgValsSingleNode = []
		counter = 0
		while counter < len(tSub1):
			counter1 = 1
			packSent = 0
			packRecieved = 0
			while counter1 < tSub1[counter]:
				# print counter1
				# print data[counter1]
				if counter1 == len(singleNode):
					break
				if singleNode[counter1] :
					packRecieved = packRecieved + 1
					packSent = packSent + 1
					counter1 = counter1 + 1
				else:
					packSent = packSent + 1
					counter1 = counter1 + 1
			if packSent != 0:
				avgToAdd = float (packRecieved) / float (packSent)
			# print avgToAdd
			else:
				avgToAdd = -1.0
			avgValsSingleNode.append(avgToAdd)
			counter = counter + 1
		avgValsTimeInterval.append(avgValsSingleNode)
	avgAllIntervals.append(avgValsTimeInterval)
	doubleTimeCounter = doubleTimeCounter + 1

'''
# create interval tables
for inter in selectIntervals:
	tableQuery = "CREATE TABLE Interval" + str(MBPS) + str(int(inter*1000)) + " ("
	count = 0
	while count < len(avgAllIntervals[0]):
		tableQuery += "NODE" + str(count) + " REAL, "
		# tableArray.append(str(count))
		count = count + 1;
	tableQuery = tableQuery[:-2] #to remove last comma	
	tableQuery += ");"
	print(tableQuery)

'''

# create table queries for all intervals
doubleTimeCounter = 0
for singleInterval in avgAllIntervals:
	finalCounter = 0
	while finalCounter < len(singleInterval):
		update_time = str(selectIntervals[doubleTimeCounter])
		if update_time == "0.5":
			update_time = "_pFive"
		if update_time == "1.0":
			update_time = "_One"
		if update_time == "2.0":
			update_time = "_Two"
		toSend = "entry" + str(MBPS)+ str(finalCounter) + " = Interval" + update_time +"(name = \"" + database[finalCounter][0] + "\", bit_rate = " + str(MBPS) + ", "
		count = 1
		for average in singleInterval[finalCounter]:
			toSend += "pdr_" + str(count) + " = %f, " % average
			count = count + 1
		toSend = toSend[:-2]
		toSend += ")\nentry" + str(MBPS)+ str(finalCounter) + ".save()"
		
		finalCounter = finalCounter + 1
		print toSend
	doubleTimeCounter = doubleTimeCounter + 1




'''
conn.commit()
conn.close
'''


			

			


