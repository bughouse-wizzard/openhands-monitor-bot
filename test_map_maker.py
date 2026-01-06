"""
Tests for the map_maker module.
"""

import unittest
from map_maker import get_definitions


class TestGetDefinitions(unittest.TestCase):
    """Test cases for the get_definitions function."""
    
    def test_basic_word_found(self):
        """Test that a basic word returns definitions."""
        result = get_definitions("apple")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn("A fruit that grows on trees", result)
    
    def test_word_not_found(self):
        """Test that a non-existent word returns empty list."""
        result = get_definitions("nonexistentword")
        self.assertEqual(result, [])
    
    def test_case_insensitive(self):
        """Test that function is case-insensitive."""
        result1 = get_definitions("APPLE")
        result2 = get_definitions("apple")
        result3 = get_definitions("Apple")
        
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)
    
    def test_custom_dictionary(self):
        """Test with a custom dictionary."""
        custom_dict = {
            "test": ["definition 1", "definition 2"],
            "example": ["sample", "model"]
        }
        
        result = get_definitions("test", custom_dict)
        self.assertEqual(result, ["definition 1", "definition 2"])
        
        result = get_definitions("example", custom_dict)
        self.assertEqual(result, ["sample", "model"])
        
        result = get_definitions("unknown", custom_dict)
        self.assertEqual(result, [])
    
    def test_empty_string(self):
        """Test with empty string as word."""
        result = get_definitions("")
        self.assertEqual(result, [])
    
    def test_none_word(self):
        """Test with None as word."""
        result = get_definitions(None)
        self.assertEqual(result, [])
    
    def test_multiple_definitions(self):
        """Test that words with multiple definitions return all."""
        result = get_definitions("python")
        self.assertGreater(len(result), 1)
        self.assertIn("A programming language", result)
        self.assertIn("A type of snake", result)
    
    def test_special_characters(self):
        """Test words with special characters."""
        custom_dict = {
            "test-word": ["hyphenated word"],
            "test_word": ["underscored word"],
            "test.word": ["dotted word"]
        }
        
        result = get_definitions("test-word", custom_dict)
        self.assertEqual(result, ["hyphenated word"])
        
        result = get_definitions("test_word", custom_dict)
        self.assertEqual(result, ["underscored word"])
        
        result = get_definitions("test.word", custom_dict)
        self.assertEqual(result, ["dotted word"])
    
    def test_whitespace_handling(self):
        """Test words with leading/trailing whitespace."""
        custom_dict = {
            "word": ["definition"]
        }
        
        result = get_definitions("  word  ", custom_dict)
        self.assertEqual(result, ["definition"])
        
        result = get_definitions("\tword\n", custom_dict)
        self.assertEqual(result, ["definition"])
    
    def test_numeric_words(self):
        """Test numeric words."""
        custom_dict = {
            "123": ["number"],
            "1.5": ["decimal"]
        }
        
        result = get_definitions("123", custom_dict)
        self.assertEqual(result, ["number"])
        
        result = get_definitions("1.5", custom_dict)
        self.assertEqual(result, ["decimal"])
    
    def test_unicode_words(self):
        """Test unicode/foreign language words."""
        custom_dict = {
            "café": ["coffee shop"],
            "naïve": ["innocent"],
            "résumé": ["summary"]
        }
        
        result = get_definitions("café", custom_dict)
        self.assertEqual(result, ["coffee shop"])
        
        result = get_definitions("naïve", custom_dict)
        self.assertEqual(result, ["innocent"])
        
        result = get_definitions("résumé", custom_dict)
        self.assertEqual(result, ["summary"])
    
    def test_empty_dictionary(self):
        """Test with empty dictionary."""
        result = get_definitions("anyword", {})
        self.assertEqual(result, [])
    
    def test_none_dictionary(self):
        """Test with None as dictionary (should use default)."""
        result = get_definitions("apple", None)
        self.assertGreater(len(result), 0)
    
    def test_list_type_return(self):
        """Test that return type is always a list."""
        # Test with word found
        result = get_definitions("apple")
        self.assertIsInstance(result, list)
        
        # Test with word not found
        result = get_definitions("nonexistent")
        self.assertIsInstance(result, list)
        
        # Test with custom dictionary - string should be converted to list
        custom_dict = {"test": "not a list"}
        result = get_definitions("test", custom_dict)
        self.assertIsInstance(result, list)
        self.assertEqual(result, ["not a list"])
    
    def test_dictionary_modification(self):
        """Test that function doesn't modify the input dictionary."""
        custom_dict = {"word": ["definition"]}
        original_dict = custom_dict.copy()
        
        get_definitions("word", custom_dict)
        get_definitions("nonexistent", custom_dict)
        
        self.assertEqual(custom_dict, original_dict)
    
    def test_duplicate_definitions(self):
        """Test handling of duplicate definitions in dictionary."""
        custom_dict = {
            "test": ["def1", "def1", "def2", "def2"]
        }
        
        result = get_definitions("test", custom_dict)
        self.assertEqual(len(result), 4)  # Should return all duplicates
        self.assertEqual(result.count("def1"), 2)
        self.assertEqual(result.count("def2"), 2)


if __name__ == "__main__":
    unittest.main()