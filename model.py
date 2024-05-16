import numpy
import tensorflow as tf
import keras.src

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2 as cv


# https://www.geeksforgeeks.org/how-to-convert-images-to-numpy-array/ used for image to numpy conversion
# LOTS of help from this google tutorial
# https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/tutorials/keras/classification.ipynb#scrollTo=oZTImqg_CaW1

class Model:
    def __init__(self, dataset):
        (self.train_img, self.train_label), (self.test_img, self.test_label) = dataset
        self.train_img = self.train_img / 255.0
        self.test_img = self.test_img / 255.0

    @staticmethod
    def evalCustomImage(index: int) -> numpy.ndarray:  # loads image, converts it to a numpy arary, and compresses it
        img = Image.open(
            f"custom_training/num{index}.png")  # https://stackoverflow.com/questions/48121916/numpy-resize-rescale-image resizing help
        numpyImg = numpy.array(img)
        numpyImg = numpyImg / 255.0
        compressed = cv.resize(numpyImg, dsize=(28, 28), interpolation=cv.INTER_AREA)
        return compressed

    def displayData(self, count, img_list, label_list, predictions: bool):
        col, row = 7, 7
        if count > (col * row):
            print("Cannot render: see the column and row counts for a possible fix")
            return None
        plt.figure(figsize=(12, 7))
        for c, i in enumerate(range(count)):
            plt.subplot(row, col, c + 1)
            plt.imshow(img_list[i], cmap=plt.cm.binary)
            plt.grid(False)
            plt.subplots_adjust(top=0.95, hspace=0.98)
            if not predictions:
                plt.xlabel(label_list[i])
            else:
                prediction = label_list[i]
                num = int(np.argmax(prediction))
                percentage = np.max(prediction) * 100
                color = 'red'
                if num == int(self.test_label[i]):
                    color = 'blue'
                else:
                    print(num, self.test_label[i])
                plt.xlabel(f"{self.classNames[num]} ; {np.round(percentage, 2)}").set_color(color)

        plt.show()


class HandWrittenNumbersModel(Model):
    def __init__(self):
        super().__init__(keras.datasets.mnist.load_data(path="mnist.npz"))
        self.classNames = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        self.model = None

    def trainModel(self):
        model = keras.Sequential([
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(10)
        ])  # setting up the model
        model.compile(optimizer="adam", loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])  # compiling everything, now ready to train the model
        model.fit(self.train_img, self.train_label)  # training the model
        self.model = model

    def predict(self, CUSTOM_IMAGE: numpy.ndarray = None):  # Predicts and graphs 10 of the test images
        prediction_model = keras.Sequential([self.model, keras.layers.Softmax()])
        if CUSTOM_IMAGE is not None:
            pass
            # Not working at the moment
            # predictions = prediction_model.predict(CUSTOM_IMAGE)
            # print(int(np.argmax(predictions)))
            # self.displayData(1, [CUSTOM_IMAGE], ["1", "2"], False)
        else:
            predictions = prediction_model.predict(self.test_img)
            self.displayData(49, self.test_img, predictions, True)


m = HandWrittenNumbersModel()
# model = Model(keras.datasets.mnist.load_data(path="mnist.npz"))

# model.displayData(2, [model.evalCustomImage(1), model.evalCustomImage(2)], ["1", "2"], False)
input("Ready? ")
m.trainModel()
input("Trained! Ready for the predictions? ")
m.predict(CUSTOM_IMAGE=m.evalCustomImage(2))
