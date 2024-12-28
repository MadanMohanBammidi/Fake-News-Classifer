# app.py
from fastapi import FastAPI
from pydantic import BaseModel
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

# Initialize the FastAPI app
app = FastAPI()

# Define the request body
class NewsTitle(BaseModel):
    title: str

# Preprocessing function
def preprocess_title(title):
    ps = PorterStemmer()
    review = re.sub('[^a-zA-Z]', ' ', title)
    review = review.lower()
    review = review.split()
    review = [ps.stem(word) for word in review if word not in stopwords.words('english')]
    return ' '.join(review)

# Define the classification endpoint
@app.post("/classify/")
def classify_news(news: NewsTitle):
    processed_title = preprocess_title(news.title)
    title_vector = cv.transform([processed_title]).toarray()
    prediction = mnb.predict(title_vector)
    result = "Fake News" if prediction[0] == 1 else "Real News"
    return {"title": news.title, "prediction": result}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Fake News Classifier API! Use the /classify/ endpoint to classify news titles."}

# Run the app with: uvicorn app:app --reload