import os
import json
import datetime
from flask import Flask, render_template, request, jsonify, send_file
from news_harvester import NewsScraper
from news_classifier import NewsClassifier
from news_analyzer import NewsAnalyzer
from text_to_speech import TextToSpeech

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize components
news_scraper = NewsScraper()
news_classifier = NewsClassifier()
news_analyzer = NewsAnalyzer()
text_to_speech = TextToSpeech()

# Create data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/harvest_news', methods=['POST'])
def harvest_news():
    try:
        articles = news_scraper.harvest()
        categorized_articles = news_classifier.categorize(articles)
        
        # Save the categorized news to a JSON file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/fiji_news_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(categorized_articles, f, indent=4)
        
        return jsonify({
            "status": "success",
            "message": f"Harvested {len(articles)} articles",
            "data": categorized_articles
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/get_news_files', methods=['GET'])
def get_news_files():
    files = [f for f in os.listdir('data') if f.startswith('fiji_news_')]
    return jsonify({"files": files})

@app.route('/load_news', methods=['POST'])
def load_news():
    filename = request.json.get('filename')
    if not filename:
        return jsonify({"status": "error", "message": "No filename provided"}), 400
    
    try:
        with open(f"data/{filename}", 'r', encoding='utf-8') as f:
            news_data = json.load(f)
        return jsonify({"status": "success", "data": news_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    try:
        news_data = request.json.get('news_data')
        if not news_data:
            return jsonify({"status": "error", "message": "No news data provided"}), 400
        
        summary = news_analyzer.generate_summary(news_data)
        
        # Save the summary
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/summary_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        return jsonify({
            "status": "success",
            "summary": summary,
            "filename": filename
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/analyze_trends', methods=['POST'])
def analyze_trends():
    try:
        news_data = request.json.get('news_data')
        if not news_data:
            return jsonify({"status": "error", "message": "No news data provided"}), 400
        
        analysis = news_analyzer.analyze_trends(news_data)
        
        # Save the analysis
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/analysis_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=4)
        
        return jsonify({
            "status": "success",
            "analysis": analysis,
            "filename": filename
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/text_to_speech', methods=['POST'])
def convert_to_speech():
    try:
        text = request.json.get('text')
        if not text:
            return jsonify({"status": "error", "message": "No text provided"}), 400
        
        audio_file = text_to_speech.convert(text)
        
        return jsonify({
            "status": "success",
            "audio_file": audio_file
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_file(f"data/{filename}", mimetype="audio/mp3")

if __name__ == '__main__':
    app.run(debug=True) 