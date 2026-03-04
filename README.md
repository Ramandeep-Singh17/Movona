# 🎬 Movona – AI Movie Recommendation System

Movona is an AI-powered movie recommendation system that helps users discover movies they might enjoy.
The system allows users to search for movies, view detailed information, and receive intelligent recommendations based on similarity.

The project uses a **FastAPI backend** for handling recommendation logic and a **Streamlit frontend** for an interactive user interface.

---

## 🚀 Live Demo

🔗 https://movona-ramandeep.streamlit.app

---

## ✨ Features

* 🔎 Search movies using keywords
* 🎬 View movie details including overview, release date, and genres
* ⭐ Get similar movie recommendations
* 🎥 Explore more movies with genre-based suggestions
* ⚡ Fast and responsive API powered by FastAPI
* 🎨 Clean and interactive UI built with Streamlit

---

## 🧠 How It Works

1. User searches for a movie in the interface.
2. The query is sent to the **FastAPI backend**.
3. The backend processes the request and fetches movie data.
4. A **TF-IDF similarity model** identifies similar movies.
5. Recommended movies are returned to the frontend and displayed to the user.

---

## 🏗 Architecture

```
Streamlit (Frontend)
        │
        ▼
FastAPI (Backend API)
        │
        ▼
Recommendation Engine (TF-IDF)
        │
        ▼
TMDB Movie Data
```

---

## 🛠 Tech Stack

**Frontend**

* Streamlit

**Backend**

* FastAPI
* Python

**Machine Learning**

* Scikit-learn
* TF-IDF Vectorization

**Data Source**

* TMDB Movie Dataset / API

---

## 📂 Project Structure

```
movona/
│
├── backend/
│   ├── main.py
│   ├── recommendation.py
│
├── frontend/
│   └── app.py
│
├── models/
│   └── similarity.pkl
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository

```
git clone https://github.com/ramandeep-singh17/movona.git
cd movona
```

Install dependencies

```
pip install -r requirements.txt
```

Run the backend server

```
uvicorn main:app --reload
```

Run the Streamlit frontend

```
streamlit run app.py
```

---

## 👨‍💻 Author

**Ramandeep Singh**

B.Tech Computer Science Student | Machine Learning & Web Development Enthusiast

📧 Email: [omraman3333@gmail.com](mailto:omraman3333@gmail.com)

---

## ⭐ Future Improvements

* Movie trailer integration
* User watchlist feature
* Personalized recommendations
* Rating-based filtering

---

## 📌 License

This project is created for educational and portfolio purposes.
