import numpy as np
import tensorflow as tf
import autokeras as ak
import pandas as pd
from tensorflow.keras.models import load_model

def read(path="./Dataset/data.csv"):
    df = pd.read_csv(path)
    df = df.values
    sentences = df.T[0]
    classes = df.T[1]
    return sentences, classes.reshape((-1, 1))

sentences, classes = read()

loaded_model = load_model("model_autokeras", custom_objects=ak.CUSTOM_OBJECTS)

predicted_y = loaded_model.predict(sentences[:3])
print(predicted_y)