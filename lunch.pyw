import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
from PIL import Image, ImageTk

# 런처에 등록할 프로그램 및 폴더
PROGRAMS = [
    {
        "name": "한강위젯",
        "icon": "hangang.png",
        "path": r"C:\Users\slave\업무 모음집 %내부파일 이동 금지%\develop 폴더\한강 물 온도 위젯\한강위젯.pyw",
        "type": "python"
    },
    {
        "name": "파일 일괄 삭제",
        "icon": "delete.png",
        "path": r"C:\Users\slave\업무 모음집 %내부파일 이동 금지%\develop 폴더\폴더내용삭제프로그램\파일 일괄 삭제.pyw",
        "type": "python"
    },
    {
        "name": "파일 통합 변환",
        "icon": "convert.png",
        "path": r"C:\Users\slave\업무 모음집 %내부파일 이동 금지%\develop 폴더\파일 통합 변환 프로그램\파일 통합 변환.pyw",
        "type": "python"
    },
    {
        "name": "개발 폴더 바로가기",
        "icon": "folder.png",
        "path": r"C:\Users\slave\업무 모음집 %내부파일 이동 금지%\develop 폴더",
        "type": "folder"
    },
]

COLORS = {
    "background": "#181820",
    "primary": "#FF4D00",
    "secondary": "#8A2BE2",
    "text": "#FFFFFF"
}

class Launcher:
    def __init__(self, root):
        self.root = root
        self.root.title("런처")
        self.root.geometry("800x600")
        self.root.configure(bg=COLORS["background"])
        self.icon_cache = {}
        self.create_widgets()

    def create_widgets(self):
        # 상단 타이틀
        header_frame = tk.Frame(self.root, bg=COLORS["background"])
        header_frame.pack(pady=30)
        title_label = tk.Label(
            header_frame, 
            text="Launcher", 
            font=("Impact", 32), 
            fg=COLORS["primary"], 
            bg=COLORS["background"]
        )
        title_label.pack()

        # 버튼 그리드
        grid_frame = tk.Frame(self.root, bg=COLORS["background"])
        grid_frame.pack(expand=True)

        for idx, app in enumerate(PROGRAMS):
            row, col = divmod(idx, 4)
            btn_frame = tk.Frame(grid_frame, bg=COLORS["background"], padx=20, pady=20)
            btn_frame.grid(row=row, column=col, padx=20, pady=20)
            icon_img = self.load_icon(app["icon"])
            btn = tk.Label(
                btn_frame, image=icon_img, bg=COLORS["background"], cursor="hand2"
            )
            btn.image = icon_img
            btn.pack()
            btn.bind("<Button-1>", lambda e, p=app: self.run_app(p))
            btn.bind("<Enter>", lambda e: e.widget.master.configure(bg=COLORS["secondary"]))
            btn.bind("<Leave>", lambda e: e.widget.master.configure(bg=COLORS["background"]))
            tk.Label(
                btn_frame, text=app["name"], font=("Arial", 12, "bold"),
                fg=COLORS["text"], bg=COLORS["background"]
            ).pack()

    def load_icon(self, filename):
        # images 폴더에 없으면 기본 사각형
        if filename in self.icon_cache:
            return self.icon_cache[filename]
        path = os.path.join("images", filename)
        if os.path.exists(path):
            img = Image.open(path).resize((80, 80))
            icon = ImageTk.PhotoImage(img)
        else:
            # 기본 사각형
            img = Image.new('RGB', (80, 80), color=COLORS["primary"])
            icon = ImageTk.PhotoImage(img)
        self.icon_cache[filename] = icon
        return icon

    def run_app(self, app):
        try:
            if app["type"] == "python":
                subprocess.Popen(['pythonw', app["path"]], shell=True)
            elif app["type"] == "folder":
                os.startfile(app["path"])
            else:
                subprocess.Popen(app["path"], shell=True)
            # 실행 시 시각적 피드백
            self.root.configure(bg="#FF0000")
            self.root.after(100, lambda: self.root.configure(bg=COLORS["background"]))
        except Exception as e:
            messagebox.showerror("실행 오류", f"실행 실패:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Launcher(root)
    root.mainloop()
