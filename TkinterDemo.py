import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
import webbrowser
def func1():
    webbrowser.open("https://youtu.be/N7KyMjqp-QQ?feature=shared")
def w2():
    age1=age.get()
    window2=tk.Toplevel()
    window2.title("Next Page")
    window2.geometry("1000x1000")
    window2.configure(bg="grey")
    name1=name.get()
    tk.Label(window2,text=f"Form saved successfully , {name1}").pack()
    tk.Label(window2,text=f"You are {age1} years old").pack()
    button2=tk.Button(window2,text="----->",command=func1,bg="Green",fg="white",relief=RAISED,bd=12,height=1,width=2)
    button2.pack()
window1=tk.Tk()
window1.geometry("1080x2400")
Lab1=tk.Label(window1,text="FORM",fg="white",bg="black",font=('Arial',15,'underline')).pack()
tk.Label(window1,text="Enter your name",fg="blue").pack()
name=tk.StringVar()
entry=tk.Entry(window1,textvariable=name)
entry.pack()
tk.Label(window1,text="Enter your age",fg="blue").pack()
age=tk.StringVar()
entry1=tk.Entry(window1,textvariable=age)
entry1.pack()
tk.Label(window1,text="Enter your DOB",fg="blue").pack()
dob=tk.StringVar()
entry2=tk.Entry(window1,textvariable=dob)
entry2.pack()
tk.Label(window1,text="State you gender",fg="blue").pack()
gend=tk.StringVar()
tk.Radiobutton(window1,text="Male",variable=gend,value="Male").pack()
tk.Radiobutton(window1,text="Female",variable=gend,value="Female").pack()
c1=tk.Checkbutton(text="@__@",bg="white",fg="#394893")
c1.pack()

tk.Button(window1,text="Save",command=w2,bg="black",fg="white",relief=RAISED,bd=10).pack()
tk.Button(window1,text="QUIT",command=window1.destroy,bg="red",fg="white",relief=SUNKEN,bd=15).pack()
window1.mainloop()