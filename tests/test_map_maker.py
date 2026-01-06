"""
Тесты для функции get_definitions из модуля map_maker.

Тесты покрывают все сценарии использования функции:
- Базовые случаи использования
- Граничные случаи
- Обработку ошибок
- Unicode и специальные символы
- Пользовательские словари
"""

import pytest
import sys
import os

# Добавляем родительскую директорию в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from map_maker import get_definitions


class TestGetDefinitions:
    """Тесты для функции get_definitions."""
    
    def test_basic_functionality(self):
        """Тест базовой функциональности."""
        # Тест с существующим словом
        result = get_definitions("apple")
        expected = [
            "A fruit that grows on trees",
            "A technology company founded by Steve Jobs"
        ]
        assert result == expected
        
        # Тест с другим существующим словом
        result = get_definitions("python")
        expected = [
            "A high-level programming language",
            "A large constricting snake"
        ]
        assert result == expected
    
    def test_word_not_found(self):
        """Тест случая, когда слово не найдено в словаре."""
        result = get_definitions("nonexistentword")
        assert result == []
        
        result = get_definitions("unknown")
        assert result == []
    
    def test_case_insensitivity(self):
        """Тест нечувствительности к регистру."""
        # Разные регистры должны возвращать одинаковый результат
        result_lower = get_definitions("apple")
        result_upper = get_definitions("APPLE")
        result_mixed = get_definitions("ApPlE")
        
        assert result_lower == result_upper == result_mixed
    
    def test_whitespace_handling(self):
        """Тест обработки пробелов."""
        # С пробелами в начале и конце
        result_with_spaces = get_definitions("  apple  ")
        result_without_spaces = get_definitions("apple")
        
        assert result_with_spaces == result_without_spaces
        
        # Только пробелы
        result = get_definitions("   ")
        assert result == []
    
    def test_empty_string(self):
        """Тест пустой строки."""
        result = get_definitions("")
        assert result == []
    
    def test_custom_dictionary(self):
        """Тест работы с пользовательским словарем."""
        custom_dict = {
            "python": ["Мой любимый язык программирования"],
            "openhands": ["Платформа для разработки ИИ"],
            "customword": ["Пользовательское определение"]
        }
        
        # С пользовательским словарем
        result = get_definitions("python", custom_dict)
        assert result == ["Мой любимый язык программирования"]
        
        # Слово есть только в пользовательском словаре
        result = get_definitions("customword", custom_dict)
        assert result == ["Пользовательское определение"]
        
        # Слово есть в стандартном словаре, но не в пользовательском
        result = get_definitions("apple", custom_dict)
        assert result == []
        
        # Пустой пользовательский словарь
        result = get_definitions("apple", {})
        assert result == []
    
    def test_unicode_and_special_characters(self):
        """Тест Unicode и специальных символов."""
        # Русские слова
        custom_dict = {
            "яблоко": ["Фрукт, растущий на деревьях"],
            "привет": ["Форма greeting на русском"]
        }
        
        result = get_definitions("яблоко", custom_dict)
        assert result == ["Фрукт, растущий на деревьях"]
        
        result = get_definitions("ПРИВЕТ", custom_dict)  # Проверка регистра
        assert result == ["Форма greeting на русском"]
        
        # Специальные символы
        custom_dict_special = {
            "test-word": ["Слово с дефисом"],
            "word_with_underscore": ["Слово с подчеркиванием"],
            "word@email.com": ["Электронная почта как слово"]
        }
        
        result = get_definitions("test-word", custom_dict_special)
        assert result == ["Слово с дефисом"]
        
        result = get_definitions("word@email.com", custom_dict_special)
        assert result == ["Электронная почта как слово"]
    
    def test_none_custom_dict(self):
        """Тест передачи None как пользовательского словаря."""
        # None должен обрабатываться как использование стандартного словаря
        result = get_definitions("apple", None)
        expected = [
            "A fruit that grows on trees",
            "A technology company founded by Steve Jobs"
        ]
        assert result == expected
    
    def test_dict_with_empty_values(self):
        """Тест словаря с пустыми значениями."""
        custom_dict = {
            "word1": [],
            "word2": [""],
            "word3": ["", ""]
        }
        
        result = get_definitions("word1", custom_dict)
        assert result == []
        
        result = get_definitions("word2", custom_dict)
        assert result == [""]
        
        result = get_definitions("word3", custom_dict)
        assert result == ["", ""]
    
    def test_multiple_definitions_order(self):
        """Тест порядка определений."""
        # Порядок определений должен сохраняться
        custom_dict = {
            "test": ["Первое определение", "Второе определение", "Третье определение"]
        }
        
        result = get_definitions("test", custom_dict)
        assert result == ["Первое определение", "Второе определение", "Третье определение"]
        assert len(result) == 3
    
    def test_numbers_as_words(self):
        """Тест чисел как слов."""
        custom_dict = {
            "123": ["Число сто двадцать три"],
            "42": ["Ответ на главный вопрос жизни, вселенной и всего такого"]
        }
        
        result = get_definitions("123", custom_dict)
        assert result == ["Число сто двадцать три"]
        
        result = get_definitions("42", custom_dict)
        assert result == ["Ответ на главный вопрос жизни, вселенной и всего такого"]
    
    def test_long_words(self):
        """Тест длинных слов."""
        long_word = "a" * 1000
        custom_dict = {
            long_word: ["Очень длинное слово"]
        }
        
        result = get_definitions(long_word, custom_dict)
        assert result == ["Очень длинное слово"]
    
    def test_edge_cases(self):
        """Тест граничных случаев."""
        # Слово с только пробелами и табами
        result = get_definitions(" \t\n ")
        assert result == []
        
        # Очень длинная строка с пробелами
        long_spaces = " " * 1000 + "apple" + " " * 1000
        result = get_definitions(long_spaces)
        expected = [
            "A fruit that grows on trees",
            "A technology company founded by Steve Jobs"
        ]
        assert result == expected
    
    def test_return_type(self):
        """Тест типа возвращаемого значения."""
        result = get_definitions("apple")
        assert isinstance(result, list)
        
        result = get_definitions("nonexistent")
        assert isinstance(result, list)
        
        # Все элементы должны быть строками
        result = get_definitions("python")
        for item in result:
            assert isinstance(item, str)


if __name__ == "__main__":
    # Запуск тестов при прямом выполнении файла
    pytest.main([__file__, "-v"])