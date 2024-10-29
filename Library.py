import asyncio
from google.oauth2.service_account import Credentials
import gspread_asyncio

# Настройка OAuth scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Функция для создания асинхронного клиента
def get_creds():
    return Credentials.from_service_account_file(
        'C:/Users/pasch/Пашино/Колледж/4 КУРС/Практика/mylibrarypython-3e7c1bcefbd1.json', scopes=SCOPES
    )

# Создание асинхронного клиента gspread
agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)

# Функция для нахождения столбца по названию и вывода данных ниже заголовка
async def get_data_by_column_name(worksheet, column_name):
    cell = await worksheet.find(column_name)
    if not cell:
        print(f"Заголовок '{column_name}' не найден.")
        return []

    col_values = await worksheet.col_values(cell.col)
    return [value for value in col_values[cell.row:] if value.strip()]

# Функция для поиска групп по ФИО куратора
async def get_groups_by_curator(worksheet, curator_name):
    group_cell = await worksheet.find('№ группы')
    curator_cell = await worksheet.find('ФИО куратора')

    if not group_cell or not curator_cell:
        print("Не удалось найти нужные заголовки в таблице.")
        return []

    group_numbers = await worksheet.col_values(group_cell.col)
    curators = await worksheet.col_values(curator_cell.col)

    groups = [group_numbers[i] for i in range(len(curators)) if curators[i].strip() == curator_name]
    return groups

# Основная логика программы
async def main():
    client = await agcm.authorize()  # Получаем клиента без async with
    sheet = await client.open_by_key('1CLCT_AzSWgqzz-PMqRJIIJNfb0UxvyfDfKuXwa184KM')
    worksheet = await sheet.get_worksheet(0)

    print("Выберите действие:")
    print("1. Вывести все группы")
    print("2. Вывести всех студентов")
    print("3. Вывести группы определенного куратора")

    choice = input("Введите номер действия (1, 2 или 3): ").strip()

    if choice == '1':
        show_groups = input("Вывести все группы? (Да/Нет): ").strip().lower()
        if show_groups == 'да':
            groups = await get_data_by_column_name(worksheet, '№ группы')
            print("Группы:")
            print("\n".join(groups))
        else:
            print("Ничего не будет выведено.")

    elif choice == '2':
        show_students = input("Вывести всех студентов? (Да/Нет): ").strip().lower()
        if show_students == 'да':
            students = await get_data_by_column_name(worksheet, 'ФИО куратора')
            print("Студенты:")
            print("\n".join(students))
        else:
            print("Ничего не будет выведено.")

    elif choice == '3':
        curator_name = input("Введите ФИО куратора: ").strip()
        if curator_name:
            groups = await get_groups_by_curator(worksheet, curator_name)
            if groups:
                print(f"Группы куратора {curator_name}:")
                print("\n".join(groups))
            else:
                print(f"Группы для куратора {curator_name} не найдены.")
        else:
            print("Ничего не будет выведено.")
    else:
        print("Неверный выбор. Попробуйте снова.")

# Запуск асинхронного кода
if __name__ == "__main__":
    asyncio.run(main())
