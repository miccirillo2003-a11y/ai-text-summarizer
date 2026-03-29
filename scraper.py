import httpx
from bs4 import BeautifulSoup


def scrape_url(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; AI-Summarizer/1.0)"
        )
    }

    response = httpx.get(url, headers=headers, follow_redirects=True, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove noise elements
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
        tag.decompose()

    # Try to find the main content block
    main = (
        soup.find("article")
        or soup.find("main")
        or soup.find(id="content")
        or soup.find(class_="content")
        or soup.body
    )

    if main:
        text = main.get_text(separator="\n", strip=True)
    else:
        text = soup.get_text(separator="\n", strip=True)

    # Clean up excessive blank lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)
