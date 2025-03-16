import nltk
import re
import datetime
from collections import Counter, defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder

class NewsAnalyzer:
    def __init__(self):
        # Download necessary NLTK data
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
            nltk.download('punkt')
        
        self.stop_words = set(stopwords.words('english'))
        
        # Keywords to monitor for potential threats
        self.threat_keywords = [
            'protest', 'riot', 'unrest', 'violence', 'conflict', 'strike', 'coup',
            'demonstration', 'crisis', 'tension', 'opposition', 'controversial',
            'disaster', 'emergency', 'threat', 'attack', 'warning', 'security',
            'concern', 'issue', 'problem', 'critical', 'serious', 'dispute',
            'political instability', 'economic crisis', 'corruption', 'scandal'
        ]
    
    def generate_summary(self, news_data):
        """Generate a comprehensive summary of the news articles"""
        summary = []
        
        # Add header
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        summary.append(f"FIJI NEWS SUMMARY - Generated on {now}\n")
        
        # Summary by category
        for category, articles in news_data.items():
            if articles:
                summary.append(f"\n== {category.upper()} NEWS ==")
                summary.append(f"Number of articles: {len(articles)}")
                
                # Get top sources
                sources = Counter([article['source'] for article in articles])
                top_sources = sources.most_common()
                summary.append("Sources: " + ", ".join([f"{source} ({count})" for source, count in top_sources]))
                
                # Extract key topics using frequent words
                all_text = " ".join([article['text'] for article in articles])
                topics = self._extract_key_topics(all_text, 5)
                summary.append("Key topics: " + ", ".join(topics))
                
                # Recent headlines
                summary.append("\nRecent headlines:")
                for article in articles[:5]:  # Top 5 articles
                    summary.append(f"- {article['title']} ({article['source']})")
                
                # Most important article summary
                if articles:
                    longest_article = max(articles, key=lambda x: len(x['text']))
                    summary.append("\nFeatured article:")
                    summary.append(f"Title: {longest_article['title']}")
                    summary.append(f"Source: {longest_article['source']}")
                    summary.append(f"Date: {longest_article['published_date']}")
                    summary.append(f"Summary: {longest_article['summary']}")
        
        # Overall statistics
        total_articles = sum(len(articles) for articles in news_data.values())
        summary.append(f"\n== OVERALL STATISTICS ==")
        summary.append(f"Total articles analyzed: {total_articles}")
        
        category_counts = {category: len(articles) for category, articles in news_data.items()}
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        summary.append("Articles by category:")
        for category, count in sorted_categories:
            if count > 0:
                percentage = (count / total_articles) * 100
                summary.append(f"- {category.capitalize()}: {count} ({percentage:.1f}%)")
        
        return "\n".join(summary)
    
    def analyze_trends(self, news_data):
        """Analyze trends, identify emerging threats, and suggest mitigation strategies"""
        analysis = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "overview": {},
            "trends": {},
            "emerging_threats": [],
            "mitigation_strategies": []
        }
        
        # Flatten all articles for overall analysis
        all_articles = []
        for category, articles in news_data.items():
            all_articles.extend(articles)
        
        # Overall statistics
        analysis["overview"]["total_articles"] = len(all_articles)
        analysis["overview"]["articles_by_category"] = {cat: len(arts) for cat, arts in news_data.items()}
        analysis["overview"]["articles_by_source"] = dict(Counter([a["source"] for a in all_articles]).most_common())
        
        # Find trends
        # 1. Common topics
        all_text = " ".join([a["text"] for a in all_articles])
        analysis["trends"]["top_topics"] = self._extract_key_topics(all_text, 10)
        
        # 2. Common phrases
        analysis["trends"]["common_phrases"] = self._extract_common_phrases(all_text, 10)
        
        # 3. Trends by category
        analysis["trends"]["category_topics"] = {}
        for category, articles in news_data.items():
            if articles:
                category_text = " ".join([a["text"] for a in articles])
                analysis["trends"]["category_topics"][category] = self._extract_key_topics(category_text, 5)
        
        # Identify potential emerging threats
        analysis["emerging_threats"] = self._identify_threats(all_articles)
        
        # Generate mitigation strategies based on threats
        analysis["mitigation_strategies"] = self._generate_mitigation_strategies(analysis["emerging_threats"])
        
        return analysis
    
    def _extract_key_topics(self, text, num_topics=5):
        """Extract key topics from text using word frequency"""
        # Tokenize and filter stop words
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalpha() and word not in self.stop_words and len(word) > 3]
        
        # Get most common words
        fdist = FreqDist(words)
        return [word for word, _ in fdist.most_common(num_topics)]
    
    def _extract_common_phrases(self, text, num_phrases=5):
        """Extract common phrases (bigrams) from text"""
        # Tokenize and filter stop words
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalpha() and word not in self.stop_words]
        
        # Find bigrams
        bigram_measures = BigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(words)
        finder.apply_freq_filter(3)  # Filter out bigrams that appear less than 3 times
        
        # Get top bigrams by PMI (Pointwise Mutual Information)
        bigrams = finder.nbest(bigram_measures.pmi, num_phrases)
        return [" ".join(bigram) for bigram in bigrams]
    
    def _identify_threats(self, articles):
        """Identify potential emerging threats from news articles"""
        threats = []
        
        # Scan all articles for threat keywords
        for article in articles:
            threat_matches = []
            for keyword in self.threat_keywords:
                if keyword in article['text'].lower() or keyword in article['title'].lower():
                    threat_matches.append(keyword)
            
            if threat_matches:
                threats.append({
                    "title": article['title'],
                    "source": article['source'],
                    "date": article['published_date'],
                    "url": article['url'],
                    "keywords": threat_matches,
                    "summary": article['summary']
                })
        
        return threats
    
    def _generate_mitigation_strategies(self, threats):
        """Generate mitigation strategies based on identified threats"""
        strategies = []
        
        if not threats:
            strategies.append({
                "type": "general",
                "description": "No significant threats detected. Continue monitoring the situation."
            })
            return strategies
        
        # Count threat keywords to identify main concerns
        threat_keyword_counts = defaultdict(int)
        for threat in threats:
            for keyword in threat['keywords']:
                threat_keyword_counts[keyword] += 1
        
        # Generate strategies for top threats
        top_threats = sorted(threat_keyword_counts.items(), key=lambda x: x[1], reverse=True)
        
        threat_strategies = {
            "protest": "Monitor social media and increase community engagement to address concerns.",
            "riot": "Coordinate with security forces and implement emergency response protocols.",
            "unrest": "Establish communication channels with community leaders to ease tensions.",
            "violence": "Increase security presence in affected areas and facilitate dialogue.",
            "conflict": "Identify key stakeholders and initiate mediation processes.",
            "strike": "Engage with labor representatives to address grievances.",
            "coup": "Monitor military movements and secure key government facilities.",
            "demonstration": "Ensure peaceful assembly rights while maintaining public order.",
            "crisis": "Activate crisis management team and develop contingency plans.",
            "tension": "Promote intercommunal dialogue and peace-building initiatives.",
            "disaster": "Prepare emergency services and coordinate humanitarian assistance.",
            "emergency": "Activate emergency response protocols and allocate resources.",
            "corruption": "Strengthen transparency measures and anti-corruption initiatives.",
            "scandal": "Implement communication strategy to address public concerns."
        }
        
        # Add specific strategies for top threats
        for keyword, count in top_threats[:3]:
            if keyword in threat_strategies:
                strategies.append({
                    "type": keyword,
                    "description": threat_strategies[keyword],
                    "articles": count
                })
        
        # Add a general strategy
        strategies.append({
            "type": "general",
            "description": "Continue monitoring news sources and update analysis regularly."
        })
        
        return strategies 