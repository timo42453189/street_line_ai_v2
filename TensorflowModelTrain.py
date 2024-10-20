import tensorflow as tf
from model_architectures.models import *

class TensorflowModelTrain:
    def __init__(self, model_version, config):
        self.model_version = model_version
        self.config = config
        self.model = None
        
    def load_model(self):
        if self.model_version in globals():
            model_function = globals()[self.model_version]
            if callable(model_function):
                self.model = model_function(self.StringToTuple(self.config['input_shape']), self.StringToTuple(self.config['output_shape']))
        if self.model is None:
            raise Exception('There is no model with version ' + self.model_version + ' in the model_architectures/models.py file')
    
    def compile(self):
        if self.model is not None:
            self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=float(self.config['learning_rate'])), loss=self.config['loss'], metrics=[self.config['metrics']])
    
    def train(self, x_train, y_train, x_test, y_test):
        if self.model is not None:
            self.model.fit(x_train, y_train, epochs=int(self.config['epochs']), batch_size=int(self.config['batch_size']), 
                        validation_data=(x_test, y_test), shuffle=self.StringToBool(self.config['shuffle']))
    
    def evaluate(self, x_test, y_test):
        if self.model is not None:
            return self.model.evaluate(x_test, y_test)
        
    def save_model(self, path):
        if self.model is not None:
            self.model.save(path)
        
    def StringToTuple(self, string):
        return tuple(map(int, string.split(',')))
    
    def StringToBool(self, string):
        return string.lower() == 'true'
    