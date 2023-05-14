# from gettext import translation
from gettext import gettext as _

# -*- coding: utf-8 -*-
#
#
# # Установка языка пользователя
# def set_user_language(language):
#     translation_file = f'../locales/{language}/messages.mo'
#     user_translation = translation('messages', localedir='locales', languages=[language])
#     user_translation.install()
#
#
# # Отправка сообщения с учетом выбранного языка
# def send_message():
#     # ...
#     translated_message = _('Hello, World!')
#     print(translated_message)
#     # ...
#
#
# set_user_language("ru")
# send_message()


from gettext import translation

# Установка языка пользователя
def set_user_language(user_id, language):
    user_translation = translation('messages', localedir='/home/kirshine/PycharmProjects/WAY_OUT_PROJECT/locales/locales/ru/messages.mo', languages=[language])
    user_translation.install()


# from gettext import GNUTranslations
#
# # Установка языка пользователя
# def set_user_language(user_id, language):
#     translation_file = f'/home/kirshine/PycharmProjects/WAY_OUT_PROJECT/locales/locales/ru/messages.mo'
#     user_translation = GNUTranslations(open(translation_file, 'rb'), 'utf-8')
#     user_translation.install()

# Отправка сообщения с учетом выбранного языка
def send_message(user_id, message):
    # ...
    translated_message = _('Hello, World!')
    print(translated_message)
    # ...

user_id = "user_id"
language = "ru"
set_user_language(user_id, language)

send_message(user_id, "message")

