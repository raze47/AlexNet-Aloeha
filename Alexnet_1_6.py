import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from sklearn.metrics import confusion_matrix , classification_report
import matplotlib.pyplot as plt
import numpy as np
import random
import os
import cv2
from keras.utils import np_utils

DATADIR = "aloeha_dataset_2/"
CATEGORIES = ["healthy", "rot", "rust"]
ML_PHASE = ["Training", "Testing", "Validation"]
IMG_SIZE = 227
LEARNING_RATE = 0.001

##Getting the dataset for training
DATADIR_TRAINING = "aloeha_dataset_2/Training"

training_data = []


def create_training_data():
  for category in CATEGORIES:
    print(category)
    category_path = os.path.join(DATADIR_TRAINING, category)
    print(category_path)
    class_num = CATEGORIES.index(category)
    for img in os.listdir(category_path):
    
      try:
        img_array = cv2.imread(os.path.join(category_path,img))
        new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        
        training_data.append([new_array, class_num])
      except Exception as e:
        pass

create_training_data() 
print(len(training_data))

random.shuffle(training_data)

X_train = []
y_train = []

for features, labels in training_data:
  X_train.append(features)
  y_train.append(labels)

X_train = np.array(X_train).reshape(-1, IMG_SIZE, IMG_SIZE, 3)
print(X_train.shape)

##Getting the dataset for testing

DATADIR_TESTING = "aloeha_dataset_2/Testing"

testing_data = []


def create_testing_data():

  for category in CATEGORIES:
    testing_ctr = 0
    print(category)
    category_path = os.path.join(DATADIR_TESTING, category)
    print(category_path)
    class_num = CATEGORIES.index(category)
    for img in os.listdir(category_path):
    
      try:
        img_array = cv2.imread(os.path.join(category_path,img))
        new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        
        testing_data.append([new_array, class_num])
      except Exception as e:
        pass

create_testing_data() 

random.shuffle(testing_data)

X_test = []
y_test = []


for features, labels in testing_data:
  X_test.append(features)
  y_test.append(labels)

X_test = np.array(X_test).reshape(-1, IMG_SIZE, IMG_SIZE, 3)

##Getting the dataset for Validation
DATADIR_VALIDATION = "aloeha_dataset_2/Validation"

validation_data = []


def create_validation_data():
  for category in CATEGORIES:
    validation_ctr = 0
    print(category)
    category_path = os.path.join(DATADIR_VALIDATION, category)
    print(category_path)
    class_num = CATEGORIES.index(category)
    for img in os.listdir(category_path):
    
      try:

        img_array = cv2.imread(os.path.join(category_path,img))
        new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        validation_data.append([new_array, class_num])
      except Exception as e:
        pass

create_validation_data() 

random.shuffle(validation_data)

X_valid = []
y_valid = []

for features, labels in validation_data:
  X_valid.append(features)
  y_valid.append(labels)

X_valid = np.array(X_valid).reshape(-1, IMG_SIZE, IMG_SIZE, 3)


##Shaping
y_train = np.array(y_train).reshape(-1,)
y_test = np.array(y_test).reshape(-1,)
y_valid = np.array(y_valid).reshape(-1,)

##AlexNet

leaky_relu_alpha = 0.1

cnn_alex = models.Sequential([
    layers.Conv2D(filters=96, kernel_size=(11,11), strides=(4,4), input_shape=(IMG_SIZE,IMG_SIZE,3)),
	layers.LeakyReLU(alpha=leaky_relu_alpha),
    layers.BatchNormalization(),
    layers.MaxPool2D(pool_size=(3,3), strides=(2,2)),
    layers.Conv2D(filters=256, kernel_size=(5,5), strides=(1,1), padding="same"),
	layers.LeakyReLU(alpha=leaky_relu_alpha),
    layers.BatchNormalization(),
    layers.MaxPool2D(pool_size=(3,3), strides=(2,2)),
    layers.Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), padding="same"), 
	layers.LeakyReLU(alpha=leaky_relu_alpha),
    layers.BatchNormalization(),
    layers.Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), padding="same"), 
	layers.LeakyReLU(alpha=leaky_relu_alpha),
    layers.BatchNormalization(),
    layers.Conv2D(filters=256, kernel_size=(3,3), strides=(1,1), padding="same"), 
	layers.LeakyReLU(alpha=leaky_relu_alpha),
    layers.BatchNormalization(),
    layers.MaxPool2D(pool_size=(3,3), strides=(2,2)), 
    layers.Flatten(),
    layers.Dense(4096),
	layers.LeakyReLU(alpha=leaky_relu_alpha),
    layers.Dropout(0.5),
    layers.Dense(4096),
	layers.LeakyReLU(alpha=leaky_relu_alpha),
    layers.Dropout(0.5),
    layers.Dense(3, activation='softmax')
])


cnn_alex.compile(loss='sparse_categorical_crossentropy', optimizer=tf.optimizers.Adamax(learning_rate=LEARNING_RATE), metrics=['accuracy'])
cnn_alex.summary()

cnn_alex.fit(X_train, y_train,
          epochs=4,
          validation_data=(X_valid, y_valid),
          validation_freq=1,
          )

cnn_alex.evaluate(X_test, y_test)

y_pred = cnn_alex.predict(X_test)
y_classes = [np.argmax(element) for element in y_pred]

print("Classification Report: \n", classification_report(y_test, y_classes))

cnn_alex.save("model")

