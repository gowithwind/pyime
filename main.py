#coding:utf-8
from Tkinter import *
root = Tk(className ="pyime")

outs = StringVar() # defines the widget state as string
output = Entry(root,textvariable=outs) # adds a textarea widget
output.pack()

svalue = StringVar() # defines the widget state as string
input = Entry(root,textvariable=svalue,justify=LEFT) # adds a textarea widget
input.pack()
input.focus_force()

text= Label(root,text="", name="text")
text.pack()

def init_dictionary():
    dicts={}
    with open("luna_pinyin.dict.yaml","r") as f:
        for line in f.read().split('\n'):
            if line.startswith("#"):continue
            else:
                items=line.split("	")
                if len(items)<1:continue
                key,value=items[1].replace(" ",""),items[0]
                if key=='de':pass
                if not dicts.get(key):dicts[key]=[value]
                else: 
                    if len(items)>2:dicts[key].insert(0,value)
                    dicts[key].append(value)
    return dicts

def init_gb2312():
    dicts={}
    with open("gb2312_pinyin.dict.yaml","r") as f:
        for line in f.read().split('\n'):
            if line.startswith("#"):continue
            else:
                items=line.split(" ")
                if len(items)<1:continue
                key,value=items[1],items[0]
                if not dicts.get(key):dicts[key]=[value]
                else: dicts[key].append(value)
    return dicts

dictionary={"jiang":"蒋 讲 将 江 奖","lin":"林 琳 临 霖 淋","wszgr":"我是中国人"}
dictionary=init_dictionary()
dictionary=init_gb2312()

print len(dictionary)
print dictionary.get("lin")
class Model:
    choices=[]
    page=0
    def pager(self):
        return self.choices[self.page*10:self.page*10+10]
    def prev(self):
        if self.page>1:self.page=self.page-1
    def next(self):
        if len(self.choices)/10>self.page:self.page=self.page+1
    def query(self,input):
        self.choices=dictionary.get(input)
        self.page=0

model=Model()

def copy(event=None):
    print "copy"
    root.clipboard_clear()
    root.clipboard_append(outs.get())

def show():
    if model.choices:
        new=['%s %s'%((i+1)%10,x) for i,x in enumerate(model.pager())]
        text.config(text=' '.join(new))
    else:
        text.config(text="")

def on_key(event):
    ins= svalue.get()
    key= event.keysym
    print key
    if key=="space": key="1"
    if key=='minus':
        model.prev()
        show()
        return
    if key=='equal':
        model.next()
        show()
        return
    if key in "1234567890":
        if key=='0':num=10-1
        else:num=int(key)-1
        result=model.pager()[num]
        outs.set(outs.get()+result.decode("utf-8"))
        svalue.set("")
        text.config(text="")
    else:
        model.query(ins)
        show()
        

root.bind('<Control-c>', copy)
input.bind("<KeyRelease>", on_key)
input.bind("<Return>",copy)

root.wm_attributes("-topmost", 1)
root.mainloop()
