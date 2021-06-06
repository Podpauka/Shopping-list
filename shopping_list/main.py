def main():
    shopping_list = []
    print("Witaj!")
    while True:
        option_choice = int(input(
            "Wybierz opcję: \n 1. Pokaż listę zakupów \n 2. Dodaj nowy element \n 3. Edytuj element \n 4. Usuń element \n 5. Wyczyść listę"))
        if option_choice == 1:
            if shopping_list:
                for index, value in enumerate(shopping_list):
                    print(f"{index + 1}. {value}")
            else:
                print("Lista jest pusta.")
        elif option_choice == 2:
            item = input("Wpisz nazwę produktu: ")
            shopping_list.append(item)
            print(f"Dodano pozycję {item} do listy zakupów.")
        elif option_choice == 3:
            choice = int(input("Podaj numer elementu, który chcesz edytować: "))
            chosen_item = choice - 1
            if 0 < chosen_item < len(shopping_list):
                updated_item = input("Edytuj element: ")
                shopping_list[chosen_item] = updated_item
                print(f"Element został edytowany na {updated_item}.")
            else:
                print("Wskazanego numeru nie ma na liście.")
        elif option_choice == 4:
            choice = int(input("Podaj numer elementu, który chcesz usunąć: "))
            chosen_item = choice - 1
            shopping_list.remove(shopping_list[chosen_item])
            print(f"Element został usunięty z listy.")
        elif option_choice == 5:
            shopping_list.clear()
            print("Wszystkie elementy zostały usunięte z listy.")


main()
