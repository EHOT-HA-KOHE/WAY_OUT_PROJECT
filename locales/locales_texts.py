import gettext
import os

from src.db.models import User
from src.db.connection import Session, first_db_connect

db_session = Session()


def return_local_text_for_user(
        user_id,
        language='en',
        text="error: message was crashed",
        locales_dir="locales/mo_files"
):
    translation_domain = 'messages'

    user_in_db = db_session.query(User).filter(User.tg_id == user_id).first()
    user_lang = user_in_db.language

    gettext.bindtextdomain(translation_domain, locales_dir)
    gettext.textdomain(translation_domain)
    translation = gettext.translation(translation_domain, locales_dir, languages=[user_lang], fallback=True)
    _ = translation.gettext

    return _(text)
