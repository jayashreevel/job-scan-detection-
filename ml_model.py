from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

texts = [
    "earn money fast registration fee telegram",
    "work from home no experience whatsapp",
    "official company hiring software engineer",
    "government job notification through website"
]

labels = [1, 1, 0, 0]  # 1 = Fake, 0 = Real

vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

pickle.dump(model, open("job_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ ML Model Trained Successfully")
