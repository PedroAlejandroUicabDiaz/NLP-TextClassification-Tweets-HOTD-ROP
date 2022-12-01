import numpy as np
import json

import tensorflow as tf
from tensorflow import keras
from collections import Counter
from keras.preprocessing.text import Tokenizer

from flask import Flask, request, jsonify

app =  Flask(__name__)

modelLSTM =  keras.models.load_model("my_model_LSTM_classifier.h5")


def word_count(text):
  count= Counter()
  for i in text:
    for word in i.split():
      count[word]+=1
  return count
  
def counter_word(text):
    counter= word_count(text)
    num_words= len(counter)

    tokenizer= Tokenizer(num_words= num_words)
    tokenizer.fit_on_texts(text)
    word_index= tokenizer.word_index
    text_sequence = tokenizer.texts_to_sequences(text)
 
    text_padded= tf.keras.preprocessing.sequence.pad_sequences(text_sequence, 
                                                                maxlen=50, 
                                                                padding='post', 
                                                                truncating='post')

    return text_padded

def tweet_classifier(counter):
    y_pred = modelLSTM.predict(counter)

    y_pred=(y_pred>0.5)

    value_pred = y_pred.tolist()

    return value_pred[0][0]


@app.route("/tweet/new",methods=["POST"])
def index():
    if request.data:
        tweetDict = json.loads(request.data)

        counter = counter_word(tweetDict['tweet'])

        ypred = tweet_classifier(counter)

        if ypred == True:
            tweetClass = 'HOTD'
        else:
            tweetClass = 'ROP'
            
        return jsonify({'label':tweetClass}), 200
    else:
        return "400 BAD REGQUEST", 400


if __name__ == '__main__':
    app.debug = True
    app.run()