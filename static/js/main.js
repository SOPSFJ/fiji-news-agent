// Main JavaScript for Fiji News Agent

// Global state
let currentNewsData = null;
let currentSummary = null;
let categoryChart = null;
let sourceChart = null;

// DOM elements
const harvestNewsBtn = document.getElementById('harvestNewsBtn');
const loadSelectedNewsBtn = document.getElementById('loadSelectedNewsBtn');
const generateSummaryBtn = document.getElementById('generateSummaryBtn');
const analyzeTrendsBtn = document.getElementById('analyzeTrendsBtn');
const convertToSpeechBtn = document.getElementById('convertToSpeechBtn');
const newsFileSelect = document.getElementById('newsFileSelect');
const statusMessages = document.getElementById('statusMessages');
const loadingOverlay = document.getElementById('loadingOverlay');
const summaryContent = document.getElementById('summaryContent');
const analysisContent = document.getElementById('analysisContent');
const audioPlayerContainer = document.getElementById('audioPlayerContainer');
const audioPlayer = document.getElementById('audioPlayer');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    addStatusMessage('Application initialized. Ready to harvest news.');
    loadNewsFiles();
    initializeCharts();
    attachEventListeners();
});

// Initialize Chart.js charts
function initializeCharts() {
    // Category chart
    const categoryCtx = document.getElementById('categoryChart').getContext('2d');
    categoryChart = new Chart(categoryCtx, {
        type: 'pie',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: [
                    '#007bff', // Politics
                    '#28a745', // Community
                    '#fd7e14', // Sports
                    '#dc3545', // Crime
                    '#6c757d'  // Others
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });

    // Source chart
    const sourceCtx = document.getElementById('sourceChart').getContext('2d');
    sourceChart = new Chart(sourceCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Articles per Source',
                data: [],
                backgroundColor: '#17a2b8',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
}

// Attach event listeners
function attachEventListeners() {
    // Harvest news button
    harvestNewsBtn.addEventListener('click', function() {
        harvestNews();
    });

    // Load selected news button
    loadSelectedNewsBtn.addEventListener('click', function() {
        const selectedFile = newsFileSelect.value;
        if (selectedFile) {
            loadNews(selectedFile);
        } else {
            addStatusMessage('Please select a news file to load.', 'error');
        }
    });

    // Generate summary button
    generateSummaryBtn.addEventListener('click', function() {
        if (currentNewsData) {
            generateSummary();
        } else {
            addStatusMessage('No news data loaded. Please harvest or load news first.', 'error');
        }
    });

    // Analyze trends button
    analyzeTrendsBtn.addEventListener('click', function() {
        if (currentNewsData) {
            analyzeTrends();
        } else {
            addStatusMessage('No news data loaded. Please harvest or load news first.', 'error');
        }
    });

    // Convert to speech button
    convertToSpeechBtn.addEventListener('click', function() {
        if (currentSummary) {
            convertToSpeech(currentSummary);
        } else {
            addStatusMessage('No summary available. Please generate a summary first.', 'error');
        }
    });

    // Article click handler - delegate to parent
    document.addEventListener('click', function(e) {
        if (e.target.closest('.news-item')) {
            const newsItem = e.target.closest('.news-item');
            const articleData = JSON.parse(newsItem.getAttribute('data-article'));
            showArticleModal(articleData);
        }
    });
}

// Show loading overlay
function showLoading() {
    loadingOverlay.classList.remove('d-none');
}

// Hide loading overlay
function hideLoading() {
    loadingOverlay.classList.add('d-none');
}

// Add a message to the status log
function addStatusMessage(message, type = 'info') {
    const now = new Date();
    const timeString = now.toTimeString().split(' ')[0];
    const statusEntry = document.createElement('div');
    statusEntry.className = 'status-entry';
    
    statusEntry.innerHTML = `
        <span class="status-time">${timeString}</span>
        <span class="status-msg ${type === 'error' ? 'text-danger' : ''}">${message}</span>
    `;
    
    statusMessages.appendChild(statusEntry);
    statusMessages.scrollTop = statusMessages.scrollHeight;
}

// Load the list of available news files
function loadNewsFiles() {
    fetch('/get_news_files')
        .then(response => response.json())
        .then(data => {
            // Clear current options
            while (newsFileSelect.options.length > 1) {
                newsFileSelect.options.remove(1);
            }
            
            // Add new options
            data.files.forEach(file => {
                const option = document.createElement('option');
                option.value = file;
                option.textContent = file;
                newsFileSelect.appendChild(option);
            });
            
            if (data.files.length > 0) {
                addStatusMessage(`Found ${data.files.length} saved news files.`);
            } else {
                addStatusMessage('No saved news files found.');
            }
        })
        .catch(error => {
            console.error('Error loading news files:', error);
            addStatusMessage('Error loading news files: ' + error.message, 'error');
        });
}

// Harvest news from sources
function harvestNews() {
    showLoading();
    addStatusMessage('Harvesting news from sources...');
    
    fetch('/harvest_news', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        if (data.status === 'success') {
            addStatusMessage(`Successfully harvested ${data.message}`);
            currentNewsData = data.data;
            displayNewsData(currentNewsData);
            loadNewsFiles();  // Refresh the file list
            
            // Enable buttons
            generateSummaryBtn.disabled = false;
            analyzeTrendsBtn.disabled = false;
        } else {
            addStatusMessage('Error harvesting news: ' + data.message, 'error');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error harvesting news:', error);
        addStatusMessage('Error harvesting news: ' + error.message, 'error');
    });
}

// Load news from a file
function loadNews(filename) {
    showLoading();
    addStatusMessage(`Loading news file: ${filename}`);
    
    fetch('/load_news', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ filename: filename })
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        if (data.status === 'success') {
            addStatusMessage(`Successfully loaded news file: ${filename}`);
            currentNewsData = data.data;
            displayNewsData(currentNewsData);
            
            // Enable buttons
            generateSummaryBtn.disabled = false;
            analyzeTrendsBtn.disabled = false;
        } else {
            addStatusMessage('Error loading news: ' + data.message, 'error');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error loading news:', error);
        addStatusMessage('Error loading news: ' + error.message, 'error');
    });
}

