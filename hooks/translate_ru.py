import requests
import json

cyrillic_latin = {u'а': 'a', u'б': 'b', u'в': 'v', u'г': 'g',
                  u'д': 'd', u'е': 'ye', u'ё': 'yo', u'ж': 'zh',
                  u'з': 'z', u'и': 'i', u'й': 'j', u'к': 'k',
                  u'л': 'l', u'м': 'm', u'н': 'n', u'о': 'o',
                  u'п': 'p', u'р': 'r', u'с': 's', u'т': 't',
                  u'у': 'u', u'ф': 'f', u'х': 'h', u'ц': 'ts',
                  u'ч': 'ch', u'ш': 'sh', u'щ': 'sch', u'ы': 'i',
                  u'э': 'e', u'ю': 'yu', u'я': 'ya', u' ': ' ', 
                  u'ъ': '', u'ь': ''}


def translate_text(bot, text):
    api_key = bot.config['Yandex']['translate_key']
    api_url = "https://translate.yandex.net/api/v1.5/tr.json/translate?key=%s&text=%s&lang=ru-en" % (api_key, text)
    api_response = requests.get(api_url).text
    api_json = json.loads(api_response)
    print(api_json)
    return api_json['text'][0]


def message_hook(bot, channel, sender, message):
    if set(message) <= set(cyrillic_latin.keys()):
        translit = ''.join(str(c) for c in map(lambda x: cyrillic_latin[x], message))
        translate = translate_text(bot, message)
        bot.message(channel, '%s <%s> ~ %s' % (message, translit, translate))
