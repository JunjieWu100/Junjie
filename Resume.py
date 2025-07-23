# === 1. Install Required Libraries ===
!pip install -q PyMuPDF sentence-transformers

# === 2. Import Libraries ===
import fitz  # PyMuPDF
import re
from sentence_transformers import SentenceTransformer, util
from google.colab import files

# === 3. Upload Resume ===
print("📁 Upload your resume PDF")
uploaded = files.upload()
filename = next(iter(uploaded))
print(f"✅ Uploaded: {filename}")

# === 4. Extract Resume Text ===
doc = fitz.open(filename)
resume_text = ""
for page in doc:
    resume_text += page.get_text()

resume_text = re.sub(r'\s+', ' ', resume_text).strip()
print("✅ Resume text extracted.\n")

# === 5. Paste Job Description ===
print("Paste your job description below (press Enter twice to finish):")
job_description = ""
while True:
    try:
        line = input()
        if line.strip() == "":
            break
        job_description += line + " "
    except EOFError:
        break

job_description = re.sub(r'\s+', ' ', job_description).strip()

# === 6. Use BERT for Semantic Similarity ===
model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight, fast, accurate

embeddings = model.encode([job_description, resume_text], convert_to_tensor=True)
similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

# === 7. Display Match Score ===
match_percentage = round(similarity * 100, 2)
print(f"\n🤖 Semantic Resume Match Score: {match_percentage}%")
