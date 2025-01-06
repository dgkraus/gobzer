import customtkinter
import tkinterDnD
import gobzer
import threading
#from main import run

customtkinter.set_ctk_parent_class(tkinterDnD.Tk)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
def import_app():
    return app
app.geometry("440x440")
app.title("gobzer")
app.resizable(0,0)


app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

def start_button(event=None):
    gobzer.run()
    import main
    main.run()

def cancel_button(event=None):
    app.quit()

def toggle_section():
    global section_open
    if section_open:
        section_label.grid_forget()  # Hide the section content
        toggle_button.configure(text="Show Options")
    else:
        section_label.grid(row=9,column=1,pady=10,padx=10)
        toggle_button.configure(text="Hide Options")
    section_open = not section_open


frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, text="gobzer Auction House Bot", justify=customtkinter.CENTER)
label_1.grid(row=0,column=1,pady=10, padx=10)

button_1 = customtkinter.CTkButton(master=frame_1, text="(R)un bot", command=start_button)
button_1.grid(row=2,column=1,pady=10, padx=10)
app.bind("r", start_button)

button_2 = customtkinter.CTkButton(master=frame_1, text="(C)ancel", command=cancel_button)
button_2.grid(row=3,column=1,pady=10, padx=10)
#app.bind("c", cancel_button)

spacer = customtkinter.CTkLabel(master=frame_1, text="")
spacer.grid(row=4,column=0)

label_2 = customtkinter.CTkLabel(master=frame_1, text="Settings", justify=customtkinter.LEFT)
label_2.grid(row=5, column=1, pady=10, padx=10)

checkbox_1 = customtkinter.CTkCheckBox(master=frame_1, text="enable cross-realm auctioning?",checkbox_height=20,checkbox_width=20)
checkbox_1.grid(row=6,columnspan=2,pady=10, padx=10)

label_3 = customtkinter.CTkLabel(master=frame_1, text="char no.")
label_3.grid(row=7,column=0,pady=10,padx=10)
entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="character no.")
entry_1.grid(row=7,column=1,pady=10, padx=10)

section_label = customtkinter.CTkLabel(master=frame_1, text="Extra options")
section_open = False 

toggle_button = customtkinter.CTkButton(master=frame_1, text="Show Options", command=toggle_section)
toggle_button.grid(row=8, column=1, pady=10, padx=10)