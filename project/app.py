from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.corpus import brown
from nltk.util import ngrams
from collections import defaultdict, Counter
import numpy as np
from Levenshtein import distance
import pickle
import os

app = Flask(__name__)
CORS(app)

class PredictiveKeyboard:
    def __init__(self):
        self.trigram_model = defaultdict(Counter)
        self.bigram_model = defaultdict(Counter)
        self.vocab = set()
        self.word_vectors = {}
        self.load_or_train_model()

    def load_or_train_model(self):
        if os.path.exists('model.pkl'):
            with open('model.pkl', 'rb') as f:
                saved_data = pickle.load(f)
                self.trigram_model = saved_data['trigram']
                self.bigram_model = saved_data['bigram']
                self.vocab = saved_data['vocab']
        else:
            self.train_model()

    def train_model(self):
        # Train on Brown corpus
        sentences = brown.sents()
        
        for sentence in sentences:
            # Convert to lowercase
            sentence = [word.lower() for word in sentence]
            
            # Build vocabulary
            self.vocab.update(sentence)
            
            # Create bigrams and trigrams
            bigrams = list(ngrams(sentence, 2))
            trigrams = list(ngrams(sentence, 3))
            
            # Update models
            for w1, w2 in bigrams:
                self.bigram_model[w1][w2] += 1
            
            for w1, w2, w3 in trigrams:
                self.trigram_model[(w1, w2)][w3] += 1
        
        # Save model
        with open('model.pkl', 'wb') as f:
            pickle.dump({
                'trigram': self.trigram_model,
                'bigram': self.bigram_model,
                'vocab': self.vocab
            }, f)

    def predict_next_words(self, context, n=5):
        words = context.lower().strip().split()
        
        if len(words) < 2:
            # Use bigram model for single word
            if len(words) == 1:
                predictions = self.bigram_model[words[0]]
            else:
                # Return most common words if no context
                return list(sorted(self.vocab, key=lambda x: sum(count for counts in self.bigram_model.values() for word, count in counts.items() if word == x), reverse=True))[:n]
        else:
            # Use trigram model
            predictions = self.trigram_model[(words[-2], words[-1])]
        
        # Get top n predictions
        return [word for word, _ in predictions.most_common(n)]

    def autocorrect(self, word, max_distance=2):
        word = word.lower()
        if word in self.vocab:
            return word
        
        # Find closest words by Levenshtein distance
        candidates = []
        for vocab_word in self.vocab:
            dist = distance(word, vocab_word)
            if dist <= max_distance:
                candidates.append((vocab_word, dist))
        
        if candidates:
            # Return the closest match
            return min(candidates, key=lambda x: x[1])[0]
        
        return word

# Initialize the keyboard
keyboard = PredictiveKeyboard()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    context = data.get('context', '')
    predictions = keyboard.predict_next_words(context)
    return jsonify({'predictions': predictions})

@app.route('/autocorrect', methods=['POST'])
def autocorrect():
    data = request.get_json()
    word = data.get('word', '')
    correction = keyboard.autocorrect(word)
    return jsonify({'correction': correction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)