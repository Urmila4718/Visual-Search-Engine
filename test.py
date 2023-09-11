import tensorflow
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.layers import GlobalMaxPooling2D 
import cv2
import os
import numpy as np
from numpy.linalg import norm
import pickle
from sklearn.neighbors import NearestNeighbors


feature_list=np.array(pickle.load(open("featurevector.pkl", "rb")))
filename=pickle.load(open("filenames.pkl", "rb"))
print(filename)
model=ResNet50(weights='imagenet',include_top=False, input_shape=(224,224,3))
model.trainable=False

model=tensorflow.keras.Sequential([
    model, 
    GlobalMaxPooling2D()
])
model.summary()

image_path = os.path.abspath(r'C:\Urmila\Fashion Recommander System\uploads\1636.jpg')
img=cv2.imread(image_path)
if img is None:
    print("Error: Image not loaded.")
else:
    img=cv2.resize(img, (224,224))

img=np.array(img)
expand_img=np.expand_dims(img, axis=0)
pre_img=preprocess_input(expand_img)
result=model.predict(pre_img).flatten()
normalized=result/norm(result)


neighbors=NearestNeighbors(n_neighbors=6, algorithm="brute", metric="euclidean")
neighbors.fit(feature_list)


distance, indices = neighbors.kneighbors([normalized])

print("indice:",indices)

for file in indices[0][1:6]:
    print("file:",filename[file])
    imgName=cv2.imread(filename[file])
    cv2.imshow("Frame",cv2.resize(imgName, (640,480)))
    cv2.waitKey(0)





