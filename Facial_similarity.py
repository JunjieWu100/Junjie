# 📦 INSTALL + EXECUTE ALL IN ONE CELL
!pip install deepface -q

from google.colab import files
from deepface import DeepFace

# Upload both images
print("Upload FIRST face image:")
img1_path = list(files.upload().keys())[0]

print("Upload SECOND face image:")
img2_path = list(files.upload().keys())[0]

# ✅ Compare using a stable model: Facenet
result = DeepFace.verify(img1_path, img2_path, model_name="Facenet", enforce_detection=True)
similarity = 100 - result["distance"] * 100
status = "✅ MATCH" if result["verified"] else "❌ NOT a match"

print(f"{status}: {similarity:.2f}% similar")
