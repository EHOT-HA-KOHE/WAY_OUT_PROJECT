import gettext
import os

from src.db.models import User
from src.db.connection import Session

# from src.user_func.main_menu.user_profile_dir.files.change_language import update_user

db_session = Session()


def return_local_text(user_id, text="error: message was crashed", locales_dir="locales/mo_files"):
    translation_domain = 'messages'

    user_in_db = db_session.query(User).filter(User.tg_id == user_id).first()

    if user_in_db is None:
        user_lang = "en"
        new_user = User(tg_id=user_id, language=user_lang)
        db_session.add(new_user)
        db_session.commit()

    else:
        user_lang = user_in_db.language

    gettext.bindtextdomain(translation_domain, locales_dir)
    gettext.textdomain(translation_domain)
    translation = gettext.translation(translation_domain, locales_dir, languages=[user_lang], fallback=True)
    _ = translation.gettext

    return _(text)
