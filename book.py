books = []
next_id = 1


def add_book(title, author, price, genre):
    global next_id
    book = {
        "id": next_id,
        "title": title,
        "author": author,
        "price": float(price),
        "genre": genre
    }
    books.append(book)
    next_id += 1
    print(f"\nbook '{title}' added successfully (id: {book['id']})")


def find_book(book_id):
    for book in books:
        if book["id"] == book_id:
            return book
    return None


def show_book(book_id):
    book = find_book(book_id)
    if not book:
        print("\nbook not found.")
        return
    print(f"""
id     : {book['id']}
title  : {book['title']}
author : {book['author']}
genre  : {book['genre']}
price  : ${book['price']:.2f}""")


def edit_book(book_id):
    book = find_book(book_id)
    if not book:
        print("\nbook not found.")
        return

    print(f"\nediting '{book['title']}' — press enter to keep current value\n")

    title = input(f"title [{book['title']}]: ").strip()
    author = input(f"author [{book['author']}]: ").strip()
    genre = input(f"genre [{book['genre']}]: ").strip()
    price = input(f"price [{book['price']:.2f}]: ").strip()

    if title:
        book["title"] = title
    if author:
        book["author"] = author
    if genre:
        book["genre"] = genre
    if price:
        try:
            book["price"] = float(price)
        except ValueError:
            print("invalid price, keeping old value")

    print("\nbook updated.")


def delete_book(book_id):
    book = find_book(book_id)
    if not book:
        print("\nbook not found.")
        return
    books.remove(book)
    print(f"\nbook '{book['title']}' deleted.")


def list_books():
    if not books:
        print("\nno books in the store yet.")
        return
    print(f"\n{'id':<5} {'title':<30} {'author':<25} {'genre':<15} {'price'}")
    print("-" * 85)
    for book in books:
        print(f"{book['id']:<5} {book['title']:<30} {book['author']:<25} {book['genre']:<15} ${book['price']:.2f}")


def menu():
    while True:
        print("""
=== bookstore ===
1. add book
2. list all books
3. show book
4. edit book
5. delete book
0. exit""")

        choice = input("\nchoice: ").strip()

        if choice == "1":
            title  = input("title: ").strip()
            author = input("author: ").strip()
            genre  = input("genre: ").strip()
            price  = input("price: ").strip()
            if title and author and genre and price:
                try:
                    add_book(title, author, price, genre)
                except ValueError:
                    print("invalid price.")
            else:
                print("all fields are required.")

        elif choice == "2":
            list_books()

        elif choice == "3":
            try:
                book_id = int(input("book id: "))
                show_book(book_id)
            except ValueError:
                print("invalid id.")

        elif choice == "4":
            try:
                book_id = int(input("book id: "))
                edit_book(book_id)
            except ValueError:
                print("invalid id.")

        elif choice == "5":
            try:
                book_id = int(input("book id: "))
                delete_book(book_id)
            except ValueError:
                print("invalid id.")

        elif choice == "0":
            print("\ngoodbye.")
            break

        else:
            print("invalid choice.")


if __name__ == "__main__":
    menu()