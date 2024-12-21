import gradio as gr
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import nltk
import torch
from urllib.parse import urlparse


try:
    nltk.download('punkt')
except Exception as e:
    print(f"Error downloading NLTK data: {e}")


try:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)  # I have used BART-Large-CNN, you can use any model as per your preference like gpt2, t5, etc
    #summarizer = pipeline("summarization", model="openai-community/gpt2", device=device) 
except Exception as e:
    print(f"Error loading model: {e}")
    summarizer = None

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def extract_article_text(url):
    """Extract article text using BeautifulSoup instead of newspaper3k"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements --- to avoid the model to get distract and generate wrong summary
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            tag.decompose()
        
 
        article_text = ""


        main_content = soup.find('article') or soup.find(class_=['article', 'post-content', 'entry-content', 'content'])
        
        if main_content:
            paragraphs = main_content.find_all('p')
        else:
            # Fallback to all paragraphs if no article container found
            paragraphs = soup.find_all('p')
        
        # Extract text from paragraphs
        article_text = ' '.join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 50])
        
        return article_text
    
    except Exception as e:
        raise Exception(f"Error fetching article: {str(e)}")

def extract_and_summarize(url):
    if not url or not url.strip():
        return "Please enter a valid URL"
    
    if not is_valid_url(url):
        return "Please enter a valid URL starting with http:// or https://"
    
    try:
        # Extract article text
        text = extract_article_text(url)
        
        if not text:
            return "Could not extract text from the article. Please make sure it's a valid news article."
            
        # Split text into chunks if it's too long  --- it will divide the text into 1024 tokens
        max_chunk_length = 1024
        chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]
        
        # Summarize each chunk --- each small part will be summarized indiviually
        summaries = []
        for chunk in chunks:
            if len(chunk.strip()) > 100:  # Only summarize substantial chunks
                try:
                    summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
                    summaries.append(summary[0]['summary_text'])
                except Exception as e:
                    print(f"Error summarizing chunk: {e}")
                    continue
        
        if not summaries:
            return "Could not generate summary. Please try a different article."
            
        # Combine all summaries --- we need to combine all summaries to get a complete summary
        final_summary = " ".join(summaries)
        
        return final_summary
        
    except Exception as e:
        return f"Error processing article: {str(e)}"

# Create Gradio interface
demo = gr.Interface(
    fn=extract_and_summarize,
    inputs=gr.Textbox(
        label="Enter News Article URL",
        placeholder="https://...",
        info="Enter a news article URL to get a summary"
    ),
    outputs=gr.Textbox(label="Summary", lines=5),
    title="📰 News Article Summarizer",
    description="""This app creates concise summaries of news articles using AI.
Simply paste a URL of a news article and get a summary!
⏳ Processing Time: The summarization process typically takes 30-60 seconds, depending on article length.
📊 Status Indicator: Look for "Processing" in the output box - this indicates the model is actively generating your summary.
✨ Quality Assurance: Please wait for the process to complete for the best results.""",
    examples=[
        ["https://www.bbc.com/sport/football/articles/cvgxmzy86e4o"],
        ["https://globalsouthworld.com/article/biden-approves-571-million-in-defense-support-for-taiwan"]
    ],
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    demo.launch()
