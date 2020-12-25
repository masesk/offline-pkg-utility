
from tkinter import *
from tkinter import filedialog 
from tkinter import ttk 
from tkinter.messagebox import askyesno 
from pathlib import Path
import time

window = Tk() 
tabControl = ttk.Notebook(window) 
  
tab1 = ttk.Frame(tabControl) 
tab2 = ttk.Frame(tabControl) 
  
tabControl.add(tab1, text ='Download Repos') 
tabControl.add(tab2, text ='Setup/Update Server') 
tabControl.pack(expand = 1, fill ="both") 


style = ttk.Style() 
style.configure('TEntry', foreground = 'green')


window.title('offline-pkg-manager') 

window.geometry("500x500") 
   

# file explorer window 
def browseFiles(): 
    filename = filedialog.askdirectory(initialdir = Path(__file__).resolve().parent, 
                                          title = "Select output directory", 
                                        ) 
    path_input.delete(0, END)
    path_input.insert(0, filename)

def bar():
    progress.grid(column=1, row=4, pady=15, sticky="ew", columnspan=3)
    value = 0
    while True:
        value += 10
        if value >= 100:
            value = 0
            progress.grid_remove()
            break
        progress['value'] = value
        window.update_idletasks() 
        time.sleep(0.1) 
   

sync = Button(tab1, text="Download Packages", command = bar)


path_button = Button(tab1, text="...", command = browseFiles)


txt = ttk.Entry(tab1, justify = CENTER, 
                                     font = ('arial', 10, 'bold'))    


path_input = ttk.Entry(tab1, justify = CENTER, 
                                     font = ('arial', 10, 'bold'))    


path_txt = Label(tab1, text="Output Path: ")

input_txt = Label(tab1, text="Name: ")

progress = ttk.Progressbar(tab1, orient = HORIZONTAL, 
            length = 100, mode = 'indeterminate') 
progress["value"] = 0

path_txt.grid(column = 1, row = 1,  sticky="ew")
path_input.grid(column=2, row=1, ipadx = 25, ipady = 5,  sticky="ew")
path_button.grid(column=3, row=1,  sticky="ew")
input_txt.grid(column = 1, row = 2, pady=20,  sticky="ew")
txt.grid(column=2, row=2, ipadx = 25, ipady = 5,  sticky="ew", columnspan=2)
sync.grid(column=1, row=3, pady=15, sticky="ew", columnspan=3)
tab1.grid_columnconfigure((0, 4), weight=1)  

   
# Let the window wait for any events 
window.mainloop() 