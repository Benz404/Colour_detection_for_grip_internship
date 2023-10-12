# Importing the required modules
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt

# Creating a full screen window with tkinter
root = tk.Tk()
root.title("Image Color Analyzer")
root.attributes('-fullscreen', True)

# Creating a frame to hold the image and the color preview
image_frame = tk.Frame(root, bg="white")
image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Creating a label to display the image
image_label = tk.Label(image_frame, bg="white")
image_label.pack(padx=10, pady=10)

# Creating a label to display the color preview
color_label = tk.Label(image_frame, bg="white", text="Click on the image to see the color", font=("Arial", 16))
color_label.pack(pady=10)

# Creating a frame to hold the pie chart and the button
chart_frame = tk.Frame(root, bg="white")
chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Creating a canvas to display the pie chart
chart_canvas = tk.Canvas(chart_frame, bg="white")
chart_canvas.pack(padx=10, pady=10)

# Creating a button to load an image
load_button = tk.Button(chart_frame, text="Load Image", font=("Arial", 16), command=lambda: load_image())
load_button.pack(pady=10)

# Defining a function to load an image
def load_image():
    # Asking the user to select an image file
    file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.jpg *.png *.bmp")])
    if file_path:
        # Opening the image file and resizing it to fit the label
        image = Image.open(file_path)
        width, height = image.size
        max_size = min(image_label.winfo_width(), image_label.winfo_height()) - 20
        if width > height:
            new_width = max_size
            new_height = int(max_size * height / width)
        else:
            new_height = max_size
            new_width = int(max_size * width / height)
        image = image.resize((new_width, new_height))

        # Converting the image to tkinter format and displaying it on the label
        photo = ImageTk.PhotoImage(image)
        image_label.image = photo # Keeping a reference to avoid garbage collection
        image_label.config(image=photo)

        # Converting the image to numpy array and getting the unique colors and their counts
        array = np.array(image)
        colors, counts = np.unique(array.reshape(-1, array.shape[-1]), axis=0, return_counts=True)

        # Sorting the colors by their counts in descending order
        sorted_indices = np.argsort(-counts)
        colors = colors[sorted_indices]
        counts = counts[sorted_indices]

        # Creating a pie chart of the main colors and displaying it on the canvas
        chart_canvas.delete("all") # Clearing the previous chart if any
        fig = plt.figure(figsize=(4, 4))
        plt.pie(counts[:10], labels=(["#" + "".join(hex(c)[2:].zfill(2) for c in color)] for color in colors[:10]))
        plt.title("Main colors in the image")
        chart_canvas.figure = fig # Keeping a reference to avoid garbage collection
        chart_canvas.draw_figure(fig) # Drawing the figure on the canvas

# Defining a function to get the color of a pixel when the mouse clicks on the image
def get_color(event):
    # Getting the coordinates of the mouse click relative to the image label
    x = event.x - image_label.winfo_x()
    y = event.y - image_label.winfo_y()

    # Checking if the mouse click is within the image bounds
    if 0 <= x < image_label.winfo_width() and 0 <= y < image_label.winfo_height():
        # Getting the color of the pixel at the mouse click position
        pixel = image_label.image.get(x, y)

        # Converting the color to hexadecimal format and displaying it on the color label
        hex_color = "#" + "".join(hex(c)[2:].zfill(2) for c in pixel)
        color_label.config(text=hex_color, bg=hex_color)

# Binding the mouse click event to the image label
image_label.bind("<Button-1>", get_color)

# Starting the main loop of tkinter
root.mainloop()