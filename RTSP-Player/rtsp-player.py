import os
import tkinter as tk
from tkinter import LEFT, Button, filedialog
from tkinter import ttk
from videoPlayer import Player
from functools import partial
import cv2
import socket
import threading

choose_video = 0
Max_video_num = 10

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.player = [[0] for x in range(Max_video_num + 1)]
        
        self.videopath = [[0] for x in range(Max_video_num)]
        self.entry     = [[0] for x in range(Max_video_num)]
        self._canvas   = [[0] for x in range(Max_video_num)]
        self.frame     = [[0] for x in range(Max_video_num)]
        self.frame_    = [[0] for x in range(Max_video_num)]
        
        self.Time = 0
        self.v = 0
        self.choose_voice = 0
        self.total_question_num = 0
        self.now_question_num = 0
        self.mark = 1
        self.question = list()
        self.ans = [[0] for x in range(10000)]
        self.time_sq = 0.5
        
        self.title("media_player")
        self.state("zoomed")
        # self.choose_mode()
        
        # self.dir_name = filedialog.askdirectory()
        # self.video_list = self.getAllFiles()
        
        self.rtsp_list = ["rtsp://admin:cuhksz123456@10.20.30.101", 
                "rtsp://admin:cuhksz123456@10.20.30.123", 
                "rtsp://admin:cuhksz123456@10.20.30.121",
                "rtsp://admin:cuhksz123456@10.20.30.124",
                "rtsp://admin:cuhksz123456@10.20.30.116",
                "rtsp://admin:cuhksz123456@10.20.30.129",
                "rtsp://admin:cuhksz123456@10.20.30.119"]
        
        self.video_list = []
        
        for url in self.rtsp_list:
            capture = cv2.VideoCapture(url)
            if not capture.isOpened():
                print(f"Failed to open video stream from {url}")
            else:
                self.video_list.append(url)
                
        self.video_num = len(self.video_list)
        
        #print(self.video_list)
        
        for x in range(len(self.video_list)+1):
            self.player[x] = Player()
            
        self.que = tk.Frame(self, width=100, height=100)
        label = tk.Label(self.que, text="Now Choosed Video No.: " + str( choose_video + 1), font=('',10, 'bold italic'),bg="#7CCD7C",
                width=65 ,height=2,
                padx=10, pady=2, borderwidth=10, relief="sunken")
        label.pack()
        self.que.place(x = 950, y = 10)
            
        fp=open('timeline.txt', 'w')
        print("", file=fp)
        fp.close()
        fp=open('timeline.txt', 'a')
        print("0: " + self.video_list[0], file=fp)
        fp.close()
            
        self.player[ choose_video].set_volume(100)
        for x in range(self.video_num):
            if x !=  choose_video:
                # print(x, self.player[x].get_volume())
                self.player[x].set_volume(0)
        #print(self.video_num)
        self.create_video_view()
        
        # self.create_time()
        # self.create_choose()
        self.create_choose_video()
        # self.bind_all("<space>", self.pause_click)
        client_thread = threading.Thread(target=self.start_client)
        client_thread.start()
        
    def start_client(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

        host = '10.26.10.103'

        port = 9999

        print('Waiting for server.')
        s.connect((host, port))
        while True:
            msg = s.recv(1024)
            
            if msg == 'q':
                break
            
            elif msg.decode('utf-8') != '':
                num = int(msg.decode('utf-8'))
                print (num)
                self.click((num - 1)*4 + 2)
                s.send('Data received successfully!'.encode('utf-8'))

            
        s.close()    
    
    def getAllFiles(self):
        listFiles = os.listdir(self.dir_name)
        return listFiles

    def choose_mode(self):
        self.frame[0] = tk.Frame(self, width=1000, height=1000)
        self.entry[0] = tk.Entry(self.frame[0])
        self.entry[0].pack(padx=0, pady=0)
        self.entry[0].insert(0, 'enter num of video')
        tk.Button(self.frame[0], text="confirm", width=5, command=lambda: self.click(99)).place(x=100, y=0)
        self.frame[0].place(x=700, y=400)

    def create_video_view(self):
        for x in range(self.video_num):
            self.frame_[x] = tk.Frame(self, width=300, height=120)
        for x in range(self.video_num):
            self._canvas[x] = tk.Canvas(self, bg="black", width=300, height=200)
            self._canvas[x].place(x=300*(x%3), y=250*(int(x/3)))
            self.player[x].set_window(self._canvas[x].winfo_id())
            # self.player[x].play(self.dir_name + '/' + self.video_list[x])
            # self.videopath[x] = self.dir_name + '/' + self.video_list[x]
            
            self.player[x].play(self.video_list[x])
            self.videopath[x] = self.video_list[x]
            
            
            # self.player[x].set_volume(0)
            # tk.Button(self.frame_[x], text="Play / Stop" + str(x+1), width=13, command=partial (self.click, (1 + x * 4))).place(x=0, y=0)
            tk.Button(self.frame_[x], text="Choose video" + str(x+1), width=13, command=partial (self.click, (2 + x * 4))).place(x=30, y=0)
            tk.Button(self.frame_[x], text="Choose Voice" + str(x+1), width=13, command=partial (self.click, (3 + x * 4))).place(x=170, y=0)
            
            # self.entry[x] = tk.Entry(self.frame_[x])
            # self.entry[x].pack(padx=120,pady=70)
            # self.entry[x].insert(0,'Enter Jump Time')
            
            self.frame_[x].place(x=0 + 300*(x%3), y=210 + 250*(int(x/3)))
        
        self._canvas[self.video_num] = tk.Canvas(self, bg="black", width=580, height=400)
        self._canvas[self.video_num].place(x=930, y=200)
        self.player[self.video_num].set_window(self._canvas[self.video_num].winfo_id())
        self.player[self.video_num].play(self.videopath[ choose_video])
        self.player[self.video_num].set_position(self.player[ choose_video].get_position())
        self.player[self.video_num].set_volume(0)
        
        # tk.Button(self, text="Play / Stop", width=10, command=lambda: self.click(100)).place(x=1100, y=60)
        # tk.Button(self, text="Play from Begin", width=10, command=lambda: self.click(101)).place(x=1300, y=60)
        tk.Button(self, text="End", width=10, command=lambda: self.click(102)).place(x=1200, y=700)
        # self.entry[x] = tk.Entry(self.frame_[x])
        # self.entry[x].pack(padx=120,pady=70)
        # self.entry[x].insert(0,'Now choose Video No.: ')
        
    def create_time(self):
        self.Time += self.time_sq
        for i in range(0, self.video_num):
            self.frame[i] = tk.Frame(self, width=100, height=50)
            if self.player[i].get_time() == -1:
                label = tk.Label(self.frame[i], text="0:0",font=('time: ',10, 'bold italic'),bg="#7CCD7C",
                    width=10,height=2,
                    padx=10, pady=5, borderwidth=10, relief="sunken")
            else:
                label = tk.Label(self.frame[i], text=str(int((self.player[i].get_time()/60000)))+":"+str((int(self.player[i].get_time()/1000)%60)) + '\n�???�?�?�??: '+str(int((self.player[i].get_length()/60000)))+":"+str((int(self.player[i].get_length()/1000)%60)),font=('?�?�?',10, 'bold italic'),bg="#7CCD7C",
                    width=10,height=2,
                    padx=10, pady=5, borderwidth=10, relief="sunken")
            label.pack()
            self.frame[i].place(x=150+300*(i%4), y=260+ 400*(int(i/4)))
        
        self.after(500, self.create_time)
    
    def create_choose_video(self):
        self.Time += self.time_sq
        #print(self.mark)
        #self.player[self.video_num].set_position(self.player[ choose_video].get_position())
        self.after(500, self.create_choose_video)
        
        
    def create_choose(self):
        q = ""
        fp=open('question.txt')
        lines = fp.readlines()
        for line in lines:
            for c in line:
                if c != '#':
                    q += c
                else:
                    self.question.append(q.lstrip())
                    q = ""
                    self.total_question_num += 1
                    
        choose = tk.Frame(self, width=10, height=10)
        site = [('Perfect', 1),
                ('Good', 2),
                ('Normal', 3),
                ('Bad', 4),
                ('Awful', 5)]
        self.v = tk.IntVar()
        for name, num in site:
            radio_button = tk.Radiobutton(choose,text = name, variable = self.v, value =num)
            radio_button.pack(anchor ='w', side = LEFT)
        choose.place(x=1100, y=600)
        
        que = tk.Frame(self, width=1000, height=100)
        label = tk.Label(que, text=self.question[self.now_question_num],font=('',10, 'bold italic'),bg="#7CCD7C",
            width=60 ,height=26,
            padx=10, pady=5, borderwidth=10, relief="sunken")
        label.pack()
        que.place(x = 1000, y = 50)
        
        check = tk.Frame(self, width=1000, height=100)
        tk.Button(check, text="Last question", width=13, command=lambda: self.click(103)).place(x=0, y=0)
        tk.Button(check, text="Confirm", width=13, command=lambda: self.click(104)).place(x=200, y=0)
        tk.Button(check, text="Next question", width=13, command=lambda: self.click(105)).place(x=100, y=0)
        check.place(x = 1100, y = 450)
        
        name = tk.Frame(self, width=100, height=100)
        self.entry[11] = tk.Entry(name)
        self.entry[11].insert(0,'Your name')
        self.entry[11].pack(padx=0,pady=0)
        name.place(x = 1000, y = 650)
        
        
        save = tk.Frame(self, width=200, height=200)
        tk.Button(save, text="confirm", width=13, command=lambda: self.click(102)).place(x=50, y=50)
        save.place(x = 1100, y =650)
    
    def click(self, action):
        n = int (action / 4)
 
        if action == 99:
            self.video_num = int(self.entry[0].get())
            self.frame[0].destroy()
            self.create_video_view()
            self.create_time()
            self.create_choose()
        
        if action == 100:
            self.mark = 1
            for x in range(self.video_num + 1):
                if self.player[x].get_state() == 1:
                    self.mark = 0
                    self.player[x].pause()
                    self.time_sq = 0
                
            if self.mark == 1:
                for x in range(self.video_num + 1):
                    self.player[x].resume()
                    self.time_sq = 0.5
            
        elif action == 101:
            self.Time = 0
            for x in range(self.video_num):
                self.player[x].play(self.videopath[x])
        
        # elif action == 102:
        #     fp=open(self.entry[11].get()+'.txt', 'w')
        #     for x in range(self.total_question_num):
        #         print(self.ans[x], file=fp)
        #     fp.close()
        #     exit()
            
        elif action == 102:
            fp=open('timeline.txt', 'a')
            print(str(int(self.Time)) + ": end", file=fp)
            fp.close()
            exit()
            
        elif action == 103:
            if self.now_question_num >= 1:
                self.now_question_num -= 1
                que = tk.Frame(self, width=1000, height=100)
                label = tk.Label(que, text=self.question[self.now_question_num],font=('?�?�?',10, 'bold italic'),bg="#7CCD7C",
                    width=60 ,height=26,
                    padx=10, pady=5, borderwidth=10, relief="sunken")
                label.pack()
                que.place(x = 1000, y = 50)
                
        elif action == 104:
            if self.now_question_num < self.total_question_num-1:
                self.now_question_num += 1
                que = tk.Frame(self, width=1000, height=100)
                label = tk.Label(que, text=self.question[self.now_question_num],font=('?�?�?',10, 'bold italic'),bg="#7CCD7C",
                    width=60 ,height=26,
                    padx=10, pady=5, borderwidth=10, relief="sunken")
                label.pack()
                que.place(x = 1000, y = 50)
            
        elif action == 105:
            self.ans[self.now_question_num] = self.v.get()
          
        elif action % 4 == 0:
            self.videopath[n] = filedialog.askopenfilename()
            self.player[n].play(self.videopath[n])
        
        #USEFUL      
        elif action % 4 == 1:
            if self.player[n].get_state() == 1:
                self.player[n].pause()
            else:
                self.player[n].resume() 
        
        elif action % 4 == 2:
            choose_video = n
            fp = open('timeline.txt', 'a')
            print(str(int(self.Time)) + ": " + self.video_list[n], file=fp)
            fp.close()
            
            self.player[self.video_num].play(self.videopath[ choose_video])
            self.player[self.video_num].set_position(self.player[ choose_video].get_position())
            self.player[self.video_num].set_volume(0)
            self.que.destroy
            self.que = tk.Frame(self, width=100, height=100)
            label = tk.Label(self.que, text="Now Play video No.: " + str( choose_video + 1), font=('?�?�?',10, 'bold italic'),bg="#7CCD7C",
                width=65 ,height=2,
                padx=10, pady=2, borderwidth=10, relief="sunken")
            label.pack()
            self.que.place(x = 950, y = 10)
            
            if self.mark == 0 and self.player[self.video_num].get_state() ==  1: 
                    self.player[self.video_num].pause()
            # self.player[n].set_volume(100)
            
        # elif action % 4 == 2:
        #     self.player[n].stop()
            
        #elif action % 4 == 3:
        #     self.player[n].set_position(int(self.entry[n].get())*1000/self.player[n].get_length())
        
        elif action % 4 == 3:
            self.choose_voice = n;
            for x in range(self.video_num):
                if x != self.choose_voice:
                    self.player[x].set_volume(0)
            self.player[self.choose_voice].set_volume(100)
            


    def pause_click(self, event):
        if self.player[0].get_state() == 1 and self.player[1].get_state() == 1:
            self.player[0].pause()
            self.player[1].pause()
        else:
            self.player[0].resume()
            self.player[1].resume()

if "__main__" == __name__:
    app = App()
    app.mainloop()