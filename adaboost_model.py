# -*- coding: utf-8 -*-
"""ML PROJECT.ipynb
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1yzNuwhKUoKIezKU-tbr5L2KLeGzd9KWp
"""

#from google.colab import drive
#drive.mount('/content/gdrive')
import random
from keras.applications.nasnet import NASNetMobile
from keras import applications
from keras import optimizers
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.models import Model
from keras.applications import densenet
from keras.layers import Dense, GlobalAveragePooling2D,Flatten,Dropout
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator
from PIL import Image
import glob
import numpy as np
import cv2 as cv

from scipy.signal import convolve2d
random.seed(20)
def edge(im_small):
  n=100
  sobel_x = np.c_[
      [-1,0,1],
      [-2,0,2],
      [-1,0,1]
  ]

  sobel_y = np.c_[
      [1,2,1],
      [0,0,0],
      [-1,-2,-1]
  ]

  ims = []
  for d in range(3):
      sx = convolve2d(im_small[:,:,d], sobel_x, mode="same", boundary="symm")
      sy = convolve2d(im_small[:,:,d], sobel_y, mode="same", boundary="symm")
      ims.append(np.sqrt(sx*sx + sy*sy))

  im_conv = np.stack(ims, axis=2).astype("uint8")
  return im_conv

def emboss(im_small):
  karnel = np.array(
  [
      [-1,-1,0],
      [-1,0,1],
      [0,1,1]
  ])
  ims = []
  for d in range(3):
      sx = convolve2d(im_small[:,:,d], karnel, mode="same", boundary="symm")
      ims.append(sx)
  im_conv = np.stack(ims, axis=2).astype("uint8")
  return im_conv

def simple_threshold(im, threshold=50):
    return ((im > threshold) * 255).astype("uint8")

def sifat(image):
    original_image = image

    #contrast change
    new_image = np.zeros(image.shape, image.dtype)
    alpha = 4.4 # Simple contrast control
    beta = -10    # Simple brightness control
    # Initialize values
    #print(' Basic Linear Transforms ')
    print('-------------------------')

    # Do the operation new_image(i,j) = alpha*image(i,j) + beta
    # Instead of these 'for' loops we could have used simply:
    # new_image = cv.convertScaleAbs(image, alpha=alpha, beta=beta)
    # but we wanted to show you how to access the pixels :)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            for c in range(image.shape[2]):
                new_image[y,x,c] = np.clip(alpha*image[y,x,c] + beta, 0, 255)



    image = new_image
    #brightness with gamma correction
    gamma = 0.8
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    new_image = cv.LUT(image, table)



    image = new_image
    #Sharpening
    # Create our shapening kernel, it must equal to one eventually
    kernel_sharpening = np.array([[-1,-1,-1],
                                  [-1, 9,-1],
                                  [-1,-1,-1]])
    # applying the sharpening kernel to the input image & displaying it.
    new_image = cv.filter2D(image, -1, kernel_sharpening)



    image = new_image
    #Saturation change
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    for i in range(len(hsv)):
        for j in range(len(hsv[i])):
            hsv[i,j,1] += 75 #change saturation value
            #hsv[i,j,0] += 0 #change hue value
            #hsv[i,j,2] += 10

    new_image = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    return new_image

Images = []
labels = []
dim = 96
from scipy import ndimage
alpha = 300
#print(glob.glob('/content/gdrive/My Drive/train/fold_1/all/*.bmp'))
m=0

for filename in glob.glob('fold_0/all/*.bmp'): #assuming gif
    m+=1
    
    im = image.load_img(filename, target_size=(dim, dim))
    im = image.img_to_array(im)
    im = np.array(im)
    
    filter_blurred_f = ndimage.gaussian_filter(im, 1)
    sharpened = im + alpha * (im - filter_blurred_f)
    im = emboss(im)
    #im = edge(im)
    #im = edge(im)
    Images.append(im)
    labels.append(1)
    print(m)
m=0
for filename in glob.glob('fold_1/all/*.bmp'): #assuming gif
    m+=1
    
    try:
      im = image.load_img(filename, target_size=(dim, dim))
      im = image.img_to_array(im)
      im = np.array(im)
      filter_blurred_f = ndimage.gaussian_filter(im, 1)
      sharpened = im + alpha * (im - filter_blurred_f)
      im = emboss(im)
      #im = edge(im)
      #im = edge(im)
      Images.append(im)
      labels.append(1)
    except(OSError):
      print('error',m)
