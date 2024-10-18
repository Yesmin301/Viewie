from tkinter import *
#windo of the actual GUI
root = Tk()
root.title("Viewie")
root.geometry("1030x920")

#Label aka title.
label = Label(root, text="Welcome to Viewie!", font=('Arial', 20))
label.pack(padx=20, pady=25)


frame = Frame(root)
frame.pack()

#here i made the text boxes 1 for uploading the code and the other for displaying the diagram.

#Textbox1 is for python source code upload.
textbox1 = Text(frame, height=15, width=30, font=('MonoLisa', 18))  
textbox1.grid(row=0, column=0, padx=40)
textbox1.insert(END, "Placeholder text for Textbox 1")

#Textbox2 is for "output" of source code -viewie .
textbox2 = Text(frame, height=15, width=30, font=('MonoLisa', 18))  
textbox2.grid(row=0, column=1, padx=10)
textbox2.insert(END, "Placeholder text for Textbox 2")

#Making button to upload
def upload_click():
    print("Uploaded")
#Actually making the button to upload this PYTHON source code
upload_button = Button(frame, text="Upload", command=upload_click)
upload_button.grid(row=1, column=0, pady=20)

#button for the diagram to be save (maybe we should add a drop down button to be saved as a pdf. or png.)
def save_click():
    print("Saved")
#Another button i guesss
save_button = Button(frame, text="Save", command=save_click)
save_button.grid(row=1, column=1, pady=20)

#Here is the new page buttom -not sure what this need to do yet
def new_page_button():
   print("New page")

#actually making the stupid button
new_page_button = Button(root, text="New Page", command=new_page_button)
#moving the button~~
new_page_button.pack(side=TOP, padx=(10))

root.mainloop()
