import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk

# Для работы Drag and Drop: pip install tkinterdnd2
try:
    import tkinterdnd2 as tkdnd
except ImportError:
    print("Ошибка: Библиотека tkinterdnd2 не найдена. Установите её: pip install tkinterdnd2")

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor 640x640")
        
        # Общий размер окна
        self.root.geometry("1750x780")

        # Папка для поиска обработанных изображений
        self.processed_dir = "processed_data"
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

        # Настройка Drag-and-Drop
        self.root.drop_target_register(tkdnd.DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_drop)

        self._setup_ui()

    def _setup_ui(self):
        # --- Панель управления (Toolbar) ---
        toolbar = ttk.Frame(self.root, padding="10")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка выбора файла
        self.btn_load = ttk.Button(toolbar, text="Выбрать файл", command=self.load_file_dialog)
        self.btn_load.pack(side=tk.LEFT, padx=5)

        # НОВАЯ КНОПКА: Очистить
        self.btn_clear = ttk.Button(toolbar, text="Очистить данные", command=self.clear_data)
        self.btn_clear.pack(side=tk.LEFT, padx=5)
        
        hint_label = ttk.Label(toolbar, text="  <-- Можно перетащить файл прямо в окно", 
                              font=("Arial", 10, "italic"), foreground="gray")
        hint_label.pack(side=tk.LEFT, padx=20)

        # --- Основной контейнер ---
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 1. Окно исходного изображения
        self.frame_orig = self._create_fixed_frame(main_container, "Входное изображение (640x640)")
        self.label_orig = ttk.Label(self.frame_orig, text="ПЕРЕТАЩИТЕ ФАЙЛ", justify=tk.CENTER, font=("Arial", 12))
        self.label_orig.pack(expand=True)

        # 2. Окно обработанного изображения
        self.frame_proc = self._create_fixed_frame(main_container, "Результат обработки (640x640)")
        self.label_proc = ttk.Label(self.frame_proc, text="ОЖИДАНИЕ", justify=tk.CENTER, font=("Arial", 12))
        self.label_proc.pack(expand=True)

        # 3. Окно текста
        self.frame_text = ttk.LabelFrame(main_container, text="Инфо / Статус")
        self.frame_text.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)
        self.frame_text.pack_propagate(False)
        self.frame_text.config(width=400, height=640)
        
        self.text_area = tk.Text(self.frame_text, wrap=tk.WORD, font=("Consolas", 10), bg="#f4f4f4")
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _create_fixed_frame(self, parent, title):
        """Вспомогательный метод для создания рамок 640x640"""
        frame = ttk.LabelFrame(parent, text=title)
        frame.pack(side=tk.LEFT, padx=5, pady=5)
        frame.pack_propagate(False) 
        frame.config(width=640, height=640)
        return frame

    def clear_data(self):
        """Метод для полной очистки интерфейса"""
        # Сбрасываем первое окно
        self.label_orig.config(image='', text="ПЕРЕТАЩИТЕ ФАЙЛ")
        self.label_orig.image = None
        
        # Сбрасываем второе окно
        self.label_proc.config(image='', text="ОЖИДАНИЕ")
        self.label_proc.image = None
        
        # Очищаем текст
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", "Данные очищены. Готов к новой загрузке.")

    def handle_drop(self, event):
        """Обработка Drag-and-Drop"""
        files = self.root.tk.splitlist(event.data)
        if files:
            self.process_logic(files[0])

    def load_file_dialog(self):
        """Выбор файла через проводник"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp *.webp")]
        )
        if file_path:
            self.process_logic(file_path)

    def process_logic(self, input_path):
        """Загрузка оригинала и поиск обработанного фото"""
        filename = os.path.basename(input_path)
        processed_path = os.path.join(self.processed_dir, filename)

        # Выводим оригинал
        self._set_img(self.label_orig, input_path)

        # Чистим текст перед выводом нового статуса
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, f"Файл: {filename}\n")
        self.text_area.insert(tk.END, "-"*30 + "\n")

        # Проверка и вывод результата
        if os.path.exists(processed_path):
            self._set_img(self.label_proc, processed_path)
            self.text_area.insert(tk.END, "СТАТУС: Результат найден и отображен.\n")
        else:
            self.label_proc.config(image='', text="НЕТ РЕЗУЛЬТАТА")
            self.text_area.insert(tk.END, f"СТАТУС: Обработанная копия не найдена в папке '{self.processed_dir}'\n")

    def _set_img(self, label, path):
        """Загрузка картинки в 640x640"""
        try:
            img = Image.open(path)
            img = img.resize((640, 640), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label.config(image=photo, text="")
            label.image = photo 
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить: {path}\n{e}")

if __name__ == "__main__":
    root = tkdnd.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()