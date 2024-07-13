import os
import tkinter as tk
from tkinter import LEFT, Button, filedialog
from tkinter import ttk
from videoPlayer import Player
from functools import partial

Max_vedio_num = 10


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.player = [[0] for x in range(Max_vedio_num + 1)]
        
        self.videopath = [[0] for x in range(Max_vedio_num)]
        self.entry     = [[0] for x in range(Max_vedio_num)]
        self._canvas   = [[0] for x in range(Max_vedio_num)]
        self.frame     = [[0] for x in range(Max_vedio_num)]
        self.frame_    = [[0] for x in range(Max_vedio_num)]
        
        self.Time = 0
        self.v = 0
        self.choose_vedio = 0
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
        
        self.dir_name = filedialog.askdirectory()
        self.video_list = self.getAllFiles()
        self.vedio_num = len(self.video_list)
        for x in range(len(self.video_list)+1):
            self.player[x] = Player()
            
        self.que = tk.Frame(self, width=100, height=100)
        label = tk.Label(self.que, text="瑜版挸澧犻柅澶嬶拷?锟介敍姘筹拷鍡涳拷锟�?" + str(self.choose_vedio + 1), font=('鐎癸拷?锟界秼',10, 'bold italic'),bg="#7CCD7C",
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
            
        self.player[self.choose_vedio].set_volume(100)
        for x in range(self.vedio_num):
            if x != self.choose_vedio:
                # print(x, self.player[x].get_volume())
                self.player[x].set_volume(0)
        #print(self.vedio_num)
        self.create_video_view()
        # self.create_time()
        # self.create_choose()
        self.create_choose_vedio()
        # self.bind_all("<space>", self.pause_click)
        
    def getAllFiles(self):
        listFiles = os.listdir(self.dir_name)
        return listFiles

    def choose_mode(self):
        self.frame[0] = tk.Frame(self, width=1000, height=1000)
        self.entry[0] = tk.Entry(self.frame[0])
        self.entry[0].pack(padx=0, pady=0)
        self.entry[0].insert(0, '鏉堟挸鍙嗙憴鍡涳拷鎴炴殶闁诧拷')
        tk.Button(self.frame[0], text="锟�?锟界拋锟�?", width=5, command=lambda: self.click(99)).place(x=100, y=0)
        self.frame[0].place(x=700, y=400)

    def create_video_view(self):
        for x in range(self.vedio_num):
            self.frame_[x] = tk.Frame(self, width=300, height=120)
        for x in range(self.vedio_num):
            self._canvas[x] = tk.Canvas(self, bg="black", width=300, height=200)
            self._canvas[x].place(x=300*(x%3), y=250*(int(x/3)))
            self.player[x].set_window(self._canvas[x].winfo_id())
            self.player[x].play(self.dir_name + '/' + self.video_list[x])
            self.videopath[x] = self.dir_name + '/' + self.video_list[x]
            
            # self.player[x].set_volume(0)
            tk.Button(self.frame_[x], text="閹撅拷閺€锟�?/閺嗗倸浠犵憴鍡涳拷锟�?" + str(x+1), width=11, command=partial (self.click, (1 + x * 4))).place(x=0, y=0)
            tk.Button(self.frame_[x], text="锟�?澶嬶拷?锟界憴鍡涳拷锟�?" + str(x+1), width=11, command=partial (self.click, (2 + x * 4))).place(x=90, y=0)
            tk.Button(self.frame_[x], text="锟�?澶嬶拷?锟介棅鎶斤拷锟�?" + str(x+1), width=11, command=partial (self.click, (3 + x * 4))).place(x=180, y=0)
            
            # self.entry[x] = tk.Entry(self.frame_[x])
            # self.entry[x].pack(padx=120,pady=70)
            # self.entry[x].insert(0,'鏉堟挸鍙嗙捄瀹犳祮閺冨爼妫块敍锟�?(閸楁洑缍呴敍锟�?)')
            
            self.frame_[x].place(x=20 + 300*(x%3), y=210 + 250*(int(x/3)))
        
        self._canvas[self.vedio_num] = tk.Canvas(self, bg="black", width=580, height=400)
        self._canvas[self.vedio_num].place(x=930, y=200)
        self.player[self.vedio_num].set_window(self._canvas[self.vedio_num].winfo_id())
        self.player[self.vedio_num].play(self.videopath[self.choose_vedio])
        self.player[self.vedio_num].set_position(self.player[self.choose_vedio].get_position())
        self.player[self.vedio_num].set_volume(0)
        
        tk.Button(self, text="娑撯偓鐠ч攱鎸遍弨锟�?/閺嗗倸锟�?", width=10, command=lambda: self.click(100)).place(x=1100, y=60)
        tk.Button(self, text="娑撯偓鐠ц渹绮犳径瀛樻尡閺€锟�?", width=10, command=lambda: self.click(101)).place(x=1300, y=60)
        tk.Button(self, text="缂佹挻锟�?", width=10, command=lambda: self.click(102)).place(x=1200, y=700)
        self.entry[x] = tk.Entry(self.frame_[x])
        self.entry[x].pack(padx=120,pady=70)
        self.entry[x].insert(0,'鏉堟挸鍙嗙捄瀹犳祮閺冨爼妫块敍锟�?(閸楁洑缍呴敍锟�?)')
        
    def create_time(self):
        self.Time += self.time_sq
        for i in range(0, self.vedio_num):
            self.frame[i] = tk.Frame(self, width=100, height=50)
            if self.player[i].get_time() == -1:
                label = tk.Label(self.frame[i], text="0:0",font=('鐎癸拷?锟界秼',10, 'bold italic'),bg="#7CCD7C",
                    width=10,height=2,
                    padx=10, pady=5, borderwidth=10, relief="sunken")
            else:
                label = tk.Label(self.frame[i], text=str(int((self.player[i].get_time()/60000)))+":"+str((int(self.player[i].get_time()/1000)%60)) + '\n锟�?缁橈拷?锟介梹锟�?: '+str(int((self.player[i].get_length()/60000)))+":"+str((int(self.player[i].get_length()/1000)%60)),font=('鐎癸拷?锟界秼',10, 'bold italic'),bg="#7CCD7C",
                    width=10,height=2,
                    padx=10, pady=5, borderwidth=10, relief="sunken")
            label.pack()
            self.frame[i].place(x=150+300*(i%4), y=260+ 400*(int(i/4)))
        
        self.after(500, self.create_time)
    
    def create_choose_vedio(self):
        self.Time += self.time_sq
        #print(self.mark)
        #self.player[self.vedio_num].set_position(self.player[self.choose_vedio].get_position())
        self.after(500, self.create_choose_vedio)
        
        
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
        site = [('瀵板牊寮ч幇锟�?', 1),
                ('濮ｆ棁绶濓拷?锟解剝锟�?', 2),
                ('濠娾剝锟�?', 3),
                ('濮ｆ棁绶濇稉宥嗗姬閹帮拷', 4),
                ('瀵板牅绗夛拷?锟解剝锟�?', 5)]
        self.v = tk.IntVar()
        for name, num in site:
            radio_button = tk.Radiobutton(choose,text = name, variable = self.v, value =num)
            radio_button.pack(anchor ='w', side = LEFT)
        choose.place(x=1100, y=600)
        
        que = tk.Frame(self, width=1000, height=100)
        label = tk.Label(que, text=self.question[self.now_question_num],font=('鐎癸拷?锟界秼',10, 'bold italic'),bg="#7CCD7C",
            width=60 ,height=26,
            padx=10, pady=5, borderwidth=10, relief="sunken")
        label.pack()
        que.place(x = 1000, y = 50)
        
        check = tk.Frame(self, width=1000, height=100)
        tk.Button(check, text="娑撳﹣绔存０锟�?", width=13, command=lambda: self.click(103)).place(x=0, y=0)
        tk.Button(check, text="娑擄拷?锟斤拷?锟芥０锟�?", width=13, command=lambda: self.click(104)).place(x=200, y=0)
        tk.Button(check, text="锟�?锟界€癸拷", width=13, command=lambda: self.click(105)).place(x=100, y=0)
        check.place(x = 1100, y = 450)
        
        name = tk.Frame(self, width=100, height=100)
        self.entry[11] = tk.Entry(name)
        self.entry[11].insert(0,'鏉堟挸鍙嗛幃銊ф畱閸氬秴锟�?')
        self.entry[11].pack(padx=0,pady=0)
        name.place(x = 1000, y = 650)
        
        
        save = tk.Frame(self, width=200, height=200)
        tk.Button(save, text="娣囨繂锟�?", width=13, command=lambda: self.click(102)).place(x=50, y=50)
        save.place(x = 1100, y =650)
    
    def click(self, action):
        n = int (action / 4)
 
        if action == 99:
            self.vedio_num = int(self.entry[0].get())
            self.frame[0].destroy()
            self.create_video_view()
            self.create_time()
            self.create_choose()
        
        if action == 100:
            self.mark = 1
            for x in range(self.vedio_num + 1):
                if self.player[x].get_state() == 1:
                    self.mark = 0
                    self.player[x].pause()
                    self.time_sq = 0
                
            if self.mark == 1:
                for x in range(self.vedio_num + 1):
                    self.player[x].resume()
                    self.time_sq = 0.5
            
        elif action == 101:
            self.Time = 0
            for x in range(self.vedio_num):
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
                label = tk.Label(que, text=self.question[self.now_question_num],font=('鐎癸拷?锟界秼',10, 'bold italic'),bg="#7CCD7C",
                    width=60 ,height=26,
                    padx=10, pady=5, borderwidth=10, relief="sunken")
                label.pack()
                que.place(x = 1000, y = 50)
                
        elif action == 104:
            if self.now_question_num < self.total_question_num-1:
                self.now_question_num += 1
                que = tk.Frame(self, width=1000, height=100)
                label = tk.Label(que, text=self.question[self.now_question_num],font=('鐎癸拷?锟界秼',10, 'bold italic'),bg="#7CCD7C",
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
            self.choose_vedio = n
            fp=open('timeline.txt', 'a')
            print(str(int(self.Time)) + ": " + self.video_list[n], file=fp)
            fp.close()
            
            self.player[self.vedio_num].play(self.videopath[self.choose_vedio])
            self.player[self.vedio_num].set_position(self.player[self.choose_vedio].get_position())
            self.player[self.vedio_num].set_volume(0)
            self.que.destroy
            self.que = tk.Frame(self, width=100, height=100)
            label = tk.Label(self.que, text="瑜版挸澧犻柅澶嬶拷?锟介敍姘筹拷鍡涳拷锟�?" + str(self.choose_vedio + 1), font=('鐎癸拷?锟界秼',10, 'bold italic'),bg="#7CCD7C",
                width=65 ,height=2,
                padx=10, pady=2, borderwidth=10, relief="sunken")
            label.pack()
            self.que.place(x = 950, y = 10)
            
            if self.mark == 0 and self.player[self.vedio_num].get_state() ==  1: 
                    self.player[self.vedio_num].pause()
            # self.player[n].set_volume(100)
            
        # elif action % 4 == 2:
        #     self.player[n].stop()
            
        #elif action % 4 == 3:
        #     self.player[n].set_position(int(self.entry[n].get())*1000/self.player[n].get_length())
        
        elif action % 4 == 3:
            self.choose_voice = n;
            for x in range(self.vedio_num):
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