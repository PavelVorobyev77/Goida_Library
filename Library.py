import gspread
from google.oauth2.service_account import Credentials


# Настройка OAuth scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Настройка учетных данных с добавлением scopes
creds = Credentials.from_service_account_file('C:/Users/pasch/Desktop/mylibrarypython-3e7c1bcefbd1.json', scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key('1CLCT_AzSWgqzz-PMqRJIIJNfb0UxvyfDfKuXwa184KM')  # Укажите ID вашей таблицы
worksheet = sheet.get_worksheet(0)  # Получаем первый лист таблицы


# Функция для нахождения столбца по названию и вывода данных ниже заголовка
def get_data_by_column_name(column_name):
    # Находим ячейку с указанным заголовком
    cell = worksheet.find(column_name)
    if not cell:
        print(f"Заголовок '{column_name}' не найден.")
        return []

    # Получаем данные из соответствующего столбца начиная со строки под заголовком и удаляем пустые строки
    col_values = worksheet.col_values(cell.col)[cell.row:]
    return [value for value in col_values if value.strip()]  # Фильтруем пустые строки


# Основная логика программы
def main():
    show_groups = input("Вывести все группы? (Да/Нет): ").strip().lower()

    if show_groups == 'да':
        groups = get_data_by_column_name('№ группы')
        print("Группы:")
        print("\n".join(groups))
    else:
        show_students = input("Вывести всех студентов? (Да/Нет): ").strip().lower()

        if show_students == 'да':
            students = get_data_by_column_name('ФИО куратора')
            print("Студенты:")
            print("\n".join(students))
        else:
            print("Ни группы, ни студенты не будут выведены.")


if __name__ == "__main__":
    main()
