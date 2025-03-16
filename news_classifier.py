import nltk
import re
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class NewsClassifier:
    def __init__(self):
        # Download necessary NLTK data
        try:
            nltk.data.find('corpora/stopwords')
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('stopwords')
            nltk.download('wordnet')
            nltk.download('punkt')
        
        self.categories = ['politics', 'community', 'sports', 'crime', 'others']
        self.model_path = 'data/classifier_model.pkl'
        
        # Initialize or load model
        self.classifier = self._initialize_model()
        
        # Keywords for each category to help with classification
        self.category_keywords = {
            'politics': [
                'government', 'parliament', 'election', 'minister', 'policy', 'political', 
                'prime minister', 'opposition', 'vote', 'legislat', 'party', 'MP', 'democracy',
                'constitutional', 'cabinet', 'president', 'diplomatic', 'international relations'
            ],
            'community': [
                'community', 'festival', 'celebration', 'culture', 'heritage', 'tradition', 
                'charity', 'volunteer', 'donation', 'environment', 'education', 'school', 
                'hospital', 'health', 'development', 'village', 'ceremony', 'church'
            ],
            'sports': [
                'rugby', 'soccer', 'football', 'cricket', 'athletics', 'medal', 'tournament', 
                'championship', 'team', 'player', 'coach', 'olympic', 'win', 'lose', 'match',
                'competition', 'league', 'sport', 'game', 'swimming', 'volleyball', 'netball'
            ],
            'crime': [
                'police', 'arrest', 'crime', 'criminal', 'murder', 'theft', 'robbery', 'court', 
                'trial', 'sentence', 'prison', 'victim', 'suspect', 'investigation', 'corruption',
                'fraud', 'drugs', 'assault', 'illegal', 'violence', 'rape', 'abuse'
            ],
            'others': []  # Default category
        }
    
    def _initialize_model(self):
        """Initialize or load the classifier model"""
        # If a saved model exists, load it
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                return pickle.load(f)
        
        # Otherwise, create a new model
        # This is a basic pipeline - in a real application, 
        # you would train this with labeled data
        return Pipeline([
            ('vectorizer', TfidfVectorizer(stop_words='english')),
            ('classifier', MultinomialNB())
        ])
    
    def _preprocess_text(self, text):
        """Preprocess text for classification"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters
        text = re.sub(r'[^\w\s]', '', text)
        
        # Tokenize
        tokens = nltk.word_tokenize(text)
        
        # Remove stop words and lemmatize
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))
        tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
        
        return ' '.join(tokens)
    
    def _rule_based_classification(self, article):
        """Use keyword matching to classify the article"""
        processed_text = self._preprocess_text(article["text"] + " " + article["title"])
        
        # Calculate scores for each category
        scores = {}
        for category, keywords in self.category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in processed_text)
            scores[category] = score
        
        # Check if any category has a clear signal
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        else:
            return "others"
    
    def categorize(self, articles):
        """Categorize a list of articles into defined categories"""
        categorized = {cat: [] for cat in self.categories}
        
        for article in articles:
            # Use rule-based classification for now
            category = self._rule_based_classification(article)
            article["category"] = category
            categorized[category].append(article)
        
        return categorized 