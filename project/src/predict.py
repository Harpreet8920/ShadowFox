import collections
import json
from typing import List, Dict, Optional

class NGramPredictor:
    def __init__(self):
        # Store trigrams and their frequencies
        self.trigrams: Dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
        # Store common corrections for misspelled words
        self.corrections = {
            "teh": "the",
            "recieve": "receive",
            "wierd": "weird",
            "theyre": "they're",
            "im": "i'm",
            "dont": "don't",
            "cant": "can't",
            "wont": "won't"
        }
        
        # Initialize with some sample training data
        self.train([
            "I am going to the store",
            "I am happy to see you",
            "Would you like to join us",
            "Thank you for your help",
            "I need to finish this work",
            "I want to learn more",
            "Going to be a great day",
            "Need to get some rest"
        ])

    def train(self, sentences: List[str]) -> None:
        """Train the n-gram model with example sentences."""
        for sentence in sentences:
            words = sentence.lower().split()
            if len(words) < 3:
                continue
                
            # Build trigrams
            for i in range(len(words) - 2):
                context = f"{words[i]} {words[i + 1]}"
                next_word = words[i + 2]
                self.trigrams[context][next_word] += 1

    def predict_next(self, context: str, max_suggestions: int = 5) -> List[str]:
        """Predict the next word given the previous words."""
        context = context.lower().strip()
        words = context.split()
        
        if len(words) < 2:
            # Return common sentence starters if not enough context
            return ["the", "i", "we", "this", "that"]
            
        # Get the last two words as context
        context_key = f"{words[-2]} {words[-1]}"
        
        # Get predictions from trigrams
        predictions = self.trigrams[context_key]
        if not predictions:
            # Fallback to common words if no predictions
            return ["the", "to", "a", "and", "is"]
            
        # Return most common predictions
        return [word for word, _ in predictions.most_common(max_suggestions)]

    def autocorrect(self, word: str) -> Optional[str]:
        """Suggest correction for potentially misspelled word."""
        word = word.lower()
        return self.corrections.get(word)

    def to_json(self) -> str:
        """Export the model data as JSON."""
        export_data = {
            'trigrams': {k: dict(v) for k, v in self.trigrams.items()},
            'corrections': self.corrections
        }
        return json.dumps(export_data)

def main():
    # Initialize predictor
    predictor = NGramPredictor()
    
    # Example usage
    context = "I am"
    predictions = predictor.predict_next(context)
    print(f"Context: '{context}'")
    print(f"Predictions: {predictions}")
    
    # Export model data
    model_json = predictor.to_json()
    with open('model_data.json', 'w') as f:
        f.write(model_json)

if __name__ == "__main__":
    main()