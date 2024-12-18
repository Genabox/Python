# by Genabox (23/08/2024)
import tkinter as tk
from tkinter import ttk
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw, ImageFont
import threading
import math

class PercentageCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Percentage Calculator")
        self.root.geometry("900x900")
        self.center_window()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        
        self.pnl_frame = ttk.Frame(self.notebook)
        self.mounts_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.pnl_frame, text='PnL Calculation')
        self.notebook.add(self.mounts_frame, text='Mounts Calculation')
        
        self.create_pnl_widgets(self.pnl_frame)
        self.create_mounts_widgets(self.mounts_frame)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_pnl_widgets(self, frame):
        self.label = ttk.Label(frame, text="Order price:")
        self.label.pack(pady=10)

        self.entry = ttk.Entry(frame, font=("Arial", 18))
        self.entry.pack(pady=10)
        self.entry.insert(0, "10")
        self.entry.bind('<KeyRelease>', self.dynamic_update)

        self.percentage_label = ttk.Label(frame, text="Select percentage:")
        self.percentage_label.pack(pady=10)

        # Обновляем диапазон ползунка от -250 до 250
        self.slider = ttk.Scale(frame, from_=-250, to=250, orient="horizontal", command=self.update_result)
        self.slider.set(0)  # Устанавливаем начальное значение посередине
        self.slider.pack(pady=10, fill='x', expand=True)

        self.scale_frame = tk.Frame(frame)
        self.scale_frame.pack(fill='x')
        for i in range(6):
            label = ttk.Label(self.scale_frame, text=f"{i*100-250}%")
            label.place(x=i*(900/5)-10, y=0)

        self.total_label = tk.Label(frame, text="Total: ", font=("Arial", 26))
        self.total_label.pack(pady=20)

        self.result_label = tk.Label(frame, text="Current price: ", font=("Arial", 26))
        self.result_label.pack(pady=10)

        self.amount_label = ttk.Label(frame, text="Amount:")
        self.amount_label.pack(pady=10)

        # Используем отдельное поле для Amount на первой вкладке
        self.pnl_amount_entry = ttk.Entry(frame, font=("Arial", 18))
        self.pnl_amount_entry.pack(pady=10)
        self.pnl_amount_entry.insert(0, "1")  # Добавляем начальное значение для Amount
        self.pnl_amount_entry.bind('<KeyRelease>', self.dynamic_update)

        # Убеждаемся, что Order value и income_label обновляются
        self.order_value_label = tk.Label(frame, text="Order value: ", font=("Arial", 18))
        self.order_value_label.pack(pady=10)

        self.income_label = tk.Label(frame, text="Income: ", font=("Arial", 18))
        self.income_label.pack(pady=10)

        self.max_percentage_label = ttk.Label(frame, text="Set maximum percentage:")
        self.max_percentage_label.pack(pady=10)

        self.max_percentage_entry = ttk.Entry(frame, font=("Arial", 18))
        self.max_percentage_entry.pack(pady=10)
        self.max_percentage_entry.insert(0, "250")
        self.max_percentage_entry.bind('<KeyRelease>', self.update_slider)

        self.footer_label = tk.Label(frame, text="by Genabox https://github.com/genabox", font=("Arial", 8), anchor='e')
        self.footer_label.pack(side="bottom", anchor="se", padx=10, pady=5)

        self.update_result(0)  # Обновляем результат при инициализации

    def create_mounts_widgets(self, frame):
        self.initial_deposit_label = ttk.Label(frame, text="Initial deposit:")
        self.initial_deposit_label.pack(pady=10)

        self.initial_deposit_entry = ttk.Entry(frame, font=("Arial", 18))
        self.initial_deposit_entry.pack(pady=10)
        self.initial_deposit_entry.insert(0, "15.0")

        self.growth_rates_label = ttk.Label(frame, text="Growth rates (comma-separated):")
        self.growth_rates_label.pack(pady=10)

        self.growth_rates_entry = ttk.Entry(frame, font=("Arial", 18))
        self.growth_rates_entry.pack(pady=10)
        self.growth_rates_entry.insert(0, "55.0, 355.0")

        self.target_amount_label = ttk.Label(frame, text="Target amount:")
        self.target_amount_label.pack(pady=10)

        self.target_amount_entry = ttk.Entry(frame, font=("Arial", 18))
        self.target_amount_entry.pack(pady=10)
        self.target_amount_entry.insert(0, "10000.0")

        self.calculate_button = ttk.Button(frame, text="Calculate", command=self.calculate_growth)
        self.calculate_button.pack(pady=20)

        # Добавляем кнопку "Copy result" перед полем результата
        self.copy_button = ttk.Button(frame, text="Copy result", command=self.copy_result)
        self.copy_button.pack(pady=10)

        self.result_label_mounts = ttk.Label(frame, text="Result will be shown here", font=("Arial", 18))
        self.result_label_mounts.pack(pady=20)

        # Создаем контейнер для текста с полосой прокрутки
        self.report_frame = tk.Frame(frame)
        self.report_frame.pack(pady=10, fill='both', expand=True)

        self.report_text = tk.Text(self.report_frame, height=10, font=("Arial", 12), wrap='none')
        self.report_text.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.report_frame, command=self.report_text.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.report_text.config(yscrollcommand=self.scrollbar.set)
        self.report_text.bind("<Control-c>", lambda event: self.root.clipboard_append(self.report_text.selection_get()))

    def calculate_growth(self):
        try:
            initial_deposit = self.convert_to_float(self.initial_deposit_entry.get())
            growth_rates = [self.convert_to_float(rate) for rate in self.growth_rates_entry.get().split(",")]
            target_amount = self.convert_to_float(self.target_amount_entry.get())

            average_growth_rate = self.calculate_average_rate(growth_rates)
            months_needed, report = self.perform_calculation(initial_deposit, average_growth_rate, target_amount)

            self.result_label_mounts.config(text=f"Months needed: {months_needed}")
            self.report_text.delete(1.0, tk.END)

            # Выводим вводные данные в текстовый контейнер
            input_data = (
                f"Initial deposit: {initial_deposit}\n"
                f"Growth rates: {growth_rates}\n"
                f"Target amount: {target_amount}\n"
                f"Months needed: {months_needed}\n\n"
            )
            self.report_text.insert(tk.END, input_data)

            report_lines = [
                "Month | Balance (dollars) | Income per month (dollars)",
                "-" * 40,
            ]
            for month, balance, income in report:
                report_lines.append(f"{month:5} | {balance:18,.2f} | {income:21,.2f}")
            
            self.report_text.insert(tk.END, "\n".join(report_lines))
        except ValueError:
            self.result_label_mounts.config(text="Invalid input. Please enter valid numbers.")

    def calculate_average_rate(self, rates):
        return sum(rates) / len(rates)

    def perform_calculation(self, initial_deposit, average_growth_rate, target_amount):
        r = average_growth_rate / 100.0
        balance = initial_deposit
        month = 0
        monthly_report = []

        while balance < target_amount:
            month += 1
            income = balance * r
            balance += income
            monthly_report.append((month, balance, income))

        return month, monthly_report

    def copy_result(self):
        # Копируем текст из контейнера с результатом в буфер обмена
        result_text = self.report_text.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(result_text)
        self.root.update()  # Обновляем буфер обмена

    def dynamic_update(self, event=None):
        if hasattr(self, 'result_label'):
            self.update_result(self.slider.get())

    def update_result(self, value):
        try:
            if hasattr(self, 'result_label'):
                order_price = self.convert_to_float(self.entry.get())
                amount = self.convert_to_float(self.pnl_amount_entry.get()) if hasattr(self, 'pnl_amount_entry') and self.pnl_amount_entry.get() else 1
                percentage = float(value)
                percentage_value = order_price * (percentage / 100)
                current_price = order_price + percentage_value
                total = order_price * amount
                income = (current_price - order_price) * amount
                order_value = total + income

                self.total_label.config(text=f"Total: {total:.5f}")

                if current_price >= order_price:
                    self.result_label.config(text=f"Current price: {current_price:.5f} ({percentage:.2f}%)", fg="green")
                else:
                    self.result_label.config(text=f"Current price: {current_price:.5f} ({percentage:.2f}%)", fg="red")
                
                self.income_label.config(text=f"Income: {income:.4f}")  # Обновляем income_label
                self.order_value_label.config(text=f"Order value: {order_value:.5f}")  # Обновляем order_value_label
        except ValueError:
            if hasattr(self, 'result_label'):
                self.result_label.config(text="Enter a valid number")
            if hasattr(self, 'income_label'):
                self.income_label.config(text="Income: N/A")
            if hasattr(self, 'order_value_label'):
                self.order_value_label.config(text="Order value: N/A")

    def update_slider(self, event=None):
        try:
            max_percentage = self.convert_to_float(self.max_percentage_entry.get())
            self.slider.config(to=max_percentage, from_=-max_percentage)
            self.update_result(self.slider.get())
        except ValueError:
            if hasattr(self, 'result_label'):
                self.result_label.config(text="Enter a valid percentage")
            if hasattr(self, 'income_label'):
                self.income_label.config(text="Income: N/A")
            if hasattr(self, 'order_value_label'):
                self.order_value_label.config(text="Order value: N/A")

    def convert_to_float(self, value):
        try:
            # Убираем все пробелы, чтобы избежать ошибки
            value = value.replace(" ", "")
            # Заменяем запятые на точки для единообразия
            value = value.replace(",", ".")
            # Преобразуем строку в число с плавающей точкой
            return float(value)
        except ValueError:
            raise ValueError("Invalid input format")

