from Configurator import Configuarator
from data_storing.DataReader import DataReader
from sklearn.model_selection import train_test_split
from TensorflowModelTrain import TensorflowModelTrain

config = Configuarator('config_contrast.ini')
reader = DataReader()
config = config.read_config()
train_images, train_labels = reader.load_directory('train_images_contrast', numpy_array=True)
print(train_images.shape)
print(train_labels.shape)

x_train, x_test, y_train, y_test = train_test_split(train_images, train_labels, test_size=float(config['test_size']), random_state=42)

tensorflow_model = TensorflowModelTrain('v0_contrast', config)
tensorflow_model.load_model()
tensorflow_model.compile()
tensorflow_model.train(x_train, y_train, x_test, y_test)
tensorflow_model.save_model("model_architectures/models/v0_contrast.h5")