'''import wget
url="https://www.dropbox.com/s/w3zlhing4dkgeyb/train.zip?dl=0"
dataset=wget.download(url)'''

#Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from keras.applications.mobilenet import MobileNet, preprocess_input
from keras.models import Model
from keras.layers import Flatten, Dense

from keras.preprocessing.image import ImageDataGenerator, img_to_array,load_img

base_model=MobileNet(input_shape=(224,224,3), include_top=False)
for layer in base_model.layers:
    layer.trainable=False

x=Flatten()(base_model.output)
x=Dense(units=7,activation='softmax' )(x)

#creating our model
model=Model(base_model.input, x)

#all layers of the model
model.summary()
model.compile(optimizer='adam',loss='categorical_crossentropy', metrics=['accuracy'])

#Preparing our data using data generator
train_datagen=ImageDataGenerator(zoom_range=0.2,shear_range=0.2,horizontal_flip=True,rescale=1./225)
train_data=train_datagen.flow_from_directory(directory='/Users/alicedang/Documents/Project/Face Recognition/train',target_size=(224,224),batch_size=32)
train_data.class_indices

val_datagen=ImageDataGenerator(rescale=1/225)
val_data=val_datagen.flow_from_directory(directory='/Users/alicedang/Documents/Project/Face Recognition/train',target_size=(224,224),batch_size=32)
t_img,label=train_data.next()
def plotImages(img_arr,label):
    count=0
    for im,l in zip(img_arr,label):
        plt.imshow(im)
        plt.title(im.shape)
        plt.axis=False
        plt.show()

        count+=1
        if count==10:
            break
plotImages(t_img,label)

#Having early stopping and model check point
from keras.callbacks import ModelCheckpoint, EarlyStopping

#early stopping
es=EarlyStopping(monitor='val_accuracy', min_delta=0.01, patience=5, verbose=1, mode='auto')

#model check point
mc=ModelCheckpoint(filepath="/Users/alicedang/Documents/Project/Face Recognition/best_model.h5", monitor='val_accuracy', verbose=1, save_best_only=True, mode='auto')

#puting call back in a list
call_baclk=[es,mc]

hist=model.fit_generator(train_data,steps_per_epoch=10,epochs=10,validation_data=val_data, validation_steps=8,callbacks=[es,mc])

#Load the best fit model
from keras.models import load_model
model=load_model("/Users/alicedang/Documents/Project/Face Recognition/best_model.h5")
h=hist.history
h.keys()
plt.plot(h['accuracy'])
plt.plot(h['val_accuracy'],c='red')
plt.title('acc vs v-acc')
plt.show()

plt.plot(h['loss'])
plt.plot(h['val_loss'],c='red')
plt.title('loss vs v-loss')
plt.show()

path="/Users/alicedang/Documents/Project/Face Recognition/Screenshot 2023-05-17 at 10.18.17 AM.pdf"
img=load_img(path,target_size=(224,224))
i=img_to_array(img)/225
input_arr=np.array([i])
input_arr.shape

#map o/p values
op=dict(zip(train_data.class_indices.values(), train_data.class_indices.keys()))
pred=np.argmax(model.predict(input_arr))
print(f" the image is of {op[pred]}")

plt.imshow(input_arr[0])
plt.title("input image")
plt.show