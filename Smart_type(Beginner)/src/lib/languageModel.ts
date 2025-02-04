// Simple trigram language model
const commonTrigrams = {
  "i am": ["a", "not", "going", "the", "so"],
  "going to": ["be", "the", "get", "have", "make"],
  "want to": ["go", "see", "make", "be", "get"],
  "need to": ["get", "make", "be", "do", "find"],
  "would like": ["to", "some", "the", "a", "more"],
  "thank you": ["for", "so", "very", "all", "!"],
};

const commonWords = [
  "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
  "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
];

export function predictNextWords(input: string): string[] {
  const words = input.toLowerCase().trim().split(/\s+/);
  
  if (words.length >= 2) {
    const lastTwoWords = words.slice(-2).join(" ");
    const predictions = commonTrigrams[lastTwoWords];
    if (predictions) {
      return predictions;
    }
  }

  // Fallback to common words if no trigram match
  return commonWords;
}

export function autocorrectWord(word: string): string {
  const commonMisspellings: Record<string, string> = {
    "teh": "the",
    "recieve": "receive",
    "wierd": "weird",
    "theyre": "they're",
    "im": "I'm",
    "dont": "don't",
    "cant": "can't",
    "wont": "won't",
  };

  return commonMisspellings[word.toLowerCase()] || word;
}