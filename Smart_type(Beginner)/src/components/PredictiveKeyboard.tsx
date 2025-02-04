import React, { useState, useEffect } from 'react';
import { predictNextWords, autocorrectWord } from '../lib/languageModel';
import { Send } from 'lucide-react';

export function PredictiveKeyboard() {
  const [input, setInput] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [messages, setMessages] = useState<string[]>([]);

  useEffect(() => {
    const words = input.split(/\s+/);
    const lastWord = words[words.length - 1];
    
    // Only show predictions if the last character is a space
    if (input.endsWith(' ')) {
      setSuggestions(predictNextWords(input));
    } else if (lastWord) {
      // Show autocorrect suggestions for the current word
      const correctedWord = autocorrectWord(lastWord);
      if (correctedWord !== lastWord) {
        setSuggestions([correctedWord]);
      } else {
        setSuggestions([]);
      }
    } else {
      setSuggestions([]);
    }
  }, [input]);

  const handleSuggestionClick = (word: string) => {
    const words = input.split(/\s+/);
    if (input.endsWith(' ')) {
      setInput(input + word + ' ');
    } else {
      words[words.length - 1] = word;
      setInput(words.join(' ') + ' ');
    }
  };

  const handleSubmit = () => {
    if (input.trim()) {
      setMessages([...messages, input.trim()]);
      setInput('');
      setSuggestions([]);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-4">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-4 text-gray-800">Predictive Keyboard</h2>
        
        {/* Messages Display */}
        <div className="bg-gray-50 rounded-lg p-4 mb-4 h-64 overflow-y-auto">
          {messages.map((msg, index) => (
            <div key={index} className="mb-2 p-2 bg-blue-50 rounded">
              {msg}
            </div>
          ))}
        </div>

        {/* Input Area */}
        <div className="relative">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-transparent resize-none"
            placeholder="Start typing..."
            rows={3}
          />
          <button
            onClick={handleSubmit}
            className="absolute bottom-3 right-3 p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-colors"
          >
            <Send size={20} />
          </button>
        </div>

        {/* Suggestions */}
        {suggestions.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-3">
            {suggestions.map((word, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(word)}
                className="px-3 py-1 bg-gray-100 rounded-full text-sm hover:bg-gray-200 transition-colors"
              >
                {word}
              </button>
            ))}
          </div>
        )}

        {/* Instructions */}
        <div className="mt-4 text-sm text-gray-600">
          <p>Tips:</p>
          <ul className="list-disc ml-5">
            <li>Type normally and see word predictions appear above</li>
            <li>Click on suggested words to auto-complete</li>
            <li>Common misspellings will be automatically detected</li>
          </ul>
        </div>
      </div>
    </div>
  );
}