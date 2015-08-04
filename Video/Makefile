
#
# Makefile for localServer
#

CC = gcc
CXX = g++
INCLUDES = 
CFLAGX = -g -Wall $(INCLUDES)
CXXFLAGS = -g -Wall $(INCLUDES)
LDFLAGS = 
LDLIBS = 

local-video-server: localServer.o
	gcc -g -Wall localServer.o -o local-video-server

localServer.o: localServer.c

.PHONY: clean
clean:
	rm -f *.o local-video-server

