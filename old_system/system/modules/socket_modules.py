# -*- coding: utf-8 -*-
import socket
import time
import threading

def grid_list2str(grid_list, cp_pair):
	grid_str_list = ["Grid ["+", ".join(grid.teams)+"] "+str(cp_pair[0](grid))+" "+str(cp_pair[1](grid)) for grid in grid_list]
	return "["+", ".join(grid_str_list)+"]"

def send(data, pid):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(("localhost", 50000+pid))
    soc.send(data.encode('utf-8'))
    soc.close()

def receive(pid):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(("localhost", 50000+pid))
    data = soc.recv(1024)
    soc.close()
    return data

def send_and_receive(data, pid):
	
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.connect(("localhost", 50000+pid))

	def snd(soc, data):
	    soc.send(data.encode('utf-8'))

	t1 = threading.Thread(target=snd, args=(soc, data))
	t1.setDaemon(True)
	t1.start()

	data = soc.recv(1024)
	soc.close()
	return data

if __name__ == '__main__':
    #send("Yo", 0)
    #print(receive(0))
    print(send_and_receive("Hi", 0))