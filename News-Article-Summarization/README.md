---
title: News Article Summarizer
emoji: 📰
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 5.9.1
app_file: app.py
pinned: false
license: mit
---
# 📰 News Article Summarizer

A powerful and efficient news article summarization tool powered by BART-Large-CNN model. This application automatically extracts and summarizes news articles from URLs, making it easier to quickly grasp the key points of any news article.

## 🚀 Features

- **Smart Article Extraction**: Automatically extracts article content from news URLs
- **Advanced Summarization**: Uses BART-Large-CNN model for high-quality summaries
- **Chunk Processing**: Handles long articles by processing them in chunks
- **Clean Output**: Removes unwanted elements like ads and navigation for better results
- **User-Friendly Interface**: Simple Gradio interface for easy interaction

## 🛠️ Technology Stack

- **Python**: Core programming language
- **BART-Large-CNN**: State-of-the-art summarization model
- **Gradio**: Web interface framework
- **BeautifulSoup4**: HTML parsing and content extraction
- **PyTorch**: Deep learning framework
- **Transformers**: Hugging Face transformers library

## 📋 Requirements

```
gradio==5.9.1
transformers
torch
beautifulsoup4
requests
nltk
```

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Use the App**:
   - Open the provided URL in your browser
   - Paste a news article URL
   - Wait for the summary (processing time depends on article length)
   - Get your concise summary!

## 💡 How It Works

1. **Article Extraction**:
   - Fetches article content from the provided URL
   - Removes unwanted elements (ads, navigation, etc.)
   - Extracts main article text

2. **Text Processing**:
   - Splits long articles into manageable chunks (1024 tokens each)
   - Cleans and prepares text for summarization

3. **Summarization**:
   - Uses BART-Large-CNN model for each chunk
   - Combines summaries for a coherent final output
   - Provides clean, readable summaries

## ⚠️ Notes

- Processing time varies based on article length
- Look for "Running..." indicator while processing
- Wait patiently for best results
- Model can be changed to T5 or GPT-2 for different results

## 🔄 Example Usage

```python
# Example URLs:
https://www.bbc.com/sport/football/articles/cvgxmzy86e4o
https://globalsouthworld.com/article/biden-approves-571-million-in-defense-support-for-taiwan
```

## 🤝 Contributing

Feel free to:
- Open issues
- Suggest improvements
- Submit pull requests

## 📝 License

This project is open source and available under the MIT License.
