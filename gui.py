
from tkinter import *
from tkinter import filedialog 
from tkinter import ttk, messagebox
import threading
from pathlib import Path
from offline_pkg_utility import OfflinePkgUtility
import threading 
import re








def main():
    window = Tk() 
    tabControl = ttk.Notebook(window) 
    
    download_repo_tab = ttk.Frame(tabControl) 
    setup_server_tab = ttk.Frame(tabControl) 
    client_tab = ttk.Frame(tabControl) 
    
    tabControl.add(download_repo_tab, text ='Download Repos') 
    tabControl.add(setup_server_tab, text ='Setup/Update Server') 
    tabControl.add(client_tab, text ='Setup Client') 
    tabControl.pack(expand = 1, fill ="both") 


    style = ttk.Style() 
    style.configure('Label', foreground = 'green')


    window.title('offline-pkg-utility') 

    window.geometry("700x700") 

    def is_valid_ipv4(ip):
        """Validates IPv4 addresses.
        """
        pattern = re.compile(r"""
            ^
            (?:
            # Dotted variants:
            (?:
                # Decimal 1-255 (no leading 0's)
                [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
            |
                0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
            |
                0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
            )
            (?:                  # Repeat 0-3 times, separated by a dot
                \.
                (?:
                [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
                |
                0x0*[0-9a-f]{1,2}
                |
                0+[1-3]?[0-7]{0,2}
                )
            ){0,3}
            |
            0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
            |
            0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
            |
            # Decimal notation, 1-4294967295:
            429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
            42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
            4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
            )
            $
        """, re.VERBOSE | re.IGNORECASE)
        return pattern.match(ip) is not None
    
    def button_pressed_toggle_views(status, button, progress, label, label_content):
        if status == "error" or status == "done":
            progress.stop()
            progress.grid_remove()
            label["text"] = label_content
            label.grid(column=1, row=6, pady=15, sticky="ew", columnspan=3)
            button["state"] = "active"
        else:
            button["state"] = "disabled"
            label["text"] = label_content
            label.grid_remove()
            progress.start(interval=10)
            progress.grid(column=1, row=6, pady=15, sticky="ew", columnspan=3)
    

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
            opu = OfflinePkgUtility(sudo_password=root_password_input.get(),callback=add_download_console)
            opu.download_repos(name_input.get(), path_input.get())
            button_pressed_toggle_views(status="done", button=start_download_button, progress=download_progress, label=download_error_label, label_content="")
        except Exception as e:
            button_pressed_toggle_views(status="error", button=start_download_button, progress=download_progress, label=download_error_label, label_content=e)
    def start_download():
        try:
            button_pressed_toggle_views(status="none", button=start_download_button, progress=download_progress, label=download_error_label, label_content="")
            t1 = threading.Thread(target=start_download_thread, args=(download_console_output,)) 
            t1.start()
        except Exception as e:
            button_pressed_toggle_views(status="error", button=start_download_button, progress=download_progress, label=download_error_label, label_content=e)

    def start_setup_thread():
        try:
            opu = OfflinePkgUtility(sudo_password=root_password_server_input.get())
            opu.setup_pm_server(saved_path_input.get())
            button_pressed_toggle_views(status="done", button=setup_server_button, progress=setup_server_progress, label=setup_server_error_label, label_content="")
        except Exception as e:
            button_pressed_toggle_views(status="error", button=setup_server_button, progress=setup_server_progress, label=setup_server_error_label, label_content=e)
    
    def start_server_setup():
        try:
            button_pressed_toggle_views(status="none", button=setup_server_button, progress=setup_server_progress, label=setup_server_error_label, label_content="")
            t1 = threading.Thread(target=start_setup_thread) 
            t1.start()
        except Exception as e:
            button_pressed_toggle_views(status="error", button=setup_server_button, progress=setup_server_progress, label=setup_server_error_label, label_content=e)
    
    def start_client_setup():
        button_pressed_toggle_views(status="none", button=setup_client_button, progress=setup_client_progress, label=setup_client_error_label, label_content="")
        if not is_valid_ipv4(ip_input.get()):
            button_pressed_toggle_views(status="error", button=setup_client_button, progress=setup_client_progress, label=setup_client_error_label, label_content="Invalid IPv4 format")
            return
        try:
            button_pressed_toggle_views(status="none", button=setup_client_button, progress=setup_client_progress, label=setup_client_error_label, label_content="")
            t1 = threading.Thread(target=start_client_thread) 
            t1.start()
        except Exception as e:
            button_pressed_toggle_views(status="error", button=setup_client_button, progress=setup_client_progress, label=setup_client_error_label, label_content=e)
    
    def start_client_thread():
        try:
            opu = OfflinePkgUtility(sudo_password=root_password_server_input.get())
            opu.setup_client(saved_path_input.get())
            time.sleep(5.5)
            button_pressed_toggle_views(status="done", button=setup_client_button, progress=setup_client_progress, label=setup_client_error_label, label_content="")
        except Exception as e:
            button_pressed_toggle_views(status="error", button=setup_client_button, progress=setup_client_progress, label=setup_client_error_label, label_content=e)
    

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

    root_password_input = ttk.Entry(download_repo_tab, justify= CENTER,
                                        font = ('arial', 10, 'bold'), show="*")


    path_label = Label(download_repo_tab, text="Output Path: ")

    name_label = Label(download_repo_tab, text="Name: ")

    root_password_label = Label(download_repo_tab, text="Root Password: ")

    download_progress = ttk.Progressbar(download_repo_tab, orient = HORIZONTAL, 
                length = 100, mode = 'indeterminate') 
    download_progress["value"] = 0

    path_label.grid(column = 1, row = 1,  sticky="ew")
    path_input.grid(column=2, row=1, ipadx = 25, ipady = 5,  sticky="ew")
    path_button.grid(column=3, row=1,  sticky="ew")
    name_label.grid(column = 1, row = 2, pady=20,  sticky="ew")
    name_input.grid(column=2, row=2, ipadx = 25, ipady = 5,  sticky="ew", columnspan=2)
    root_password_label.grid(column = 1, row = 3,  sticky="ew")
    root_password_input.grid(column=2, row=3, ipadx = 25, ipady = 5,  sticky="ew", columnspan=2)
    start_download_button.grid(column=2, row=4, pady=15, sticky="ew", columnspan=1)
    download_console_output.grid(column=1, rowspan=1, row=5, sticky="ew", columnspan=3)
    download_repo_tab.grid_columnconfigure((0, 4), weight=1) 


    ### Server Tab


    setup_server_error_label = Label(setup_server_tab, text="")
    setup_server_error_label.configure(foreground="red")

    setup_server_button = Button(setup_server_tab, text="Setup/Update Server", command=start_server_setup)


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

    root_password_server_input = ttk.Entry(setup_server_tab, justify= CENTER,
                                        font = ('arial', 10, 'bold'), show="*")

    root_password_server_label = Label(setup_server_tab, text="Root Password: ")
    setup_server_progress = ttk.Progressbar(setup_server_tab, orient = HORIZONTAL, 
                length = 100, mode = 'indeterminate') 
    setup_server_progress["value"] = 0

    saved_path_label.grid(column = 1, row = 1,  sticky="ew")
    saved_path_input.grid(column=2, row=1, ipadx = 25, ipady = 5,  sticky="ew")
    saved_path_button.grid(column=3, row=1,  sticky="ew")
    saved_pm_label.grid(column=1, row=2, sticky="ew")
    saved_pm_dropdown.grid(column=2, pady=15 ,row=2, sticky="ew", columnspan=2)
    root_password_server_label.grid(column = 1, row = 3,  sticky="ew")
    root_password_server_input.grid(column=2, row=3, ipadx = 25, ipady = 5,  sticky="ew", columnspan=2)
    setup_server_button.grid(column=1, row=4, pady=15, sticky="ew", columnspan=3)
    setup_server_tab.grid_columnconfigure((0, 4), weight=1) 

    ### Client Tab

    setup_client_error_label = Label(client_tab, text="")
    setup_client_error_label.configure(foreground="red")

    ip_label = Label(client_tab, text="Server IPv4: ")
    ip_input = ttk.Entry(client_tab, justify = CENTER, 
                                        font = ('arial', 10, 'bold')) 
    root_password_client_input = ttk.Entry(client_tab, justify= CENTER,
                                        font = ('arial', 10, 'bold'), show="*")

    root_password_client_label = Label(client_tab, text="Root Password: ")
    setup_client_button = Button(client_tab, text="Setup Client", command=start_client_setup)
    setup_client_progress = ttk.Progressbar(client_tab, orient = HORIZONTAL, 
                length = 100, mode = 'indeterminate') 
    setup_client_progress["value"] = 0
    ip_label.grid(column = 1, row = 1,  sticky="ew")
    ip_input.grid(column=2, row=1, ipadx = 25, ipady = 5,  sticky="ew")
    setup_client_button.grid(column=1, row=4, pady=15, sticky="ew", columnspan=3)
    client_tab.grid_columnconfigure((0, 4), weight=1)

    


    window.mainloop()

if __name__ == '__main__':
    main()
     