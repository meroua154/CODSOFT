import tensorflow as tf
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input
import numpy as np
import string
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import add
import os

# Fonction pour extraire les caractéristiques des images
def extract_features(img_path):
    img = image.load_img(img_path, target_size=(299, 299))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    features = model.predict(img_array)
    return features

# Fonction pour prétraiter les légendes
def preprocess_captions(captions):
    table = str.maketrans('', '', string.punctuation)
    processed_captions = []
    for caption in captions:
        caption = caption.lower().translate(table)
        processed_captions.append(caption)
    return processed_captions

# Fonction pour créer le modèle de génération de légendes
def create_model(vocab_size, max_length):
    inputs1 = tf.keras.layers.Input(shape=(2048,))
    fe1 = tf.keras.layers.Dropout(0.5)(inputs1)
    fe2 = tf.keras.layers.Dense(256, activation='relu')(fe1)
    
    inputs2 = tf.keras.layers.Input(shape=(max_length,))
    se1 = tf.keras.layers.Embedding(vocab_size, 256, mask_zero=True)(inputs2)
    se2 = tf.keras.layers.Dropout(0.5)(se1)
    se3 = tf.keras.layers.LSTM(256)(se2)
    
    decoder1 = add([fe2, se3])
    decoder2 = tf.keras.layers.Dense(256, activation='relu')(decoder1)
    outputs = tf.keras.layers.Dense(vocab_size, activation='softmax')(decoder2)
    
    model = tf.keras.models.Model(inputs=[inputs1, inputs2], outputs=outputs)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model

# Fonction générateur de données
def data_generator(descriptions, features, tokenizer, max_length):
    while 1:
        for key, desc_list in descriptions.items():
            feature = features[key]
            for desc in desc_list:
                seq = tokenizer.texts_to_sequences([desc])[0]
                for i in range(1, len(seq)):
                    in_seq, out_seq = seq[:i], seq[i]
                    in_seq = pad_sequences([in_seq], maxlen=max_length)[0]
                    out_seq = to_categorical([out_seq], num_classes=vocab_size)[0]
                    yield ([np.expand_dims(feature, axis=0), in_seq], out_seq)

if __name__ == "__main__":
    # Charger le modèle InceptionV3 pré-entraîné
    base_model = InceptionV3(weights='imagenet')
    model = Model(inputs=base_model.input, outputs=base_model.layers[-2].output)
    
    # Exemple d'utilisation pour l'extraction de caractéristiques
    img_path = '/content/im4.jpg'
    features = extract_features(img_path)

    # Prétraitement des légendes
    captions = ["A dog is playing with a ball.", "A cat is sitting on the table."]
    processed_captions = preprocess_captions(captions)

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(processed_captions)
    sequences = tokenizer.texts_to_sequences(processed_captions)
    padded_sequences = pad_sequences(sequences, padding='post')

    vocab_size = len(tokenizer.word_index) + 1
    max_length = max(len(seq) for seq in sequences)

    # Créer le modèle
    model = create_model(vocab_size, max_length)
    model.summary()

    # Exemple de descriptions et de caractéristiques d'entraînement
    train_descriptions = {'img1': ['startseq a dog playing endseq']}
    train_features = {'img1': features}

    # Générateur de données
    generator = data_generator(train_descriptions, train_features, tokenizer, max_length)

    # Créez un dataset TensorFlow à partir du générateur
    dataset = tf.data.Dataset.from_generator(
        lambda: generator,
        output_signature=(
            (tf.TensorSpec(shape=(None, 2048), dtype=tf.float32), 
             tf.TensorSpec(shape=(max_length,), dtype=tf.float32)),
            tf.TensorSpec(shape=(vocab_size,), dtype=tf.float32)
        )
    )

    # Entraînement du modèle
    model.fit(dataset, epochs=20, steps_per_epoch=len(train_descriptions))
