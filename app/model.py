import numpy as np
import cv2
import tensorflow as tf

IMG_SIZE = 128
ColorChannels = 3

class RaspberryPiViolenceDetection:
    def __init__(self, model_path):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def preprocess_image(self, image):
        image = cv2.imread(image)
        image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
        image = image / 255.0  # Normalize to [0,1]
        image = np.expand_dims(image, axis=0)  # Add batch dimension
        return image

    def detect_violence(self, image):
        input_data = self.preprocess_image(image)
        
        # Set the input tensor to the normalized image
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)

        # Run the inference
        self.interpreter.invoke()

        # Get the output tensor
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])

        # Assuming binary classification
        return "Violence detected!" if output_data[0][0] > 0.5 else "No violence detected"
