import tkinter as tk
import itertools
import hashlib
import time
from tkinter import filedialog



def generate_combinations(charset, minlength, maxlength):
    for length in range(minlength, maxlength + 1):
        for combination in itertools.product(charset, repeat=length):
            yield "".join(combination)


def crack_md5(hash, charset, minlength, maxlength):
    start_time = time.time()


    for password in generate_combinations(charset, minlength, maxlength):
        if hashlib.md5(password.encode()).hexdigest() == hash:
            end_time = time.time()
            elapsed_time = end_time - start_time
            result_text.set(f"Şifre Bulundu: {password}\nGeçen zaman: {elapsed_time:.2f} saniye")
            return


    end_time = time.time()
    elapsed_time = end_time - start_time
    result_text.set(f"Şifre Bulunamadı\nGeçen zaman: {elapsed_time:.2f} saniye")


def start_cracking():
    hash = hash_entry.get()
    charset = ""
    if include_lowercase.get():
        charset += "abcdefghijklmnopqrstuvwxyz"
    if include_uppercase.get():
        charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if include_digits.get():
        charset += "0123456789"
    if include_special.get():
        charset += "!@#$%^&*()_+-=[]{}|;':\,./<>?"
    minlength = int(minlength_entry.get())
    maxlength = int(maxlength_entry.get())
    crack_md5(hash, charset, minlength, maxlength)


def stop_loop():
    global loop_active
    loop_active = False


def start_comparison():
  global target_hash
  target_hash = hash_entry.get()
  with open("wordlist.txt", "r") as wordlist:
    for line in wordlist:
      hash = hashlib.md5(line.strip().encode("utf-8")).hexdigest()
      if hash == target_hash:
        result.delete(0, "end")
        result.insert(0, line.strip())
        break
    else:
      result.delete(0, "end")
      result.insert(0, "Eşleşen kelime bulunamadı.")


def open_file():
    filepath = filedialog.askopenfilename(initialdir=wentry.get())
    filename = filepath.split('/')[-1]

    if filename == "wordlist.txt":
        with open(filepath, 'r') as f:
            file_contents = f.read()
            result.delete(0, "end")
            result.insert(0, "wordlist.txt dosyasını seçtiniz")
            wentry.delete(0, "end")
            wentry.insert(0, filepath)
    else:
        result.delete(0, "end")
        result.insert(0, "Yanlış dosyayı seçtiniz. Lütfen wordlist.txt dosyasını seçin.")
        wentry.delete(0, "end")
        wentry.insert(0, filepath)



root = tk.Tk()
root.title("MD5 Şifre kırıcı")
root.geometry("990x600")
root.resizable(False, False)

label = tk.Label(root, text="Çözülmesini İstediğiniz Hash Kodunu Giriniz!", font="Calibri 18")
label.pack()

hash_entry = tk.Entry(root, font="Calibri 13", width=70, )
hash_entry.pack()


#Wordlist


wlist = tk.Label(root, text="Wordlist Kullan", font="Calibri 16", width= 20)
wlist.pack()
wlist.place(x=30, y=220)

wStart = tk.Button(root, text="Başla", font="Calibri 13", width=7, command=start_comparison)
wStart.pack()
wStart.place(x=100, y=480)

wlabel = tk.Label(root, text="Aşağıya Wordlist Yüklenecek konumu giriniz:", font="Calibri 12")
wlabel.pack()
wlabel.place(x=20, y=270)

wentry = tk.Entry(root, font="Calibri 10", width=34, )
wentry.pack()
wentry.place(x=20, y=310)


wbutton = tk.Button(root, text="Gözat ...", width=8, command=open_file)
wbutton.pack()
wbutton.place(x=270, y=307)


stop = tk.Button(root, text="Dur", font="Calibri 13", width=8, command=stop_loop)
stop.pack()
stop.place(x=450, y=480)


#Brute Force


bforce = tk.Label(root, text="Brute Force Kullan", font="Calibri 16", width= 70)
bforce.pack()
bforce.place(x=440, y=220)

bStart = tk.Button(root, text="Başla", font="Calibri 13", width=7, command=start_cracking)
bStart.pack()
bStart.place(x=780, y=480)

result_text = tk.StringVar()
result = tk.Entry(root, font="Calibri 15", justify="left", textvariable=result_text, )
result.place(x=345, y=200, width=300, height=170, anchor="nw")



include_lowercase = tk.BooleanVar()
lowercase = tk.Checkbutton(root, text="Küçük Harf (a)", font="Calibri 13", variable=include_lowercase)
lowercase.pack()
lowercase.place(x=672, y=260)

include_uppercase = tk.BooleanVar()
uppercase = tk.Checkbutton(root, text="Büyük Harf (A)", font="Calibri 13", variable=include_uppercase)
uppercase.pack()
uppercase.place(x=672, y=290)

include_digits = tk.BooleanVar()
digits = tk.Checkbutton(root, text="Rakam (1)", font="Calibri 13", variable=include_digits)
digits.pack()
digits.place(x=830, y=260)

include_special = tk.BooleanVar()
special = tk.Checkbutton(root, text="Özel Karakter (*) ", font="Calibri 13", variable=include_special)
special.pack()
special.place(x=830, y=290)

length = tk.Label(root, text="Taramak istediğiniz alanı belirtin", font="Calibri 13")
length.pack()
length.place(x=700, y=340)


minlength_entry = tk.Entry(root, width=7)
minlength_entry.pack()
minlength_entry.place(x=750, y=380)


maxlength_entry = tk.Entry(root, width=7)
maxlength_entry.pack()
maxlength_entry.place(x=840, y=380)


root.mainloop()