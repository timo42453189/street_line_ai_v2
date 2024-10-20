import tensorflow as tf

class TensorflowModelTest:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)
    
    def predict(self, image):
        return self.model.predict(image)