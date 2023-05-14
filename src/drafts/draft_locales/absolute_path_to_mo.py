import os

# Получение абсолютного пути к текущей директории
current_directory = os.getcwd()

# Формирование пути к файлу messages.mo
mo_file_path = os.path.abspath(os.path.join(current_directory, 'locales', '../../../locales/mo_files/ru', 'messages.mo'))

# Формирование пути к файлу messages.texts
po_file_path = os.path.abspath(os.path.join(current_directory, 'locales', '../../../locales/mo_files/ru', 'messages.texts'))

# Вывод абсолютных путей к файлам
print("Путь к messages.mo:", mo_file_path)
print("Путь к messages.texts:", po_file_path)