print(m)

m=0    
for filename in glob.glob('fold_0/hem/*.bmp'): #assuming gif
    m+=1
    
    im = image.load_img(filename, target_size=(dim, dim))
    im = image.img_to_array(im)
    im = np.array(im)
    filter_blurred_f = ndimage.gaussian_filter(im, 1)
    sharpened = im + alpha * (im - filter_blurred_f)
    im = emboss(im)
    #im = edge(im)
    #im = edge(im)
    Images.append(im)
    labels.append(0)
print(m)
m=0
for filename in glob.glob('fold_1/hem/*.bmp'): #assuming gif
    m+=1
    
    im = image.load_img(filename, target_size=(dim, dim))
    im = image.img_to_array(im)
    im = np.array(im)
    filter_blurred_f = ndimage.gaussian_filter(im, 1)
    sharpened = im + alpha * (im - filter_blurred_f)
    im = emboss(im)
    #im = edge(im)
    #im = edge(im)
    Images.append(im)
    labels.append(0)
print(m)
m=0


print(len(Images), Images[0].shape)
import matplotlib.pyplot as plt
plt.imshow( image.array_to_img(Images[7]) , cmap='gray')

from keras.applications.vgg16 import VGG16
from keras.applications.nasnet import NASNetMobile
from keras.applications.mobilenet_v2 import MobileNetV2
base_model = MobileNetV2(weights='imagenet', include_top=False,input_shape=(dim,dim,3))

# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
#x = Flatten()(x)
# let's add a fully-connected layer
x= Dropout(0.25)(x)
x = Dense(100, activation='relu')(x)
x= Dropout(0.25)(x)
#x = Dense(2, activation='softmax')
# and a logistic layer -- let's say we have 200 classes
predictions = Dense(1, activation='sigmoid')(x)

# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional InceptionV3 layers
for layer in base_model.layers:
    layer.trainable = False

# compile the model (should be done *after* setting layers to non-trainable)
model.compile(optimizer='rmsprop', loss='binary_crossentropy',metrics=['accuracy'])


# at this point, the top layers are well trained and we can start fine-tuning
# convolutional layers from inception V3. We will freeze the bottom N layers
# and train the remaining top layers.

# let's visualize layer names and layer indices to see how many layers
# we should freeze:
for i, layer in enumerate(base_model.layers):
   print(i, layer.name)

# we chose to train the top 2 inception blocks, i.e. we will freeze
# the first 249 layers and unfreeze the rest:
print(len(model.layers))
for layer in model.layers:
   layer.trainable = True


# we need to recompile the model for these modifications to take effect
# we use SGD with a low learning rate
from keras.optimizers import SGD
model.compile(optimizer='Adam', loss='binary_crossentropy',metrics=['accuracy'])
model.summary()

