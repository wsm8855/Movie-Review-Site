import pickle
import re
import numpy as np
import os

from sklearn.feature_extraction.text import HashingVectorizer


stop_path = os.path.join(os.path.dirname(__file__), 'nltk_misc/stopwords.pickle')
clf_path = os.path.join(os.path.dirname(__file__), 'trained_clfs/clf_v2.pickle')

sentiment = {
    1: 'positive',
    0: 'negative'
}


def clean_text(text: str) -> str:
    """
    Uses regular expressions to clean a string of text.
    This method:
        * Removes decoration tags (such as html markup)
        * Finds all emojies (i.e. :) :( ;-) xD), simplifies them, then appends to the end aof the string.
        * Converts all words to lowercase.
    :param text: string of text to be cleaned
    :return: the cleaned text as a string.
    """
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=|x|X)(?:-)?(?:\)|\(|D|P)', text)
    text = (re.sub('[\W]+', ' ', text.lower()) + ' '.join(emoticons).replace('-', ''))
    return text


def tokenizer(text):
    with open(stop_path, 'rb') as f:
        stopwords = pickle.load(f)
    text = clean_text(text)
    tokenized = [w for w in text.split() if w not in stopwords]
    return tokenized


def get_prediction(text):
    with open(clf_path, 'rb') as f:
        clf = pickle.load(f)
    text = clean_text(text)
    vectorizer = HashingVectorizer(decode_error='ignore', preprocessor=None, tokenizer=tokenizer)
    X = vectorizer.transform([text])
    y = clf.predict(X)[0]
    prob = np.max(clf.predict_proba(X))

    words = tokenizer(text)

    return sentiment[y], prob, words
