import tkinter.filedialog
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox

class BaseWindow():
    def __init__(self):
        self.top = Tk()
        self.uiCount = 0
        self.uiWidth = 20
        self.uiHeight = 30
        self.InitUI()

    def InitUI(self):
        pass

    def SetTitle(self,txt):
        self.top.title(txt)
    #设置屏幕宽高 并居中
    def SetScreenSize(self,width,height):
        sw = self.top.winfo_screenwidth()
        sh = self.top.winfo_screenheight()
        
        x = (sw-width) / 2
        y = (sh-height) / 2

        self.top.geometry("%dx%d+%d+%d"%(width,height,x,y))

    def ShowWindow(self):    
        self.top.mainloop()

    def AddLabel(self,txt,autoSet=True):
        label = Label(self.top,text=txt)
        label.pack()
        if autoSet:
            label.place(x=0,y=self.uiHeight*self.uiCount)
        self.uiCount += 1
        return label

    def AddBtn(self,txt,cmd,width=20,height=1):
        btn = Button(self.top,text=txt,command=cmd,width=width,height=height)
        btn.pack()
        return btn

    def AddCheckBtn(self,txt,checkVar,cmd):
        checkBtn = Checkbutton(self.top,text=txt,variable=checkVar,onvalue=1,offvalue=0,command=cmd)
        checkBtn.pack()
        checkBtn.place(x=0,y=self.uiHeight*self.uiCount)
        self.uiCount += 1
        return checkBtn

    def AddInput(self,txt='输入路径',height=1,width=30,bg='white',fg='black',autoSet=True):
        text = Text(self.top,height=height,width=width,bg=bg,fg=fg)
        text.insert(INSERT,txt)
        text.pack()
        if autoSet:
            text.place(x=20,y=self.uiHeight*self.uiCount)
        self.uiCount += 1    
        return text

    def OpenFile(self):
        return tkinter.filedialog.askopenfilename()

    def OpenDir(self):
        return tkinter.filedialog.askdirectory()

    def AddList(self,autoSet=True,addScrollbar=True):
        list = Listbox(self.top,width=100)
        if addScrollbar:
            s1 = self.AddScrollbar(list)
            s2 = self.AddScrollbar(list,False)
            list.config(yscrollcommand=s1,xscrollcommand=s2)
        list.pack()
        if autoSet:
            list.place(x=0,y=self.uiHeight*self.uiCount)
        self.uiCount += 1
        
        return list

    def AddTree(self,autoSet=True,addScrollbar=True):
        columns = ['索引','内容']
        list = ttk.Treeview(self.top,show="headings",columns=columns)
        if addScrollbar:
            s1 = self.AddScrollbar(list)
            s2 = self.AddScrollbar(list,False)
            list.config(yscrollcommand=s1.set,xscrollcommand=s2.set)
        for column in columns:
            list.heading(column=column,text=column, anchor=CENTER,command=lambda name=column:messagebox.showinfo('', '{}描述信息~~~'.format(name)))  # 定义表头
        list.column(0,width=50)
        list.column(1)
        list.pack(expand=1)   
        if autoSet:
            list.place(x=0,y=self.uiHeight*self.uiCount)
        self.uiCount += 1

        return list

    def AddScrollbar(self,list,isY=True):           
        if isY:
            scroll = Scrollbar(self.top) 
            scroll.config(command=list.yview)
            scroll.pack(side=RIGHT,fill=Y)
        else:
            scroll = Scrollbar(self.top,orient=HORIZONTAL) 
            scroll.config(command=list.xview)
            scroll.pack(side=BOTTOM,fill=X,anchor=S)
        return scroll

    def delButton(self,tree):
        x=tree.get_children()
        for item in x:
            tree.delete(item)
 
    def SetTreeContent(self,list,arr):
        self.delButton(list)
        for i in range(len(arr)):
            list.insert('',END,values=(i,arr[i]))

    def SetListContent(self,list,arr):
        list.delete(0,'end')
        for i in range(len(arr)):
            list.insert(END, str(i)+arr[i])  #插入数据
        
