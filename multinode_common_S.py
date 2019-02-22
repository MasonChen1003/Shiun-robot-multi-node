# Write your code here :-)
#Microbit Radio multi-node bi-direction communication test
#Features:
#   multi-nodes communication with re-transmition
#   current ids show on LEDs (sid: brighter,did: darker)
#   random tx rate test
#   auto select non-used sid
#   sid collision avoidence
#Usage:
#   Button-A: start, Button-B: change sid
#   plot format: (tx_rate,rx_rate,ack_loss rate)
#   rate unit: Hz/s, throughput can estimated by * 32
#   limitation: max nodes = 20, due to reserved 20 LEDs to show device id
#LICENSE: MIT
#Author: WuLung Hsu, wuulong@gmail.com
#Document: https://paper.dropbox.com/doc/MbitBot--AWWwIfCnEicRuc7gSfO_tmcJAg-DG5SSj5zQhBv1CoAgDtAG

# Add one motion file to test Shiun robot by Mason

from microbit import *
import radio
import utime
import random

class Comm():
    def __init__(self):
        self.sid = 0
        self.ack = "~"
        self.ack_cnt = 0
        self.used_ids = []
        self.used_ids_next = []
        self.ack_received = False
# Add "Say Hi" motion file by Mason
        self.p0_angle = 0
        self.p1_angle = 0
        self.p2_angle = 0
        self.sayhi_p0 = [  90, 105, 110, 110,110, 110,110,110,110, 110, 110, 105, 100,  95, 90,  90, 200 ]
        self.sayhi_p1 = [  90,  90, 90, 90,90, 90,90,90,90, 90,  90,  90,  90,  90,  90,  90, 200 ]
        self.sayhi_p2 = [  90, 105, 110, 85, 60, 85,110, 85, 60,85, 110,105, 100, 95, 90,  90, 200 ]

        radio.config(queue=6,address=0x75626972,channel=4,data_rate=radio.RATE_1MBIT)
        radio.on()
        sleep(100)
        pin0.set_analog_period(17)
        pin0.write_analog(90)
        pin1.set_analog_period(17)
        pin1.write_analog(90)
        pin2.set_analog_period(17)
        pin2.write_analog(90)
        pass

    def say_hi(self,s0, s1,s2):
        for j in range(16) :
            pin0.write_analog(int(s0[j]))
            pin1.write_analog(int(s1[j]))
            pin2.write_analog(int(s2[j]))
            sleep(60)

    def tx(self,did,value):
        tx_txt = "%i:%i:%s" %(self.sid,did,str(value))
        radio.send(tx_txt)
    def get_new_id(self,used_ids):
        while True:
            id = len(self.used_ids) + 1
            if id in used_ids:
               id = id +1
            else:
                break
        return id

    def wait_start(self):
        while True:
            if button_a.was_pressed():
                display.show("F")
                self.used_ids = self.find_used_ids()
                self.sid = self.get_new_id(self.used_ids)
                self.show_id()
                break
    def show_id(self):
        display.clear()
        sid = self.sid - 1
        display.set_pixel(sid%5,int(sid/5),9)
        for id in self.used_ids:
            if id>0:
                uid = id - 1
                display.set_pixel(uid%5,int(uid/5),5)
    def find_used_ids(self):
        used_ids=[]
        time_s = utime.ticks_us()

        while True: # start current measurement
            time_now = utime.ticks_us()
            time_use = utime.ticks_diff(time_now,time_s)
            if 1500000 - time_use <0: # 1.5s
                #display.show("W")
                break
            incoming = radio.receive()
            print (incoming)
            if incoming:
                items = incoming.split(":")
                if len(items)==3:
                    did = int(items[0])
                    if not (did in used_ids):
                        used_ids.append(did)
        return used_ids

    def bi_transfer(self):
        cur_num_tx = 0
        self.wait_start()

        while True:
            self.rx_cnt = 0
            self.rx_new_cnt = 0
            self.tx_cnt = 0
            self.tx_new_cnt = 0
            self.ack_cnt = 0
            test_period = 1 #s
            test_tick = int(test_period * 1000000)
            time_s = utime.ticks_us()
            time_l = time_s

            #broadcast device exist every test period
            self.tx(0,str(0))
            # rate target hz
            rate_target = random.randint(1, 100)
            send_tick = int(test_tick/rate_target)

            while True: # start current measurement
                incoming = radio.receive()
                if incoming:
                    items = incoming.split(":")
                    if len(items)==3:

                        sid,did,value = items
                        sid = int(sid)
                        did = int(did)
                        if not sid in self.used_ids:
                            self.used_ids.append(sid)
                            self.show_id()

                        if not sid in self.used_ids_next:
                            self.used_ids_next.append(sid)

                        if sid == self.sid: # sid collision
                            self.sid = self.get_new_id(self.used_ids)

                        if did == self.sid:
                            if value == self.ack:
                                self.ack_received = True
                                self.ack_cnt += 1
                            elif value == 'a':
                                display.show("Y")
                                self.say_hi(self.sayhi_p0,self.sayhi_p1,self.sayhi_p2)
                                display.clear()
                            elif value == 'b':
                                display.show("A")
                                self.say_hi(self.sayhi_p0,self.sayhi_p1,self.sayhi_p2)
                                display.clear()
                            else:
                                self.rx_new_cnt += 1
                                self.tx(sid,self.ack)

comm = Comm()
comm.bi_transfer()