def getModels(dimension,channel):
  model = Sequential()
  model.add(Conv2D(32, kernel_size=(3, 3),
                   activation='relu',
                   input_shape=(dimension,dimension,channel)))
  model.add(Conv2D(64, (3, 3), activation='relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  model.add(Dropout(0.25))
  model.add(Flatten())
  model.add(Dense(128, activation='relu'))
  model.add(Dropout(0.5))
  model.add(Dense(1, activation='softmax'))

  model.compile(loss=keras.losses.categorical_crossentropy,
                optimizer='adam',
                metrics=['accuracy'])
  return model

import numpy as np
from keras.utils import np_utils

indices=list(range(len(Images)))
np.random.seed(23)
np.random.shuffle(indices)
Images = np.array(Images)
Images= Images/255.0
labels = np.array(labels)
#labels=np_utils.to_categorical(labels)
ind=int(len(indices)*0.60)
ind2 = int(len(indices)*0.20)
# train data
X_train=Images[indices[:ind]] 
y_train=labels[indices[:ind]]
# validation data
X_val=Images[indices[ind:ind+ind2]] 
y_val=labels[indices[ind:ind+ind2]]

X_test = Images[indices[ind+ind2:]] 
y_test = labels[indices[ind+ind2:]]

print(X_train[0].shape)

image_gen = ImageDataGenerator(
    samplewise_center=True,
    featurewise_std_normalization=True,
    featurewise_center=True,
   
    zca_epsilon=0.7,
    zca_whitening=True,
    )

#image_gen.fit(X_train, augment=False)
model.fit(x=X_train, y=y_train,
            epochs=5, 
            verbose=1, 
            validation_data=(X_val,y_val),
            shuffle=True,
            
            )
predictions=model.predict(X_train,verbose=1)
model1=model



#previous model end here
x_train2=[]
y_train2=[]
for i in range(len(predictions)):
    if predictions[i]>0.5 and y_train[i]==0:
        x_train2.append(X_train[i])
        y_train2.append(y_train[i])
    elif predictions[i]<=0.5 and y_train[i]==1:
        x_train2.append(X_train[i])
        y_train2.append(y_train[i])
while(len(x_train2)<=len(X_train)):
    index=int(random.uniform(0,len(X_train)))
    x_train2.append(X_train[index])
    y_train2.append(y_train[index])
x_train2 = np.array(x_train2)
y_train2 = np.array(y_train2)    
base_model =densenet.DenseNet121(weights='imagenet', include_top=False,input_shape=(dim,dim,3))

# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
#x = Flatten()(x)
# let's add a fully-connected layer
x= Dropout(0.25)(x)
x = Dense(100, activation='relu')(x)
x= Dropout(0.25)(x)
#x = Dense(2, activation='softmax')
# and a logistic layer -- let's say we have 200 classes
predictions = Dense(1, activation='sigmoid')(x)

# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional InceptionV3 layers
for layer in base_model.layers:
    layer.trainable = False

# compile the model (should be done *after* setting layers to non-trainable)
model.compile(optimizer='rmsprop', loss='binary_crossentropy',metrics=['accuracy'])

model.fit(x=x_train2, y=y_train2,
            epochs=5, 
            verbose=1, 
            validation_data=(X_val,y_val),
            shuffle=True,
            
            )
predictions=model.predict(X_train,verbose=1)
model2=model




#previous model end here
x_train3=[]
y_train3=[]
for i in range(len(predictions)):
    if predictions[i]>0.5 and y_train[i]==0:
        x_train3.append(X_train[i])
        y_train3.append(y_train[i])
    elif predictions[i]<=0.5 and y_train[i]==1:
        x_train3.append(X_train[i])
        y_train3.append(y_train[i])
while(len(x_train3)<=len(X_train)):
    index=int(random.uniform(0,len(X_train)))
    x_train3.append(X_train[index])
    y_train3.append(y_train[index])
x_train3 = np.array(x_train3)
y_train3 = np.array(y_train3)    
base_model =NASNetMobile(weights='imagenet', include_top=False,input_shape=(dim,dim,3))    
# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
#x = Flatten()(x)
# let's add a fully-connected layer
x= Dropout(0.25)(x)
x = Dense(100, activation='relu')(x)
x= Dropout(0.25)(x)
#x = Dense(2, activation='softmax')
# and a logistic layer -- let's say we have 200 classes
predictions = Dense(1, activation='sigmoid')(x)

# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional InceptionV3 layers
for layer in base_model.layers:
    layer.trainable = False

# compile the model (should be done *after* setting layers to non-trainable)
model.compile(optimizer='rmsprop', loss='binary_crossentropy',metrics=['accuracy'])

#image_gen.fit(X_train, augment=False)
from keras.callbacks import ModelCheckpoint

checkpointer = ModelCheckpoint('model.h5', verbose=1, save_best_only=True)

model.fit(x=x_train3, y=y_train3,
            epochs=5, 
            verbose=1, 
            validation_data=(X_val,y_val),
            shuffle=True,
            callbacks=[
                checkpointer,
            ]
            )   
model3=model

predictions1=model1.predict(X_test,verbose=1)
predictions2=model2.predict(X_test,verbose=1)
predictions3=model3.predict(X_test,verbose=1)
acc = 0
tcc = 0
for i in range(len(predictions1)):
    tcc+=1
    p = predictions1[i]+predictions2[i]+predictions3[i]
    p = np.sum(p)
    p=p/3.0
    print(p,y_test[i] )
    if  p<0.5 and y_test[i]==0:
        acc+=1
        
    elif p>=0.5 and y_test[i]==1:
        acc+=1
    
print("accuracy", 100*acc/tcc)