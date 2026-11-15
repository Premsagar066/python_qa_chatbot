import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocess import preprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'python_qa_final.csv')

THRESHOLD = 0.2
FALLBACK = "Sorry, I don't know the answer to that yet. Try asking about Python basics, functions, lists, NumPy or Pandas."


class PythonQAChatbot:
    def __init__(self, data_path=DATA_PATH, threshold=THRESHOLD):
        self.threshold = threshold
        self.df = pd.read_csv(data_path)
        self.df['keywords'] = self.df['keywords'].fillna('')

        # Rebuild search text with the current preprocess() so it always matches
        self.df['search_text'] = (
            self.df['question'] + ' ' + self.df['keywords']
        ).apply(preprocess)

        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform(self.df['search_text'])

    def get_answer(self, user_question):
        clean = preprocess(user_question)
        if not clean.strip():
            return {"answer": FALLBACK, "score": 0.0, "matched_question": None,
                    "category": None, "found": False}

        vec = self.vectorizer.transform([clean])
        scores = cosine_similarity(vec, self.matrix).flatten()
        idx = scores.argmax()
        score = float(scores[idx])

        if score < self.threshold:
            return {"answer": FALLBACK, "score": score, "matched_question": None,
                    "category": None, "found": False}

        row = self.df.iloc[idx]
        return {"answer": row['answer'], "score": score,
                "matched_question": row['question'],
                "category": row['category'], "found": True}


if __name__ == "__main__":
    bot = PythonQAChatbot()
    print("Python Q&A Bot (type 'quit' to exit)")
    while True:
        q = input("You: ").strip()
        if q.lower() in ("quit", "exit"):
            break
        result = bot.get_answer(q)
        print(f"Bot: {result['answer']}  (score {result['score']:.2f})\n")