// Display news data in the UI
function displayNewsData(newsData) {
    // Clear current content
    document.getElementById('politicsNewsList').innerHTML = '';
    document.getElementById('communityNewsList').innerHTML = '';
    document.getElementById('sportsNewsList').innerHTML = '';
    document.getElementById('crimeNewsList').innerHTML = '';
    document.getElementById('othersNewsList').innerHTML = '';
    
    // Count total articles and sources
    let totalArticles = 0;
    let sourceSet = new Set();
    
    // Prepare data for charts
    const categoryLabels = [];
    const categoryData = [];
    const sourceCounts = {};
    
    // Process each category
    for (const category in newsData) {
        const articles = newsData[category];
        totalArticles += articles.length;
        
        // Add to category chart data
        categoryLabels.push(category.charAt(0).toUpperCase() + category.slice(1));
        categoryData.push(articles.length);
        
        // Count sources
        articles.forEach(article => {
            sourceSet.add(article.source);
            
            // For source chart
            if (sourceCounts[article.source]) {
                sourceCounts[article.source]++;
            } else {
                sourceCounts[article.source] = 1;
            }
        });
        
        // Display articles in appropriate tab
        const newsList = document.getElementById(`${category}NewsList`);
        
        if (articles.length === 0) {
            newsList.innerHTML = `<div class="placeholder-text">No ${category} news available.</div>`;
        } else {
            newsList.innerHTML = articles.map(article => `
                <div class="news-item" data-article='${JSON.stringify(article)}'>
                    <div class="d-flex justify-content-between align-items-start">
                        <span class="category-badge category-${category}">${category}</span>
                        <div>
                            <span class="news-source">${article.source}</span>
                            <span class="news-date ms-2">${article.published_date}</span>
                        </div>
                    </div>
                    <h5 class="news-title">${article.title}</h5>
                    <p class="news-summary">${article.summary}</p>
                </div>
            `).join('');
        }
    }
    
    // Update statistics
    document.getElementById('totalArticles').textContent = totalArticles;
    document.getElementById('categoriesCount').textContent = Object.keys(newsData).length;
    document.getElementById('sourcesCount').textContent = sourceSet.size;
    
    // Update charts
    updateCategoryChart(categoryLabels, categoryData);
    
    // Sort sources by count for the bar chart
    const sortedSources = Object.entries(sourceCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5); // Top 5 sources
    
    updateSourceChart(
        sortedSources.map(item => item[0]),
        sortedSources.map(item => item[1])
    );
}

// Update the category chart
function updateCategoryChart(labels, data) {
    categoryChart.data.labels = labels;
    categoryChart.data.datasets[0].data = data;
    categoryChart.update();
}

// Update the source chart
function updateSourceChart(labels, data) {
    sourceChart.data.labels = labels;
    sourceChart.data.datasets[0].data = data;
    sourceChart.update();
}

