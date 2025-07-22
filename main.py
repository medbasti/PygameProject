import tkinter as tk
def add_char():
    name=userentry.get()
    result= name+"@gmail.com"
window = tk.Tk()
window.geometry("800x800")
greeting = tk.Label(window, text="Enter Your Name",font=("Arial",20))
greeting.grid(row=0,column=0)
userentry = tk.Entry(font=("Arial",20), width=20 )
userentry.grid(row=0, column=1)
button=tk.Button(text="Start",command=add_char, bg="red", fg="white", font=("Arial",20) , height=2)
button.grid(row=4, column=1)
window.mainloop()
