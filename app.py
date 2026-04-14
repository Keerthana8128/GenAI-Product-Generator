import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Add it to your .env file.")

client = OpenAI(api_key=api_key)


def generate_description(fact_sheet: str) -> str:
    prompt = f"""
You are an AI assistant generating product descriptions for a retail website.

Requirements:
- Use a professional and clear tone
- Focus on materials, construction, and durability
- Highlight affordability, cost-effectiveness, and value for money
- Appeal to budget-conscious customers without making the product sound cheap

Output format:
- Return ONLY raw HTML
- DO NOT include ```html or ``` or markdown formatting
- Start directly with <div>
- Include every 7-character Product ID found in the input
- After the description, add a table titled 'Product Dimensions'
- The dimensions table must have exactly 2 columns:
  1. Dimension
  2. Measurement
- Show measurements in inches only

Technical specifications:
```{fact_sheet}```
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output[0].content[0].text


def save_html_file(content: str, filename: str = "output.html") -> None:
    html_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Product Description</title>
</head>
<body>
{content}
</body>
</html>
"""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_page)


if __name__ == "__main__":
    print("Enter product details. Press Enter on an empty line when finished:\n")

    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)

    fact_sheet = "\n".join(lines)

    if not fact_sheet.strip():
        print("No product details were entered.")
    else:
        result = generate_description(fact_sheet)
        save_html_file(result)
        print("\nGenerated Output:\n")
        print(result)
        print("\nHTML file saved as output.html")