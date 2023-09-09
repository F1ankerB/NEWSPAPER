from django import template

register = template.Library()

@register.filter
def censor(value):
    # Список нежелательных слов, которые вы хотите заменить
    unwanted_words = ["сиськижопа", "жопа", 'сиськи']

    # Разбиваем строку на слова
    words = value.split()

    # Заменяем нежелательные слова на "*"
    censored_words = [word if word.lower() not in unwanted_words else '*' * len(word) for word in words]

    # Собираем обратно в строку
    censored_text = ' '.join(censored_words)

    return censored_text