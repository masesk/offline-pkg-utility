
from tkinter import *
from tkinter import filedialog 
from tkinter import ttk, messagebox
import threading
from pathlib import Path
from offline_pkg_utility import OfflinePkgUtility
import threading 








def main():
    window = Tk() 
    tabControl = ttk.Notebook(window) 
    
    download_repo_tab = ttk.Frame(tabControl) 
    setup_server_tab = ttk.Frame(tabControl) 
    
    tabControl.add(download_repo_tab, text ='Download Repos') 
    tabControl.add(setup_server_tab, text ='Setup/Update Server') 
    tabControl.pack(expand = 1, fill ="both") 


    style = ttk.Style() 
    style.configure('Label', foreground = 'green')


    window.title('offline-pkg-manager') 

    window.geometry("700x700") 


    
    def button_pressed_toggle_views(status, button, progress, label, label_content):
        if status == "error":
            progress.stop()
            progress.grid_remove()
            label["text"] = label_content
            label.grid(column=1, row=5, pady=15, sticky="ew", columnspan=3)
            button["state"] = "active"
        else:
            button["state"] = "disabled"
            label["text"] = label_content
            label.grid_remove()
            progress.start(interval=10)
            progress.grid(column=1, row=5, pady=15, sticky="ew", columnspan=3)
    

    def select_download_path(): 
        filename = filedialog.askdirectory(initialdir = Path(__file__).resolve().parent, 
                                            title = "Select output directory", 
                                            ) 
        path_input.delete(0, END)
        path_input.insert(0, filename)

    def select_server_path():
        filename = filedialog.askdirectory(initialdir = Path(__file__).resolve().parent, 
                                            title = "Select saved repo directory", 
                                            ) 
        saved_path_input.delete(0, END)
        saved_path_input.insert(0, filename)
    

    def add_download_console(message):
        download_console_output["state"] = "normal"
        download_console_output.insert(END, message + '\n')
        download_console_output["state"] = "disabled"

    def start_download_thread(download_console_output):
        try:
            opu = OfflinePkgUtility(add_download_console)
            opu.download_repos(name_input.get(), path_input.get())
            button_pressed_toggle_views(status="error", button=start_download_button, progress=download_progress, label=download_error_label, label_content="")
        except Exception as e:
            button_pressed_toggle_views(status="error", button=start_download_button, progress=download_progress, label=download_error_label, label_content=e)
    def start_download():
        try:
            button_pressed_toggle_views(status="none", button=start_download_button, progress=download_progress, label=download_error_label, label_content="")
            t1 = threading.Thread(target=start_download_thread, args=(download_console_output,)) 
            t1.start()
        except Exception as e:
            button_pressed_toggle_views(status="error", button=start_download_button, progress=download_progress, label=download_error_label, label_content=e)

    def start_setup():
        setup_server_button["state"] = "disabled"
        download_error_label["text"] = ""
        download_error_label.grid_remove()
        setup_server_progress.start(interval=10)
        setup_server_progress.grid(column=1, row=5, pady=15, sticky="ew", columnspan=3)

        


    ### Download 
    
    download_error_label = Label(download_repo_tab, text="")
    download_error_label.configure(foreground="red")

    download_console_output = Text(download_repo_tab)
    download_console_output["state"] = "disabled"

    start_download_button = Button(download_repo_tab, text="Download Packages", command=start_download)


    path_button = Button(download_repo_tab, text="...", command = select_download_path)


    name_input = ttk.Entry(download_repo_tab, justify = CENTER, 
                                        font = ('arial', 10, 'bold'))    


    path_input = ttk.Entry(download_repo_tab, justify = CENTER, 
                                        font = ('arial', 10, 'bold'))    


    path_label = Label(download_repo_tab, text="Output Path: ")

    name_label = Label(download_repo_tab, text="Name: ")

    download_progress = ttk.Progressbar(download_repo_tab, orient = HORIZONTAL, 
                length = 100, mode = 'indeterminate') 
    download_progress["value"] = 0

    path_label.grid(column = 1, row = 1,  sticky="ew")
    path_input.grid(column=2, row=1, ipadx = 25, ipady = 5,  sticky="ew")
    path_button.grid(column=3, row=1,  sticky="ew")
    name_label.grid(column = 1, row = 2, pady=20,  sticky="ew")
    name_input.grid(column=2, row=2, ipadx = 25, ipady = 5,  sticky="ew", columnspan=2)
    start_download_button.grid(column=2, row=3, pady=15, sticky="ew", columnspan=1)
    download_console_output.grid(column=1, rowspan=1, row=4, sticky="ew", columnspan=3)
    download_repo_tab.grid_columnconfigure((0, 4), weight=1) 


    ### Server Tab

    setup_server_button = Button(setup_server_tab, text="Setup/Update Server", command=start_setup)


    saved_path_button = Button(setup_server_tab, text="...", command = select_server_path)


    saved_name_input = ttk.Entry(setup_server_tab, justify = CENTER, 
                                        font = ('arial', 10, 'bold'))    


    saved_path_input = ttk.Entry(setup_server_tab, justify = CENTER, 
                                        font = ('arial', 10, 'bold'))    


    saved_path_label = Label(setup_server_tab, text="Saved Repo Path: ")

    saved_pm_label = Label(setup_server_tab, text="Package Manager: ")


    saved_pm_dd_sel = StringVar(setup_server_tab)
    saved_pm_dd_sel.set("YUM")

    saved_pm_dropdown = OptionMenu(setup_server_tab, saved_pm_dd_sel, "YUM")



    setup_server_progress = ttk.Progressbar(setup_server_tab, orient = HORIZONTAL, 
                length = 100, mode = 'indeterminate') 
    setup_server_progress["value"] = 0

    saved_path_label.grid(column = 1, row = 1,  sticky="ew")
    saved_path_input.grid(column=2, row=1, ipadx = 25, ipady = 5,  sticky="ew")
    saved_path_button.grid(column=3, row=1,  sticky="ew")
    saved_pm_label.grid(column=1, row=2, sticky="ew")
    saved_pm_dropdown.grid(column=2, pady=15 ,row=2, sticky="ew", columnspan=2)
    setup_server_button.grid(column=1, row=3, pady=15, sticky="ew", columnspan=3)
    setup_server_tab.grid_columnconfigure((0, 4), weight=1) 



    window.mainloop()

if __name__ == '__main__':
    main()
     