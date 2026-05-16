import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment
import os

def change_speed(sound, speed=1.0):
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
    })
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def select_files():
    files = filedialog.askopenfilenames(filetypes=[('Audio Files', '*.mp3 *.wav *.ogg')])
    file_list_var.set('\n'.join(files))

def process_files():
    try:
        speed = float(speed_var.get())
        output_format = format_var.get()
        files = file_list_var.get().split('\n')
        if not files or files == ['']:
            raise Exception("الرجاء اختيار ملفات الصوت أولاً.")
        for file_path in files:
            song = AudioSegment.from_file(file_path)
            faster_song = change_speed(song, speed)
            base = os.path.splitext(file_path)[0]
            new_file = f"{base}_speed{speed:.2f}.{output_format}"
            faster_song.export(new_file, format=output_format)
        messagebox.showinfo("تم!", "تم تعديل الملفات وحفظها بنجاح.")
    except Exception as e:
        messagebox.showerror("خطأ", str(e))

def increase_speed():
    try:
        current = float(speed_var.get())
        speed_var.set(f"{current + 0.1:.2f}")
    except:
        speed_var.set("1.00")

def decrease_speed():
    try:
        current = float(speed_var.get())
        if current > 0.1:
            speed_var.set(f"{current - 0.1:.2f}")
    except:
        speed_var.set("1.00")

root = tk.Tk()
root.title("تغيير سرعة الملفات الصوتية")

tk.Label(root, text="اختر ملفات الصوت:").pack()
tk.Button(root, text="اختيار الملفات", command=select_files).pack()

file_list_var = tk.StringVar()
tk.Label(root, textvariable=file_list_var, wraplength=400, height=5, justify="left", anchor="w").pack()

speed_frame = tk.Frame(root)
speed_frame.pack()

tk.Label(speed_frame, text="السرعة:").pack(side=tk.LEFT)
speed_var = tk.StringVar(value="1.00")
speed_entry = tk.Entry(speed_frame, textvariable=speed_var, width=6, justify="center")
speed_entry.pack(side=tk.LEFT)
tk.Button(speed_frame, text="+", width=2, command=increase_speed).pack(side=tk.LEFT)
tk.Button(speed_frame, text="-", width=2, command=decrease_speed).pack(side=tk.LEFT)

tk.Label(root, text="0.5=بطيء | 1=عادي | 2=ضعف السرعة").pack()

# قائمة منسدلة لاختيار نوع الملف
format_frame = tk.Frame(root)
format_frame.pack()
tk.Label(format_frame, text="صيغة الإخراج:").pack(side=tk.LEFT)
format_var = tk.StringVar(value="mp3") # الافتراضي mp3
format_options = ["mp3", "wav", "ogg"]
tk.OptionMenu(format_frame, format_var, *format_options).pack(side=tk.LEFT)

tk.Button(root, text="تعديل و حفظ", command=process_files).pack()

root.mainloop()
