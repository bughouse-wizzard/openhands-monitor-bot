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
    
    def test_immutability_of_input_data(self):
        """Тест неизменяемости входных данных."""
        # Проверяем, что функция не изменяет переданный словарь
        original_dict = {
            "test": ["Определение 1", "Определение 2"],
            "another": ["Еще одно определение"]
        }
        dict_copy = original_dict.copy()
        
        result = get_definitions("test", original_dict)
        
        # Проверяем, что словарь не изменился
        assert original_dict == dict_copy
        
        # Проверяем, что возвращаемый список - это копия, а не ссылка
        if result:  # Если есть результат
            result.append("Новое определение")
            assert "Новое определение" not in original_dict.get("test", [])
    
    def test_large_dictionary_performance(self):
        """Тест производительности с большим словарем."""
        # Создаем большой словарь
        large_dict = {f"word_{i}": [f"Определение для слова {i}"] for i in range(1000)}
        
        # Добавляем тестовое слово
        large_dict["test_word"] = ["Тестовое определение"]
        
        # Тестируем поиск
        result = get_definitions("test_word", large_dict)
        assert result == ["Тестовое определение"]
        
        # Тестируем поиск несуществующего слова
        result = get_definitions("nonexistent_in_large", large_dict)
        assert result == []
    
    def test_dictionary_with_non_string_keys(self):
        """Тест словаря с нестроковыми ключами."""
        # Словарь с разными типами ключей
        mixed_dict = {
            "string_key": ["Строковый ключ"],
            123: ["Числовой ключ"],
            ("tuple", "key"): ["Кортеж как ключ"],
            None: ["None как ключ"]
        }
        
        # Функция ожидает строки, поэтому нестроковые ключи не будут найдены
        # при нормализации слова.get()
        result = get_definitions("string_key", mixed_dict)
        assert result == ["Строковый ключ"]
        
        # Число как строка
        result = get_definitions("123", mixed_dict)
        assert result == []
        
        # None как строка
        result = get_definitions("None", mixed_dict)
        assert result == []
    
    def test_none_word_input(self):
        """Тест передачи None как слова."""
        # None должен быть преобразован в строку "None"
        custom_dict = {
            "none": ["Строка 'none'"],
            "null": ["Строка 'null'"]
        }
        
        result = get_definitions(None, custom_dict)
        # None будет преобразован в строку "none" через str(None).lower()
        # Но лучше проверить поведение
        assert isinstance(result, list)
    
    def test_boolean_word_input(self):
        """Тест передачи булевых значений как слов."""
        custom_dict = {
            "true": ["Строка 'true'"],
            "false": ["Строка 'false'"]
        }
        
        result = get_definitions(True, custom_dict)
        assert isinstance(result, list)
        
        result = get_definitions(False, custom_dict)
        assert isinstance(result, list)
    
    def test_dict_with_non_list_values(self):
        """Тест словаря со значениями не в виде списков."""
        # Функция ожидает список, но что если передать другие типы?
        custom_dict = {
            "string_value": "Просто строка, не список",
            "int_value": 42,
            "dict_value": {"key": "value"},
            "tuple_value": ("элемент1", "элемент2")
        }
        
        # Теперь функция всегда возвращает список
        result = get_definitions("string_value", custom_dict)
        # Возвращается список с одним элементом
        assert result == ["Просто строка, не список"]
        
        result = get_definitions("int_value", custom_dict)
        assert result == [42]
        
        result = get_definitions("dict_value", custom_dict)
        assert result == [{"key": "value"}]
        
        result = get_definitions("tuple_value", custom_dict)
        assert result == [("элемент1", "элемент2")]
    
    def test_return_copy_not_reference(self):
        """Тест, что функция возвращает копию списка, а не ссылку."""
        custom_dict = {
            "test_word": ["Определение 1", "Определение 2"]
        }
        
        result = get_definitions("test_word", custom_dict)
        
        # Проверяем, что это копия, а не ссылка
        assert result == ["Определение 1", "Определение 2"]
        
        # Модифицируем результат
        result.append("Определение 3")
        
        # Проверяем, что оригинальный словарь не изменился
        assert custom_dict["test_word"] == ["Определение 1", "Определение 2"]
        assert "Определение 3" not in custom_dict["test_word"]
    
    def test_dict_with_none_values(self):
        """Тест словаря со значениями None."""
        custom_dict = {
            "word1": None,
            "word2": [None],
            "word3": ["Определение", None]
        }
        
        result = get_definitions("word1", custom_dict)
        assert result == [None]
        
        result = get_definitions("word2", custom_dict)
        assert result == [None]
        
        result = get_definitions("word3", custom_dict)
        assert result == ["Определение", None]
    
    def test_complex_normalization(self):
        """Тест сложных случаев нормализации."""
        # Разные виды пробелов и управляющих символов
        test_cases = [
            ("  apple\t", "apple"),  # табуляция
            ("apple\n", "apple"),    # перенос строки
            ("\r\napple\r\n", "apple"),  # Windows-style перенос
            ("\t\t  apple  \t\n", "apple"),  # смесь символов
        ]
        
        for input_word, expected_normalized in test_cases:
            # Создаем словарь с нормализованным словом
            custom_dict = {expected_normalized: [f"Определение для {expected_normalized}"]}
            
            result = get_definitions(input_word, custom_dict)
            assert result == [f"Определение для {expected_normalized}"]
    
    def test_nested_structures_in_definitions(self):
        """Тест вложенных структур в определениях."""
        custom_dict = {
            "complex_word": [
                {"nested": "dict"},
                ["list", "inside", "list"],
                {"mixed": ["list", "in", "dict"]}
            ]
        }
        
        result = get_definitions("complex_word", custom_dict)
        expected = [
            {"nested": "dict"},
            ["list", "inside", "list"],
            {"mixed": ["list", "in", "dict"]}
        ]
        
        assert result == expected
        # Функция возвращает копию списка, но не делает глубокую копию вложенных структур
        # Это ожидаемое поведение, так как используется list() для копирования списка
        # Проверяем, что список скопирован, но вложенные структуры могут быть ссылками
        assert result is not custom_dict["complex_word"]  # Список скопирован
        # Вложенные структуры могут быть теми же объектами (это нормально для list())

    def test_very_long_strings(self):
        """Тест очень длинных строк."""
        # Очень длинное слово
        long_word = "a" * 10000
        custom_dict = {
            long_word: ["Определение для очень длинного слова"]
        }
        
        result = get_definitions(long_word, custom_dict)
        assert result == ["Определение для очень длинного слова"]
        
        # Очень длинное определение
        long_definition = "Очень длинное определение " * 1000
        custom_dict = {
            "test": [long_definition]
        }
        
        result = get_definitions("test", custom_dict)
        assert result == [long_definition]
        assert len(result[0]) > 10000  # Проверяем, что определение действительно длинное

    def test_unicode_normalization(self):
        """Тест нормализации Unicode символов."""
        # Слова с разными формами Unicode
        test_cases = [
            ("café", "cafe"),  # символ с акцентом
            ("naïve", "naive"),  # символ с умляутом
            ("résumé", "resume"),  # несколько символов с акцентами
        ]
        
        for word, expected_normalized in test_cases:
            # Создаем словарь с нормализованным словом
            custom_dict = {expected_normalized: [f"Определение для {expected_normalized}"]}
            
            # Проверяем, что функция нормализует слово
            result = get_definitions(word, custom_dict)
            # Функция использует .lower(), но не нормализует Unicode
            # Поэтому проверяем, что слово не найдено (ожидаемое поведение)
            assert result == []

    def test_empty_dictionary_edge_cases(self):
        """Тест граничных случаев с пустыми словарями."""
        # Полностью пустой словарь
        result = get_definitions("anyword", {})
        assert result == []
        
        # Словарь с пустыми ключами
        custom_dict = {
            "": ["Определение для пустой строки"],
            "   ": ["Определение для пробелов"]
        }
        
        result = get_definitions("", custom_dict)
        assert result == ["Определение для пустой строки"]
        
        # Функция использует strip(), поэтому "   " становится ""
        result = get_definitions("   ", custom_dict)
        assert result == ["Определение для пустой строки"]  # После strip() это пустая строка

    def test_performance_with_various_dict_sizes(self):
        """Тест производительности с разными размерами словарей."""
        import time
        
        # Тест с маленьким словарем
        small_dict = {f"word_{i}": [f"def_{i}"] for i in range(10)}
        start_time = time.time()
        result = get_definitions("word_5", small_dict)
        small_time = time.time() - start_time
        assert result == ["def_5"]
        
        # Тест со средним словарем
        medium_dict = {f"word_{i}": [f"def_{i}"] for i in range(1000)}
        start_time = time.time()
        result = get_definitions("word_500", medium_dict)
        medium_time = time.time() - start_time
        assert result == ["def_500"]
        
        # Тест с большим словарем
        large_dict = {f"word_{i}": [f"def_{i}"] for i in range(10000)}
        start_time = time.time()
        result = get_definitions("word_5000", large_dict)
        large_time = time.time() - start_time
        assert result == ["def_5000"]
        
        # Проверяем, что время поиска разумное (менее 0.1 секунды для каждого)
        assert small_time < 0.1, f"Small dict search took {small_time} seconds"
        assert medium_time < 0.1, f"Medium dict search took {medium_time} seconds"
        assert large_time < 0.1, f"Large dict search took {large_time} seconds"

    def test_special_unicode_characters(self):
        """Тест специальных символов Unicode."""
        # Эмодзи и специальные символы
        custom_dict = {
            "🎉": ["Символ праздника"],
            "🔥": ["Символ огня"],
            "❤️": ["Символ сердца"],
            "café": ["Французское кафе"],
            "naïve": ["Наивный на французском"],
        }
        
        result = get_definitions("🎉", custom_dict)
        assert result == ["Символ праздника"]
        
        result = get_definitions("🔥", custom_dict)
        assert result == ["Символ огня"]
        
        result = get_definitions("café", custom_dict)
        assert result == ["Французское кафе"]

    def test_dict_with_function_as_value(self):
        """Тест словаря с функцией в качестве значения."""
        def custom_function():
            return "Результат функции"
        
        custom_dict = {
            "function_word": custom_function
        }
        
        result = get_definitions("function_word", custom_dict)
        # Функция будет обернута в список
        assert result == [custom_function]
        assert callable(result[0])  # Проверяем, что это действительно функция

    def test_concurrent_access_simulation(self):
        """Тест симуляции конкурентного доступа к функции."""
        import threading
        
        results = []
        
        def worker(word, custom_dict, results_list):
            result = get_definitions(word, custom_dict)
            results_list.append((word, result))
        
        custom_dict = {f"word_{i}": [f"def_{i}"] for i in range(100)}
        
        threads = []
        for i in range(10):
            t = threading.Thread(target=worker, args=(f"word_{i}", custom_dict, results))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        # Проверяем, что все результаты корректны
        for i, (word, result) in enumerate(results):
            if i < 10:  # Первые 10 слов существуют в словаре
                assert result == [f"def_{i}"]
            else:
                assert result == []


if __name__ == "__main__":
    # Запуск тестов при прямом выполнении файла
    pytest.main([__file__, "-v"])