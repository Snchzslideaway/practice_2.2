import requests

bazoviy_url = "https://api.github.com"
zagolovki = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

print("Запуск приложения для работы с GitHub...")

while True:
    print("\n--- Меню GitHub API ---")
    print("1. Посмотреть профиль пользователя")
    print("2. Получить все репозитории пользователя")
    print("3. Найти репозитории по названию")
    print("4. Выйти из программы")

    vibor = input("Выберите пункт меню (1-4): ")

    if vibor == '1':
        imya_polzovatelya = input("\nВведите никнейм пользователя GitHub: ")
        url_profilya = f"{bazoviy_url}/users/{imya_polzovatelya}"

        try:
            otvet = requests.get(url_profilya, headers=zagolovki, timeout=10)

            if otvet.status_code == 200:
                dannie = otvet.json()

                imya = dannie.get('name')
                if imya is None:
                    imya = "Не указано"

                ssylka = dannie.get('html_url')
                repozitorii = dannie.get('public_repos')
                podpischiki = dannie.get('followers')
                podpiski = dannie.get('following')

                print(f"\nИнформация о профиле ({imya_polzovatelya}):")
                print(f"Имя: {imya}")
                print(f"Ссылка на профиль: {ssylka}")
                print(f"Количество репозиториев: {repozitorii}")
                print("Количество обсуждений: недоступно в базовом REST API")
                print(f"Количество подписок: {podpiski}")
                print(f"Количество подписчиков: {podpischiki}")

            elif otvet.status_code == 404:
                print("Ошибка: Такой пользователь не найден.")
            elif otvet.status_code == 403:
                print("Ошибка: Превышен лимит запросов к GitHub API.")
            else:
                print(f"Неизвестная ошибка. Код ответа: {otvet.status_code}")

        except requests.exceptions.RequestException:
            print("Ошибка соединения. Проверьте интернет.")

    elif vibor == '2':
        imya_polzovatelya = input("\nВведите никнейм пользователя: ")
        url_repozitoriev = f"{bazoviy_url}/users/{imya_polzovatelya}/repos"

        try:
            otvet = requests.get(url_repozitoriev, headers=zagolovki, timeout=10)

            if otvet.status_code == 200:
                spisok_repozitoriev = otvet.json()

                if len(spisok_repozitoriev) == 0:
                    print("У этого пользователя нет публичных репозиториев.")
                else:
                    print(f"\nРепозитории пользователя {imya_polzovatelya}:")
                    for repozitoriy in spisok_repozitoriev:
                        nazvanie = repozitoriy.get('name')
                        ssylka_repo = repozitoriy.get('html_url')
                        prosmotry = repozitoriy.get('watchers_count')
                        yazyk = repozitoriy.get('language')

                        if yazyk is None:
                            yazyk = "Не определен"

                        vidimost = repozitoriy.get('visibility')
                        vetka = repozitoriy.get('default_branch')

                        print(f"\nНазвание: {nazvanie}")
                        print(f"Ссылка: {ssylka_repo}")
                        print(f"Отслеживают (вместо просмотров): {prosmotry}")
                        print(f"Язык: {yazyk}")
                        print(f"Видимость: {vidimost}")
                        print(f"Ветка по умолчанию: {vetka}")

            elif otvet.status_code == 404:
                print("Ошибка: Пользователь не найден.")
            else:
                print(f"Произошла ошибка. Код: {otvet.status_code}")

        except requests.exceptions.RequestException:
            print("Ошибка соединения с сервером.")

    elif vibor == '3':
        zapros_poiska = input("\nВведите название репозитория для поиска: ")
        url_poiska = f"{bazoviy_url}/search/repositories?q={zapros_poiska}"

        try:
            otvet = requests.get(url_poiska, headers=zagolovki, timeout=10)

            if otvet.status_code == 200:
                rezultaty = otvet.json()
                naydennie_repozitorii = rezultaty.get('items', [])

                if len(naydennie_repozitorii) == 0:
                    print("По вашему запросу ничего не найдено.")
                else:
                    print("\nТоп результатов поиска:")

                    schetchik = 0
                    for repozitoriy in naydennie_repozitorii:
                        if schetchik >= 5:
                            break

                        nazvanie = repozitoriy.get('name')
                        ssylka_repo = repozitoriy.get('html_url')
                        prosmotry = repozitoriy.get('watchers_count')
                        yazyk = repozitoriy.get('language')

                        if yazyk is None:
                            yazyk = "Не определен"

                        vidimost = repozitoriy.get('visibility')
                        vetka = repozitoriy.get('default_branch')
                        avtor = repozitoriy.get('owner', {}).get('login', 'Неизвестен')

                        print(f"\nНазвание: {nazvanie} (Автор: {avtor})")
                        print(f"Ссылка: {ssylka_repo}")
                        print(f"Отслеживают: {prosmotry}")
                        print(f"Язык: {yazyk}")
                        print(f"Видимость: {vidimost}")
                        print(f"Ветка: {vetka}")

                        schetchik += 1
            else:
                print(f"Ошибка при поиске. Код: {otvet.status_code}")

        except requests.exceptions.RequestException:
            print("Ошибка соединения с интернетом.")

    elif vibor == '4':
        print("\nРабота завершена.")
        break

    else:
        print("\nНекорректный ввод! Пожалуйста, введите цифру от 1 до 4.")