import tkinter as tk
from tkinter import scrolledtext, messagebox
from langdetect import detect
from deep_translator import GoogleTranslator
from nltk.corpus import wordnet
import nltk, string, pyttsx3, speech_recognition as sr

nltk.download('wordnet')
engine = pyttsx3.init()
engine.setProperty('rate', 150)
r = sr.Recognizer()

BG1, BG2 = "#5f2eea", "#b983ff"
BTN, TXT = "#7f5af0", "#ffffff"
translated = ""

def show(f): f.tkraise()

def speak():
    if translated:
        engine.say(translated); engine.runAndWait()

def voice_input():
    try:
        with sr.Microphone() as src:
            messagebox.showinfo("Voice Input", "Speak now...")
            audio = r.listen(src)
            text = r.recognize_google(audio)
            input_box.delete("1.0", tk.END)
            input_box.insert(tk.END, text)
    except:
        messagebox.showerror("Error", "Voice recognition failed")

def analyze():
    global translated
    text = input_box.get("1.0", tk.END).strip()
    if len(text.split()) < 3:
        messagebox.showwarning("Input Error", "Enter at least 3 words"); return
    try:
        lang = detect(text)
    except:
        messagebox.showerror("Error", "Language detection failed"); return

    names = {"en":"English","fr":"French","es":"Spanish","hi":"Hindi","de":"German","it":"Italian"}
    detected.config(text=f"Detected Language: {names.get(lang,'Unknown')}")

    translated = GoogleTranslator(source=lang, target="en").translate(text) if lang!="en" else text
    trans_lbl.config(text=f"Translated Text:\n{translated}")

    output.delete("1.0", tk.END)
    for w in [x.strip(string.punctuation).lower() for x in translated.split()]:
        s = wordnet.synsets(w)
        output.insert(tk.END, f"{w}: {s[0].definition() if s else 'Meaning not found'}\n")
    show(p3)

# ---------------- Window ----------------
root = tk.Tk()
root.title("Language Learning App")
root.geometry("900x650")
root.resizable(False, False)

container = tk.Frame(root)
container.pack(fill="both", expand=True)

# ---------------- Background Canvas ----------------
def bg(frame):
    c = tk.Canvas(frame, bg=BG1, highlightthickness=0)
    c.pack(fill="both", expand=True)
    c.create_oval(-100, -100, 300, 300, fill=BG2, outline="")
    c.create_oval(600, 100, 1000, 500, fill="#a06cd5", outline="")
    c.create_oval(200, 400, 700, 900, fill="#9d4edd", outline="")
    return c

# ---------------- Pages ----------------
p1, p2, p3 = [tk.Frame(container) for _ in range(3)]
for p in (p1, p2, p3): p.place(relwidth=1, relheight=1)

# ---------------- Page 1 ----------------
c1 = bg(p1)
c1.create_text(450, 140, text="Welcome 👋", fill=TXT, font=("Segoe UI",32,"bold"))
c1.create_text(450, 220, text="Translate • Listen • Learn Languages",
               fill=TXT, font=("Segoe UI",15))
tk.Button(p1, text="Get Started", bg=BTN, fg="white",
          font=("Segoe UI",12,"bold"), width=20,
          relief="flat", command=lambda: show(p2)).place(x=350, y=300)

# ---------------- Page 2 ----------------
c2 = bg(p2)
c2.create_text(450, 80, text="Enter Sentence", fill=TXT,
               font=("Segoe UI",24,"bold"))

input_box = scrolledtext.ScrolledText(p2, height=4, width=70, font=("Segoe UI",11))
input_box.place(x=140, y=140)

tk.Button(p2, text="🎤 Voice Input", bg="#3a0ca3", fg="white",
          font=("Segoe UI",10,"bold"), relief="flat",
          command=voice_input).place(x=250, y=240)

tk.Button(p2, text="Analyze", bg=BTN, fg="white",
          font=("Segoe UI",11,"bold"), width=15,
          relief="flat", command=analyze).place(x=400, y=240)

tk.Button(p2, text="← Back", bg=BG1, fg="white",
          border=0, command=lambda: show(p1)).place(x=20, y=20)

# ---------------- Page 3 ----------------
c3 = bg(p3)
c3.create_text(450, 60, text="Result", fill=TXT,
               font=("Segoe UI",24,"bold"))

detected = tk.Label(p3, text="Detected Language:",
                    bg=BG1, fg="white", font=("Segoe UI",11,"bold"))
detected.place(x=80, y=100)

trans_lbl = tk.Label(p3, text="Translated Text:",
                     bg=BG1, fg="white", font=("Segoe UI",11),
                     wraplength=740, justify="left")
trans_lbl.place(x=80, y=140)

output = scrolledtext.ScrolledText(p3, height=12, width=85, font=("Segoe UI",10))
output.place(x=80, y=200)

tk.Button(p3, text="🔊 Speak Translation", bg="#3a0ca3",
          fg="white", font=("Segoe UI",10,"bold"),
          width=20, relief="flat", command=speak).place(x=350, y=520)

tk.Button(p3, text="← Back", bg=BG1, fg="white",
          border=0, command=lambda: show(p2)).place(x=20, y=20)

show(p1)
root.mainloop()
