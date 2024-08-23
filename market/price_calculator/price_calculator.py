# by Genabox (23/08/2024)
# if you want, say thanks ~ btc: 14CZG7Tp9vyHLxJoCi1FYKzgyjeG3BuPMe

import tkinter as tk
from tkinter import ttk
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw, ImageFont
import threading

class PercentageCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Percentage Calculator")
        self.root.geometry("900x500")
        
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.root, text="Order price:")
        self.label.pack(pady=10)

        self.entry = ttk.Entry(self.root, font=("Arial", 18))
        self.entry.pack(pady=10)
        self.entry.insert(0, "10")  # Default value for Current price
        self.entry.bind('<KeyRelease>', self.dynamic_update)

        self.percentage_label = ttk.Label(self.root, text="Select percentage:")
        self.percentage_label.pack(pady=10)

        self.slider = ttk.Scale(self.root, from_=0.01, to=25, orient="horizontal", command=self.update_result)
        self.slider.set(10)  # Default value set to 10%
        self.slider.pack(pady=10, fill='x', expand=True)

        # Adding scale markings below the slider
        self.scale_frame = tk.Frame(self.root)
        self.scale_frame.pack(fill='x')
        for i in range(6):
            label = ttk.Label(self.scale_frame, text=f"{i*5}%")
            label.place(x=i*(900/5)-10, y=0)  # Adjust the positions of the scale labels

        self.result_label = tk.Label(self.root, text="Current price: ", font=("Arial", 26))
        self.result_label.pack(pady=20)

        # Amount field
        self.amount_label = ttk.Label(self.root, text="Amount:")
        self.amount_label.pack(pady=10)

        self.amount_entry = ttk.Entry(self.root, font=("Arial", 18))
        self.amount_entry.pack(pady=10)
        self.amount_entry.bind('<KeyRelease>', self.dynamic_update)

        self.income_label = tk.Label(self.root, text="Income: ", font=("Arial", 18))
        self.income_label.pack(pady=10)

        self.max_percentage_label = ttk.Label(self.root, text="Set maximum percentage:")
        self.max_percentage_label.pack(pady=10)

        self.max_percentage_entry = ttk.Entry(self.root, font=("Arial", 18))
        self.max_percentage_entry.pack(pady=10)
        self.max_percentage_entry.insert(0, "25")  # Default value
        self.max_percentage_entry.bind('<KeyRelease>', self.update_slider)

        # Adding the footer
        self.footer_label = tk.Label(self.root, text="by Genabox https://github.com/genabox", font=("Arial", 8), anchor='e')
        self.footer_label.pack(side="bottom", anchor="se", padx=10, pady=5)

        # Trigger initial update to display default values
        self.update_result(10)

    def dynamic_update(self, event=None):
        self.update_result(self.slider.get())

    def update_result(self, value):
        try:
            order_price = self.convert_to_float(self.entry.get())
            amount = self.convert_to_float(self.amount_entry.get()) if self.amount_entry.get() else 1  # Default to 1 if empty
            percentage = float(value)
            percentage_value = order_price * (percentage / 100)
            current_price = order_price + percentage_value
            income = (current_price - order_price) * amount
            self.result_label.config(text=f"Current price: {current_price:.2f} ({percentage:.2f}%)")
            self.income_label.config(text=f"Income: {income:.4f}")
        except ValueError:
            self.result_label.config(text="Enter a valid number")
            self.income_label.config(text="Income: N/A")

    def update_slider(self, event=None):
        try:
            max_percentage = self.convert_to_float(self.max_percentage_entry.get())
            self.slider.config(to=max_percentage)
            self.update_result(self.slider.get())  # Update result based on new max percentage
        except ValueError:
            self.result_label.config(text="Enter a valid percentage")
            self.income_label.config(text="Income: N/A")

    def convert_to_float(self, value):
        try:
            # Replace commas with dots and convert to float
            return float(value.replace(',', '.'))
        except ValueError:
            raise ValueError("Invalid input format")

def create_image():
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (0, 128, 255))
    
    d = ImageDraw.Draw(image)
    
    # Gradient background
    for i in range(height):
        r = 0
        g = 128 + int(127 * (i / height))
        b = 255 - int(127 * (i / height))
        d.line([(0, i), (width, i)], fill=(r, g, b))
    
    # Text "Calc"
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

def hide_window():
    root.withdraw()

def create_tray_icon():
    image = create_image()
    menu = Menu(MenuItem('Open', show_window), MenuItem('Exit', on_quit))
    icon = Icon("Percentage Calculator", image, "Percentage Calculator", menu)
    threading.Thread(target=icon.run).start()
    return icon

if __name__ == "__main__":
    root = tk.Tk()
    app = PercentageCalculatorApp(root)

    root.protocol("WM_DELETE_WINDOW", hide_window)
    tray_icon = create_tray_icon()

    root.mainloop()

