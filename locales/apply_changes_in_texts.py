import os
import glob
import subprocess

# Каталог с файлами перевода
LOCALE_DIR = 'mo_files'

# Удаляем старые .mo файлы
mo_files = glob.glob(os.path.join(LOCALE_DIR, '*', 'LC_MESSAGES', 'messages.mo'))
if not mo_files:
    print("Не найдено .mo файлов для удаления.")
else:
    for mo_file in mo_files:
        os.remove(mo_file)
        print(f"Удален .mo файл: {mo_file}")


# Компилируем .texts файлы в .mo файлы
po_files = glob.glob(os.path.join('texts', '*.po'))
if not po_files:
    print("Не найдено .texts файлов для компиляции.")
else:
    for po_file in po_files:
        # Определение языка и каталога для .mo файла
        language = os.path.splitext(os.path.basename(po_file))[0]
        mo_file_dir = os.path.join(LOCALE_DIR, language, 'LC_MESSAGES')
        mo_file_path = os.path.join(mo_file_dir, 'messages.mo')

        # Удаление старого .mo файла, если он существует
        if os.path.isfile(mo_file_path):
            os.remove(mo_file_path)
            print(f"Удален старый .mo файл: {mo_file_path}")

        # Создание каталога, если он не существует
        os.makedirs(mo_file_dir, exist_ok=True)

        # Компиляция .texts файла в .mo файл
        subprocess.run(['msgfmt', po_file, '-o', mo_file_path])
        print(f"Создан .mo файл: {mo_file_path}")


if __name__ == '__main__':
    print('I AM ALIVE')
