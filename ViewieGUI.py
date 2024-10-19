from tkinter import *
from ViewieBack import ViewieCodeVisualizer

# window of the actual GUI
root = Tk()
root.title("Viewie")

root.geometry("1030x920")
root.configure(bg="white")

# Label aka title.
label = Label(root, text="Welcome to Viewie!", font=('Arial', 20, "bold",))
label.pack(padx=20, pady=25)
label.configure(bg="maroon")
label.configure(foreground="White")

frame = Frame(root)
frame.pack()
frame.configure(bg="Black")
# here i made the text boxes 1 for uploading the code and the other for displaying the diagram.

# Textbox1 is for python source code upload.
textbox1 = Text(frame, height=15, width=30, font=('MonoLisa', 18, "bold"))
textbox1.grid(row=0, column=0, padx=40, pady=10)
textbox1.insert(END, "Please upload your source code :)")
textbox1.configure(bg="Black")

# Textbox2 is for "output" of source code -viewie .
textbox2 = Text(frame, height=15, width=30, font=('MonoLisa', 18, "bold"))
textbox2.grid(row=0, column=1, padx=40, pady=10)
textbox2.insert(END, "Your source code diagram will be displayed here. You can then save it :)")
textbox2.configure(bg="black")


# Making button to upload
def upload_click():
    print("Uploaded")

    # REDHOUSE CHANGES -- NEED TO GET THE CODE FROM TEXTBOX1 --
    code = textbox1.get("1.0", END) # "1.0" starts on line 1, character 0 all the way to the end of the input.
    visualizer = ViewieCodeVisualizer(textbox2)

    tree = visualizer.parse_code(code)

    if tree:
        classes, functions = visualizer.code_extraction(tree)

        uml_file = visualizer.uml_generation(classes, functions)

        textbox2.delete("1.0", END)
        textbox2.insert(END, f"UML generated and saves as {uml_file} :0 \n")
    else:
        pass


# Actually making the button to upload this PYTHON source code
upload_button = Button(frame, text="Upload", command=upload_click)
upload_button.grid(row=1, column=0, pady=20)


# button for the diagram to be save (maybe we should add a drop down button to be saved as a pdf. or png.)
def save_click():
    print("Saved")
    textbox2.insert(END, f"UML saved as uml_diagram.png :0 \n")


# Another button i guesss
save_button = Button(frame, text="Save", command=save_click)
save_button.grid(row=1, column=1, pady=20)


# Here is the new page buttom -not sure what this need to do yet
def new_page_button():
    print("New page")


# actually making the stupid button
new_page_button = Button(root, text="New Page", command=new_page_button)
# moving the button~~
new_page_button.pack(side=TOP, padx=(10))

root.mainloop()