def create_image():
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (0, 128, 255))
    
    d = ImageDraw.Draw(image)
    
    for i in range(height):
        r = 0
        g = 128 + int(127 * (i / height))
        b = 255 - int(127 * (i / height))
        d.line([(0, i), (width, i)], fill=(r, g, b))
    
    text = "Calc"
    font_size = 20
    font = ImageFont.truetype("arial.ttf", font_size)
    
    text_bbox = d.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_position = ((width - text_width) // 2, (height - text_height) // 2)
    
    d.text(text_position, text, fill="white", font=font)
    
    return image

def on_quit(icon, item):
    icon.stop()
    root.quit()

def show_window(icon, item):
    root.after(0, root.deiconify)

def on_double_click(icon, item):
    root.after(0, root.deiconify)

def hide_window():
    root.withdraw()

def create_tray_icon():
    image = create_image()
    menu = Menu(MenuItem('Open', show_window), MenuItem('Exit', on_quit))
    icon = Icon("Percentage Calculator", image, "Percentage Calculator", menu)

    icon.default_action = on_double_click
    threading.Thread(target=icon.run).start()
    return icon

if __name__ == "__main__":
    root = tk.Tk()
    app = PercentageCalculatorApp(root)

    root.protocol("WM_DELETE_WINDOW", hide_window)
    tray_icon = create_tray_icon()

    root.mainloop()


