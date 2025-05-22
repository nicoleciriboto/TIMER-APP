import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import threading
from datetime import datetime, timedelta

#
class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Android-Style Timer/Alarm")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")

        self.create_widgets()
        self.update_clock()

    def create_widgets(self):
        # === Live Clock ===
        self.clock_label = tk.Label(self.root, text="", font=("Arial", 24), fg="cyan", bg="#1e1e1e")
        self.clock_label.pack(pady=20)

        # === Entry Frame ===
        entry_frame = tk.Frame(self.root, bg="#1e1e1e")
        entry_frame.pack(pady=10)

        self.hour_var = tk.StringVar()
        self.minute_var = tk.StringVar()
        self.second_var = tk.StringVar()

        tk.Entry(entry_frame, textvariable=self.hour_var, width=5, font=("Arial", 18)).grid(row=0, column=0, padx=5)
        tk.Label(entry_frame, text=":", font=("Arial", 18), bg="#1e1e1e", fg="white").grid(row=0, column=1)
        tk.Entry(entry_frame, textvariable=self.minute_var, width=5, font=("Arial", 18)).grid(row=0, column=2, padx=5)
        tk.Label(entry_frame, text=":", font=("Arial", 18), bg="#1e1e1e", fg="white").grid(row=0, column=3)
        tk.Entry(entry_frame, textvariable=self.second_var, width=5, font=("Arial", 18)).grid(row=0, column=4, padx=5)

        # === Buttons ===
        button_frame = tk.Frame(self.root, bg="#1e1e1e")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Start", command=self.start_timer, width=10, font=("Arial", 14), bg="green", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Reset", command=self.reset_timer, width=10, font=("Arial", 14), bg="red", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Set Default", command=self.set_default, width=10, font=("Arial", 14), bg="blue", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Exit", command=self.root.quit, width=10, font=("Arial", 14), bg="orange", fg="white").grid(row=0, column=3, padx=5)
 


        # === Countdown Label ===
        self.timer_label = tk.Label(self.root, text="", font=("Arial", 30), fg="lime", bg="#1e1e1e")
        self.timer_label.pack(pady=20)

        self.running = False

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=f"Current Time: {now}")
        self.root.after(1000, self.update_clock)

    def start_timer(self):
        if self.running:
            return
        try:
            h = int(self.hour_var.get() or 0)
            m = int(self.minute_var.get() or 0)
            s = int(self.second_var.get() or 0)
            total_seconds = h * 3600 + m * 60 + s

            if total_seconds <= 0:
                messagebox.showwarning("Invalid", "Please enter a valid time!")
                return

            self.running = True
            self.timer_end_time = datetime.now() + timedelta(seconds=total_seconds)
            threading.Thread(target=self.countdown, daemon=True).start()

        except ValueError:
            messagebox.showerror("Error", "Please enter numeric values!")

    def countdown(self):
        while self.running:
            remaining = self.timer_end_time - datetime.now()
            total_seconds = int(remaining.total_seconds())

            if total_seconds <= 0:
                self.timer_label.config(text="Time's up!")
                messagebox.showinfo("Timer", "Timer finished!")
                self.running = False
                break

            h, rem = divmod(total_seconds, 3600)
            m, s = divmod(rem, 60)
            self.timer_label.config(text=f"{h:02}:{m:02}:{s:02}")
            time.sleep(1)

    def reset_timer(self):
        self.running = False
        self.timer_label.config(text="")
        self.hour_var.set("")
        self.minute_var.set("")
        self.second_var.set("")

    def set_default(self):
        # Default to 0h 1m 30s
        self.hour_var.set("0")
        self.minute_var.set("1")
        self.second_var.set("30")
        messagebox.showinfo("Default Set", "Default time set to 00:01:30")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()

