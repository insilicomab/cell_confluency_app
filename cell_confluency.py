import tkinter
import tkinter.filedialog

from PIL import Image, ImageTk


class CellConfluency:
    def __init__(self, image_path) -> None:
        self._image_path = image_path


# 画像を選択する関数
def add_image():
    file_type = [("Image files", "*.jpg; *.jpeg; *.png; *.tif; *.tiff")]  # 画像ファイルを閲覧
    file_path = tkinter.filedialog.askopenfilename(filetypes=file_type)
    file_label.configure(text=f"{file_path}")


# 元画像を表示する関数
def display_original_image():
    file_path = file_label.cget("text")
    print(file_path)
    # 画像の読み込みとサイズ情報の取得
    image = Image.open(file_path)
    w, h = image.size
    photo = ImageTk.PhotoImage(image)
    # サブウィンドウ
    original_image_window = tkinter.Toplevel(root)
    original_image_window.title("元画像")
    original_image_window.geometry(f"{w}x{h}")
    image_label = tkinter.Label(original_image_window, image=photo)
    image_label.pack()
    image_label.image = photo


if __name__ == "__main__":
    # ウィンドウの作成
    root = tkinter.Tk()
    root.title("細胞コンフルエンシー算出アプリ")
    root.iconbitmap("cell.ico")
    root.geometry("500x200")
    root.resizable(False, False)

    # フレームの作成
    input_frame = tkinter.Frame(root)
    filename_frame = tkinter.Frame(root)
    button_frame = tkinter.Frame(root)
    input_frame.pack()
    filename_frame.pack()
    button_frame.pack()

    # ファイル選択ボタン
    add_button = tkinter.Button(input_frame, text="ファイル選択", command=add_image)
    add_button.grid(pady=15)

    # ファイル名を表示するラベル
    file_label = tkinter.Label(filename_frame, text="ファイルが選択されていません")
    file_label.pack(pady=10)

    # 元画像と解析ボタン
    original_button = tkinter.Button(
        button_frame, text="元画像", command=display_original_image
    )
    analysis_button = tkinter.Button(button_frame, text="解析")
    original_button.grid(row=0, column=0, padx=5, pady=15, ipadx=5)
    analysis_button.grid(row=0, column=1, padx=5, pady=15, ipadx=5)

    # ループ処理の実行
    root.mainloop()
