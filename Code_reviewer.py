# === 1. Install Required Dependencies ===
!pip install -q openai

# === 2. Imports ===
import openai
import re
import os
from google.colab import files

# === 3. Set Your OpenAI API Key (Insecure for quick demo) ===
openai.api_key = ""  # Replace with your key

# === 4. Upload a Python File ===
print("📁 Upload a Python script to explain/review (.py)")
uploaded = files.upload()
filename = next(iter(uploaded))
print(f"✅ Uploaded: {filename}")

# === 5. Read and Clean Code ===
with open(filename, "r", encoding="utf-8") as f:
    code = f.read()

# Optional cleanup
code = re.sub(r'\n\s*\n', '\n\n', code).strip()

# === 6. Chunk Code by Functions/Classes ===
def split_code_into_chunks(code):
    chunks = []
    current = []
    lines = code.splitlines()
    for line in lines:
        if re.match(r'^\s*(def|class)\s', line) and current:
            chunks.append('\n'.join(current))
            current = [line]
        else:
            current.append(line)
    if current:
        chunks.append('\n'.join(current))
    return chunks

chunks = split_code_into_chunks(code)
print(f"🧠 Split into {len(chunks)} code blocks.")

# === 7. Build and Send Prompt per Chunk ===
system_prompt = "You are a senior Python engineer. Read the code and provide:\n- A short explanation of what it does\n- Possible bugs or improvements\n- Best practice suggestions\n"

for i, chunk in enumerate(chunks):
    print(f"\n=== 🧩 Code Chunk {i+1} ===\n")
    print(chunk[:300] + ("\n..." if len(chunk) > 300 else ""))

    user_prompt = f"Review the following Python code:\n\n```python\n{chunk}\n```"
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_tokens=600
    )

    explanation = response.choices[0].message.content.strip()
    print(f"\n💬 GPT Review:\n{explanation}")
