import json

# Путь к файлу для хранения данных
DATA_FILE = "library.json"

def load_data() -> list:
    """Загружает данные библиотеки из файла JSON."""
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(data: list) -> None:
    """Сохраняет список книг в файл JSON."""
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except IOError:
        print("Ошибка: Не удалось сохранить данные.")

def validate_year(prompt: str) -> int:
    """Запрашивает и проверяет корректность ввода года."""
    while True:
        year = input(prompt).strip()
        if not year.isdigit() or len(year) != 4:
            print("Ошибка: Год должен быть четырёхзначным числом.")
        else:
            return int(year)

def add_book() -> None:
    """Добавление новой книги в библиотеку."""
    title = input("Введите название книги: ").strip()
    author = input("Введите автора книги: ").strip()
    year = validate_year("Введите год издания: ")

    books = load_data()
    new_id = max((book["id"] for book in books), default=0) + 1

    new_book = {
        "id": new_id,
        "title": title,
        "author": author,
        "year": year,
        "status": "в наличии"
    }

    books.append(new_book)
    save_data(books)

    print("\n" + "-" * 50)
    print(f"Книга '{title}' успешно добавлена с ID {new_id}.")
    print("-" * 50)

def delete_book() -> None:
    """Удаление книги из библиотеки по ID."""
    try:
        book_id = int(input("Введите ID книги, которую хотите удалить: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return

    books = load_data()
    book_to_delete = None

    # Ищем книгу по ID
    for book in books:
        if book["id"] == book_id:
            book_to_delete = book
            break

    if book_to_delete is None:
        print(f"Ошибка: Книга с ID {book_id} не найдена.")
        return

    books.remove(book_to_delete)
    save_data(books)
    print(f"Книга с ID {book_id} успешно удалена.")

def search_books() -> None:
    """Поиск книг в библиотеке по названию, автору или году."""
    print("\nПоиск книги")
    print("1. По названию")
    print("2. По автору")
    print("3. По году")
    choice = input("Выберите критерий поиска (1/2/3): ").strip()
    
    books = load_data()
    if choice == "1":
        search_term = input("Введите название книги: ").strip().lower()
        found_books = [book for book in books if search_term in book["title"].lower()]
    elif choice == "2":
        search_term = input("Введите имя автора: ").strip().lower()
        found_books = [book for book in books if search_term in book["author"].lower()]
    elif choice == "3":
        year = validate_year("Введите год издания: ")
        found_books = [book for book in books if book["year"] == year]
    else:
        print("Некорректный выбор. Попробуйте снова.")
        return

    if found_books:
        print("\nНайденные книги:")
        print("{:<5} {:<30} {:<20} {:<10} {:<10}".format("ID", "Название", "Автор", "Год", "Статус"))
        print("-" * 75)
        for book in found_books:
            print("{:<5} {:<30} {:<20} {:<10} {:<10}".format(
                book["id"], book["title"], book["author"], book["year"], book["status"]
            ))
    else:
        print("Книг по указанному критерию не найдено.")

def display_books() -> None:
    """Выводит список всех книг в библиотеке."""
    books = load_data()

    if not books:
        print("Библиотека пуста.")
        return

    print("\nСписок книг в библиотеке:")
    print("{:<5} {:<30} {:<20} {:<10} {:<10}".format("ID", "Название", "Автор", "Год", "Статус"))
    print("-" * 75)
    for book in books:
        print("{:<5} {:<30} {:<20} {:<10} {:<10}".format(
            book["id"], book["title"], book["author"], book["year"], book["status"]
        ))

def change_status() -> None:
    """Изменяет статус книги в библиотеке."""
    try:
        book_id = int(input("Введите ID книги, статус которой хотите изменить: "))
    except ValueError:
        print("Ошибка: ID должен быть числом.")
        return

    books = load_data()
    book_to_update = None

    # Ищем книгу по ID
    for book in books:
        if book["id"] == book_id:
            book_to_update = book
            break

    if book_to_update is None:
        print(f"Ошибка: Книга с ID {book_id} не найдена.")
        return

    print("Выберите новый статус книги:")
    print("1. В наличии")
    print("2. Выдана")

    while True:
        choice = input("Введите номер статуса (1/2): ").strip()
        if choice == "1":
            book_to_update["status"] = "в наличии"
        elif choice == "2":
            book_to_update["status"] = "выдана"
        else:
            print("Ошибка: Некорректный выбор статуса. Попробуйте снова!")
            continue
        break

    save_data(books)
    print(f"Статус книги с ID {book_id} успешно обновлён.")

def main() -> None:
    """Основное меню приложения."""
    print("Добро пожаловать в библиотечную систему!")
    while True:
        print("\nДоступные команды:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        command = input("Введите номер команды: ").strip()

        if command == "1":
            add_book()
        elif command == "2":
            delete_book()
        elif command == "3":
            search_books()
        elif command == "4":
            display_books()
        elif command == "5":
            change_status()
        elif command == "6":
            print("Выход из программы. До свидания!")
            break
        else:
            print("Некорректная команда. Попробуйте снова.")

if __name__ == "__main__":
    main()
