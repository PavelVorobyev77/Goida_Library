import gspread
from google.oauth2.service_account import Credentials

# Настройка OAuth scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Настройка учетных данных с добавлением scopes
creds = Credentials.from_service_account_file(
    'C:/Users/pasch/Пашино/Колледж/4 КУРС/Практика/mylibrarypython-3e7c1bcefbd1.json', scopes=SCOPES
)
client = gspread.authorize(creds)
sheet = client.open_by_key('1CLCT_AzSWgqzz-PMqRJIIJNfb0UxvyfDfKuXwa184KM')  # Укажите ID вашей таблицы
worksheet = sheet.get_worksheet(0)  # Получаем первый лист таблицы


# Функция для нахождения столбца по названию и вывода данных ниже заголовка
def get_data_by_column_name(column_name):
    cell = worksheet.find(column_name)
    if not cell:
        print(f"Заголовок '{column_name}' не найден.")
        return []

    col_values = worksheet.col_values(cell.col)[cell.row:]
    return [value for value in col_values if value.strip()]


# Функция для поиска групп по ФИО куратора
def get_groups_by_curator(curator_name):
    group_cell = worksheet.find('№ группы')
    curator_cell = worksheet.find('ФИО куратора')

    if not group_cell or not curator_cell:
        print("Не удалось найти нужные заголовки в таблице.")
        return []

    group_numbers = worksheet.col_values(group_cell.col)[group_cell.row:]
    curators = worksheet.col_values(curator_cell.col)[curator_cell.row:]

    groups = [group_numbers[i] for i in range(len(curators)) if curators[i].strip() == curator_name]
    return groups


# Основная логика программы
def main():
    print("Выберите действие:")
    print("1. Вывести все группы")
    print("2. Вывести всех студентов")
    print("3. Вывести группы определенного куратора")

    choice = input("Введите номер действия (1, 2 или 3): ").strip()

    if choice == '1':
        show_groups = input("Вывести все группы? (Да/Нет): ").strip().lower()
        if show_groups == 'да':
            groups = get_data_by_column_name('№ группы')
            print("Группы:")
            print("\n".join(groups))
        else:
            print("Ничего не будет выведено.")

    elif choice == '2':
        show_students = input("Вывести всех студентов? (Да/Нет): ").strip().lower()
        if show_students == 'да':
            students = get_data_by_column_name('ФИО куратора')
            print("Студенты:")
            print("\n".join(students))
        else:
            print("Ничего не будет выведено.")

    elif choice == '3':
        curator_name = input("Введите ФИО куратора: ").strip()
        if curator_name:
            groups = get_groups_by_curator(curator_name)
            if groups:
                print(f"Группы куратора {curator_name}:")
                print("\n".join(groups))
            else:
                print(f"Группы для куратора {curator_name} не найдены.")
        else:
            print("Ничего не будет выведено.")
    else:
        print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()