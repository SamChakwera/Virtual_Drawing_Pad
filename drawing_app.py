
import streamlit as st
import numpy as np
import cv2
from streamlit.components.v1 import declare_component
import base64
import io
from PIL import ImageFont, Image, ImageDraw
from tensorflow.keras.models import load_model

# Function to initialize the webcam
def initialize_webcam():
    cap = cv2.VideoCapture(0)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    return cap, width, height

# Function to load the model
def load_digit_model():
    return load_model("assets/hwd.h5")

# Function to preprocess the image
def preprocess_image(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img_gray, (21, 21), 0)
    _, img_binary = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY)
    return img_binary

# Function to predict the digit
def predict_digit(model, img):
    img = cv2.resize(img, (28,28), interpolation = cv2.INTER_AREA)
    img = np.array(img)
    img = img.reshape(1,28,28,1)
    img = img/255.0
    res = model.predict([img])[0]
    return np.argmax(res)

# Function to overlay fonts
def overlay_font(img, text, pos, color, width):
    fontsize = int(width*0.3)
    fontpath = "assets/SFProDisplay-Regular.ttf"
    font = ImageFont.truetype(fontpath, fontsize)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text(pos, text, font=font, fill=color, anchor="ls")
    return np.array(img_pil)


# Load the custom component for drawing canvas
DrawingCanvas = declare_component("drawing_canvas_component")

def main():
    st.title("Virtual Drawing Pad")

    # Sidebar for tools and options
    st.sidebar.header("Tools")
    clear_canvas = st.sidebar.button("Clear Canvas")

    # Use the custom component for drawing canvas
    canvas_result = DrawingCanvas()

    # If the canvas has data (user has drawn something)
    if canvas_result:
        # Convert dataURL to image
        header, encoded = canvas_result.split(",", 1)
        binary_data = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(binary_data))
        
        # Preprocess the image and predict the digit
        preprocessed_image = preprocess_image(np.array(image))
        try:
            digit_model = load_digit_model()
            predicted_digit = predict_digit(digit_model, preprocessed_image)
            st.subheader(f"Predicted Digit: {{predicted_digit}}")
        except:
            st.subheader("Model not available. Couldn't predict the digit.")

        # Display the drawn and preprocessed image
        col1, col2 = st.beta_columns(2)
        with col1:
            st.image(image, caption="Drawn Image", use_column_width=True)
        with col2:
            st.image(preprocessed_image, caption="Preprocessed Image", use_column_width=True, channels="GRAY")

if __name__ == "__main__":
    main()
