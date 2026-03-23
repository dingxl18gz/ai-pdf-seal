import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

import yaml

from src.pdf_processor import PdfSealProcessor


DEFAULT_CONFIG_FILE = "config.yaml"


class GuiLogHandler:
    def __init__(self, text_widget, level="INFO"):
        self.text_widget = text_widget
        self.level = level

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.insert(tk.END, msg)
        self.text_widget.see(tk.END)
        self.text_widget.update()

    def format(self, record):
        return f"[{record.levelname}] {record.getMessage()}\n"

    def flush(self):
        pass


class PdfSealGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI PDF Seal - 批量盖章工具")
        self.root.geometry("650x580")
        self.root.resizable(False, False)

        self.style_config()
        self.config = self.load_config()
        self.create_widgets()
        self.load_config_to_ui()

    def style_config(self):
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Microsoft YaHei", 12, "bold"))
        style.configure("Normal.TLabel", font=("Microsoft YaHei", 10))
        style.configure("TEntry", font=("Microsoft YaHei", 10))
        style.configure("TButton", font=("Microsoft YaHei", 10))
        style.configure("Accent.TButton", font=("Microsoft YaHei", 11, "bold"))

    def load_config(self):
        if os.path.exists(DEFAULT_CONFIG_FILE):
            with open(DEFAULT_CONFIG_FILE, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {
            'directory': '',
            'image': '',
            'width': 50,
            'height': 50,
            'x': 450,
            'y': 150,
            'force': False
        }

    def save_config(self):
        with open(DEFAULT_CONFIG_FILE, 'w', encoding='utf-8') as f:
            yaml.safe_dump(self.config, f, allow_unicode=True)

    def load_config_to_ui(self):
        self.dir_var.set(self.config.get('directory', ''))
        self.image_var.set(self.config.get('image', ''))
        self.width_var.set(self.config.get('width', 50))
        self.height_var.set(self.config.get('height', 50))
        self.x_var.set(self.config.get('x', 450))
        self.y_var.set(self.config.get('y', 150))
        self.force_var.set(self.config.get('force', False))

    def create_widgets(self):
        self.dir_var = tk.StringVar()
        self.image_var = tk.StringVar()
        self.width_var = tk.IntVar(value=50)
        self.height_var = tk.IntVar(value=50)
        self.x_var = tk.IntVar(value=450)
        self.y_var = tk.IntVar(value=150)
        self.force_var = tk.BooleanVar(value=False)

        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="AI PDF Seal - 批量盖章工具", style="Title.TLabel")
        title_label.pack(pady=(0, 15))

        config_frame = ttk.LabelFrame(main_frame, text="配置参数", padding="12")
        config_frame.pack(fill=tk.X, pady=(0, 12))

        row = 0
        ttk.Label(config_frame, text="目录选择:", style="Normal.TLabel").grid(row=row, column=0, sticky=tk.W, pady=8)
        ttk.Entry(config_frame, textvariable=self.dir_var, width=52).grid(row=row, column=1, padx=8, pady=8, sticky=(tk.W, tk.E))
        ttk.Button(config_frame, text="浏览", command=self.browse_directory, width=6).grid(row=row, column=2, pady=8, sticky=tk.W)

        row += 1
        ttk.Label(config_frame, text="印章图片:", style="Normal.TLabel").grid(row=row, column=0, sticky=tk.W, pady=8)
        ttk.Entry(config_frame, textvariable=self.image_var, width=52).grid(row=row, column=1, padx=8, pady=8, sticky=(tk.W, tk.E))
        ttk.Button(config_frame, text="浏览", command=self.browse_image, width=6).grid(row=row, column=2, pady=8, sticky=tk.W)

        row += 1
        size_frame = ttk.Frame(config_frame)
        size_frame.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=8, padx=98)

        ttk.Label(size_frame, text="印章尺寸:", style="Normal.TLabel").pack(side=tk.LEFT)
        ttk.Label(size_frame, text="宽度:").pack(side=tk.LEFT, padx=(15, 5))
        ttk.Entry(size_frame, textvariable=self.width_var, width=8).pack(side=tk.LEFT)
        ttk.Label(size_frame, text="像素").pack(side=tk.LEFT, padx=(5, 15))
        ttk.Label(size_frame, text="高度:").pack(side=tk.LEFT)
        ttk.Entry(size_frame, textvariable=self.height_var, width=8).pack(side=tk.LEFT)
        ttk.Label(size_frame, text="像素").pack(side=tk.LEFT, padx=(5, 0))

        row += 1
        pos_frame = ttk.Frame(config_frame)
        pos_frame.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=8, padx=98)

        ttk.Label(pos_frame, text="印章位置:", style="Normal.TLabel").pack(side=tk.LEFT)
        ttk.Label(pos_frame, text="X坐标:").pack(side=tk.LEFT, padx=(15, 5))
        ttk.Entry(pos_frame, textvariable=self.x_var, width=8).pack(side=tk.LEFT)
        ttk.Label(pos_frame, text="像素").pack(side=tk.LEFT, padx=(5, 15))
        ttk.Label(pos_frame, text="Y坐标:").pack(side=tk.LEFT)
        ttk.Entry(pos_frame, textvariable=self.y_var, width=8).pack(side=tk.LEFT)
        ttk.Label(pos_frame, text="像素").pack(side=tk.LEFT, padx=(5, 0))

        row += 1
        ttk.Checkbutton(config_frame, text="强制覆盖已盖章文件", variable=self.force_var,
                       command=self.on_config_change).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=10)

        row += 1
        self.run_button = ttk.Button(config_frame, text="立即执行", command=self.run_seal, style="Accent.TButton")
        self.run_button.grid(row=row, column=0, columnspan=3, pady=15, ipadx=40, ipady=8)

        log_frame = ttk.LabelFrame(main_frame, text="运行日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 0))

        self.log_text = tk.Text(log_frame, width=70, height=14, state='disabled',
                                font=("Consolas", 9), wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)

        self.dir_var.trace_add("write", lambda *args: self.on_config_change())
        self.image_var.trace_add("write", lambda *args: self.on_config_change())
        self.width_var.trace_add("write", lambda *args: self.on_config_change())
        self.height_var.trace_add("write", lambda *args: self.on_config_change())
        self.x_var.trace_add("write", lambda *args: self.on_config_change())
        self.y_var.trace_add("write", lambda *args: self.on_config_change())
        self.force_var.trace_add("write", lambda *args: self.on_config_change())

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_var.set(directory)

    def browse_image(self):
        image_file = filedialog.askopenfilename(
            title="选择印章图片",
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.bmp"), ("所有文件", "*.*")]
        )
        if image_file:
            self.image_var.set(image_file)

    def on_config_change(self, *args):
        self.config['directory'] = self.dir_var.get()
        self.config['image'] = self.image_var.get()
        self.config['width'] = self.width_var.get()
        self.config['height'] = self.height_var.get()
        self.config['x'] = self.x_var.get()
        self.config['y'] = self.y_var.get()
        self.config['force'] = self.force_var.get()
        self.save_config()

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def run_seal(self):
        directory = self.dir_var.get()
        image = self.image_var.get()
        width = self.width_var.get()
        height = self.height_var.get()
        x = self.x_var.get()
        y = self.y_var.get()
        force = self.force_var.get()

        if not directory:
            messagebox.showwarning("警告", "请选择目录")
            return
        if not image:
            messagebox.showwarning("警告", "请选择印章图片")
            return

        self.run_button.config(state='disabled')
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state='disabled')

        thread = threading.Thread(target=self._run_seal_thread, args=(directory, image, width, height, x, y, force))
        thread.start()

    def _run_seal_thread(self, directory, image, width, height, x, y, force):
        try:
            self.log("=" * 50)
            self.log("AI PDF Seal 开始运行")
            self.log("=" * 50)
            self.log(f"目录: {directory}")
            self.log(f"印章图片: {image}")
            self.log(f"印章尺寸: {width}x{height}")
            self.log(f"印章位置: ({x}, {y})")
            self.log(f"强制覆盖: {force}")
            self.log("=" * 50)

            pdf_files = []
            for filename in os.listdir(directory):
                if filename.lower().endswith('.pdf') and '_sealed' not in filename:
                    pdf_files.append(os.path.join(directory, filename))

            pdf_files = sorted(pdf_files)

            if not pdf_files:
                self.log("目录中没有需要处理的 PDF 文件")
                self.root.after(0, self.enable_button)
                return

            total = len(pdf_files)
            processed = 0
            skipped = 0
            failed = 0

            self.log(f"开始批量处理，共 {total} 个文件")

            for i, pdf_path in enumerate(pdf_files, 1):
                filename = os.path.basename(pdf_path)
                self.log(f"[{i}/{total}] 处理: {filename}")

                base, ext = os.path.splitext(pdf_path)
                sealed_path = f"{base}_sealed{ext}"

                if os.path.exists(sealed_path) and not force:
                    self.log(f"[{i}/{total}] 跳过: {filename} (已盖章)")
                    skipped += 1
                    continue

                try:
                    processor = PdfSealProcessor(
                        pdf_path=pdf_path,
                        image_path=image,
                        width=width,
                        height=height,
                        x=x,
                        y=y
                    )
                    processor.validate()
                    output_path = processor.process(sealed_path)
                    self.log(f"[{i}/{total}] 完成: {filename} -> {os.path.basename(output_path)}")
                    processed += 1
                except Exception as e:
                    self.log(f"[{i}/{total}] 失败: {filename}")
                    self.log(f"错误信息: {e}")
                    failed += 1

            self.log("=" * 50)
            self.log(f"处理完成！总计: {total}, 已处理: {processed}, 已跳过: {skipped}, 失败: {failed}")

            self.root.after(0, lambda: messagebox.showinfo("完成", f"处理完成！\n已处理: {processed}\n已跳过: {skipped}\n失败: {failed}"))

        except Exception as e:
            self.log(f"错误: {e}")
        finally:
            self.root.after(0, self.enable_button)

    def enable_button(self):
        self.run_button.config(state='normal')


def main():
    root = tk.Tk()
    app = PdfSealGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
