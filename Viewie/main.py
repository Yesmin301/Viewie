from tkinter import *

root = Tk()  # Notice the capitalization here: Tk() instead of tk.TK()

root.title("Viewie")
root.geometry("800x500")

label = Label(root,text="Welcome to Viewie!", font =('Arial', 40 ))
label.pack(padx=20, pady=25)

textbox = Text(root, height=4, font=('MonoLisa',18))
textbox.pack()

myentry = Entry(root)
myentry.pack()










root.mainloop()
