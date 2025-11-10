# Vibe Matcher (Mini AI Recommendation System)

This project is a lightweight vibe-based recommendation system using text embeddings + cosine similarity.  
User inputs a *vibe query* (e.g., "energetic urban chic"), and the system returns the top-3 matching fashion items.

---

### 🔗 Open in Google Colab
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ITSYOURAHLAWAT/vibe-matcher-ai/blob/main/vibe_matcher.ipynb)

---

### 🧠 Why AI at Nexora?

Nexora focuses on translating human expression (vibes, moods, identity) into structured product relevance. Fashion discovery is emotional, not technical. AI embeddings convert natural language style cues directly into vector meaning. This prototype shows how a lightweight embedding + cosine similarity model can power human-centered personalization at scale.

---

### ⚙️ How It Works
1. Mock fashion catalog (5–10 products)
2. Encode product descriptions using OpenAI embeddings
3. Encode user vibe query
4. Calculate cosine similarity
5. Return Top-3 matching items
6. Evaluate match quality (≥ 0.70 = good)
7. Plot latency for 3 test queries

---

### 📦 Requirements
```bash
pip install openai pandas scikit-learn matplotlib
