# Shantanu Barua, S377141
# https://github.com/Shantanu-Barua/hit137_assignment3.git

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import tensorflow as tf
import numpy as np

# Helper function to load and preprocess images 
def preprocess_image(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

# Base class for Tkinter interface 
class BaseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Image Classifier")
        self.geometry("400x400")
        self._model = None  #  Hide AI model 

    def load_model(self, model_path):
        #  model loading 
        self._model = tf.keras.models.load_model(model_path)
        messagebox.showinfo("Info", "AI Model Loaded Successfully")

    def classify_image(self, image_path):
        if self._model is None:
            messagebox.showerror("Error", "No model loaded!")
            return
        img = preprocess_image(image_path)
        predictions = self._model.predict(img)
        class_idx = np.argmax(predictions)
        return class_idx

# Polymorphism: changing how a button behaves for each specific app
class ImageClassifierApp(BaseApp):
    def __init__(self):
        super().__init__()
        self.label = tk.Label(self, text="Upload an Image")
        self.label.pack(pady=20)

        self.upload_btn = tk.Button(self, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack(pady=10)

        self.classify_btn = tk.Button(self, text="Classify Image", command=self.classify_image_button)
        self.classify_btn.pack(pady=10)

        self.image_path = None
        self.image_label = None

    def upload_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            img = Image.open(self.image_path)
            img.thumbnail((200, 200))
            img = ImageTk.PhotoImage(img)

            if self.image_label is not None:
                self.image_label.destroy()

            self.image_label = tk.Label(self, image=img)
            self.image_label.image = img  # Keep reference to avoid garbage collection
            self.image_label.pack(pady=20)

    # Providing a specific implementation
    def classify_image_button(self):
        if self.image_path:
            class_idx = self.classify_image(self.image_path)
            messagebox.showinfo("Classification Result", f"Predicted Class: {class_idx}")
        else:
            messagebox.showwarning("Warning", "No image uploaded!")

#  adding decorator functionality
class DecoratorMixin:
    def __init__(self):
        pass

    @staticmethod
    def decorator_function(func):
        def wrapper(*args, **kwargs):
            print("Before function execution")
            result = func(*args, **kwargs)
            print("After function execution")
            return result
        return wrapper

class AdvancedImageClassifierApp(ImageClassifierApp, DecoratorMixin):
    def __init__(self):
        ImageClassifierApp.__init__(self)
        DecoratorMixin.__init__(self)

    @DecoratorMixin.decorator_function
    def classify_image_button(self):
        super().classify_image_button()  # Calling the original method

if __name__ == "__main__":
    app = AdvancedImageClassifierApp()
    app.load_model("mobilenet_v2.h5")  # the model is created as 'mobilenet_v2.h5' by running file mobilenet.py
    app.mainloop()


# https://github.com/Shantanu-Barua/hit137_assignment3.git