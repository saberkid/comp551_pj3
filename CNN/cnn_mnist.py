from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from data_reader import *
from keras.callbacks import ModelCheckpoint
import numpy
from keras.utils.vis_utils import plot_model


batch_size = 1024
num_classes = 40
epochs = 50

TRAIN_FILE = "train_labeled_nbg"
TEST_FILE = "test_x.csv_nbg"
# TRAIN_FILE = "../data/train_labeled_nbg"
# TEST_FILE = "../data/test_x.csv_nbg"
#TRAIN_FILE = "../data/train_0.8"
#TEST_FILE = "../data/val_0.2"
# input image dimensions
img_rows, img_cols = 64, 64

# the data, shuffled and split between train and test sets
reader = Reader(TRAIN_FILE, TEST_FILE)
x_train, y_train = reader.read_train()

x_test = reader.read_test()
#x_test, y_test = reader.read_val()

if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
#y_train = keras.utils.to_categorical(y_train, num_classes)
#y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),       
                 activation='relu',padding='same',
                 input_shape=input_shape))
model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))



model.add(Flatten())
model.add(Dropout(0.5))
model.add(Dense(4096, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))


checkpointer_1 = ModelCheckpoint(filepath="weights-{epoch:02d}.hdf5", verbose=1, save_best_only=False, period=10)
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer='adam',#.optimizers.Adadelta(),
              metrics=['accuracy'])
#model.load_weights('cnn_drop4096_weights.h5') 
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          #validation_data=(x_test, y_test),
          callbacks=[checkpointer_1])

model.save_weights('cnn_drop4096_weights.h5')

seq_num = xrange(len(x_test))
with open('predic2.csv','w+') as predict_writer:
    predict_writer.writelines('Id,Label\n')
    for test_num in seq_num:          
        prediction = model.predict(numpy.asarray([x_test[test_num],]))[0].tolist()
        label = reader.num_list[prediction.index(max(prediction))]
        predict_writer.writelines(str(test_num+1) + ',' + str(label) + '\n')
        
plot_model(model, to_file='model3.png', show_shapes='true')
