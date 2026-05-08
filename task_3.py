import requests
import json

fayl_sohraneniya = 'save.json'

try:
    with open(fayl_sohraneniya, 'r', encoding='utf-8') as fayl:
        gruppy_valyut = json.load(fayl)
except FileNotFoundError:
    gruppy_valyut = {}
except json.JSONDecodeError:
    print("Ошибка чтения файла save.json. Создан новый пустой список групп.")
    gruppy_valyut = {}


def sohranit_dannie(gruppy):
    try:
        with open(fayl_sohraneniya, 'w', encoding='utf-8') as fayl:
            json.dump(gruppy, fayl, ensure_ascii=False, indent=4)
    except Exception:
        print("Не удалось сохранить данные в файл.")


def poluchit_kursy():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    try:
        otvet = requests.get(url, timeout=10)
        if otvet.status_code == 200:
            return otvet.json()['Valute']
        else:
            print("Ошибка сервера при получении курсов валют.")
            return None
    except requests.exceptions.RequestException:
        print("Ошибка соединения. Проверьте интернет или повторите попытку позже.")
        return None


print("Добро пожаловать в мониторинг валют!")

while True:
    print("\n--- Главное меню ---")
    print("1. Посмотреть все курсы валют")
    print("2. Посмотреть курс отдельной валюты по коду")
    print("3. Создать новую группу валют")
    print("4. Посмотреть все группы валют")
    print("5. Изменить группу валют (добавить/удалить валюту)")
    print("6. Выход")

    vibor = input("Выберите действие (введите цифру 1-6): ")

    if vibor == '1':
        dannye_valyut = poluchit_kursy()
        if dannye_valyut:
            print("\nТекущие курсы всех валют:")
            for kod, info in dannye_valyut.items():
                print(f"{kod} ({info['Name']}): {info['Value']} руб.")

    elif vibor == '2':
        kod_valyuty = input("Введите код валюты (например, USD, EUR): ").upper()
        dannye_valyut = poluchit_kursy()
        if dannye_valyut:
            if kod_valyuty in dannye_valyut:
                info = dannye_valyut[kod_valyuty]
                print(f"\nКурс {kod_valyuty} ({info['Name']}): {info['Value']} руб.")
            else:
                print(f"\nВалюта с кодом {kod_valyuty} не найдена. Проверьте правильность ввода.")

    elif vibor == '3':
        nazvanie_gruppy = input("Введите название для новой группы: ")
        if nazvanie_gruppy in gruppy_valyut:
            print("Группа с таким названием уже существует, придумайте другое.")
        else:
            gruppy_valyut[nazvanie_gruppy] = []
            sohranit_dannie(gruppy_valyut)
            print(f"Группа '{nazvanie_gruppy}' успешно создана!")

    elif vibor == '4':
        if not gruppy_valyut:
            print("\nУ вас пока нет созданных групп. Создайте их в пункте 3.")
        else:
            dannye_valyut = poluchit_kursy()
            if dannye_valyut:
                print("\nВаши группы валют и их курсы:")
                for nazvanie, valyuty in gruppy_valyut.items():
                    print(f"\nГруппа: {nazvanie}")
                    if not valyuty:
                        print("  (В этой группе пока нет валют)")
                    else:
                        for kod in valyuty:
                            if kod in dannye_valyut:
                                info = dannye_valyut[kod]
                                print(f"  {kod} ({info['Name']}): {info['Value']} руб.")
                            else:
                                print(f"  {kod}: валюта не найдена в базе Центрального Банка")

    elif vibor == '5':
        if not gruppy_valyut:
            print("\nУ вас нет групп для изменения. Сначала создайте группу.")
            continue

        print("\nВаши существующие группы:")
        for nazvanie in gruppy_valyut.keys():
            print(f"- {nazvanie}")

        vibor_gruppy = input("\nВведите точное название группы для изменения: ")

        if vibor_gruppy not in gruppy_valyut:
            print("Группа не найдена. Проверьте правильность написания.")
        else:
            print(f"\nРабота с группой: {vibor_gruppy}")
            tekshtie_valyuty = gruppy_valyut[vibor_gruppy]

            if tekshtie_valyuty:
                print(f"Сейчас в группе: {', '.join(tekshtie_valyuty)}")
            else:
                print("Сейчас группа пуста.")

            print("1. Добавить валюту")
            print("2. Удалить валюту")
            deystvie = input("Выберите действие (1 или 2): ")

            if deystvie == '1':
                kod_dlya_dobavleniya = input("Введите код валюты для добавления (например, USD): ").upper()
                if kod_dlya_dobavleniya in gruppy_valyut[vibor_gruppy]:
                    print("Эта валюта уже есть в данной группе.")
                else:
                    gruppy_valyut[vibor_gruppy].append(kod_dlya_dobavleniya)
                    sohranit_dannie(gruppy_valyut)
                    print(f"Валюта {kod_dlya_dobavleniya} успешно добавлена в группу '{vibor_gruppy}'.")

            elif deystvie == '2':
                kod_dlya_udaleniya ф= input("Введите код валюты для удаления: ").upper()
                if kod_dlya_udaleniya in gruppy_valyut[vibor_gruppy]:
                    gruppy_valyut[vibor_gruppy].remove(kod_dlya_udaleniya)
                    sohranit_dannie(gruppy_valyut)
                    print(f"Валюта {kod_dlya_udaleniya} удалена из группы '{vibor_gruppy}'.")
                else:
                    print("Такой валюты в этой группе нет.")
            else:
                print("Неверное действие. Нужно ввести 1 или 2.")

    elif vibor == '6':
        print("\nСохранение данных и выход из программы... До свидания!")
        break

    else:
        print("\nНеверный ввод! Пожалуйста, выберите цифру от 1 до 6.")