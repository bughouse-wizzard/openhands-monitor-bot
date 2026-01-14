"""
Module for working with word definitions.

Provides the get_definitions function for retrieving word definitions
from a standard or custom dictionary.
"""

# Standard dictionary with definitions
# dict: Standard dictionary containing word definitions.
# This dictionary contains common words with their definitions. It serves
# as the default dictionary for the get_definitions function.
# Keys are lowercase strings (words), values are lists of definition strings.
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
    Retrieves definitions for a word from a dictionary.

    This function looks up a word in either the standard dictionary or a
    provided custom dictionary. It performs case-insensitive search and
    normalizes input by converting to lowercase and stripping whitespace.

    Args:
        word (str): The word to look up definitions for. Non-string inputs
            will be converted to strings.
        custom_dict (dict, optional): Custom dictionary to use instead of
            the standard dictionary. If None, uses STANDARD_DICTIONARY.

    Returns:
        list: List of definitions for the word. Returns an empty list if
            the word is not found in the dictionary.

    Raises:
        AttributeError: If custom_dict is provided but is not a dictionary
            (does not have a .get() method).

    Examples:
        >>> get_definitions("apple")
        ['A fruit that grows on trees', 'A technology company founded by Steve Jobs']
        
        >>> custom_dict = {"python": ["My favorite programming language"]}
        >>> get_definitions("python", custom_dict)
        ['My favorite programming language']
        
        >>> get_definitions("nonexistent")
        []
        
        >>> get_definitions("  APPLE  ")  # Normalized input
        ['A fruit that grows on trees', 'A technology company founded by Steve Jobs']
    """
    # Проверяем, что word является строкой
    if not isinstance(word, str):
        # Преобразуем в строку для обработки
        word = str(word)
    
    # Нормализуем слово: приводим к нижнему регистру и удаляем лишние пробелы
    normalized_word = word.strip().lower()
    
    # Выбираем словарь для поиска
    dictionary = custom_dict if custom_dict is not None else STANDARD_DICTIONARY
    
    # Возвращаем копию списка определений или пустой список
    # Используем копию, чтобы избежать изменения оригинального словаря
    definitions = dictionary.get(normalized_word, [])
    
    # Если definitions не является списком, оборачиваем его в список
    if not isinstance(definitions, list):
        definitions = [definitions]
    
    # Возвращаем копию списка
    return list(definitions)