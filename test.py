import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk


def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        file_label.configure(text=f"{file_path}")

def display_image():
    file_path = file_label.cget("text")  # ラベルからファイル名を取得
    if file_path:
        sub_window = tk.Toplevel(window)
        sub_window.title("画像表示")
        sub_window.geometry("400x400")
        image = Image.open(file_path)
        image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(sub_window, image=photo)
        image_label.pack(pady=10)
        image_label.image = photo

# Tkinterウィンドウの作成
window = tk.Tk()
window.title("画像表示アプリ")
window.geometry("400x400")

# ファイル名を表示するラベル
file_label = tk.Label(window, text="ファイルが選択されていません")
file_label.pack(pady=10)

# 画像を選択するためのボタン
open_button = tk.Button(window, text="画像を選択", command=open_image)
open_button.pack(pady=10)

# 画像を表示するためのボタン
display_button = tk.Button(window, text="画像を表示", command=display_image)
display_button.pack(pady=10)

# アプリケーションの実行
window.mainloop()
