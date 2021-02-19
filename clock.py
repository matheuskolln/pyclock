# importing modules
import tkinter as tk
from tkinter import colorchooser, messagebox
from time import strftime, localtime, struct_time
import pygame


# creating a class for application
class Application(tk.Frame):

    # initiate the attributes from the class
    def __init__(self, master=None):
        super().__init__(master)
        self.timer = -1
        self.alarm = -1
        self.master = master
        self.master.resizable(False, False)
        self.main_bg = self.rgb((100, 100, 100))
        self.second_bg = self.rgb((170, 170, 170))
        self.time = tk.Label(self.master, width="7", borderwidth=2, relief="solid", bg=self.second_bg, fg="black", font=("LG Weather_Z", 70, "bold"))
        self.title = tk.Label(self.master, text = "Actually time", width="330", height="2", bg=self.main_bg, fg="black", font=("", 25, "bold"))
        self.change_theme_button = tk.Button(self.master, text="Change theme", width="13", height="2", bg=self.main_bg, fg="black", 
            font=("", 25, "bold"), command = self.change_theme_color)
        self.timer_button = tk.Button(self.master, text="Set timer", width="13", height="2", bg=self.main_bg, fg="black", 
            font=("", 25, "bold"), command = self.open_timer_window)
        self.today_date = tk.Label(self.master, text = "Today's date: {0}".format(strftime("%d/%m/%Y", localtime())), width="330", height="1", bg=self.main_bg, fg="black", font=("", 20, "bold"))
        self.pack()
        self.create_widgets()
        master.geometry("400x480")
        master.config(bg=self.main_bg)
        master.title("pyClock")

    def create_widgets(self):
        """creates widgets for the application"""
        self.title.pack(anchor='center')
        self.time.pack(anchor='center', pady=10)
        self.time_now()
        self.change_theme_button.pack(anchor='center', pady=10)
        self.timer_button.pack(anchor='center')
        self.today_date.pack(anchor='center', pady=10)

    def time_now(self): 
        """updates time label to actually time and checks if is time to alarm"""
        pygame.mixer.music.stop()
        if self.timer != -1:
            timeList = [ self.timer, self.alarm]
            totalSecs = 0
            for tm in timeList:
                timeParts = [int(s) for s in tm.split(':')]
                totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
            totalSecs, sec = divmod(totalSecs, 60)
            hr, min = divmod(totalSecs, 60)
            if ("%d:%02d:%02d" % (hr, min, sec) == strftime('%H:%M:%S')):
                self.time.config(text = "ALARM")
                pygame.mixer.music.load("alarm.ogg")
                pygame.mixer.music.play()
                messagebox.showwarning(title="Alarm!", message="Your alarm!")
                self.timer = -1
        string = strftime('%H:%M:%S') 
        self.time.config(text = string) 
        self.time.after(1000, self.time_now) 
        
    def rgb(self, rgb):
        """translates an rgb tuple of int to a tkinter friendly color code"""
        r, g, b = rgb
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def change_theme_color(self):
        """changes theme color from application"""
        color_code = colorchooser.askcolor(title="Choose theme color")[0]
        self.main_bg = self.rgb(tuple(map(int, color_code)))

        if color_code[0] >= 185 or color_code[1] >= 185 or color_code[2] >= 185:
            self.second_bg = self.rgb(tuple(x+(255-int(max(color_code))) for x in (map(int, color_code))))
        else:
            self.second_bg = self.rgb(tuple(x+70 for x in (map(int, color_code))))

        self.master.config(bg=self.main_bg)
        self.title.config(bg=self.main_bg)
        self.today_date.config(bg=self.main_bg)
        self.change_theme_button.config(bg=self.second_bg)
        self.time.config(bg=self.second_bg)
        self.timer_button.config(bg=self.second_bg)

    def open_timer_window(self):
        """opens timer window"""
        timerWindow = tk.Toplevel(self.master)
        timerWindow.resizable(False, False)
        timerWindow.title("Set your alarm!")
        timerWindow.geometry("405x190")
        timerWindow.config(bg=self.main_bg)
        def getTime():
            self.alarm = strftime('%H:%M:%S') 
            timer = strftime("%H:%M:%S", struct_time((0, 0, 0, int(h.get()), int(m.get()), int(s.get()), 0, 0, 0)))
            self.timer = timer
            timerWindow.destroy()
        h = tk.Spinbox(timerWindow, from_=0, to=99, bg=self.second_bg, fg="black", font=("", 25, "bold"), width='2')
        h_colon = tk.Label(timerWindow, text = "h:", bg=self.main_bg, fg="black", font=("", 25, "bold"), width='2')
        m = tk.Spinbox(timerWindow, from_=0, to=59, bg=self.second_bg, fg="black", font=("", 25, "bold"), width='2')
        m_colon = tk.Label(timerWindow, text = "m:", bg=self.main_bg, fg="black", font=("", 25, "bold"), width='2')
        s = tk.Spinbox(timerWindow, from_=0, to=59, bg=self.second_bg, fg="black", font=("", 25, "bold"), width='2')
        s_colon = tk.Label(timerWindow, text = "s", bg=self.main_bg, fg="black", font=("", 25, "bold"), width='1')
        set_button = tk.Button(timerWindow, text = "Set your alarm!", bg=self.main_bg, fg="black", font=("", 25, "bold"), width='15', height='1', command=getTime)
        h.place(y=40, x=20)
        h_colon.place(y=40, x=100)
        m.place(y=40, x=150)
        m_colon.place(y=40, x=230)
        s.place(y=40, x=280)
        s_colon.place(y=40, x=360)
        set_button.place(y=105, x=15)
        
if __name__ == '__main__':
    pygame.mixer.init()
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
