import inspect
import sqlite3


class ShoppingListDAO:
    def __init__(self, connection):
        self.connection = connection

    def create_database(self):
        self.connection.execute('''CREATE TABLE List (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR,
                        amount INTEGER
                        )''')
        self.connection.commit()

    def get_list(self):
        response = self.connection.execute('''SELECT *
                            FROM List
                            ''')
        all_items = response.fetchall()
        return all_items

    def insert_item(self, item, amount):
        self.connection.execute(f'INSERT INTO List (name, amount) VALUES ("{item}", {amount})')
        self.connection.commit()

    def edit_item(self, edit_name, edit_amount, user_id_to_database_id, item_id):
        self.connection.execute(
            f'''
            UPDATE List
            SET name = "{edit_name}", amount = "{edit_amount}"
            WHERE id = "{user_id_to_database_id[item_id]}"
            '''
        )
        self.connection.commit()

    def delete_item(self, user_id_to_database_id, item_id):
        self.connection.execute(
            f"""
            DELETE from List
            WHERE id = "{user_id_to_database_id[item_id]}"
            """
        )
        self.connection.commit()

    def clear_list(self):
        self.connection.execute("DELETE FROM List")
        self.connection.commit()


def show_list(shopping_list_dao: ShoppingListDAO, update_shopping_list):
    shopping_list = shopping_list_dao.get_list()
    user_id_to_database_id = {index + 1: db_id for index, (db_id, _, _) in enumerate(shopping_list)}
    update_shopping_list(user_id_to_database_id)
    if shopping_list:
        for index, (_, name, amount) in enumerate(shopping_list):
            print(f"{index + 1}. {name} szt. {amount}")
    else:
        print("Lista jest pusta")


def add_item(shopping_list_dao: ShoppingListDAO, update_shopping_ids):
    item = input("Wpisz nazwę produktu: ")
    amount = int(input("Podaj ilość"))
    shopping_list_dao.insert_item(item, amount)
    update_shopping_ids()
    print(f"Dodano pozycję {item} do listy zakupów.")


def edit_item(shopping_list_dao: ShoppingListDAO, user_id_to_database_id):
    item_id = int(input("Podaj numer produktu, który chcesz edytować: "))
    edit_name = input("Wprowadź nową nazwę: ")
    edit_amount = int(input("Wprowadź nową ilość: "))
    shopping_list_dao.edit_item(edit_name, edit_amount, user_id_to_database_id, item_id)
    print("Element został pomyślnie edytowany")


def delete_item(shopping_list_dao: ShoppingListDAO, user_id_to_database_id, update_shopping_ids):
    item_id = int(input("Podaj numer produktu, który chcesz usunąć: "))
    shopping_list_dao.delete_item(user_id_to_database_id, item_id)
    update_shopping_ids()
    print("Element został usunięty z listy.")


def clear_list(shopping_list_dao, update_shopping_ids):
    shopping_list_dao.clear_list()
    update_shopping_ids()
    print("Lista została wyczyszczona")


def main():
    connection = sqlite3.connect('data.s3db')
    shopping_list_dao = ShoppingListDAO(connection)
    # shopping_list_dao.create_database()
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
            show_list(shopping_list_dao, set_shopping_ids)
        elif option_choice == 2:
            add_item(shopping_list_dao, update_shopping_ids)
        elif option_choice == 3:
            edit_item(shopping_list_dao, user_id_to_database_id)
        elif option_choice == 4:
            delete_item(shopping_list_dao, user_id_to_database_id, update_shopping_ids)
        elif option_choice == 5:
            clear_list(shopping_list_dao, update_shopping_ids)


main()
