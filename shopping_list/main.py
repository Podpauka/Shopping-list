import inspect
import sqlite3


def create_database(connection):
    connection.execute('''CREATE TABLE List (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR,
                    amount INTEGER
                    )''')
    connection.commit()


def get_list(connection):
    response = connection.execute('''SELECT *
                        FROM List
                        ''')
    all_items = response.fetchall()
    return all_items


def show_list(connection, update_shopping_list):
    shopping_list = get_list(connection)
    user_id_to_database_id = {index + 1: db_id for index, (db_id, _, _) in enumerate(shopping_list)}
    update_shopping_list(user_id_to_database_id)
    if shopping_list:
        for index, (_, name, amount) in enumerate(shopping_list):
            print(f"{index + 1}. {name} szt. {amount}")
    else:
        print("Lista jest pusta")


def insert_item(item, amount, connection):
    connection.execute(f'INSERT INTO List (name, amount) VALUES ("{item}", {amount})')
    connection.commit()


def add_item(connection, update_shopping_ids):
    item = input("Wpisz nazwę produktu: ")
    amount = int(input("Podaj ilość"))
    insert_item(item, amount, connection)
    update_shopping_ids()
    print(f"Dodano pozycję {item} do listy zakupów.")


def edit_item(connection, user_id_to_database_id):
    item_id = int(input("Podaj numer produktu, który chcesz edytować: "))
    edit_name = input("Wprowadź nową nazwę: ")
    edit_amount = int(input("Wprowadź nową ilość: "))
    connection.execute(
        f'''
        UPDATE List
        SET name = "{edit_name}", amount = "{edit_amount}"
        WHERE id = "{user_id_to_database_id[item_id]}"
        '''
    )
    connection.commit()
    print("Element został pomyślnie edytowany")


def delete_item(connection, user_id_to_database_id, update_shopping_ids):
    item_id = int(input("Podaj numer produktu, który chcesz usunąć: "))
    connection.execute(
        f"""
        DELETE from List
        WHERE id = "{user_id_to_database_id[item_id]}"
        """
    )
    connection.commit()
    update_shopping_ids()
    print("Element został usunięty z listy.")


def clear_list(connection, update_shopping_ids):
    connection.execute("DELETE FROM List")
    connection.commit()
    update_shopping_ids()


def main():
    connection = sqlite3.connect('data.s3db')
    create_database(connection)
    print("Witaj!")
    user_id_to_database_id = {}

    def set_shopping_ids(new_mapping):
        nonlocal user_id_to_database_id
        user_id_to_database_id = new_mapping

    def update_shopping_ids():
        nonlocal user_id_to_database_id
        response = connection.execute("SELECT id FROM List")
        ids = response.fetchall()
        user_id_to_database_id = {index + 1: db_id for index, (db_id,) in enumerate(ids)}

    update_shopping_ids()
    while True:
        option_choice = int(input(inspect.cleandoc(
            '''
            Wybierz opcję:
             1. Pokaż listę zakupów
             2. Dodaj nowy element
             3. Edytuj element
             4. Usuń element
             5. Wyczyść listę
            '''
        )))
        if option_choice == 1:
            show_list(connection, set_shopping_ids)
        elif option_choice == 2:
            add_item(connection, update_shopping_ids)
        elif option_choice == 3:
            edit_item(connection, user_id_to_database_id)
        elif option_choice == 4:
            delete_item(connection, user_id_to_database_id, update_shopping_ids)
        elif option_choice == 5:
            clear_list(connection, update_shopping_ids)


main()
