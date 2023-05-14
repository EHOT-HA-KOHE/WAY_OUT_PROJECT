import gettext
import os

# Установка каталога с переводами
LOCALE_DIR = '../../../locales/mo_files'

# Установка языка и домена перевода
language = 'ua'
translation_domain = 'messages'

# Создание объекта gettext.Translations
gettext.bindtextdomain(translation_domain, LOCALE_DIR)
gettext.textdomain(translation_domain)
translation = gettext.translation(translation_domain, LOCALE_DIR, languages=[language], fallback=True)
_ = translation.gettext

# Тестирование перевода
print(_("test_message"))
print(_("hi"))
print(_("hi_with_name {name}").format(name="Alice"))
print(_("hi_with_name_and_age {name} {age}").format(name="Alice", age="20"))
print(_("fuck"))
