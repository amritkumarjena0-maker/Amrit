


import re
import json
from collections import defaultdict, Counter
from pathlib import Path
import pickle

def demonstrate_list_indexing():
    """Show basic list indexing operations"""
    print("=== LIST INDEXING ===")
    fruits = ["apple", "banana", "cherry", "date", "elderberry"]
    
    print(f"Original list: {fruits}")
    print(f"First item (index 0): {fruits[0]}")
    print(f"Last item (index -1): {fruits[-1]}")
    print(f"Third item (index 2): {fruits[2]}")
    print(f"Slice [1:4]: {fruits[1:4]}")
    print(f"Every second item [::2]: {fruits[::2]}")
    print()

def demonstrate_string_indexing():
    """Show string indexing operations"""
    print("=== STRING INDEXING ===")
    text = "Hello, World!"
    
    print(f"Original string: '{text}'")
    print(f"First character: '{text[0]}'")
    print(f"Last character: '{text[-1]}'")
    print(f"Substring [0:5]: '{text[0:5]}'")
    print(f"Reverse string [::-1]: '{text[::-1]}'")
    print()

class TextIndex:
    """Advanced text indexing with multiple features"""
    
    def __init__(self):
        self.word_positions = defaultdict(list)
        self.word_counts = Counter()
        self.original_text = ""
    
    def build_index(self, text):
        """Build comprehensive index from text using regex"""
        self.original_text = text
        
        # Use regex to extract words (more robust than split)
        words = re.findall(r'\b\w+\b', text.lower())
        
        for position, word in enumerate(words):
            self.word_positions[word].append(position)
            self.word_counts[word] += 1
    
    def search(self, term):
        """Search for a term in the index"""
        term = term.lower()
        if term in self.word_positions:
            positions = self.word_positions[term]
            count = self.word_counts[term]
            print(f"'{term}' found {count} time(s) at positions: {positions}")
            return positions
        else:
            print(f"'{term}' not found in index")
            return []
    
    def get_most_common(self, n=5):
        """Get the n most common words"""
        return self.word_counts.most_common(n)
    
    def get_context(self, word, context_size=2):
        """Get words around the search term"""
        word = word.lower()
        positions = self.word_positions.get(word, [])
        words = re.findall(r'\b\w+\b', self.original_text.lower())
        
        contexts = []
        for pos in positions:
            start = max(0, pos - context_size)
            end = min(len(words), pos + context_size + 1)
            context = ' '.join(words[start:end])
            contexts.append(context)
        
        return contexts
    
    def save_to_json(self, filename):
        """Save index to JSON file"""
        data = {
            'word_positions': dict(self.word_positions),
            'word_counts': dict(self.word_counts),
            'original_text': self.original_text
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Index saved to {filename}")
    
    def load_from_json(self, filename):
        """Load index from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        self.word_positions = defaultdict(list, data['word_positions'])
        self.word_counts = Counter(data['word_counts'])
        self.original_text = data['original_text']
        print(f"Index loaded from {filename}")
    
    def save_to_pickle(self, filename):
        """Save index to pickle file (faster, binary)"""
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
        print(f"Index pickled to {filename}")
    
    @staticmethod
    def load_from_pickle(filename):
        """Load index from pickle file"""
        with open(filename, 'rb') as f:
            index = pickle.load(f)
        print(f"Index loaded from {filename}")
        return index

def main():
    # Demonstrate basic indexing
    demonstrate_list_indexing()
    demonstrate_string_indexing()
    
    # Create advanced text index
    print("=== ADVANCED TEXT INDEX ===")
    sample_text = """
    Python is great. Python is versatile and powerful. 
    Programming with Python is fun! Python developers love Python.
    The Python community is amazing. Python, Python, Python!
    """
    
    index = TextIndex()
    index.build_index(sample_text)
    
    print(f"Sample text: '{sample_text.strip()}'")
    print()
    
    # Show word positions
    print("Word Index (sample):")
    for word in ['python', 'is', 'programming']:
        if word in index.word_positions:
            print(f"  {word}: {index.word_positions[word]}")
    print()
    
    # Search with counts
    print("=== SEARCHING WITH COUNTS ===")
    index.search("python")
    index.search("is")
    index.search("java")
    print()
    
    # Most common words
    print("=== MOST COMMON WORDS ===")
    common = index.get_most_common(5)
    for word, count in common:
        print(f"  {word}: {count} occurrences")
    print()
    
    # Context search
    print("=== CONTEXT SEARCH ===")
    contexts = index.get_context("python", context_size=2)
    print(f"Contexts for 'python':")
    for i, ctx in enumerate(contexts, 1):
        print(f"  {i}. ...{ctx}...")
    print()
    
    # Save and load demo
    print("=== SAVE/LOAD DEMO ===")
    try:
        index.save_to_json("text_index.json")
        print("✓ JSON save successful")
        
        index.save_to_pickle("text_index.pkl")
        print("✓ Pickle save successful")
        
        # Clean up demo files
        Path("text_index.json").unlink(missing_ok=True)
        Path("text_index.pkl").unlink(missing_ok=True)
        print("✓ Demo files cleaned up")
    except Exception as e:
        print(f"Note: File operations require write permissions: {e}")

if __name__ == "__main__":
    main()
