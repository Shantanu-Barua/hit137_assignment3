import tensorflow as tf

# Load the MobileNetV2 model pre-trained on ImageNet
model = tf.keras.applications.MobileNetV2(weights='imagenet')

# Save the model as a .h5 file
model.save('mobilenet_v2.h5')

# https://github.com/Shantanu-Barua/hit137_assignment3.git