import tkinter
import tkinter.filedialog

import cv2
import numpy as np
from PIL import Image, ImageTk


class CellConfluency:
    def __init__(self, image_path: str) -> None:
        self._image_path = image_path
        self._image_bgr = cv2.imread(image_path)

    @property
    def image_path(self):
        return self._image_path

    @property
    def image_bgr(self):
        return self._image_bgr

    def run(self):
        # BGR to RGB
        image_rgb = cv2.cvtColor(self._image_bgr, cv2.COLOR_BGR2RGB)

        # gray scale
        image_gray = cv2.cvtColor(self._image_bgr, cv2.COLOR_BGR2GRAY)

        # binarization using Otsu's method
        _, th = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # configure the kernel
        kernel = np.ones((3, 3), np.uint8)

        # morphological transformation(Opening -> Dilation)
        th = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=1)
        th = cv2.dilate(th, kernel, iterations=1)

        # contour extraction
        contours, _ = cv2.findContours(th, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        # draw the contours on the source image
        image_contour = cv2.drawContours(image_rgb.copy(), contours, -1, (0, 255, 0), 2)

        # total number of pixels
        whole_area = th.size

        # number of zero area pixels
        white_area = cv2.countNonZero(th)

        # calculate confluency
        confluency = white_area / whole_area * 100

        return confluency, image_contour, th


class Application(tkinter.Frame):
    def __init__(self, master=None) -> None:
        super().__init__(master)
        # ウィンドウの作成
        self.pack()
        self.master.title("細胞コンフルエンシー算出アプリ")
        self.master.iconbitmap("cell.ico")
        self.master.geometry("500x160")
        self.master.resizable(False, False)

        # フレームの作成
        self.input_frame = tkinter.Frame(self.master)
        self.filename_frame = tkinter.Frame(self.master)
        self.button_frame = tkinter.Frame(self.master)
        self.input_frame.pack()
        self.filename_frame.pack()
        self.button_frame.pack()

        # ファイル選択ボタン
        self.add_button = tkinter.Button(
            self.input_frame, text="ファイル選択", command=self.add_image
        )
        self.add_button.grid(pady=15)

        # ファイル名を表示するラベル
        self.file_label = tkinter.Label(self.filename_frame, text="ファイルが選択されていません")
        self.file_label.pack(pady=10)

        # 元画像と解析ボタン
        self.original_button = tkinter.Button(
            self.button_frame, text="元画像", command=self.display_original_image
        )
        self.analysis_button = tkinter.Button(
            self.button_frame, text="解析", command=self.display_results
        )
        self.original_button.grid(row=0, column=0, padx=5, pady=15, ipadx=5)
        self.analysis_button.grid(row=0, column=1, padx=5, pady=15, ipadx=5)

    # 画像を選択する関数
    def add_image(self):
        file_type = [
            ("Image files", "*.jpg; *.jpeg; *.png; *.tif; *.tiff")
        ]  # 画像ファイルを閲覧
        file_path = tkinter.filedialog.askopenfilename(filetypes=file_type)
        self.file_label.configure(text=f"{file_path}")

    # 元画像を表示する関数
    def display_original_image(self):
        file_path = self.file_label.cget("text")

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

    # 解析結果を表示する関数
    def display_results(self):
        file_path = self.file_label.cget("text")
        cc = CellConfluency(file_path)
        confluency, image_contour, _ = cc.run()

        # PillowのImageオブジェクトに変換
        image_contour = Image.fromarray(image_contour)
        w, h = image_contour.size
        photo = ImageTk.PhotoImage(image_contour)
        # サブウィンドウ
        result_window = tkinter.Toplevel(root)
        result_window.title("解析結果")
        result_window.geometry(f"{w}x{h+50}")

        # フレームの作成
        result_image_frame = tkinter.Frame(result_window)
        confluency_frame = tkinter.Frame(result_window)
        result_image_frame.pack()
        confluency_frame.pack()

        # 解析結果（画像）の表示
        image_label = tkinter.Label(result_image_frame, image=photo)
        image_label.pack()
        image_label.image = photo

        # 解析結果（コンフルエンシー）の表示
        confluency_label = tkinter.Label(
            confluency_frame, text=f"コンフルエンシー：{confluency:.1f}"
        )
        confluency_label.pack(pady=10)


if __name__ == "__main__":
    root = tkinter.Tk()
    app = Application(master=root)
    # ループ処理の実行
    root.mainloop()
