"""
Модуль для работы с определениями слов.

Предоставляет функцию get_definitions для получения определений слов
из стандартного или пользовательского словаря.
"""

# Стандартный словарь с определениями
STANDARD_DICTIONARY = {
    "apple": [
        "A fruit that grows on trees",
        "A technology company founded by Steve Jobs"
    ],
    "python": [
        "A high-level programming language",
        "A large constricting snake"
    ],
    "openhands": [
        "A platform for AI development and collaboration"
    ],
    "test": [
        "A procedure intended to establish the quality, performance, or reliability of something",
        "An examination of someone's knowledge or proficiency"
    ],
    "hello": [
        "A greeting or expression of goodwill",
        "Used to attract attention"
    ],
    "world": [
        "The earth, together with all of its countries and peoples",
        "A particular region or group of countries"
    ]
}


def get_definitions(word: str, custom_dict: dict = None) -> list:
    """
    Получает определения слова из словаря.
    
    Args:
        word (str): Слово для поиска определений
        custom_dict (dict, optional): Пользовательский словарь. 
            Если не указан, используется стандартный словарь.
    
    Returns:
        list: Список определений слова. Если слово не найдено, 
              возвращает пустой список.
    
    Examples:
        >>> get_definitions("apple")
        ['A fruit that grows on trees', 'A technology company founded by Steve Jobs']
        
        >>> custom_dict = {"python": ["Мой любимый язык программирования"]}
        >>> get_definitions("python", custom_dict)
        ['Мой любимый язык программирования']
        
        >>> get_definitions("nonexistent")
        []
    """
    # Нормализуем слово: приводим к нижнему регистру и удаляем лишние пробелы
    normalized_word = word.strip().lower()
    
    # Выбираем словарь для поиска
    dictionary = custom_dict if custom_dict is not None else STANDARD_DICTIONARY
    
    # Возвращаем определения или пустой список
    return dictionary.get(normalized_word, [])