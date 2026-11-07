"""SMART CAMPUS AI • AI02 • desktop UI V6 for the existing CNN V5.

Uses the original cnn_utils.predict_image() without modifying its model,
checkpoint format, probabilities, or preprocessing. Python's tkinter/ttk only.
"""
from __future__ import annotations

import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageOps, ImageTk
from cnn_utils import LABELS, VI, available_models, predict_image

NAVY = '#102A39'
NAVY_LIGHT = '#173A4B'
TEAL = '#009E94'
TEAL_DARK = '#007E7A'
BG = '#F3F7F8'
WHITE = '#FFFFFF'
INK = '#153647'
MUTED = '#718895'
BORDER = '#DFE9EB'
LIGHT_TEAL = '#E5F8F3'
AMBER = '#A5640B'
AMBER_BG = '#FFF5DF'
LIGHT_PANEL = '#F8FBFB'

FONT = 'Segoe UI'


def font(size, weight='normal'):
    return (FONT, size, weight)


def label(parent, text, size=10, weight='normal', color=INK, bg=WHITE,
          **kwargs):
    return tk.Label(parent, text=text, font=font(size, weight), fg=color,
                    bg=bg, **kwargs)


def button(parent, text, command, primary=False):
    bg, hover = (TEAL, TEAL_DARK) if primary else (NAVY_LIGHT, NAVY)
    return tk.Button(parent, text=text, command=command,
                     bg=bg, fg=WHITE, activebackground=hover,
                     activeforeground=WHITE, font=font(10, 'bold'),
                     padx=19, pady=11, relief='flat', bd=0,
                     cursor='hand2', highlightthickness=0)


class ProbabilityChart(tk.Frame):
    """Six colored bars, with graphic width adjusting to resizing."""

    def __init__(self, master):
        super().__init__(master, bg=WHITE)
        self.rows = []
        for code in LABELS:
            line = tk.Frame(self, bg=WHITE)
            line.pack(fill='x', pady=5)
            label(line, VI[code], size=10, bg=WHITE, anchor='w', width=12).pack(side='left')
            amount = label(line, '0,0%', size=10, weight='bold', bg=WHITE,
                           color=MUTED, width=7, anchor='e')
            amount.pack(side='right')
            bar = tk.Canvas(line, height=14, bg=WHITE, highlightthickness=0,
                            bd=0)
            bar.pack(side='left', fill='x', expand=True, padx=(8, 14))
            self.rows.append((code, bar, amount))
            bar.bind('<Configure>', lambda _event: self.draw())
        self.probs = {code: 0.0 for code in LABELS}
        self.winner = None

    def set_values(self, probabilities, winner=None):
        self.probs = {code: max(0.0, min(1.0, float(probabilities.get(code, 0.0))))
                      for code in LABELS}
        self.winner = winner
        self.draw()

    def draw(self):
        for code, bar, amount in self.rows:
            value = self.probs[code]
            width = max(bar.winfo_width() - 2, 2)
            bar.delete('all')
            bar.create_rectangle(0, 2, width, 12, fill='#E9F0F1', outline='')
            fill_color = TEAL if code == self.winner else '#8ABCC0'
            if value:
                bar.create_rectangle(0, 2, max(2, width * value), 12,
                                     fill=fill_color, outline='')
            amount.configure(text=f'{value * 100:.1f}%'.replace('.', ','),
                             fg=TEAL_DARK if code == self.winner else MUTED)


