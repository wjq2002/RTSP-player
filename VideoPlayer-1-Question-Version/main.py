
import tkinter as tk
from tkinter import LEFT, Button, filedialog
from tkinter import ttk
from videoPlayer import Player
from functools import partial

Max_vedio_num = 15


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.player = [[0] for x in range(Max_vedio_num)]
        
        self.videopath = [[0] for x in range(Max_vedio_num)]
        self.entry     = [[0] for x in range(Max_vedio_num)]
        self._canvas   = [[0] for x in range(Max_vedio_num)]
        self.frame     = [[0] for x in range(Max_vedio_num)]
        self.frame_    = [[0] for x in range(Max_vedio_num)]
        
        self.total_question_num = 0
        self.now_question_num = 0
        self.question = list()
        self.ans = [[0] for x in range(10000)]
        
        for x in range(10):
            self.player[x] = Player()
        
        self.vedio_num = 0
        self.v = 0
        self.title("media_player")
        self.state("zoomed")
        self.choose_mode()
        self.bind_all("<space>", self.pause_click)

    def choose_mode(self):
        self.frame[0] = tk.Frame(self, width=1000, height=1000)
        self.entry[0] = tk.Entry(self.frame[0])
        self.entry[0].pack(padx=0, pady=0)
        self.entry[0].insert(0, '输入视频数量')
        
        tk.Button(self.frame[0], text="确认", width=5, command=lambda: self.click(99)).place(x=100, y=0)
        self.frame[0].place(x=700, y=400)

    def create_video_view(self):
        for x in range(self.vedio_num):
            self.frame_[x] = tk.Frame(self, width=100, height=120)
        for x in range(self.vedio_num):
            self._canvas[x] = tk.Canvas(self, bg="black", width=300, height=250)
            self._canvas[x].place(x=300*(x%3) + 10, y=400*(int(x/3)))
            self.player[x].set_window(self._canvas[x].winfo_id())
            tk.Button(self.frame_[x], text="选择视频" + str(x+1), width=13, command = partial (self.click, (0 + x * 4))).place(x=0, y=0)
            tk.Button(self.frame_[x], text="播放/暂停视频" + str(x+1), width=13, command=partial (self.click, (1 + x * 4))).place(x=0, y=30)
            tk.Button(self.frame_[x], text="停止视频" + str(x+1), width=13, command=partial (self.click, (2 + x * 4))).place(x=0, y=60)
            tk.Button(self.frame_[x], text="跳转", width=13, command=partial (self.click, (3 + x * 4))).place(x=0, y=90)
            
            self.entry[x] = tk.Entry(self.frame_[x])
            self.entry[x].pack(padx=120,pady=70)
            self.entry[x].insert(0,'输入跳转时间：(单位：s)')
            
            self.frame_[x].place(x=30 + 300*(x%3), y=260 + 400*(int(x/3)))
            
        tk.Button(self, text="一起播放/暂停", width=10, command=lambda: self.click(100)).place(x=1150, y=10)
        tk.Button(self, text="一起从头播放", width=10, command=lambda: self.click(101)).place(x=1250, y=10)
        
    def create_time(self):
        for i in range(0, self.vedio_num):
            self.frame[i] = tk.Frame(self, width=100, height=50)
            if self.player[i].get_time() == -1:
                label = tk.Label(self.frame[i], text="0:0",font=('宋体',10, 'bold italic'),bg="#7CCD7C",
                    width=10,height=2,
                    padx=10, pady=5, borderwidth=10, relief="sunken")
            else:
                label = tk.Label(self.frame[i], text=str(int((self.player[i].get_time()/60000)))+":"+str((int(self.player[i].get_time()/1000)%60)) + '\n总时长: '+str(int((self.player[i].get_length()/60000)))+":"+str((int(self.player[i].get_length()/1000)%60)),font=('宋体',10, 'bold italic'),bg="#7CCD7C",
                    width=10,height=2,
                    padx=10, pady=5, borderwidth=10, relief="sunken")
            label.pack()
            self.frame[i].place(x=150+300*(i%3), y=260+ 400*(int(i/3)))
        
        self.after(500, self.create_time)
    
    def create_choose(self):
        
        q = ""
        fp=open('question.txt')
        lines = fp.readlines()
        for line in lines:
            for c in line:
                if c != '#':
                    q+= c
                else:
                    self.question.append(q.lstrip())
                    q = ""
                    self.total_question_num += 1
                    
        choose = tk.Frame(self, width=10, height=10)
        site = [('很满意', 1),
                ('比较满意', 2),
                ('满意', 3),
                ('比较不满意', 4),
                ('很不满意', 5)]
        self.v = tk.IntVar()
        for name, num in site:
            radio_button = tk.Radiobutton(choose,text = name, variable = self.v, value =num)
            radio_button.pack(anchor ='w', side = LEFT)
        choose.place(x=1100, y=600)
        
        que = tk.Frame(self, width=1000, height=100)
        label = tk.Label(que, text=self.question[self.now_question_num],font=('宋体',10, 'bold italic'),bg="#7CCD7C",
            width=60 ,height=26,
            padx=10, pady=5, borderwidth=10, relief="sunken")
        label.pack()
        que.place(x = 1000, y = 50)
        
        check = tk.Frame(self, width=1000, height=100)
        tk.Button(check, text="上一题", width=13, command=lambda: self.click(103)).place(x=0, y=0)
        tk.Button(check, text="下一题", width=13, command=lambda: self.click(104)).place(x=200, y=0)
        tk.Button(check, text="确定", width=13, command=lambda: self.click(105)).place(x=100, y=0)
        check.place(x = 1100, y = 450)
        
        name = tk.Frame(self, width=100, height=100)
        self.entry[11] = tk.Entry(name)
        self.entry[11].insert(0,'输入您的名字')
        self.entry[11].pack(padx=0,pady=0)
        name.place(x = 1000, y = 650)
        
        
        save = tk.Frame(self, width=200, height=200)
        tk.Button(save, text="保存", width=13, command=lambda: self.click(102)).place(x=50, y=50)
        save.place(x = 1100, y =650)
    
    def click(self, action):
        n = int (action / 4)
 
        if action == 99:
            self.vedio_num = int(self.entry[0].get())
            self.frame[0].destroy()
            self.create_video_view()
            self.create_time()
            self.create_choose()
        
        elif action == 100:
            mark = 1
            for x in range(self.vedio_num):
                if self.player[x].get_state() == 1:
                    mark = 0
                    self.player[x].pause()
                
            if mark == 1:
                for x in range(self.vedio_num):
                    self.player[x].resume()
            
        elif action == 101:
            for x in range(self.vedio_num):
                self.player[x].play(self.videopath[x])
        
        elif action == 102:
            fp=open(self.entry[11].get()+'.txt', 'w')
            for x in range(self.total_question_num):
                print(self.ans[x], file=fp)
            fp.close()
            exit()
            
        elif action == 103:
            if self.now_question_num >= 1:
                self.now_question_num -= 1
                que = tk.Frame(self, width=1000, height=100)
                label = tk.Label(que, text=self.question[self.now_question_num],font=('宋体',10, 'bold italic'),bg="#7CCD7C",
                    width=60 ,height=26,
                    padx=10, pady=5, borderwidth=10, relief="sunken")
                label.pack()
                que.place(x = 1000, y = 50)
                
        elif action == 104:
            if self.now_question_num < self.total_question_num-1:
                self.now_question_num += 1
                que = tk.Frame(self, width=1000, height=100)
                label = tk.Label(que, text=self.question[self.now_question_num],font=('宋体',10, 'bold italic'),bg="#7CCD7C",
                    width=60 ,height=26,
                    padx=10, pady=5, borderwidth=10, relief="sunken")
                label.pack()
                que.place(x = 1000, y = 50)
            
        elif action == 105:
            self.ans[self.now_question_num] = self.v.get()
            
        elif action % 4 == 0:
            self.videopath[n] = filedialog.askopenfilename()
            self.player[n].play(self.videopath[n])
              
        elif action % 4 == 1:
            if self.player[n].get_state() == 1:
                self.player[n].pause()
            else:
                self.player[n].resume()
        
        elif action % 4 == 2:
            self.player[n].stop()
            
        elif action % 4 == 3:
            self.player[n].set_position(int(self.entry[n].get())*1000/self.player[n].get_length())


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