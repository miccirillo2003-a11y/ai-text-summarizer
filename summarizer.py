import anthropic

PROMPTS = {
    "structured": """You are a precise summarization assistant. Given the text below, respond with a structured summary in this exact markdown format:

## [Title — infer a clear, descriptive title from the content]

**Summary**
A 2-3 sentence overview of the main argument or topic.

**Key Takeaways**
- Takeaway one
- Takeaway two
- Takeaway three
- (add more if needed, but keep each one concise)

Text to summarize:
{text}""",

    "paragraph": """You are a precise summarization assistant. Summarize the following text in a single clear, well-written paragraph of 3-5 sentences. Capture the main argument and most important points. Do not use bullet points or headers.

Text to summarize:
{text}""",

    "bullets": """You are a precise summarization assistant. Summarize the following text as a concise bullet-point list. Each bullet should capture one distinct idea or fact. Use 4-8 bullets. Be specific, not vague.

Text to summarize:
{text}""",
}


def summarize_text(text: str, format: str = "structured") -> str:
    client = anthropic.Anthropic()

    # Truncate very long texts to avoid token limits
    max_chars = 12000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[Text truncated for length]"

    prompt = PROMPTS[format].format(text=text)

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text
