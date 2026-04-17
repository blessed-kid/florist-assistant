import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from PIL import Image, ImageTk
import tkinterdnd2 as tkdnd

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Просмотр изображений")
        self.root.geometry("900x600")
        
        # Центрируем окно на экране
        self.center_window()
        
        # Создаем папку data если её нет
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Список для хранения путей к изображениям
        self.image_paths = [None, None, None]
        self.image_labels = []
        
        self.setup_ui()
        
    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        width = 900
        height = 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        # Настройка grid для центрирования содержимого
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Главный фрейм с центрированием
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Настройка grid для main_frame
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=0)
        main_frame.grid_rowconfigure(3, weight=0)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Настройка drag and drop
        self.root.drop_target_register(tkdnd.DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)
        
        # Фрейм для изображений
        images_frame = ttk.LabelFrame(main_frame, text="Изображения", padding="20")
        images_frame.grid(row=0, column=0, pady=(0, 10), sticky="nsew")
        
        # Настройка grid для images_frame
        images_frame.grid_columnconfigure(0, weight=1)
        images_frame.grid_columnconfigure(1, weight=1)
        images_frame.grid_columnconfigure(2, weight=1)
        images_frame.grid_rowconfigure(0, weight=1)
        
        # Создаем 3 места для изображений
        for i in range(3):
            # Контейнер для центрирования
            container = ttk.Frame(images_frame)
            container.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            
            # Настройка grid для контейнера
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)
            
            # Фрейм для каждого изображения
            frame = ttk.Frame(container, relief="solid", borderwidth=2)
            frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            
            # Настройка grid для frame
            frame.grid_rowconfigure(0, weight=0)
            frame.grid_rowconfigure(1, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            
            # Метка для номера изображения
            label = ttk.Label(frame, text=f"Изображение {i+1}", 
                            font=("Arial", 10, "bold"))
            label.grid(row=0, column=0, pady=5)
            
            # Метка для отображения изображения
            img_label = ttk.Label(frame, text="Нет изображения", 
                                 background="lightgray", anchor="center")
            img_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
            self.image_labels.append(img_label)
        
        # Фрейм для drag and drop
        drop_frame = ttk.LabelFrame(main_frame, text="Перетащите файлы сюда", padding="20")
        drop_frame.grid(row=1, column=0, pady=10, sticky="nsew")
        
        # Настройка grid для drop_frame
        drop_frame.grid_rowconfigure(0, weight=1)
        drop_frame.grid_columnconfigure(0, weight=1)
        
        drop_label = ttk.Label(drop_frame, 
                              text="Перетащите файлы изображений в эту область\n\nПоддерживаемые форматы: PNG, JPG, JPEG, GIF, BMP, TIFF",
                              background="#E1F0FF", padding="30", anchor="center", justify="center")
        drop_label.grid(row=0, column=0, sticky="nsew")
        
        # Кнопки с центрированием
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, pady=20)
        
        # Центрируем кнопки
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=0)
        buttons_frame.grid_columnconfigure(2, weight=0)
        buttons_frame.grid_columnconfigure(3, weight=0)
        buttons_frame.grid_columnconfigure(4, weight=1)
        
        load_button = ttk.Button(buttons_frame, text="Загрузить данные", 
                                command=self.load_images, width=20)
        load_button.grid(row=0, column=1, padx=5)
        
        info_button = ttk.Button(buttons_frame, text="Информация", 
                               command=self.show_info, width=15)
        info_button.grid(row=0, column=2, padx=5)
        
        clear_button = ttk.Button(buttons_frame, text="Очистить", 
                                command=self.clear_images, width=15)
        clear_button.grid(row=0, column=3, padx=5)
        
        # Статус бар
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W, padding=(5, 2))
        status_bar.grid(row=3, column=0, sticky="ew")
        
    def load_images(self):
        """Загрузка изображений через диалог выбора файлов"""
        file_paths = filedialog.askopenfilenames(
            title="Выберите изображения",
            filetypes=[
                ("Изображения", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("Все файлы", "*.*")
            ]
        )
        
        if file_paths:
            self.process_files(list(file_paths))
    
    def on_drop(self, event):
        """Обработка перетаскивания файлов"""
        files = self.root.tk.splitlist(event.data)
        self.process_files(files)
    
    def process_files(self, files):
        """Обработка списка файлов"""
        image_files = []
        
        # Фильтруем только файлы изображений
        for file_path in files:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                image_files.append(file_path)
        
        if not image_files:
            messagebox.showwarning("Предупреждение", "Выбранные файлы не являются изображениями!")
            return
        
        # Загружаем первые 3 изображения
        for i in range(min(3, len(image_files))):
            self.load_image_to_slot(i, image_files[i])
        
        # Сохраняем все изображения в папку data
        self.save_to_data_folder(image_files)
        
        self.status_var.set(f"Загружено {len(image_files)} изображений")
    
    def load_image_to_slot(self, slot_index, file_path):
        """Загрузка изображения в указанный слот"""
        try:
            # Открываем и изменяем размер изображения
            img = Image.open(file_path)
            
            # Получаем размеры области отображения
            label_width = self.image_labels[slot_index].winfo_width()
            label_height = self.image_labels[slot_index].winfo_height()
            
            # Если размеры не определены, используем стандартные
            if label_width <= 1:
                label_width = 200
            if label_height <= 1:
                label_height = 200
            
            # Масштабируем изображение
            img.thumbnail((label_width, label_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            # Обновляем метку
            self.image_labels[slot_index].configure(image=photo, text="")
            self.image_labels[slot_index].image = photo  # Сохраняем ссылку
            
            # Сохраняем путь к изображению
            self.image_paths[slot_index] = file_path
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {str(e)}")
    
    def save_to_data_folder(self, file_paths):
        """Сохранение файлов в папку data"""
        saved_count = 0
        for file_path in file_paths:
            try:
                filename = os.path.basename(file_path)
                dest_path = os.path.join(self.data_dir, filename)
                
                # Если файл уже существует, добавляем номер
                counter = 1
                base_name, ext = os.path.splitext(filename)
                while os.path.exists(dest_path):
                    new_name = f"{base_name}_{counter}{ext}"
                    dest_path = os.path.join(self.data_dir, new_name)
                    counter += 1
                
                shutil.copy2(file_path, dest_path)
                saved_count += 1
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении файла {filename}: {str(e)}")
        
        if saved_count > 0:
            self.status_var.set(f"Сохранено {saved_count} файлов в папку '{self.data_dir}'")
    
    def clear_images(self):
        """Очистка всех изображений"""
        for i in range(3):
            self.image_labels[i].configure(image="", text="Нет изображения")
            self.image_labels[i].image = None
            self.image_paths[i] = None
        
        self.status_var.set("Изображения очищены")
    
    def show_info(self):
        """Показ информационного окна"""
        info_window = tk.Toplevel(self.root)
        info_window.title("О приложении")
        info_window.geometry("450x350")
        
        # Центрируем информационное окно
        info_window.update_idletasks()
        x = info_window.winfo_screenwidth() // 2 - 225
        y = info_window.winfo_screenheight() // 2 - 175
        info_window.geometry(f"450x350+{x}+{y}")
        
        # Делаем окно модальным
        info_window.transient(self.root)
        info_window.grab_set()
        
        info_frame = ttk.Frame(info_window, padding="20")
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Центрируем содержимое
        info_frame.grid_rowconfigure(5, weight=1)
        info_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ttk.Label(info_frame, text="Просмотр изображений", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=10)
        
        version_label = ttk.Label(info_frame, text="Версия 1.0")
        version_label.grid(row=1, column=0)
        
        desc_label = ttk.Label(info_frame, text="Приложение для просмотра и управления изображениями",
                              wraplength=400, justify=tk.CENTER)
        desc_label.grid(row=2, column=0, pady=15)
        
        features_label = ttk.Label(info_frame, text="Возможности:",
                                 font=("Arial", 12, "bold"))
        features_label.grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        
        features_text = """• Отображение до 3 изображений одновременно
• Загрузка изображений через диалог выбора файлов
• Поддержка drag and drop
• Автоматическое сохранение в папку data
• Поддержка форматов: PNG, JPG, JPEG, GIF, BMP, TIFF"""
        
        features_display = ttk.Label(info_frame, text=features_text, 
                                    justify=tk.LEFT, wraplength=400)
        features_display.grid(row=4, column=0, sticky=tk.W, pady=5)
        
        close_button = ttk.Button(info_frame, text="Закрыть", 
                                 command=info_window.destroy, width=15)
        close_button.grid(row=5, column=0, pady=20)

