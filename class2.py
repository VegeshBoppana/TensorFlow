import os


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0],True)

(x_train,y_train) , (x_test, y_test) = mnist.load_data()
print(x_train.shape)
print(y_train.shape)
print(x_test.shape,y_test.shape)

x_train = x_train.reshape(-1,28*28).astype("float32") / 255.0
x_test = x_test.reshape(-1,28*28).astype("float32")/ 255.0

#sequential API of Keras (very convenient , not flexible)
model = keras.Sequential(
    [
        keras.Input(shape=(28*28)),
        layers.Dense(512,activation='relu'),
        layers.Dense(256,activation='relu'),
        layers.Dense(10)
    ]
)
# print(model.summary())

# import sys
# sys.exit()

model = keras.Sequential()
model.add(keras.Input(shape= (784) ) )
model.add(layers.Dense(512,activation = 'relu'))
model.add(layers.Dense(256,activation = 'relu',name = 'my_layer'))
model.add(layers.Dense(10))

model = keras.Model(inputs=model.inputs,
                        outputs = [layer.output for layer in model.layers])
features = model.predict(x_train)
for f in features:
    print(f.shape)

#Functional API(A bit more flexible)
import sys
sys.exit()

inputs = keras.Input(shape=(784))
x = layers.Dense(512,activation = 'relu',name = 'firstlayer')(inputs)
x = layers.Dense(256,activation = 'relu',name = 'secondlayer')(x)
outputs = layers.Dense(10,activation='softmax')(x)
model = keras.Model(inputs = inputs,outputs = outputs)

print(model.summary())


model.compile(
    loss = keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    optimizer = keras.optimizers.Adam(lr = 0.001),
    metrics = ["accuracy"]
)
print("TRAINING")
model.fit(x_train,y_train,batch_size = 32,epochs = 5,verbose = 2)
print("TESTING")
model.evaluate(x_test,y_test,batch_size= 32,verbose = 2)
