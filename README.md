# Food Image Recognition using Deep Learning?
## How I trained the Food101 Model

# IMPORTING LIBRARIES
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing import image
```

#LOADING DATA
## Here I will using Food41 Image datasets. This dataset contains 101000 images and 101 different foods.
```python

data_dir = '/kaggle/input/food41/images/'
data = tf.keras.preprocessing.image_dataset_from_directory(data_dir)
```

```python

datagen = ImageDataGenerator(
        rescale = 1./255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split = 0.2)
```

```python

height = 228
width = 228
channels = 3
batch_size = 32
img_shape = (height, width, channels)
img_size = (height, width)

```


```python

train_data = datagen.flow_from_directory(
    data_dir,
    target_size = img_size,
    batch_size = batch_size,
    class_mode = 'categorical',
    subset = 'training')

val_data = datagen.flow_from_directory(
    data_dir,
    target_size = img_size,
    batch_size = batch_size,
    class_mode='categorical',
    subset = 'validation')
```


```python

num_classes = len(data.class_names)
print('.... Number of Classes : {0} ....'.format(num_classes))
```


# Showing Images
```python

def show_img(data):
    plt.figure(figsize=(15,15))
    for images, labels in data.take(1):
        for i in range(9):
            ax = plt.subplot(3, 3, i + 1)
            ax.imshow(images[i].numpy().astype("uint8"))
            ax.axis("off")
```

# Plotting the images in dataset
```python
 
show_img(data)
```
<img src="https://github.com/stratospark/food-101-keras/raw/master/Food%20Classification%20with%20Deep%20Learning%20in%20Keras_files/Food%20Classification%20with%20Deep%20Learning%20in%20Keras_79_0.png">

# BUILDING MODEL
<h5>Here I will be using pre-trained model, which can be done using Transfer Learning. The reuse of a previously learned model on a new problem is known as transfer learning. It’s particularly popular in deep learning right now since it can train deep neural networks with a small amount of data. This is particularly valuable in the field of data science, as most real-world situations do not require millions of labelled data points to train complicated models.</h5>


# TRANSFER LEARNING USING INCEPTION V3
<h5>Previously I used MobileNet but the Accuracy went Scheiße :) </h5>


# Training Model
```python

pre_trained = InceptionV3(weights='imagenet', include_top=False, input_shape=img_shape, pooling='avg')

for layer in pre_trained.layers:
    layer.trainable = False

```


```python

x = pre_trained.output
x = BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001)(x)
x = Dropout(0.2)(x)
x = Dense(1024, activation='relu')(x)
x = Dropout(0.2)(x)
predictions = Dense(num_classes, activation='softmax')(x)

model = Model(inputs = pre_trained.input, outputs = predictions)
model.compile(optimizer = Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

```




```python
STEP_SIZE_TRAIN = train_data.n // train_data.batch_size
STEP_SIZE_VALID = val_data.n // val_data.batch_size

history = model.fit_generator(train_data,
                    steps_per_epoch = STEP_SIZE_TRAIN,
                    validation_data = val_data,
                    validation_steps = STEP_SIZE_VALID,
                    epochs = 50,
                    verbose = 1)
```

# Confusion Matrix
<h5> A confusion matrix will plot each class label and how many times it was correctly labeled vs. the other times it was incorrectly labeled as a different class.</h5>

```python
predictions = np.argmax(model.predict(test_images), axis=1)

cm = confusion_matrix(test_images.labels, predictions)
clr = classification_report(test_images.labels, predictions, target_names=test_images.class_indices, zero_division=0)

plt.figure(figsize=(50, 50))
sns.heatmap(cm, annot=True, fmt='g', vmin=0, cmap='Blues', cbar=False)
plt.xticks(ticks=np.arange(30) + 0.5, labels=test_images.class_indices, rotation=90)
plt.yticks(ticks=np.arange(30) + 0.5, labels=test_images.class_indices, rotation=0)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Food Classification")
plt.show()
```
<img src='https://github.com/samersol/FoodImageRecognition/blob/master/confusion%20matrix.png?raw=true'>

# SAVING MODEL
```python

model_name = 'food_recognition_inceptionV3.h5'
model.save(model_name, save_format='h5')
```

# Playing Time PREDICTION
```python

def ImageDetector(path):
    img = load_img(path, target_size=(224, 224, 3))
    img = img_to_array(img)
    img = img / 255
    img = np.expand_dims(img, [0])
    answer = model.predict(img)
    LabelImg = np.argmax(answer, axis=1)[0]
    LabelIs = labels[LabelImg]
    return LabelIs
```


```python

path = 'C:/Users/solim/Flask2/static/images/meatrub.jpg'
ImageDetector(path)
```

<h4>1/1 ━━━━━━━━━━━━━━━━━━━━ 1s 1s/step <br>
'Steak'</h4>

<img src='https://github.com/samersol/FoodImageRecognition/blob/master/meatrub.jpg?raw=true'>
