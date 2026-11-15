import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# Normally stop words, but meaningful in Python, so we KEEP them
KEEP = {'in', 'not', 'and', 'or', 'if', 'else', 'for', 'while',
        'as', 'with', 'from', 'no', 'all', 'any'}
STOP = set(stopwords.words('english')) - KEEP

# Symbols converted to words so they are not lost (order matters)
SYMBOLS = {
    '**kwargs': ' kwargs ',
    '*args': ' args ',
    '==': ' doubleequals ',
    '!=': ' notequals ',
    ':=': ' walrus ',
    '//': ' floordivision ',
    '**': ' doublestar ',
    '/': ' truedivision ',
    '%': ' modulus ',
}

lemmatizer = WordNetLemmatizer()


def preprocess(text):
    text = str(text).lower()
    for symbol, word in SYMBOLS.items():
        text = text.replace(symbol, word)
    tokens = re.findall(r'[a-z0-9_]+', text)
    tokens = [t.strip('_') for t in tokens]
    tokens = [t for t in tokens if t and t not in STOP]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return ' '.join(tokens)