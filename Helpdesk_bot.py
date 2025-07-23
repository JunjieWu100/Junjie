# === 1. Install Required Libraries ===
!pip install -q openai tiktoken

# === 2. Imports ===
import openai
import re
from google.colab import files

# === 3. Set Your OpenAI API Key (⚠️ quick testing only) ===
openai.api_key = ""  # Replace with your actual API key

# === 4. Upload Helpdesk Text Files ===
print("📁 Upload your helpdesk documents (txt files preferred)")
uploaded = files.upload()

docs = []
for fname in uploaded:
    with open(fname, "r", encoding="utf-8") as f:
        docs.append(f.read())

# === 5. Combine and Clean the Corpus ===
corpus_text = "\n\n".join(docs)
corpus_text = re.sub(r'\s+', ' ', corpus_text)

# === 6. Ask a Helpdesk Question ===
print("❓ Type your helpdesk question:")
question = input()

# === 7. Build Prompt with Context ===
prompt = f"""
You are a helpful internal helpdesk assistant for a company.

Only use the following internal documentation to answer. If the answer cannot be found, say "Sorry, I couldn't find that."

INTERNAL DOCUMENTS:
\"\"\"{corpus_text}\"\"\"

QUESTION:
{question}

ANSWER:
"""

# === 8. OpenAI API Call Using New Syntax ===
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.2,
    max_tokens=500
)

# === 9. Display the Answer ===
print("\n🤖 Helpdesk Response:")
print(response.choices[0].message.content.strip())
