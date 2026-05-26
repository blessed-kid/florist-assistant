import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from ultralytics import YOLO
import tkinterdnd2 as tkdnd
import cv2
import os
import shutil

class App_for_assistant:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO Image Processor")
        self.root.geometry("1200x600")
        
        self.processed_dir = "processed_data"
        if os.path.exists(self.processed_dir):
            shutil.rmtree(self.processed_dir)
        os.makedirs(self.processed_dir)
        
        self.model = YOLO("C:/Users/admin/Documents/runs/detect/train36/weights/best.pt" )
        self.interface()

    def interface(self):
        btn_frame = ttk.Frame(self.root, padding=5)
        btn_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(btn_frame, text="Выбрать файл", command=self.input_block).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Очистить данные", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Информация", command=self.info).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Возможности ввода", command = self.input_info).pack(side = tk.RIGHT, padx=5)

        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        frame_orig = ttk.LabelFrame(main_frame, text="Исходное изображение")
        frame_orig.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.lbl_orig = ttk.Label(frame_orig, text="Перетащите фото сюда\n(Drag & Drop)")
        self.lbl_orig.pack(expand=True)

        frame_proc = ttk.LabelFrame(main_frame, text="Результат детекции")
        frame_proc.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.lbl_proc = ttk.Label(frame_proc, text="Здесь будет результат")
        self.lbl_proc.pack(expand=True)

        frame_text = ttk.LabelFrame(main_frame, text="Информация об объектах")
        frame_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.text_out = tk.Text(frame_text, width=30, wrap=tk.WORD, font=("Arial", 11))
        self.text_out.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.root.drop_target_register(tkdnd.DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.input_drop)

    def input_block(self):
        path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg *.jpeg")])
        if path:
            self.handle_input(path)

    def input_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        if files:
            path = files[0].strip('{}')
            if path.lower().endswith(('.jpg', '.jpeg')):
                self.handle_input(path)
            else:
                messagebox.showwarning("Формат", "Поддерживаются только .jpg файлы!")

    def handle_input(self, path):
        self.output_orig_photo(path)
        self.process_photo(path)

    def process_photo(self, input_path):
        filename = os.path.basename(input_path)
        output_path = os.path.join(self.processed_dir, filename)
        temp_path = os.path.join(self.processed_dir, "temp_step.jpg")

        img = cv2.imread(input_path)
        alpha = 1.5
        beta = 20
        filtered_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
        cv2.imwrite(temp_path, filtered_img)

        results = self.model(temp_path, conf=0.1)
        
        res_img_array = results[0].plot()
        res_img = Image.fromarray(res_img_array[..., ::-1])
        
        res_img.save(output_path)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)

        logs = [f"Файл: {filename}"]
        logs.append(f"Найдено объектов: {len(results[0].boxes)}")
        for box in results[0].boxes:
            name = self.model.names[int(box.cls[0])]
            logs.append(f"- {name}")

        self.output_results(res_img, logs)

    def output_orig_photo(self, path):
        img = Image.open(path)
        img.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(img)
        self.lbl_orig.config(image=photo, text="")
        self.lbl_orig.image = photo

    def output_results(self, proc_pil, logs):
        if proc_pil:
            proc_pil.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(proc_pil)
            self.lbl_proc.config(image=photo, text="")
            self.lbl_proc.image = photo
        
        self.text_out.delete("1.0", tk.END)
        self.text_out.insert(tk.END, "\n".join(logs))

    def clear_all(self):
        self.lbl_orig.config(image="", text="Перетащите фото сюда\n(Drag & Drop)")
        self.lbl_orig.image = None
        self.lbl_proc.config(image="", text="Здесь будет результат")
        self.lbl_proc.image = None
        self.text_out.delete("1.0", tk.END)

    def info(self):
        info_text = (
            "Данная программа является первонаперво исполненной\n"
            "и не несет за собой огромного функционала.\n\n"
            "На вход принимаются на данный момент только\n"
            "изображения с форматом .jpg, ждите обновления позже!"
        )
        messagebox.showinfo("Информация", info_text)
    def input_info(self):
        info_text = (
            "Форматами ввода являются:\n"
            "1.Перенос файлов с компьютера в окно приложения\n"
            "2.Выбор файлов, используя кнопку 'Выбрать файл'\n"
            "На вход принимаются на данный момент только изображения формата .jpg!\n"
            "В будущем добавим больше возможностей!"
        )
        messagebox.showinfo("Информация по вводу", info_text)


if __name__ == "__main__":
    root = tkdnd.Tk()
    app = App_for_assistant(root)
    root.mainloop()