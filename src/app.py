# src/app.py
from .models import Book
from .storage import load_books, save_books, next_id

def print_book(b: Book) -> None:
    print(f"[{b.id}] {b.title} | {b.author} | {b.year}")

def list_books(books: list[Book]) -> None:
    if not books:
        print("No books have been registered.")
        return
    for b in books:
        print_book(b)

def add_book() -> None:
    books = load_books()
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Publication year: ").strip()

    if not title:
        print("Error: Title cannot be empty.")
        return
    if not author:
        print("Error: Author cannot be empty.")
        return
    if not year_str.isdigit():
        print("Error: Publication year must be a number.")
        return

    b = Book(id=next_id(books), title=title, author=author, year=int(year_str))
    books.append(b)
    save_books(books)
    print("✅ Book added:")
    print_book(b)

def search_books() -> None:
    books = load_books()
    q = input("Search term (part of the title): ").strip().lower()
    if not q:
        print("Search term is empty.")
        return

    matches = [b for b in books if q in b.title.lower()]
    print(f"Results: {len(matches)}")
    for b in matches:
        print_book(b)

def delete_book() -> None:
    books = load_books()
    mode = input("Delete by (1) ID or (2) title? ").strip()

    if mode == "1":
        id_str = input("ID: ").strip()
        if not id_str.isdigit():
            print("ID must be a number.")
            return
        book_id = int(id_str)
        new_books = [b for b in books if b.id != book_id]
        if len(new_books) == len(books):
            print("No book found with this ID.")
            return
        save_books(new_books)
        print("✅ Deleted.")
        return

    if mode == "2":
        title = input("Exact title: ").strip().lower()
        if not title:
            print("Title is empty.")
            return
        candidates = [b for b in books if b.title.lower() == title]

        if not candidates:
            print("No book found with this title.")
            return

        # If there are multiple books, ask the user to choose by ID
        if len(candidates) > 1:
            print("Multiple books with this title exist. Choose one by ID:")
            for b in candidates:
                print_book(b)
            id_str = input("Selected ID: ").strip()
            if not id_str.isdigit():
                print("ID must be a number.")
                return
            book_id = int(id_str)
            new_books = [b for b in books if b.id != book_id]
            if len(new_books) == len(books):
                print("Invalid ID.")
                return
            save_books(new_books)
            print("✅ Deleted.")
            return

        # Only one match
        victim_id = candidates[0].id
        save_books([b for b in books if b.id != victim_id])
        print("✅ Deleted.")
        return

    print("Invalid option.")

def main() -> None:
    while True:
        print("\n--- Mini Library ---")
        print("1) List all books")
        print("2) Add a book")
        print("3) Search")
        print("4) Delete")
        print("0) Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            list_books(load_books())
        elif choice == "2":
            add_book()
        elif choice == "3":
            search_books()
        elif choice == "4":
            delete_book()
        elif choice == "0":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
