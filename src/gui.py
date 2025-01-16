import customtkinter
import tkinterDnD
import gobzer
import threading
from config import settings, update_setting

customtkinter.set_ctk_parent_class(tkinterDnD.Tk)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
def import_app():
    return app
app.geometry("600x600")
app.title("gobzer")
app.resizable(0,0)

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

def start_button(event=None):
    gobzer.run()
    import main
    main.run()

def cancel_button(event=None):
    app.destroy()

def process_input(entry_widget, event=None):
    if isinstance(settings[entry_widget.field_name], int) and entry_widget.get().isnumeric():
        number = int(entry_widget.get())
        field_name = entry_widget.field_name
        update_setting(field_name, number)
        entry_widget.selection_clear()
        app.focus()
        flash_entry_field(entry_widget,valid=True)
    elif isinstance(settings[entry_widget.field_name], str) and isinstance(entry_widget.get(), str):
        entry = str(entry_widget.get())
        field_name = entry_widget.field_name
        update_setting(field_name, entry)
        entry_widget.selection_clear()
        app.focus()
        flash_entry_field(entry_widget,valid=True)
    else:
        flash_entry_field(entry_widget,valid=False)

def flash_entry_field(entry_widget,valid=True):
    if valid:
        entry_widget.configure(fg_color="green")
        app.after(250, lambda: entry_widget.configure(fg_color=entry_color))
    else:
        entry_widget.configure(fg_color="red")
        app.after(250, lambda: entry_widget.configure(fg_color=entry_color))

def set_cross_realm(event=None):
    cross_realm_setting = settings["cross_realm_logging"]
    if cross_realm_setting == int(0):
        update_setting("cross_realm_logging",1)
    elif cross_realm_setting == int(1):
        update_setting("cross_realm_logging",0)
    else:
        print("there is an issue with your cross realm settings, check the settings.json and make sure it is either 0 or 1")
        update_setting("cross_realm_logging",0)

def toggle_section():
    global section_open

    if section_open:
        # hides the extra option widgets
        for widget, row, column in toggle_widgets:
            widget.grid_forget()
        toggle_button.configure(text="Show Options")
    else:
        # constructs the extra option widgets in their corect row and column
        for widget, row, column in toggle_widgets:
            widget.grid(row=row, column=column, pady=10, padx=10)
        toggle_button.configure(text="Hide Options")
     
    section_open = not section_open


frame_1 = customtkinter.CTkFrame(master=app)
frame_1.grid(row=0,column=0,pady=20, padx=20, sticky="nsew")

label_1 = customtkinter.CTkLabel(master=frame_1, text="gobzer Auction House Bot", justify=customtkinter.CENTER)
label_1.grid(row=0,column=1,pady=10, padx=10)

button_1 = customtkinter.CTkButton(master=frame_1, text=f"Run bot ({settings["run_bot_kb"]})", command=start_button)
button_1.grid(row=2,column=1,pady=10, padx=10)
app.bind(settings["run_bot_kb"], start_button)

button_2 = customtkinter.CTkButton(master=frame_1, text=f"Cancel ({settings["cancel_bot_kb"]})", command=cancel_button)
button_2.grid(row=3,column=1,pady=10, padx=10)

spacer = customtkinter.CTkLabel(master=frame_1, text="")
spacer.grid(row=4,column=0)

label_2 = customtkinter.CTkLabel(master=frame_1, text="Settings", justify=customtkinter.LEFT)
label_2.grid(row=5, column=1, pady=10, padx=10)

checkbox_1 = customtkinter.CTkCheckBox(master=frame_1, text="enable cross-realm auctioning?",checkbox_height=20,checkbox_width=20, command=set_cross_realm)
checkbox_1.grid(row=6,columnspan=2,pady=10, padx=10)
if settings["cross_realm_logging"] == 1:
    checkbox_1.select()

cross_char_label = customtkinter.CTkLabel(master=frame_1, text="char no.")
cross_char_label.grid(row=7,column=0,pady=10,padx=10)
cross_char_entry = customtkinter.CTkEntry(master=frame_1, placeholder_text=str(settings["cross_characters"]))
cross_char_entry.grid(row=7,column=1,pady=10, padx=10)
cross_char_entry.field_name = "cross_characters"
entry_color = cross_char_entry.cget("fg_color")
cross_char_entry.bind("<Return>", lambda event: process_input(cross_char_entry))

section_label = customtkinter.CTkLabel(master=frame_1, text="Extra options")
section_open = False 

toggle_button = customtkinter.CTkButton(master=frame_1, text="Show Options", command=toggle_section)
toggle_button.grid(row=8, column=1, pady=10, padx=10)

#creates placeholder labels so that the extra option toggle doesn't blow up the GUI
for i in range(2):
    for j in range(3):
        placeholder = customtkinter.CTkLabel(frame_1, text="                                                              ")
        placeholder.grid(row=9 + i, column=j, pady=10, padx=10)

idle_time_label = customtkinter.CTkLabel(master=frame_1, text="time between undercut checks")
idle_time_label.grid(row=10,column=0,pady=10,padx=10)
idle_time_entry = customtkinter.CTkEntry(master=frame_1, placeholder_text=str(f"{settings["idle_time"]} seconds"))
idle_time_entry.field_name = "idle_time" # field name identical to settings json entries to feed into update_setting function
idle_time_entry.grid(row=10,column=1,pady=10, padx=10)
idle_time_entry.bind("<Return>", lambda event: process_input(idle_time_entry))

section_label_2 = customtkinter.CTkLabel(master=frame_1, text="keybinds")

run_bot_kb_label = customtkinter.CTkLabel(master=frame_1, text="run bot keybind")
run_bot_kb_label.grid(row=11,column=0,pady=10,padx=10)
run_bot_kb_input = customtkinter.CTkEntry(master=frame_1, placeholder_text=str(settings["run_bot_kb"]))
run_bot_kb_input.field_name = "run_bot_kb"
run_bot_kb_input.grid(row=11,column=1,pady=10, padx=10)
run_bot_kb_input.bind("<Return>", lambda event: process_input(run_bot_kb_input))

cancel_bot_kb_label = customtkinter.CTkLabel(master=frame_1, text="cancel bot keybind")
cancel_bot_kb_label.grid(row=12,column=0,pady=10,padx=10)
cancel_bot_kb_input = customtkinter.CTkEntry(master=frame_1, placeholder_text=str(settings["cancel_bot_kb"]))
cancel_bot_kb_input.field_name = "cancel_bot_kb"
cancel_bot_kb_input.grid(row=12,column=1,pady=10, padx=10)
cancel_bot_kb_input.bind("<Return>", lambda event: process_input(cancel_bot_kb_input))

#this is a list of toggle-able widgets with their row and column position to be inserted into the toggle_section function to toggle these on/off
toggle_widgets = [(idle_time_entry,10,1),
(idle_time_label,10,0),
(run_bot_kb_label,11,0),
(run_bot_kb_input,11,1),
(cancel_bot_kb_label,12,0),
(cancel_bot_kb_input,12,1)]

#this sets the widgets as toggled off initially
for widget, row, column in toggle_widgets:
    widget.grid_forget()

#app.mainloop()