# 📝 AI Text Summarizer

A Streamlit web app that summarizes text using the Anthropic Claude API. Supports pasting text, scraping URLs, and uploading PDF or `.txt` files.

## Features

- **Three input methods**: paste text, enter a URL, or upload a file (PDF / .txt)
- **Three output formats**: structured (title + summary + bullets), paragraph, or bullet points only
- Powered by Claude via the Anthropic API

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ai-text-summarizer.git
cd ai-text-summarizer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your API key

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_api_key_here
```

Get a key at [console.anthropic.com](https://console.anthropic.com).

### 4. Run the app

```bash
streamlit run app.py
```

## Project Structure

```
ai-text-summarizer/
├── app.py           # Streamlit UI
├── summarizer.py    # Claude API integration
├── scraper.py       # URL scraping
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Notes

- Long texts are automatically truncated to ~12,000 characters before sending to Claude
- URL scraping works best on article-style pages; paywalled or JS-heavy sites may not extract well
- Never commit your `.env` file — it's already in `.gitignore`

## License

MIT
