import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk
# Необходима библиотека: pip install tkinterdnd2
import tkinterdnd2 as tkdnd

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor 640x640")
        self.root.geometry("1750x750")

        # Папка, где программа будет искать обработанные фото
        self.processed_dir = "processed_data" 
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

        # Регистрация Drag and Drop
        self.root.drop_target_register(tkdnd.DND_FILES)
        self.root.dnd_bind('«Drop»', self.on_drop)

        self._setup_ui()

    def _setup_ui(self):
        # Панель управления
        toolbar = ttk.Frame(self.root, padding="10")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(toolbar, text="Выбрать файл", command=self.load_file_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Label(toolbar, text="Перетащите файл в ЛЮБОЕ место окна", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=20)

        # Контейнер для окон
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 1. Окно исходного фото
        self.frame_orig = self._create_image_frame(main_container, "Исходное (640x640)")
        self.label_orig = ttk.Label(self.frame_orig, text="Место для оригинала")
        self.label_orig.pack(expand=True)

        # 2. Окно обработанного фото
        self.frame_proc = self._create_image_frame(main_container, "Результат (640x640)")
        self.label_proc = ttk.Label(self.frame_proc, text="Место для результата")
        self.label_proc.pack(expand=True)

        # 3. Окно текста
        self.frame_text = ttk.LabelFrame(main_container, text="Статус")
        self.frame_text.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)
        self.frame_text.pack_propagate(False)
        self.frame_text.config(width=400, height=640)
        
        self.text_area = tk.Text(self.frame_text, wrap=tk.WORD, font=("Arial", 11))
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _create_image_frame(self, parent, title):
        frame = ttk.LabelFrame(parent, text=title)
        frame.pack(side=tk.LEFT, padx=5, pady=5)
        frame.pack_propagate(False)
        frame.config(width=640, height=640)
        return frame

    def on_drop(self, event):
        # Исправляем проблему путей с пробелами (убираем скобки)
        raw_path = event.data
        if raw_path.startswith('{') and raw_path.endswith('}'):
            path = raw_path[1:-1]
        else:
            path = raw_path
            
        if os.path.isfile(path):
            self.process_files(path)

    def load_file_dialog(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            self.process_files(path)

    def process_files(self, input_path):
        """Отображает входное фото и ищет обработанное с тем же именем"""
        filename = os.path.basename(input_path)
        # Путь к обработанному файлу в специальной папке
        processed_path = os.path.join(self.processed_dir, filename)

        # 1. Загружаем оригинал
        self._set_img(self.label_orig, input_path)

        # 2. Проверяем наличие обработанного файла
        if os.path.exists(processed_path):
            self._set_img(self.label_proc, processed_path)
            status = f"Успех!\nОригинал: {filename}\nРезультат найден в {self.processed_dir}"
        else:
            # Если файла нет, очищаем окно результата
            self.label_proc.config(image='', text="Файл результата не найден")
            status = f"Файл {filename} загружен.\n\nВНИМАНИЕ: Обработанный файл не найден по пути:\n{processed_path}"

        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", status)

    def _set_img(self, label, path):
        try:
            img = Image.open(path)
            img = img.resize((640, 640), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label.config(image=photo, text="")
            label.image = photo
        except Exception as e:
            label.config(text=f"Ошибка: {e}", image='')

if __name__ == "__main__":
    # Критично: используем tkdnd.Tk() вместо tk.Tk()
    root = tkdnd.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()