class SmartCampusDesktop:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('SMART CAMPUS AI | AI02 - Phân loại rác thông minh')
        self.root.geometry('1280x820')
        self.root.minsize(1020, 690)
        self.root.configure(bg=BG)
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        try:
            self.root.tk.call('tk', 'scaling', 1.12)
        except tk.TclError:
            pass

        self.image_path = None
        self.pil_image = None
        self.photo = None
        self.model_dir = 'model'
        self.choices = []
        self.jobs = queue.Queue()
        self.job_version = 0
        self.processing = False
        self.alive = True
        self._preview_after = None

        style = ttk.Style(self.root)
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        style.configure('Smart.TCombobox', padding=8, borderwidth=1,
                        fieldbackground=WHITE, background=WHITE,
                        foreground=INK, font=font(10))

        self.build()
        self.load_model_choices()
        self.root.after(100, self.process_jobs)

    def build(self):
        shell = tk.Frame(self.root, bg=BG)
        shell.pack(fill='both', expand=True)
        self.sidebar = tk.Frame(shell, width=247, bg=NAVY)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)
        self.build_sidebar()

        self.main = tk.Frame(shell, bg=BG)
        self.main.pack(side='left', fill='both', expand=True)
        self.build_main()

    def build_sidebar(self):
        brand = tk.Frame(self.sidebar, bg=NAVY)
        brand.pack(fill='x', padx=23, pady=(30, 30))
        tk.Label(brand, text='✳', font=font(24, 'bold'), fg='#42D8C2',
                 bg=NAVY, width=2).pack(side='left', anchor='n')
        block = tk.Frame(brand, bg=NAVY)
        block.pack(side='left', padx=(9, 0))
        label(block, 'SMART CAMPUS', size=12, weight='bold', color=WHITE,
              bg=NAVY).pack(anchor='w')
        label(block, 'AI LAB · UNETI 2026', size=8, color='#8FC0CC',
              bg=NAVY).pack(anchor='w', pady=(5, 0))

        label(self.sidebar, 'KHÔNG GIAN LÀM VIỆC', size=8, weight='bold',
              color='#7BA7B7', bg=NAVY).pack(anchor='w', padx=25, pady=(7, 12))
        self.menu_button('▣   Phân loại hình ảnh', lambda: self.pick_image(), selected=True)
        self.menu_button('▤   Phương pháp & dữ liệu', self.show_model_info)
        self.menu_button('ⓘ   Hướng dẫn sử dụng', self.show_help)

        bottom = tk.Frame(self.sidebar, bg=NAVY_LIGHT, highlightthickness=0)
        bottom.pack(side='bottom', fill='x', padx=16, pady=(0, 23))
        label(bottom, '●  CHẠY NGOẠI TUYẾN', size=9, weight='bold',
              color='#65DBB6', bg=NAVY_LIGHT).pack(anchor='w', padx=15, pady=(12, 5))
        label(bottom, 'Dự đoán trực tiếp trên máy\nKhông gửi ảnh lên máy chủ',
              size=9, color='#C6D8DC', bg=NAVY_LIGHT,
              justify='left').pack(anchor='w', padx=15, pady=(0, 15))
        label(self.sidebar, 'OLYMPIC TRÍ TUỆ NHÂN TẠO\nUNETI 2026',
              size=9, weight='bold', color='#95C1CE', bg=NAVY,
              justify='left').pack(side='bottom', anchor='w', padx=23, pady=(0, 23))

    def menu_button(self, text, action, selected=False):
        bg = NAVY_LIGHT if selected else NAVY
        btn = tk.Button(self.sidebar, text=text, command=action,
                        bg=bg, fg='#60E5D5' if selected else '#CADDE3',
                        activebackground=NAVY_LIGHT, activeforeground=WHITE,
                        font=font(10, 'bold' if selected else 'normal'), bd=0,
                        relief='flat', padx=24, pady=14, anchor='w', cursor='hand2')
        btn.pack(fill='x', padx=14, pady=3)

    def build_main(self):
        head = tk.Frame(self.main, bg=BG)
        head.pack(fill='x', padx=26, pady=(21, 14))
        label(head, 'AI02  /  TRƯỜNG HỌC XANH', bg=BG,
              size=9, weight='bold', color=TEAL_DARK).pack(anchor='w')
        line = tk.Frame(head, bg=BG)
        line.pack(fill='x', pady=(5, 0))
        label(line, 'Nhận diện & phân loại rác thải', bg=BG,
              size=23, weight='bold', color=INK).pack(side='left')
        label(line, 'CNN V5  ·  UI V6', bg=LIGHT_TEAL,
              size=9, weight='bold', color=TEAL_DARK,
              padx=12, pady=8).pack(side='right')
        label(head, 'Chọn một ảnh vật thể để AI phân tích và gợi ý phân loại.',
              bg=BG, size=10, color=MUTED).pack(anchor='w', pady=(7, 0))

        toolbar = tk.Frame(self.main, bg=BG)
        toolbar.pack(fill='x', padx=26, pady=(0, 16))
        button(toolbar, 'CHỌN ẢNH', self.pick_image).pack(side='left', padx=(0, 9))
        self.analyze_button = button(toolbar, 'PHÂN TÍCH HÌNH ẢNH',
                                     self.analyze, primary=True)
        self.analyze_button.pack(side='left', padx=(0, 16))
        label(toolbar, 'Mô hình:', size=10, bg=BG, color=MUTED).pack(side='left')
        self.model_choice = tk.StringVar(value='Chưa có checkpoint CNN')
        self.model_box = ttk.Combobox(toolbar, textvariable=self.model_choice,
                                      width=31, state='readonly',
                                      style='Smart.TCombobox')
        self.model_box.pack(side='left', padx=(8, 8))
        tk.Button(toolbar, text='↻', bg=BG, fg=TEAL_DARK,
                  activebackground=LIGHT_TEAL, bd=0, font=font(16),
                  command=self.load_model_choices, cursor='hand2',
                  padx=8).pack(side='left')
        tk.Button(toolbar, text='THƯ MỤC MÔ HÌNH', bg=BG, fg=INK,
                  activebackground=LIGHT_TEAL, bd=0, font=font(9, 'bold'),
                  command=self.select_model_dir, cursor='hand2').pack(side='right')

        columns = tk.Frame(self.main, bg=BG)
        columns.pack(fill='both', expand=True, padx=26, pady=(0, 8))
        columns.grid_columnconfigure(0, weight=1, uniform='panel')
        columns.grid_columnconfigure(1, weight=1, uniform='panel')
        columns.grid_rowconfigure(0, weight=1)

        left = tk.Frame(columns, bg=WHITE, highlightbackground=BORDER,
                        highlightthickness=1)
        right = tk.Frame(columns, bg=WHITE, highlightbackground=BORDER,
                         highlightthickness=1)
        left.grid(row=0, column=0, sticky='nsew', padx=(0, 9))
        right.grid(row=0, column=1, sticky='nsew', padx=(9, 0))
        self.build_left_card(left)
        self.build_right_card(right)

        footer = tk.Frame(self.main, bg=BG)
        footer.pack(fill='x', padx=28, pady=(0, 13))
        self.status_text = tk.StringVar(value='Sẵn sàng. Chọn ảnh để bắt đầu.')
        label(footer, '●', size=11, color=TEAL, bg=BG).pack(side='left')
        tk.Label(footer, textvariable=self.status_text, font=font(9),
                 fg=MUTED, bg=BG, anchor='w').pack(side='left', padx=(7, 0))
        label(footer, 'KẾT QUẢ CHỈ MANG TÍNH THAM KHẢO', size=8,
              color=MUTED, bg=BG).pack(side='right')

    def card_heading(self, parent, number, title_text, sub):
        row = tk.Frame(parent, bg=WHITE)
        row.pack(fill='x', padx=20, pady=(20, 15))
        badge = tk.Label(row, text=number, bg=LIGHT_TEAL, fg=TEAL_DARK,
                         font=font(10, 'bold'), padx=12, pady=10)
        badge.pack(side='left', padx=(0, 12))
        col = tk.Frame(row, bg=WHITE)
        col.pack(side='left', fill='x', expand=True)
        label(col, title_text, size=13, weight='bold').pack(anchor='w')
        label(col, sub, size=9, color=MUTED).pack(anchor='w', pady=(4, 0))

    def build_left_card(self, parent):
        self.card_heading(parent, '01', 'Hình ảnh cần phân loại',
                          'Hỗ trợ JPG, PNG, WEBP, BMP')
        frame = tk.Frame(parent, bg=WHITE)
        frame.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        self.preview = tk.Canvas(frame, bg='#EDF5F5', highlightthickness=0,
                                  borderwidth=0, cursor='hand2')
        self.preview.pack(fill='both', expand=True)
        self.preview.bind('<Button-1>', lambda _event: self.pick_image())
        self.preview.bind('<Configure>', self.on_preview_resize)
        info = tk.Frame(parent, bg=WHITE)
        info.pack(fill='x', padx=21, pady=(6, 21))
        self.image_caption = tk.StringVar(value='Chưa chọn ảnh · Bấm vào khung để tải lên')
        tk.Label(info, textvariable=self.image_caption, bg=WHITE,
                 fg=MUTED, font=font(9), anchor='w',
                 wraplength=350).pack(side='left', fill='x', expand=True)
        tk.Button(info, text='ĐỔI ẢNH ↗', bg=LIGHT_TEAL, fg=TEAL_DARK,
                  font=font(9, 'bold'), bd=0, padx=10, pady=7,
                  command=self.pick_image, cursor='hand2').pack(side='right')

    def build_right_card(self, parent):
        self.card_heading(parent, '02', 'Kết quả nhận diện',
                          'Nhãn dự đoán và xác suất của sáu lớp')
        summary = tk.Frame(parent, bg=LIGHT_PANEL, highlightbackground='#ECF0F0',
                           highlightthickness=1)
        summary.pack(fill='x', padx=19, pady=(0, 13))
        self.result_name = tk.StringVar(value='Sẵn sàng phân tích')
        self.confidence = tk.StringVar(value='--,-%')
        label(summary, 'DỰ ĐOÁN CỦA HỆ THỐNG', size=9, weight='bold',
              bg=LIGHT_PANEL, color=MUTED).pack(anchor='w', padx=15, pady=(14, 4))
        self.name_label = tk.Label(summary, textvariable=self.result_name,
                                   bg=LIGHT_PANEL, fg=TEAL_DARK,
                                   font=font(22, 'bold'), anchor='w')
        self.name_label.pack(anchor='w', padx=15)
        bottom = tk.Frame(summary, bg=LIGHT_PANEL)
        bottom.pack(fill='x', padx=15, pady=(5, 13))
        label(bottom, 'Mức độ tin cậy tham khảo', size=9, bg=LIGHT_PANEL,
              color=MUTED).pack(side='left')
        tk.Label(bottom, textvariable=self.confidence, font=font(21, 'bold'),
                 bg=LIGHT_PANEL, fg=INK).pack(side='right')

        self.warning_text = tk.StringVar(value='')
        self.warning_box = tk.Label(parent, textvariable=self.warning_text,
                                    bg=AMBER_BG, fg=AMBER,
                                    font=font(9, 'bold'), justify='left',
                                    wraplength=410, padx=12, pady=10,
                                    anchor='w')
        self.warning_box.pack(fill='x', padx=19, pady=(0, 9))
        self.warning_box.pack_forget()

        label(parent, 'XÁC SUẤT 6 NHÓM RÁC', size=9, weight='bold',
              color=MUTED).pack(anchor='w', padx=20, pady=(6, 8))
        self.chart = ProbabilityChart(parent)
        self.chart.pack(fill='x', padx=20)
        divider = tk.Frame(parent, bg=BORDER, height=1)
        divider.pack(fill='x', padx=20, pady=(13, 12))
        label(parent, 'GỢI Ý PHÂN LOẠI', size=9,
              weight='bold', color=MUTED).pack(anchor='w', padx=20)
        self.guide = tk.StringVar(value='Chọn ảnh, chọn mô hình rồi nhấn “Phân tích hình ảnh”.')
        self.guide_label = tk.Label(parent, textvariable=self.guide,
                                    bg=WHITE, fg=INK, justify='left',
                                    font=font(10), anchor='nw', wraplength=390)
        self.guide_label.pack(fill='x', padx=20, pady=(8, 6))
        label(parent, 'Tên vật liệu không quyết định khả năng tái chế tại mọi địa phương.',
              size=8, color=MUTED, wraplength=400,
              justify='left').pack(anchor='w', padx=20, pady=(2, 12))
        parent.bind('<Configure>', lambda e: self._resize_right(e.width))

    def _resize_right(self, width):
        self.guide_label.configure(wraplength=max(220, width - 52))
        self.warning_box.configure(wraplength=max(220, width - 70))

    def on_preview_resize(self, _event=None):
        if self._preview_after is not None:
            self.root.after_cancel(self._preview_after)
        self._preview_after = self.root.after(75, self.render_preview)

    def render_preview(self):
        self._preview_after = None
        canvas = self.preview
        w = max(10, canvas.winfo_width())
        h = max(10, canvas.winfo_height())
        canvas.delete('all')
        canvas.create_rectangle(12, 12, w - 12, h - 12,
                                outline='#C9DBDF', dash=(4, 4), width=1)
        if self.pil_image is None:
            canvas.create_text(w / 2, h / 2 - 25, text='+',
                               fill='#7DC8BE', font=font(43, 'bold'))
            canvas.create_text(w / 2, h / 2 + 22,
                               text='Nhấp để chọn ảnh rác',
                               fill=INK, font=font(13, 'bold'))
            canvas.create_text(w / 2, h / 2 + 47,
                               text='Chọn một vật thể với nền đơn giản',
                               fill=MUTED, font=font(9))
            return
        preview = self.pil_image.copy()
        preview.thumbnail((max(1, w - 45), max(1, h - 45)), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(preview)
        canvas.create_image(w // 2, h // 2, image=self.photo)

    def pick_image(self):
        path = filedialog.askopenfilename(
            title='Chọn ảnh rác',
            filetypes=[('Tệp ảnh', '*.jpg *.jpeg *.png *.bmp *.webp'),
                       ('Tất cả tệp', '*.*')])
        if not path:
            return
        try:
            with Image.open(path) as img:
                loaded = ImageOps.exif_transpose(img).convert('RGB')
                loaded.thumbnail((1200, 1200))
            self.pil_image = loaded
            self.image_path = path
            self.job_version += 1
            self.processing = False
            self.analyze_button.configure(state='normal', text='PHÂN TÍCH HÌNH ẢNH')
            self.reset_results()
            self.image_caption.set(f'{Path(path).name}  ·  {loaded.width} × {loaded.height} px')
            self.status_text.set('Đã chọn ảnh. Nhấn PHÂN TÍCH HÌNH ẢNH để nhận diện.')
            self.render_preview()
        except Exception as exc:
            messagebox.showerror('Không mở được ảnh', str(exc))

    def reset_results(self):
        self.result_name.set('Sẵn sàng phân tích')
        self.confidence.set('--,-%')
        self.chart.set_values({}, None)
        self.warning_box.pack_forget()
        self.warning_text.set('')
        self.guide.set('Nhấn “Phân tích hình ảnh” để xem kết quả.')

    def load_model_choices(self):
        models = available_models(self.model_dir)
        new = []
        if len(models) > 1:
            new.append(('Kết hợp hai CNN', models))
        for path in models:
            name = 'MobileNetV3-Large' if 'mobilenet' in path.stem else 'EfficientNet-B0'
            new.append((name, [path]))
        self.choices = new
        self.model_box.configure(values=[name for name, _ in new])
        if new:
            self.model_choice.set(new[0][0])
            self.status_text.set(f'Đã tìm thấy {len(models)} mô hình CNN trong {self.model_dir}.')
        else:
            self.model_choice.set('Chưa có checkpoint CNN')
            self.status_text.set('Chưa có CNN .pth. Cần huấn luyện V5 hoặc chọn thư mục mô hình.')

    def select_model_dir(self):
        path = filedialog.askdirectory(title='Chọn thư mục chứa ai02_*.pth')
        if path:
            self.model_dir = path
            self.load_model_choices()

    def analyze(self):
        if not self.image_path:
            messagebox.showinfo('Chưa có ảnh', 'Hãy nhấn CHỌN ẢNH trước.')
            return
        if not self.choices:
            messagebox.showwarning('Thiếu mô hình CNN',
                'Chưa tìm thấy model/ai02_mobilenet_v3_large.pth.\n'
                'Bạn cần huấn luyện CNN V5 rồi mới có dự đoán thật.')
            return
        if self.processing:
            return
        selected = dict(self.choices).get(self.model_choice.get())
        if not selected:
            messagebox.showwarning('Chưa chọn mô hình', 'Hãy chọn một mô hình đã huấn luyện.')
            return
        self.processing = True
        self.job_version += 1
        version = self.job_version
        image_path = str(self.image_path)
        paths = tuple(str(p) for p in selected)
        self.analyze_button.configure(state='disabled', text='ĐANG PHÂN TÍCH...')
        self.status_text.set('CNN đang xử lý ảnh trên máy. Có thể mất lâu hơn trong lần đầu.')
        self.warning_box.pack_forget()

        def work():
            try:
                result = predict_image(image_path, paths)
                self.jobs.put((version, result, None))
            except Exception as exc:
                self.jobs.put((version, None, str(exc)))
        threading.Thread(target=work, daemon=True).start()

    def process_jobs(self):
        if not self.alive:
            return
        try:
            while True:
                version, result, error = self.jobs.get_nowait()
                if version != self.job_version:
                    continue
                self.processing = False
                self.analyze_button.configure(state='normal', text='PHÂN TÍCH HÌNH ẢNH')
                if error:
                    self.status_text.set('Không thể phân tích. Kiểm tra checkpoint / thư viện.')
                    messagebox.showerror('Lỗi dự đoán CNN', error)
                else:
                    self.show_result(result)
        except queue.Empty:
            pass
        self.root.after(100, self.process_jobs)

    def show_result(self, result):
        self.result_name.set(result['label_vi'].upper())
        self.confidence.set(f"{result['confidence'] * 100:.1f}%".replace('.', ','))
        self.chart.set_values(result['probabilities'], result['label'])
        self.guide.set(result['recommendation'])
        if result['uncertain']:
            self.warning_text.set('LƯU Ý  ·  ' + result['warning'])
            self.warning_box.pack(fill='x', padx=19, pady=(0, 9),
                                  after=self.name_label.master)
        else:
            self.warning_box.pack_forget()
        self.status_text.set('Đã hoàn thành · ' + ', '.join(result['architectures']) +
                             ' · Kết quả chỉ mang tính tham khảo.')

    def show_model_info(self):
        messagebox.showinfo('Phương pháp AI02',
            'Mã đề AI02 · Phân loại 6 nhóm rác TrashNet.\n\n'
            'Baseline: HOG + RGB + Logistic Regression.\n'
            'Cải tiến V4: HSV, LBP, Spatial RGB + SVM RBF.\n'
            'CNN V5: MobileNetV3-Large / EfficientNet-B0 fine-tuning.\n\n'
            'Cần so sánh Macro-F1 và ma trận nhầm lẫn trên cùng tập validation.')

    def show_help(self):
        messagebox.showinfo('Hướng dẫn sử dụng',
            '1. Huấn luyện CNN V5 để có file model/ai02_*.pth.\n'
            '2. Nhấn CHỌN ẢNH và chọn một tệp JPG/PNG/WEBP.\n'
            '3. Chọn mô hình (hoặc kết hợp hai CNN nếu đã có đủ).\n'
            '4. Nhấn PHÂN TÍCH HÌNH ẢNH.\n'
            '5. Xem nhãn, sáu xác suất, cảnh báo và gợi ý phân loại.\n\n'
            'Ứng dụng là nguyên mẫu học thuật, không bảo đảm đúng mọi ảnh.')

    def close(self):
        self.alive = False
        if self._preview_after:
            self.root.after_cancel(self._preview_after)
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    SmartCampusDesktop().run()
