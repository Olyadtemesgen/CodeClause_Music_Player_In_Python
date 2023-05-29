import os
import time
from tkinter import Tk, Label, Button, filedialog, Frame, ttk
# import Frame
from PIL import Image, ImageTk
from pygame import mixer
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class MusicPlayer:
    
    def __init__(self, root):
        
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("600x400")
        
        self.timer_running_timer = False
        self.timer_seconds = 0
        self.timer_id = None
        
        self.music_file = None
        self.music_duration = 0
        self.music_start_time = 0
        
        self.music_end_time = 0
        self.music_position = 0
        self.time_string = "00:00"
        
        self.label = Label(root, text="Music Player", font=("Arial", 10, "bold"))
        self.label.pack(pady=20)
        self.is_paused = False
        self.button_text = "Select Music"
        
        button_bg_color = "#00FF00"  # Red color
        button_radius = 5
        
        self.back_image = Image.open('download.png')
        self.background_path = "sh"
        self.background_image = Image.open("stock-photo--d-illustration-of-musical-notes-and-musical-signs-of-abstract-music-sheet-songs-and-melody-concept-761313844.jpg")

        self.width, self.height = root.winfo_screenwidth(), root.winfo_screenheight()
        self.background_image = self.background_image.resize((self.width, self.height), Image.ANTIALIAS)

        self.tk_background = ImageTk.PhotoImage(self.background_image)

        # self.# Create a label widget to display the background image
        
        self.background_label = Label(root, image=self.tk_background, highlightthickness=0)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.label = Label(root, text="Music Player", font=("Arial", 10, "bold"), highlightthickness=0)
        self.label.pack(pady=10)
        
        self.select_button = Button(root, text=self.button_text, bg="#00FF00", bd=0, highlightthickness=0,
                relief="flat", activebackground=button_bg_color, padx=10, pady=5, borderwidth=0,
                font=("Arial", 12), border=0,  command=self.select_music)
        self.timer_running_timer = False
        self.timer_seconds_time = 0
        self.timer_id = None

        # self.select_button.bind("<Configure>", lambda e: self.select_button.configure(height=e.height - 4))
        self.select_button.pack()
        self.button_frame = Frame(root)
        
        self.button_frame.pack(pady=10)
        self.play_button = Button(self.button_frame, text="Play", bg="#FFFF00", bd=0, highlightthickness=0,
                relief="flat", activebackground=button_bg_color, padx=10, pady=5, borderwidth=0,
                font=("Arial", 12), border=0, command=self.play_music)
        # self.play_button.grid(column=0)
        self.play_button.pack(side='left',pady=12, padx=30)
        
        

        self.stop_button = Button(self.button_frame, text="Stop", bg="#FF0000", bd=0, highlightthickness=0,
                relief="flat", activebackground=button_bg_color, padx=10, pady=5, borderwidth=0,
                font=("Arial", 12), border=0, command=self.stop_music)
        # self.play_button.grid(column=1)
        self.stop_button.pack(side='left',pady=10, padx=30)
        self.time_and_pause = Frame(root)
        self.time_and_pause.pack(fill='x', expand=True, padx=30)
        
        style = ttk.Style()
        style.configure("Custom.Horizontal.TProgressbar",
                        troughcolor='gray',
                        background='green',
                        thickness=10)  # Adjust the thickness value as desired

        # Define a custom layout for the progress bar
        style.layout("Custom.Horizontal.TProgressbar",
                    [('Horizontal.Progressbar.trough',
                    {'children': [('Horizontal.Progressbar.pbar',
                                    {'side': 'left', 'sticky': 'ns'})],
                        'sticky': 'nswe'})])

        # Create the progress bar using the custom style
        self.progress_bar = ttk.Progressbar(self.time_and_pause,
                                            orient='horizontal',
                                            # highlightthickness=0,
                                            length=500,
                                            mode='determinate',
                                            style="Custom.Horizontal.TProgressbar")
        self.progress_bar.pack(side='left', padx=(20, 10), pady=20)

        
        self.timer_label = Label(self.time_and_pause, highlightthickness=0,text="00:00", font=("Arial", 24))
        self.timer_label.pack(side="left",pady=20, padx=(0, 30))

        self.pause_button = Button(self.time_and_pause ,text="Pause",  bg="#FFFF00", bd=0, highlightthickness=0,
                relief="flat", activebackground=button_bg_color, padx=10, pady=5, borderwidth=0,
                font=("Arial", 12), border=0, command=self.pause_mezmur)
        
        self.pause_button.pack(side="left", pady=20, padx=30)
    
    def select_music(self):
        self.timer_seconds_time = 0
        self.timer_running_timer = False
        self.timer_seconds_time = 0
        self.timer_id = None
        self.music_file = filedialog.askopenfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
        if self.music_file:
            self.label.config(text="Music Selected: " + os.path.basename(self.music_file))
            self.play_button.config(state="normal")
            self.stop_button.config(state="normal")
            self.load_music()

    def load_music(self):
        mixer.init()
        mixer.music.load(self.music_file)
        self.music_duration = mixer.Sound(self.music_file).get_length() * 1000

    def play_music(self):
        if self.music_file:
            self.music_start_time = time.time()
            self.music_end_time = self.music_start_time + (self.music_duration / 1000)
            if not self.timer_running_timer:
                self.timer_running_timer = True
                self.play_button.config(state="disabled")
                
                self.stop_button.config(state="normal")
                # self.reset_button.config(state="normal")
            
            self.update_timer()

            mixer.music.play()
    
    def pause_mezmur(self):

        if self.timer_running_timer:
            
            self.timer_running_timer = False
            self.play_button.config(state="normal")
            self.stop_button.config(state="normal")

            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
        
        if self.is_paused:
            self.pause_button.config(text="Pause")
            # self.update_timer()
            mixer.music.unpause()
            self.is_paused = False
        else:
            self.pause_button.config(text="Resume")
            self.is_paused = True
            
            mixer.music.pause()

    def stop_music(self):
        self.time_string = "00:00"
        # self.stop_timer()
        self.progress_bar.stop()
        self.progress_bar['value'] = 0
        self.timer_seconds = 0
        self.timer_label.config(text="00:00")
        
        if self.timer_running_timer:
            
            self.timer_running_timer = False
            self.play_button.config(state="normal")
            self.stop_button.config(state="disabled")

            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None

        mixer.music.stop()
    
    def update_timer(self):
        current_time = time.time()
        elapsed_time = current_time - self.music_start_time
        
        if self.music_duration:
            progress = (elapsed_time / (self.music_duration / 1000)) * 100
        
        self.progress_bar['value'] = progress

        self.timer_seconds += 1
        hours = self.timer_seconds // 3600
        minutes = (self.timer_seconds // 60) % 60
        
        seconds = self.timer_seconds % 60
        self.time_string = "{:02d}:{:02d}".format(minutes, seconds)
        self.timer_label.config(text=self.time_string)
        self.timer_id = self.root.after(1000, self.update_timer)

if __name__ == '__main__':
    root = Tk()
    music_player = MusicPlayer(root)
    root.mainloop()
