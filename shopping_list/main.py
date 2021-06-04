def main():
    shopping_list = []
    print("Witaj!")
    while True:
        option_choice = int(input("Wybierz opcję: \n 1. Pokaż listę zakupów \n 2. Dodaj nowy element"))
        if option_choice == 1:
            if shopping_list:
                for i in shopping_list:
                    print(i)
            else:
                print("Lista jest pusta.")
        elif option_choice == 2:
            item = input("Wpisz nazwę produktu: ")
            shopping_list.append(item)
            print(f"Dodano pozycję {item} do listy zakupów")


main()
