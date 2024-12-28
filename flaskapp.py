# app.py
from flask import Flask, render_template, request
import pandas as pd
import regex as re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Load the model and vectorizer
with open('model.pkl', 'rb') as model_file:
    mnb = pickle.load(model_file)

with open('cv.pkl', 'rb') as vectorizer_file:
    cv = pickle.load(vectorizer_file)

# Initialize Flask app
app = Flask(__name__)

# Preprocessing function
def preprocess_title(title):
    ps = PorterStemmer()
    review = re.sub('[^a-zA-Z]', ' ', title)
    review = review.lower()
    review = review.split()
    review = [ps.stem(word) for word in review if word not in stopwords.words('english')]
    return ' '.join(review)

# Define routes
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = ""
    if request.method == "POST":
        news_title = request.form["title"]
        processed_title = preprocess_title(news_title)
        title_vector = cv.transform([processed_title]).toarray()
        prediction = "Fake News" if mnb.predict(title_vector)[0] == 1 else "Real News"
    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)