# Mini Library App (Python)

A simple CLI app to manage a mini library: add, search, and delete books with persistent storage in JSON.

## Features
- Add a book (title, author, year)
- Search books by partial title
- Delete book by id or exact title (handles duplicates)
- Persistent storage using `data/books.json`

## Requirements
- Python 3.10+ (recommended 3.11)
- Git

## Setup
```bash
git clone https://github.com/Saman2C/mini-library-app.git
cd mini-library-app
python -m src.app


## Bonus UI (Streamlit)
To run the UI:

```bash
pip install -r requirements.txt
streamlit run ui/app_streamlit.py