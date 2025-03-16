# Fiji News Intelligence Agent

A Windows application for harvesting, categorizing, and analyzing news about Fiji.

## Features

- **News Harvesting**: Automatically collects news articles from major Fiji news sources
- **News Categorization**: Classifies articles into politics, community, sports, crime, and other categories
- **Summary Generation**: Creates comprehensive summaries of collected news
- **Trend Analysis**: Identifies emerging trends, potential threats, and suggests mitigation strategies
- **Audio Conversion**: Converts news summaries into speech for easy consumption

## Installation

### Prerequisites

- Python 3.8 or higher
- Windows 10 operating system

### Setup

1. Clone or download this repository:
   ```
   git clone https://github.com/yourusername/fiji-news-agent.git
   cd fiji-news-agent
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create necessary directories:
   ```
   mkdir -p data
   ```

## Usage

1. Start the application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Use the application:
   - Click "Harvest News" to collect the latest news about Fiji
   - View news articles categorized by topic
   - Generate a summary of all collected news
   - Analyze trends and identify potential threats
   - Convert summaries to audio for listening

## News Sources

The application collects news from the following Fiji sources:
- Fiji Times
- Fiji Sun 
- Fiji Village
- FBC News
- Islands Business

## Technical Details

- **Backend**: Python with Flask web framework
- **Frontend**: HTML, CSS, JavaScript with Bootstrap 5
- **News Harvesting**: Newspaper3k and BeautifulSoup4
- **Text Analysis**: NLTK and scikit-learn
- **Text-to-Speech**: pyttsx3 (offline) and gTTS (online)

## Customization

You can customize the application by:

1. **Adding News Sources**: Edit the `sources` list in `news_harvester.py`
2. **Modifying Categories**: Update the `categories` list and `category_keywords` in `news_classifier.py`
3. **Enhancing Analysis**: Extend the analysis capabilities in `news_analyzer.py`

## Data Storage

The application stores data in the following formats:
- Harvested news: JSON files in the `data` directory
- Summaries: Text files in the `data` directory
- Analyses: JSON files in the `data` directory
- Audio files: MP3 files in the `data` directory

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Newspaper3k for article extraction
- NLTK for natural language processing
- Flask for the web framework
- Bootstrap for the UI components 