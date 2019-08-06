import tkinter as tk 
import tkinter.filedialog as filedialog
from tkinter import *
import glob
from PIL import Image, ImageTk
import numpy as np
import sys
from tkinter import ttk

class KeyEvent(object):
    def __init__(self, master):
        master.bind("<Key>", self.func)
        
        self.len_pair = len(A_rand_idx)
        self.idx_for_pair = 0
        self.idxA = A_rand_idx[self.idx_for_pair]
        self.idxB = B_rand_idx[self.idx_for_pair]
        self.idxA_pre = None
        self.idxB_pre = None
        self.pre_decision = []
        self.draw_img_pair()
        var_current.set('Current choices')
        
    def func(self, event):
        keysym,keycode,char = event.keysym, event.keycode, event.char
        # print("鍵位：{}，ASCII碼：{}，字元：{}".format(keysym,keycode,char))
        
        if keysym not in ['q','s','b','Left','Down','Right','Up']:
            var_current.set('Invalid key.')
        
        elif keysym == 'q':
            self.close_window()

        elif keysym == 's':
            self.save_decision()
        
        elif keysym in ['Left','Down','Right','Up'] and self.idx_for_pair <= self.len_pair-1:
            
            # ground truth label choices: [-1,0,1,2]
            gt_label = ['Up','Left','Down','Right'].index(keysym)-1

            
            self.pre_decision.append(gt_label)

            if len(self.pre_decision) >0:
                var_center.set(['X','>','≈','<'][self.pre_decision[-1]+1])
            else:
                var_center.set('')
                
            var_current.set('Current choices')

            self.go_next()
            self.draw_img_pair()

        elif keysym == 'b':
            if len(self.pre_decision) >0:
                self.pre_decision.pop()
                if len(self.pre_decision) >0:
                    var_center.set(['X','>','≈','<'][self.pre_decision[-1]+1])
                else:
                    var_center.set('')
            self.go_back()
            self.draw_img_pair()


        bar['value'] = self.idx_for_pair
        var_bar.set(str(bar['value'])+'/'+str(self.len_pair))
        if self.idx_for_pair != len(self.pre_decision):
            print('Something Wrong!')
            sys.exit()

    def close_window(self):
        print('End.')
        window.destroy()
        sys.exit()


    def save_decision(self):
        save_file_name = filedialog.asksaveasfilename(initialdir = "./")
        
        if save_file_name != '':
            np.savez(save_file_name,decision=self.pre_decision, left_rand_idx=A_rand_idx, right_rand_idx=B_rand_idx, left_idx=A_idx, right_idx=B_idx, rand_idx=rand_idx, img_list=img_list)
            print('Label saved.')
        # window.destroy()
        # sys.exit()


    def go_back(self):
        if self.idx_for_pair > 0:
            var_current.set('Back to previous one.')
            self.idx_for_pair -= 1
            self.idxA = A_rand_idx[self.idx_for_pair]
            self.idxB = B_rand_idx[self.idx_for_pair]

            if self.idx_for_pair > 0:
                self.idxA_pre = A_rand_idx[self.idx_for_pair-1]
                self.idxB_pre = B_rand_idx[self.idx_for_pair-1]
            elif self.idx_for_pair == 0: 
                self.idxA_pre = None
                self.idxB_pre = None
        else:
            var_current.set('Cannot go back.')
    
    def go_next(self):

        self.idxA_pre = A_rand_idx[self.idx_for_pair]
        self.idxB_pre = B_rand_idx[self.idx_for_pair]

        self.idx_for_pair += 1

        if self.idx_for_pair <= self.len_pair -1 : 
            self.idxA = A_rand_idx[self.idx_for_pair]
            self.idxB = B_rand_idx[self.idx_for_pair]


    def draw_img_pair(self):

        size = 256, 256

        pilImage1 = Image.open(img_list[self.idxA])
        pilImage2 = Image.open(img_list[self.idxB])

        pilImage1.thumbnail(size, Image.ANTIALIAS)
        pilImage2.thumbnail(size, Image.ANTIALIAS)
        image1 = ImageTk.PhotoImage(pilImage1)
        image2 = ImageTk.PhotoImage(pilImage2)

        panelA.configure(image=image1)
        panelB.configure(image=image2)
        panelA.image = image1
        panelB.image = image2

        
        if not self.idxA_pre and not self.idxB_pre:
            panelA_pre.image = None
            panelB_pre.image = None
        else:
            pilImage1_pre = Image.open(img_list[self.idxA_pre])
            pilImage2_pre = Image.open(img_list[self.idxB_pre])
            pilImage1_pre.thumbnail(size, Image.ANTIALIAS)
            pilImage2_pre.thumbnail(size, Image.ANTIALIAS)
            image1_pre = ImageTk.PhotoImage(pilImage1_pre)
            image2_pre = ImageTk.PhotoImage(pilImage2_pre)

            panelA_pre.configure(image=image1_pre)
            panelB_pre.configure(image=image2_pre)
            panelA_pre.image = image1_pre
            panelB_pre.image = image2_pre

        
        if self.idx_for_pair == self.len_pair:
            var_command.set('Empty list. Please close the window (q), save(s), or go backward.(b)')
        else:
            var_command.set('Label command: Left is better(←). I cannot tell(↓). Right is better(→). Bad Pair(↑).')
            var_sys.set('System command: Quit(q), Back(b), Save(s).')

