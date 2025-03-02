import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Button
from PIL import Image, ImageTk
import numpy as np
from tensorflow.keras.preprocessing import image  # Corrected import statement
from tensorflow.keras.models import load_model
import pickle

# Load the pre-trained model and class indices
model = load_model('C:\\Users\\pravin\\Desktop\\pro\\input\\model.h5')

with open('class_indices.pkl', 'rb') as f:
    class_indices = pickle.load(f)

dark_mode = False  # Initial dark mode state

# Define a function to make predictions using the loaded model
def predict_class(img_path):
    img = image.load_img(img_path, target_size=(150, 150))  # Corrected usage
    img = image.img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    predictions = model.predict(img)
    class_idx = np.argmax(predictions[0])
    return class_idx

# Function to handle image upload and prediction
def predict_and_display():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Predict the class
        predicted_class = predict_class(file_path)
        for i, j in enumerate(class_indices):
            if i == predicted_class:
                predicted_class_name = j

        # Create a prediction window
        prediction_window = tk.Toplevel(root)
        prediction_window.title("Prediction")

        # Load and display the uploaded image
        img = Image.open(file_path)
        img = img.resize((400, 400))  # Resize image for display
        img = ImageTk.PhotoImage(img)
        image_label = tk.Label(prediction_window, image=img)
        image_label.image = img
        image_label.pack()

        # Display the predicted class
        prediction_label = tk.Label(prediction_window, text="Predicted class: {}".format(predicted_class_name), font=("Arial", 16))
        prediction_label.pack()

# Toggle dark mode
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    update_dark_mode()

# Update GUI elements for dark mode
def update_dark_mode():
    if dark_mode:
        left_frame.config(bg="black")
        right_frame.config(bg="black")
        greeting_label.config(fg="white", bg="black")
        introduction_label.config(fg="white", bg="black")
        dark_mode_label.config(fg="red", bg="black")
    else:
        left_frame.config(bg="burlywood")
        right_frame.config(bg="white")
        greeting_label.config(fg="black", bg="burlywood")
        introduction_label.config(fg="black", bg="burlywood")
        dark_mode_label.config(fg="red", bg="white")
        dark_mode_label.config(text="Dark Mode: On" if dark_mode else "Dark Mode: Off")

# Function to display the "About" message
def display_about():
    about_window = tk.Toplevel(root)
    about_window.title("About Handwritten Character Recognition")
    about_label = tk.Label(about_window, text="Handwritten character recognition (HCR) is a system that can recognize and analyze human handwriting in any language. HCR can be performed on both online and offline handwriting.", font=("Arial", 12))
    about_label.pack(padx=20, pady=20)

# Create the main application window
root = tk.Tk()
root.title("WORDS WORLD")

# Set the window size
window_width = 800
window_height = 400
root.geometry(f"{window_width}x{window_height}")

# Create a frame to hold the content on the left side with burlywood background
left_frame = tk.Frame(root, bg="burlywood", width=window_width // 2)
left_frame.pack(expand=True, fill="both", side="left")

# Create a label for the greeting message
greeting_label = tk.Label(left_frame, text="Welcome to Handwritten Character Recognition", font=("Arial", 16, "bold"), fg="black", bg="burlywood")
greeting_label.pack(pady=20)

# Create an introduction label
introduction_label = tk.Label(left_frame, text="This application allows you to recognize handwritten characters.\nPlease upload an image to get started.", font=("Arial", 12), fg="black", bg="burlywood")
introduction_label.pack(pady=20)

# Create a frame for the right side with white background
right_frame = tk.Frame(root, bg="white", width=window_width // 2)
right_frame.pack(expand=True, fill="both", side="right")

# Create a curved box for buttons
curved_box = tk.LabelFrame(right_frame, text="Options", font=("Arial", 14), fg="black", bg="white", relief=tk.SUNKEN, bd=2)
curved_box.pack(expand=True, fill="both", padx=20, pady=20)

# Create upload button
upload_button = Button(curved_box, text="Upload Image", command=predict_and_display)
upload_button.pack(pady=10, fill="both")

# Create dark mode button
dark_mode_button = Button(curved_box, text="Dark Mode: Off", command=toggle_dark_mode)
dark_mode_button.pack(pady=10, fill="both")

dark_mode_label = tk.Label(right_frame, text="Dark Mode: Off", font=("Arial", 12, "bold"), fg="red", bg="white")
dark_mode_label.pack(pady=5)

# Create an About button
about_button = Button(curved_box, text="About", command=display_about)
about_button.pack(pady=10, fill="both")

# Run the main event loop
root.mainloop()