// Generate a summary of the news
function generateSummary() {
    showLoading();
    addStatusMessage('Generating news summary...');
    
    fetch('/generate_summary', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ news_data: currentNewsData })
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        if (data.status === 'success') {
            addStatusMessage('Summary generated successfully.');
            summaryContent.textContent = data.summary;
            currentSummary = data.summary;
            
            // Enable the text-to-speech button
            convertToSpeechBtn.disabled = false;
        } else {
            addStatusMessage('Error generating summary: ' + data.message, 'error');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error generating summary:', error);
        addStatusMessage('Error generating summary: ' + error.message, 'error');
    });
}

// Analyze trends in the news
function analyzeTrends() {
    showLoading();
    addStatusMessage('Analyzing news trends and threats...');
    
    fetch('/analyze_trends', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ news_data: currentNewsData })
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        if (data.status === 'success') {
            addStatusMessage('Trend analysis completed successfully.');
            displayAnalysis(data.analysis);
        } else {
            addStatusMessage('Error analyzing trends: ' + data.message, 'error');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error analyzing trends:', error);
        addStatusMessage('Error analyzing trends: ' + error.message, 'error');
    });
}

// Display the analysis results
function displayAnalysis(analysis) {
    let html = `<h4>Analysis Generated on ${analysis.timestamp}</h4>`;
    
    // Overview
    html += `<h5 class="mt-3">Overview</h5>`;
    html += `<p>Total Articles: ${analysis.overview.total_articles}</p>`;
    
    // Top topics
    html += `<h5 class="mt-3">Top Topics</h5>`;
    html += `<ul>`;
    analysis.trends.top_topics.forEach(topic => {
        html += `<li>${topic}</li>`;
    });
    html += `</ul>`;
    
    // Common phrases
    html += `<h5 class="mt-3">Common Phrases</h5>`;
    html += `<ul>`;
    analysis.trends.common_phrases.forEach(phrase => {
        html += `<li>${phrase}</li>`;
    });
    html += `</ul>`;
    
    // Emerging threats
    html += `<h5 class="mt-3">Emerging Threats</h5>`;
    if (analysis.emerging_threats.length === 0) {
        html += `<p>No significant threats detected.</p>`;
    } else {
        analysis.emerging_threats.forEach(threat => {
            html += `
                <div class="threat-item">
                    <div class="threat-title">${threat.title}</div>
                    <div class="threat-source">${threat.source} - ${threat.date}</div>
                    <div class="threat-keywords"><strong>Keywords:</strong> ${threat.keywords.join(', ')}</div>
                    <div class="threat-summary"><strong>Summary:</strong> ${threat.summary}</div>
                </div>
            `;
        });
    }
    
    // Mitigation strategies
    html += `<h5 class="mt-3">Mitigation Strategies</h5>`;
    analysis.mitigation_strategies.forEach(strategy => {
        html += `
            <div class="mitigation-strategy">
                <div class="strategy-type">${strategy.type.charAt(0).toUpperCase() + strategy.type.slice(1)}</div>
                <div class="strategy-description">${strategy.description}</div>
                ${strategy.articles ? `<div class="strategy-articles"><small>Based on ${strategy.articles} articles</small></div>` : ''}
            </div>
        `;
    });
    
    analysisContent.innerHTML = html;
}

// Convert summary to speech
function convertToSpeech(text) {
    showLoading();
    addStatusMessage('Converting summary to speech...');
    
    fetch('/text_to_speech', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        if (data.status === 'success') {
            addStatusMessage('Speech conversion completed successfully.');
            
            // Set the audio source and show the player
            audioPlayer.src = `/audio/${data.audio_file.split('/').pop()}`;
            audioPlayerContainer.classList.remove('d-none');
            
            // Play the audio
            audioPlayer.play();
        } else {
            addStatusMessage('Error converting to speech: ' + data.message, 'error');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error converting to speech:', error);
        addStatusMessage('Error converting to speech: ' + error.message, 'error');
    });
}

// Show article modal
function showArticleModal(article) {
    document.getElementById('articleModalLabel').textContent = article.title;
    
    let modalContent = `
        <div class="mb-3">
            <span class="badge bg-secondary">${article.source}</span>
            <span class="badge bg-secondary ms-2">${article.published_date}</span>
            <span class="badge bg-primary ms-2">${article.category}</span>
        </div>
        <div class="article-text mb-4">
            ${article.text.replace(/\n/g, '<br>')}
        </div>
        <div class="article-keywords">
            <strong>Keywords:</strong> ${article.keywords.join(', ')}
        </div>
    `;
    
    document.getElementById('articleModalBody').innerHTML = modalContent;
    document.getElementById('articleSourceLink').href = article.url;
    
    // Show the modal
    const articleModal = new bootstrap.Modal(document.getElementById('articleModal'));
    articleModal.show();
} 