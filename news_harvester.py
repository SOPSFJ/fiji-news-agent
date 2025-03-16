import requests
from bs4 import BeautifulSoup
import newspaper
from newspaper import Article
import datetime
import re
import time
import random

class NewsScraper:
    def __init__(self):
        # List of Fiji news sources
        self.sources = [
            {"name": "Fiji Times", "url": "https://www.fijitimes.com"},
            {"name": "Fiji Sun", "url": "https://fijisun.com.fj"},
            {"name": "Fiji Village", "url": "https://www.fijivillage.com"},
            {"name": "FBC News", "url": "https://www.fbcnews.com.fj"},
            {"name": "Islands Business", "url": "https://www.islandsbusiness.com/category/fiji/"}
        ]
        
        # User agent to avoid being blocked
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def harvest(self):
        """Harvest news articles from all sources"""
        all_articles = []
        
        for source in self.sources:
            try:
                print(f"Scraping {source['name']}...")
                articles = self._scrape_source(source)
                all_articles.extend(articles)
                # Sleep to avoid overloading the servers
                time.sleep(random.uniform(1, 3))
            except Exception as e:
                print(f"Error scraping {source['name']}: {str(e)}")
                
        return all_articles
    
    def _scrape_source(self, source):
        """Scrape articles from a single source"""
        articles = []
        try:
            # Build a newspaper source
            news_source = newspaper.build(
                source['url'], 
                memoize_articles=False,
                fetch_images=False,
                headers=self.headers
            )
            
            # Get all article URLs
            for article in news_source.articles:
                try:
                    article_data = self._extract_article(article.url, source['name'])
                    if article_data and self._is_fiji_related(article_data):
                        articles.append(article_data)
                        
                        # Limit to avoid too many requests during development
                        if len(articles) >= 10:  # Adjustable limit
                            break
                            
                except Exception as article_e:
                    print(f"Error extracting article {article.url}: {str(article_e)}")
                
                # Be gentle with the servers
                time.sleep(random.uniform(0.5, 1.5))
                
        except Exception as e:
            print(f"Error in _scrape_source for {source['name']}: {str(e)}")
            
        return articles
    
    def _extract_article(self, url, source_name):
        """Extract data from a single article"""
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()  # This will generate keywords and summary
            
            # Skip if article has no content
            if not article.text or len(article.text) < 100:
                return None
                
            return {
                "title": article.title,
                "url": url,
                "source": source_name,
                "published_date": article.publish_date.strftime("%Y-%m-%d") if article.publish_date else datetime.datetime.now().strftime("%Y-%m-%d"),
                "text": article.text,
                "summary": article.summary,
                "keywords": article.keywords,
                "category": None  # Will be filled by the classifier
            }
        except Exception as e:
            print(f"Error in _extract_article for {url}: {str(e)}")
            return None
    
    def _is_fiji_related(self, article):
        """Check if the article is related to Fiji"""
        fiji_keywords = ["fiji", "fijian", "suva", "nadi", "pacific island", "viti levu", "vanua levu"]
        
        # Check title
        if any(keyword in article["title"].lower() for keyword in fiji_keywords):
            return True
            
        # Check text
        if any(keyword in article["text"].lower() for keyword in fiji_keywords):
            return True
            
        # Check keywords
        if any(keyword in " ".join(article["keywords"]).lower() for keyword in fiji_keywords):
            return True
            
        return False 