import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract

# Указание пути к исполняемому файлу Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Text Extractor")
        self.geometry("800x600")  # Увеличено для лучшего отображения

        # Создаем два рамочных виджета
        self.frame1 = tk.Frame(self, width=400, height=600, bg='grey')
        self.frame2 = tk.Frame(self, width=400, height=600, bg='white')
        self.frame1.pack(side="left", fill="both", expand=True)
        self.frame2.pack(side="right", fill="both", expand=True)

        self.label = tk.Label(self.frame1, text="Перетащите или вставьте картинку", bg='grey')
        self.label.pack(expand=True)

        # Кнопка для загрузки изображения
        self.upload_button = tk.Button(self.frame1, text="Загрузить изображение", command=self.upload_image)
        self.upload_button.pack(pady=20)

        # Текстовое поле для вывода распознанного текста
        self.text = tk.Text(self.frame2, wrap="word")
        self.text.pack(expand=True, fill='both')

        # Настройка обработчика вставки изображения
        self.bind("<Control-v>", self.paste_image)

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            self.display_image(image)

    def paste_image(self, event):
        try:
            # Пытаемся получить изображение из буфера обмена
            image = Image.open(filedialog.askopenfilename())
            self.display_image(image)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def display_image(self, image):
        photo = ImageTk.PhotoImage(image)
        self.label.config(image=photo)
        self.label.image = photo  # Сохраняем ссылку на изображение
        text = pytesseract.image_to_string(image)  # Распознавание текста
        self.text.delete(1.0, "end")
        self.text.insert("end", text)

if __name__ == "__main__":
    app = App()
    app.mainloop()
