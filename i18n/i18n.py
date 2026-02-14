import json
import locale
import os

# Get the directory where i18n.py is located
I18N_DIR = os.path.dirname(os.path.abspath(__file__))
LOCALE_DIR = os.path.join(I18N_DIR, "locale")

def load_language_list(language):
    file_path = os.path.join(LOCALE_DIR, f"{language}.json")
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


class I18nAuto:
    def __init__(self, language=None):
        if language in ["Auto", None]:
            try:
                # getdefaultlocale is deprecated, but works for older python
                # for newer ones, we just try to get something
                language = locale.getdefaultlocale()[0]
            except:
                language = "en_US"
        
        if not language or not os.path.exists(os.path.join(LOCALE_DIR, f"{language}.json")):
            language = "en_US"
            
        self.language = language
        self.language_map = load_language_list(language)

    def __call__(self, key):
        return self.language_map.get(key, key)

    def __repr__(self):
        return "Use Language: " + self.language
