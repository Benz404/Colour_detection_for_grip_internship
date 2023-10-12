from PIL import Image
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from io import BytesIO
from IPython.display import display

from PIL import Image
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from io import BytesIO
from IPython.display import display
from google.colab import files

def get_image_colors(image_path):
    img = Image.open(image_path)
    img = img.convert("RGB")
    img_data = np.array(img)
    img_data = img_data.reshape(-1, 3)
    colors, counts = zip(*Counter(map(tuple, img_data)).most_common(10))
    return colors, counts

def display_image(image_path):
    img = Image.open(image_path)
    img = img.resize((500, 400), Image.ANTIALIAS)
    display(img)

def display_pie_chart(colors, counts):
    plt.pie(counts, colors=np.array(colors) / 255.0, autopct='%1.1f%%')
    plt.axis('equal')
    plt.show()

def get_color_at_pixel(image_path, x, y):
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixel = img.getpixel((x, y))
    return "#{:02x}{:02x}{:02x}".format(*pixel)

uploaded = files.upload()
for filename in uploaded.keys():
    image_path = filename
    colors, counts = get_image_colors(image_path)
    display_image(image_path)
    display_pie_chart(colors, counts)

    # Example: Get the color at pixel (100, 150)
    x, y = 100, 150
    color = get_color_at_pixel(image_path, x, y)
    print(f"Color at pixel ({x}, {y}): {color}")
