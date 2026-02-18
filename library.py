import sqlite3
import csv


# =========================
# Создание базы данных
# =========================
def create_database():
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER,
                genre TEXT,
                is_read INTEGER DEFAULT 0
            )
        ''')

        conn.commit()
        conn.close()
        print("База данных готова!")
    except sqlite3.Error as e:
        print("Ошибка при создании БД:", e)


# =========================
# Добавление книги
# =========================
def add_book(title, author, year, genre, is_read=False):
    try:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO books (title, author, year, genre, is_read)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, author, year, genre, 1 if is_read else 0))

        conn.commit()
        conn.close()
        print("Книга добавлена!")
    except sqlite3.Error as e:
        print("Ошибка:", e)


# =========================
# Получение всех книг
# =========================
def get_all_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books


def display_books(books):
    if not books:
        print("Книг нет.")
        return

    print("\nID | Название | Автор | Год | Жанр | Прочитана")
    print("-" * 60)

    for book in books:
        status = "Да" if book[5] == 1 else "Нет"
        print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]} | {status}")


# =========================
# Поиск книги
# =========================
def search_books(term):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + term + '%',))
    books = cursor.fetchall()
    conn.close()
    return books


# =========================
# Обновление книги
# =========================
def update_book(book_id, new_title):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title = ? WHERE id = ?", (new_title, book_id))
    conn.commit()
    conn.close()
    print("Книга обновлена!")


# =========================
# Удаление книги
# =========================
def delete_book(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    print("Книга удалена!")


# =========================
# Статистика
# =========================
def get_statistics():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM books")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM books WHERE is_read = 1")
    read = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM books WHERE is_read = 0")
    unread = cursor.fetchone()[0]

    conn.close()

    print("\nСтатистика:")
    print("Всего книг:", total)
    print("Прочитано:", read)
    print("Не прочитано:", unread)


# =========================
# Экспорт в CSV
# =========================
def export_to_csv():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()

    with open('books_export.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Название", "Автор", "Год", "Жанр", "Прочитана"])
        writer.writerows(books)

    print("Экспорт завершён! Файл books_export.csv создан.")


# =========================
# Главное меню
# =========================
def main_menu():
    while True:
        print("\n1. Показать книги")
        print("2. Добавить книгу")
        print("3. Поиск")
        print("4. Обновить книгу")
        print("5. Удалить книгу")
        print("6. Статистика")
        print("7. Экспорт в CSV")
        print("8. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            display_books(get_all_books())

        elif choice == "2":
            title = input("Название: ")
            author = input("Автор: ")

            try:
                year = int(input("Год: "))
            except ValueError:
                print("Год должен быть числом!")
                continue

            genre = input("Жанр: ")
            is_read = input("Прочитана? (да/нет): ").lower() == "да"

            add_book(title, author, year, genre, is_read)

        elif choice == "3":
            term = input("Введите название для поиска: ")
            display_books(search_books(term))

        elif choice == "4":
            book_id = int(input("ID книги: "))
            new_title = input("Новое название: ")
            update_book(book_id, new_title)

        elif choice == "5":
            book_id = int(input("ID для удаления: "))
            delete_book(book_id)

        elif choice == "6":
            get_statistics()

        elif choice == "7":
            export_to_csv()

        elif choice == "8":
            print("Выход...")
            break

        else:
            print("Неверный выбор!")


# =========================
# Запуск программы
# =========================
if __name__ == "__main__":
    create_database()
    main_menu()
