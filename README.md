🎥 Movie Recommender System
This repository contains an implementation of a Content-Based Recommendation System that suggests movies based on user preferences using NLP and vector similarity techniques. The system is optimized for fast inference using preprocessed data and a cosine similarity matrix stored in .pkl files.

📚 Table of Contents
Overview

Recommendation Technique

Features

Technologies Used

Installation

How It Works

Usage Example

Project Structure

Note

🔍 Overview
This project demonstrates a Content-Based Filtering approach to recommending movies by analyzing metadata such as genres, keywords, cast, and crew.

It uses NLP techniques and vector-based similarity to find and suggest movies similar to a user’s input.

💡 Recommendation Technique
Content-Based Filtering
Uses movie attributes like overview, genres, keywords, cast, and crew to build a profile for each movie.

Processes and stems the text using PorterStemmer.

Applies CountVectorizer to convert text to feature vectors.

Computes cosine similarity between vectors to recommend similar movies.

🚀 Features
📄 Text Normalization using NLTK’s PorterStemmer

🧮 Bag-of-Words Vectorization with CountVectorizer

📊 Cosine Similarity Matrix for fast retrieval

🧠 Efficient use of pandas for preprocessing

💾 Saves movie_list.pkl and similarity.pkl for reuse

🌐 Streamlit UI for interactive recommendations

🛠️ Technologies Used
Python: Core language

pandas, NumPy: Data manipulation

nltk: Text preprocessing (PorterStemmer)

scikit-learn: CountVectorizer, cosine similarity

Streamlit: Web app for UI

pickle: Model/data serialization

🔧 Installation
1️⃣ Clone the repository

bash
Copy
Edit
git clone https://github.com/yourusername/movie-recommender-system.git
cd movie-recommender-system
2️⃣ Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
3️⃣ (Optional) Download the datasets from Kaggle:
TMDB Movie Metadata

📌 How It Works
Reads movies.csv and credits.csv from the datasets/ folder.

Merges and processes metadata (genres, cast, overview, etc.).

Stems the text and converts it to feature vectors.

Computes cosine similarity between all movies.

Saves the results as movie_list.pkl and similarity.pkl in the models/ folder.

Loads this data in the Streamlit app for fast recommendations.

🎯 Usage Example
Launch the app:

bash
Copy
Edit
streamlit run app.py
Enter a movie name in the input box.

Instantly get top 5 similar movies with titles and posters.

📁 Project Structure
perl
Copy
Edit
movie-recommender-system/
├── app.py                  # Streamlit app interface
├── recommender/
│   └── model.py            # Core recommendation logic
├── datasets/
│   ├── movies.csv
│   └── credits.csv
├── models/
│   ├── movie_list.pkl      # Serialized movie DataFrame
│   └── similarity.pkl      # Serialized similarity matrix
├── requirements.txt
└── README.md
⚠️ Note
The .pkl files are large and are not committed to GitHub.
Run model.py once to generate them.

Make sure datasets/ folder exists with the proper files before running.

Do not place model files inside venv/ — instead, keep them in models/ and add to .gitignore.