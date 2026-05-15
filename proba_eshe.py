import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk, ImageFilter
import tkinterdnd2 as tkdnd

# Попытка импорта YOLO
try:
    from ultralytics import YOLO
except ImportError:
    YOLO = None

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO Image Processor 640x640")
        self.root.geometry("1750x800")

        self.processed_dir = "processed_data"
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

        # Загрузка модели
        self.model = YOLO("yolov8n.pt") if YOLO else None

        # Настройка Drag-and-Drop
        self.root.drop_target_register(tkdnd.DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_drop)

        self._setup_ui()

    def _setup_ui(self):
        """Создание интерфейса"""
        toolbar = ttk.Frame(self.root, padding="10")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(toolbar, text="Выбрать файл", command=self.load_file_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Очистить всё", command=self.clear_data).pack(side=tk.LEFT, padx=5)
        
        self.status_lbl = ttk.Label(toolbar, text="Готов к работе", foreground="green", font=("Arial", 10, "bold"))
        self.status_lbl.pack(side=tk.RIGHT, padx=20)

        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Три секции
        self.label_orig = self._create_image_window(main_container, "Вход (Original)")
        self.label_proc = self._create_image_window(main_container, "Выход (Filter + YOLO)")
        
        # Секция текста
        text_frame = ttk.LabelFrame(main_container, text="Лог обнаружения")
        text_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)
        text_frame.pack_propagate(False)
        text_frame.config(width=400, height=640)
        
        self.text_area = tk.Text(text_frame, wrap=tk.WORD, font=("Consolas", 10))
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _create_image_window(self, parent, title):
        frame = ttk.LabelFrame(parent, text=title)
        frame.pack(side=tk.LEFT, padx=5, pady=5)
        frame.pack_propagate(False)
        frame.config(width=640, height=640)
        
        label = ttk.Label(frame, text="ОЖИДАНИЕ")
        label.pack(expand=True)
        return label

    # --- 1. ФУНКЦИИ ПРИНЯТИЯ (INPUT) ---

    def handle_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        if files:
            self.on_file_received(files[0])

    def load_file_dialog(self):
        path = filedialog.askopenfilename()
        if path:
            self.on_file_received(path)

    def on_file_received(self, file_path):
        """Точка входа после того, как путь получен"""
        self.status_lbl.config(text="Обработка...", foreground="orange")
        self.root.update()
        
        # Запускаем логику
        result = self.execute_pipeline(file_path)
        
        # Передаем данные на вывод
        self.display_output(file_path, result['processed_path'], result['logs'])

    # --- 2. ФУНКЦИЯ ОБРАБОТКИ (PROCESSING) ---

    def execute_pipeline(self, input_path):
        """Вся математика и нейросеть здесь"""
        try:
            filename = os.path.basename(input_path)
            output_path = os.path.join(self.processed_dir, filename)
            logs = []

            # Этап фильтра
            img = Image.open(input_path)
            img = img.filter(ImageFilter.DETAIL)
            temp_path = "temp_step.jpg"
            img.save(temp_path)

            # Этап YOLO
            if self.model:
                results = self.model(temp_path, conf=0.25)
                res_img_array = results[0].plot()
                res_img = Image.fromarray(res_img_array[..., ::-1])
                res_img.save(output_path)
                
                logs.append(f"Файл: {filename}")
                logs.append(f"Найдено объектов: {len(results[0].boxes)}")
                for box in results[0].boxes:
                    name = self.model.names[int(box.cls[0])]
                    logs.append(f"- {name}")
            
            if os.path.exists(temp_path): os.remove(temp_path)
            return {'processed_path': output_path, 'logs': logs}

        except Exception as e:
            return {'processed_path': None, 'logs': [f"Ошибка: {str(e)}"]}

    # --- 3. ФУНКЦИИ ВЫВОДА (OUTPUT) ---

    def display_output(self, orig_path, proc_path, logs):
        """Только отрисовка данных в окнах"""
        # Вывод оригинального фото
        self._update_label_image(self.label_orig, orig_path)

        # Вывод обработанного фото
        if proc_path and os.path.exists(proc_path):
            self._update_label_image(self.label_proc, proc_path)
            self.status_lbl.config(text="Завершено", foreground="green")
        else:
            self.label_proc.config(image='', text="Ошибка обработки")
            self.status_lbl.config(text="Ошибка", foreground="red")

        # Вывод текста
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, "\n".join(logs))

    def _update_label_image(self, label, path):
        """Вспомогательный метод для рендеринга картинки"""
        try:
            img = Image.open(path)
            img = img.resize((640, 640), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label.config(image=photo, text="")
            label.image = photo
        except:
            label.config(image='', text="Ошибка файла")

    def clear_data(self):
        """Очистка всех полей вывода"""
        self.label_orig.config(image='', text="ОЖИДАНИЕ")
        self.label_proc.config(image='', text="ОЖИДАНИЕ")
        self.text_area.delete("1.0", tk.END)
        self.status_lbl.config(text="Очищено", foreground="blue")

if __name__ == "__main__":
    root = tkdnd.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()




