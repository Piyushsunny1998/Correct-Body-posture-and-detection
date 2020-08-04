from tkinter import *
import numpy as np
import pandas as pd

def doc():
    userid=Entry1.get()
    password=Entry2.get()
    x=np.array([userid,password])
    np.save('loginend.npy',x)
    import loginend
    b=np.load('logins.npy')
    if(b[0]==1):
        import doctor1
    else:
        print("INVALID CREDENTIAL")

top=Tk()  #this will create a window
top.geometry("600x450+402+142")
top.title("New Toplevel")
top.configure(background="#d9d9d9")

Label1 = Label(top)
Label1.place(relx=0.183, rely=0.133, height=41, width=324)
Label1.configure(background="#d9d9d9")
Label1.configure(disabledforeground="#a3a3a3")
Label1.configure(foreground="#000000")
Label1.configure(text='''ENTER THE CREDENTIALS''')


Label2 = Label(top)
Label2.place(relx=0.167, rely=0.356, height=41, width=104)
Label2.configure(background="#d9d9d9")
Label2.configure(disabledforeground="#a3a3a3")
Label2.configure(foreground="#000000")
Label2.configure(text='''DOCTOR_ID''')

Entry1 = Entry(top)
Entry1.place(relx=0.383, rely=0.367,height=30, relwidth=0.273)
Entry1.configure(background="white")
Entry1.configure(disabledforeground="#a3a3a3")
Entry1.configure(font="TkFixedFont")
Entry1.configure(foreground="#000000")
Entry1.configure(insertbackground="black")

Label3 = Label(top)
Label3.place(relx=0.183, rely=0.578, height=31, width=84)
Label3.configure(background="#d9d9d9")
Label3.configure(disabledforeground="#a3a3a3")
Label3.configure(foreground="#000000")
Label3.configure(text='''PASSWORD''')

Entry2 = Entry(top)
Entry2.place(relx=0.383, rely=0.578,height=30, relwidth=0.273)
Entry2.configure(background="white")
Entry2.configure(disabledforeground="#a3a3a3")
Entry2.configure(font="TkFixedFont")
Entry2.configure(foreground="#000000")
Entry2.configure(insertbackground="black")

Button1 = Button(top)
Button1.place(relx=0.5, rely=0.756, height=44, width=77)
Button1.configure(activebackground="#ececec")
Button1.configure(activeforeground="#000000")
Button1.configure(background="#d9d9d9")
Button1.configure(disabledforeground="#a3a3a3")
Button1.configure(foreground="#000000")
Button1.configure(command=doc)
Button1.configure(highlightbackground="#d9d9d9")
Button1.configure(highlightcolor="black")
Button1.configure(pady="0")
Button1.configure(text='''Button''')
Button1.configure(text='''LOGIN IN''')

top.mainloop()