if __name__ == '__main__':
    
    window = tk.Tk()
    window.title('Easy-Label-Regression')
    window.geometry('1000x800')

    folder_selected = None
    folder_selected = filedialog.askdirectory(initialdir = "./")
    if not folder_selected:
        sys.exit()

    save_name = folder_selected.split('/')[-1]
    img_list = glob.glob(folder_selected+'/**/*.jpg', recursive=True)
    
    A_idx = []
    B_idx = []
    for i in range(len(img_list)):
        for j in range(i,len(img_list)):
            if j>i:
                A_idx.append(i)
                B_idx.append(j)

    A_idx = np.array(A_idx)
    B_idx = np.array(B_idx)
    rand_idx = np.random.permutation(len(A_idx))
    A_rand_idx = A_idx[rand_idx]
    B_rand_idx = B_idx[rand_idx]

    
    var_folder = tk.StringVar()
    label_folder = tk.Label(window, textvariable=var_folder, bg='white', fg='black', font=('Arial', 24), width=1000, height=1)
    label_folder.pack()


    bar = ttk.Progressbar(window, length=700, mode="determinate", orient=HORIZONTAL)
    bar["maximum"] = len(A_rand_idx)
    bar["value"] = 0
    bar.pack()

    var_bar = tk.StringVar()
    label_bar = tk.Label(window, textvariable=var_bar, bg='white', fg='black', font=('Arial', 24), width=1000, height=1)
    label_bar.pack()
    var_bar.set('0/'+str(bar["maximum"]))


    var_command = tk.StringVar()
    label_command = tk.Label(window, textvariable=var_command, bg='white', fg='black', font=('Arial', 24), width=1000, height=1)
    label_command.pack()

    var_sys = tk.StringVar()
    label_sys = tk.Label(window, textvariable=var_sys, bg='white', fg='black', font=('Arial', 24), width=1000, height=1)
    label_sys.pack()


    var_current = tk.StringVar()
    label_current = tk.Label(window, textvariable=var_current, bg='black', fg='white', font=('Arial', 24), width=1000, height=1)
    label_current.pack()

    fm1 = tk.Frame(window,bg='blue')

    panelA = tk.Label(fm1,image=None)
    panelA.pack(side=LEFT,expand=YES)

    panelB = tk.Label(fm1,image=None)
    panelB.pack(side=LEFT,expand=YES)

    fm1.pack(side=TOP, fill=BOTH, expand=YES)

    label_pre = tk.Label(window, text='Previous decision', bg='black', fg='white', font=('Arial', 24), width=1000, height=1)
    label_pre.pack()
    fm2 = tk.Frame(window,bg='red')
    panelA_pre = tk.Label(fm2,image=None)
    panelA_pre.pack(side=LEFT,expand=YES)

    var_center = tk.StringVar()
    label_center = tk.Label(fm2, textvariable=var_center, bg='red', fg='white', font=('Arial', 80))
    label_center.pack(side=LEFT)

    panelB_pre = tk.Label(fm2,image=None)
    panelB_pre.pack(side=LEFT,expand=YES)
    fm2.pack(side=TOP, fill=BOTH, expand=YES)

    
    var_folder.set('Selected folder:'+folder_selected)


    
    KeyEvent(window)
    window.mainloop()

