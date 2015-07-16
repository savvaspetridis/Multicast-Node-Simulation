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
exp_Name = sys.argv[10]
calcDate = datetime(int(Year), int(Month), int(Day), int(minute), int(second), 0)
dayOfWeek = calcDate.weekday()
dayOfYear = calcDate.day

# used to keep track of the last index before the user specified intervals
#  note: if you want to use intervals other than .5, 1 and 2 you must alter the db formatting section at the end (i.e. add your interval to the list of if clauses for update_time)
counter = 11


# the intervals specified by the user
selectIntervals = []



while counter < len(sys.argv):
	selectIntervals.append(float(sys.argv[counter]))
	counter = counter + 1






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

# store the names of the nodes that are access points
senders = []

# boolean list of 'recived packets' for the sender (i.e. all true)
sentData = []


# parses the pcap files of the sender(s)

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
		nodeKeyTemp=b[1].split('.pcap')
		nodeKey=nodeKeyTemp[0]
		senders.append(nodeKey)
		
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




		





# Holds lists of boolean values for the packets recieved
database = []

# Holds strings of 1's and zeros corresponding to the vectors in database
NodeStrings = []


count = 0

while count < TotalCount:
	sentData.append(True) 
	count = count + 1





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
	

	# list of booleans recieved and not recieved for given pcap file
	got = []

	# string of recieved and not recieved
	boolean_string = ""
	
	a=[]
	b=[]
	#print "current file is: " + infile	
	a=infile.split('bcast_data_rcvd_')
	b=infile.split('bcast_data_sent_')
	
	if len(b) > 1:
		continue	
	

	# Raphael

	# This is to store the names of the nodes in database

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

						ThroughputSent.append(buf)

				
						
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
				count = count + 1;

			counter = 0
			sender = 0

			while counter < len(PayloadsSender) :
				if(sender == len(PayloadsReciever)):
					break
				if(PayloadsSender[counter] == PayloadsReciever[sender]):
					got.append(True) 
					boolean_string += "1"
					sender = sender + 1
					counter = counter + 1
				else :
					got.append(False)
					boolean_string += "0"
					counter = counter + 1
			database.append(got)
			NodeStrings.append(boolean_string)
			pcapFile.close
			




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
# triple array with pdr values 
avgAllIntervals = []

for inter in selectIntervals:
	tSub1 = doubleTimeCount[doubleTimeCounter]
	avgValsTimeInterval =[]
	isSender = 0
	for singleNode in database:
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


# print queries for the access point(s)
doubleTimeCounter = 0
for access_point in senders:
	ap_wrapper = access_point.replace("-", "_")
	sent_list = "node_" + str(MBPS) + "_" + ap_wrapper + "_" + exp_Name + " = Packet_List(name = \"" + access_point + "\", bit_rate = " + str(MBPS) + ", packets = \"\", exp_name = \"" + exp_Name + "\")\nnode_" + str(MBPS) + "_" + ap_wrapper + "_" + exp_Name + ".save()"
	print sent_list

	index = 0
	
	for update_time in selectIntervals:
		time = int(8.0 / float(update_time))
		new_ud_time = ""
		if update_time == 0.5:
			new_ud_time = "_pFive"
		if update_time == 1.0:
			new_ud_time = "_One"
		if update_time == 2.0:
			new_ud_time = "_Two"
		ap_query = "entry_ap" + str(MBPS) + str(index) + " = Interval" + new_ud_time + "(name = \"" + access_point + "\", bit_rate = " + str(MBPS) + ", packets_recieved = node_" + str(MBPS) + "_" + str(ap_wrapper) + "_" + str(exp_Name) +", "
		count_ap = 0
		while count_ap < time :
			ap_query += "pdr_" + str(count_ap+1) + " = 1, pdr_" + str(count_ap + 1) + "_max_index = " + str(doubleTimeCount[index][count_ap]) + ", "
			count_ap = count_ap + 1
		ap_query += "exp_name = \"" + exp_Name + "\", is_access_point = True)\nentry_ap" + str(MBPS) + str(index) + ".save()"
		print ap_query
		index = index + 1
	doubleTimeCounter = doubleTimeCounter + 1



# create Packet_Lists models
val_list_entry_count = 0
for val_string in NodeStrings:
	val_list_name = database[val_list_entry_count][0]
	val_list_name_wrapper = val_list_name.replace("-", "_")
	# exp_name_wrapper = exp_Name.replace(" ", "_")
	node_Entry = "node_" + str(MBPS) + "_" + val_list_name_wrapper + "_" + exp_Name + " = Packet_List(name = \"" + val_list_name + "\", bit_rate = " + str(MBPS) + ", packets = \""+ val_string + "\", exp_name = \"" + exp_Name + "\")\nnode_" + str(MBPS) + "_" + val_list_name_wrapper + "_" + exp_Name + ".save()"
	print node_Entry
	val_list_entry_count = val_list_entry_count + 1

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
		val_list_name = database[finalCounter][0]
		val_list_name_wrapper = val_list_name.replace("-", "_")
		# exp_name_wrapper = exp_Name.replace(" ", "_")
		toSend = "entry" + str(MBPS)+ str(finalCounter) + " = Interval" + update_time +"(name = \"" + val_list_name + "\", bit_rate = " + str(MBPS) + ", packets_recieved = " + "node_" + str(MBPS) + "_" + val_list_name_wrapper + "_" + exp_Name + ", "
		count = 1
		for average in singleInterval[finalCounter]:
			toSend += "pdr_" + str(count) + " = %f, " % average
			toSend += "pdr_" + str(count) + "_max_index = " + str(doubleTimeCount[doubleTimeCounter][count-1]) + ", "
			count = count + 1
		toSend += "exp_name = \"" + exp_Name + "\", "
		# toSend = toSend[:-2]
		toSend += "is_access_point = False)\nentry" + str(MBPS) +  str(finalCounter) + ".save()"
		
		finalCounter = finalCounter + 1
		print toSend
	doubleTimeCounter = doubleTimeCounter + 1






			

			


