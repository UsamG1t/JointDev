import locale
import gettext
import random

# _podir = "./po"
# translation = gettext.translation("LocaleCounter", _podir, fallback=True)
# _, ngettext = translation.gettext, translation.ngettext

LOCALES = {
    ("ru_RU", "UTF-8"): gettext.translation("LocaleCounter", "./po", ["ru_RU.UTF-8"]),
    ("en_US", "UTF-8"): gettext.NullTranslations(),
}

def ngettext(*text):
    return LOCALES[random.choice([("ru_RU", "UTF-8"), ("en_US", "UTF-8")])].ngettext(*text)

while count := input():
    n = len(count.split())
    print(ngettext("Entered {} word", "Entered {} words", n).format(n))