import streamlit as st
from pathlib import Path
import sys

# اجازه بده از ریشه پروژه ماژول‌های src را import کنیم
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.models import Book
from src.storage import load_books, save_books, next_id  # noqa: E402


st.set_page_config(page_title="Mini Library", page_icon="📚", layout="centered")
st.title("📚 Mini Library App (Bonus UI)")

tabs = st.tabs(["➕ Add", "🔎 Search", "🗑️ Delete", "📖 All Books"])

def render_book(b: Book):
    st.write(f"**[{b.id}]** {b.title} — {b.author} ({b.year})")

# --- Add ---
with tabs[0]:
    st.subheader("Add a book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.text_input("Year (number)")

    if st.button("Add Book"):
        title_s = title.strip()
        author_s = author.strip()
        year_s = year.strip()

        if not title_s:
            st.error("Title cannot be empty.")
        elif not author_s:
            st.error("Author cannot be empty.")
        elif not year_s.isdigit():
            st.error("Year must be a number.")
        else:
            books = load_books()
            b = Book(id=next_id(books), title=title_s, author=author_s, year=int(year_s))
            books.append(b)
            save_books(books)
            st.success("Book added!")
            render_book(b)

# --- Search ---
with tabs[1]:
    st.subheader("Search by partial title")
    q = st.text_input("Search query").strip().lower()

    if st.button("Search"):
        books = load_books()
        if not q:
            st.warning("Enter a query.")
        else:
            matches = [b for b in books if q in b.title.lower()]
            st.info(f"Found {len(matches)} result(s).")
            for b in matches:
                render_book(b)

# --- Delete ---
with tabs[2]:
    st.subheader("Delete a book")
    mode = st.radio("Delete by:", ["ID", "Exact Title"], horizontal=True)

    books = load_books()

    if mode == "ID":
        book_id = st.text_input("Book ID")
        if st.button("Delete"):
            if not book_id.strip().isdigit():
                st.error("ID must be a number.")
            else:
                bid = int(book_id.strip())
                new_books = [b for b in books if b.id != bid]
                if len(new_books) == len(books):
                    st.warning("No book found with this ID.")
                else:
                    save_books(new_books)
                    st.success("Deleted.")
    else:
        title_exact = st.text_input("Exact Title").strip().lower()
        if st.button("Find & Delete"):
            if not title_exact:
                st.error("Title cannot be empty.")
            else:
                candidates = [b for b in books if b.title.lower() == title_exact]
                if not candidates:
                    st.warning("No book found with this title.")
                elif len(candidates) == 1:
                    victim_id = candidates[0].id
                    save_books([b for b in books if b.id != victim_id])
                    st.success("Deleted.")
                else:
                    st.warning("Multiple books match. Select an ID below to delete.")
                    ids = [b.id for b in candidates]
                    selected = st.selectbox("Select ID", ids)
                    if st.button("Confirm delete selected ID"):
                        save_books([b for b in books if b.id != int(selected)])
                        st.success("Deleted.")

# --- All books ---
with tabs[3]:
    st.subheader("All books")
    books = load_books()
    if not books:
        st.info("No books yet.")
    else:
        for b in books:
            render_book(b)
