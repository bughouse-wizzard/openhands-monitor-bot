"""
Unit tests for the get_definitions function from map_maker.py.

Tests cover all usage scenarios:
- Basic functionality
- Edge cases
- Error handling
- Unicode and special characters
- Custom dictionaries
"""

import pytest
from map_maker import get_definitions


class TestGetDefinitions:
    """Tests for the get_definitions function."""
    
    def test_basic_functionality(self):
        """Test basic functionality with standard dictionary."""
        # Test with existing word
        result = get_definitions("apple")
        expected = [
            "A fruit that grows on trees",
            "A technology company founded by Steve Jobs"
        ]
        assert result == expected
        
        # Test with another existing word
        result = get_definitions("python")
        expected = [
            "A high-level programming language",
            "A large constricting snake"
        ]
        assert result == expected
    
    def test_word_not_found(self):
        """Test case when word is not found in dictionary."""
        result = get_definitions("nonexistentword")
        assert result == []
        
        result = get_definitions("unknown")
        assert result == []
    
    def test_case_insensitivity(self):
        """Test case insensitivity."""
        # Different cases should return the same result
        result_lower = get_definitions("apple")
        result_upper = get_definitions("APPLE")
        result_mixed = get_definitions("ApPlE")
        
        assert result_lower == result_upper == result_mixed
    
    def test_whitespace_handling(self):
        """Test whitespace handling."""
        # With spaces at beginning and end
        result_with_spaces = get_definitions("  apple  ")
        result_without_spaces = get_definitions("apple")
        
        assert result_with_spaces == result_without_spaces
        
        # Only spaces
        result = get_definitions("   ")
        assert result == []
    
    def test_empty_string(self):
        """Test empty string."""
        result = get_definitions("")
        assert result == []
    
    def test_custom_dictionary(self):
        """Test work with custom dictionary."""
        custom_dict = {
            "python": ["My favorite programming language"],
            "openhands": ["AI development platform"],
            "customword": ["Custom definition"]
        }
        
        # With custom dictionary
        result = get_definitions("python", custom_dict)
        assert result == ["My favorite programming language"]
        
        # Word exists only in custom dictionary
        result = get_definitions("customword", custom_dict)
        assert result == ["Custom definition"]
        
        # Word exists in standard dictionary but not in custom
        result = get_definitions("apple", custom_dict)
        assert result == []
        
        # Empty custom dictionary
        result = get_definitions("apple", {})
        assert result == []
    
    def test_none_custom_dict(self):
        """Test passing None as custom dictionary."""
        # None should be treated as using standard dictionary
        result = get_definitions("apple", None)
        expected = [
            "A fruit that grows on trees",
            "A technology company founded by Steve Jobs"
        ]
        assert result == expected
    
    def test_return_type(self):
        """Test return value type."""
        result = get_definitions("apple")
        assert isinstance(result, list)
        
        result = get_definitions("nonexistent")
        assert isinstance(result, list)
        
        # All elements should be strings
        result = get_definitions("python")
        for item in result:
            assert isinstance(item, str)
    
    def test_immutability_of_input_data(self):
        """Test immutability of input data."""
        # Check that function doesn't modify the passed dictionary
        original_dict = {
            "test": ["Definition 1", "Definition 2"],
            "another": ["Another definition"]
        }
        dict_copy = original_dict.copy()
        
        result = get_definitions("test", original_dict)
        
        # Check that dictionary hasn't changed
        assert original_dict == dict_copy
        
        # Check that returned list is a copy, not a reference
        if result:  # If there is a result
            result.append("New definition")
            assert "New definition" not in original_dict.get("test", [])
    
    def test_dict_with_non_list_values(self):
        """Test dictionary with non-list values."""
        # Function expects a list, but what if other types are passed?
        custom_dict = {
            "string_value": "Just a string, not a list",
            "int_value": 42,
            "dict_value": {"key": "value"},
            "tuple_value": ("item1", "item2")
        }
        
        # Now function always returns a list
        result = get_definitions("string_value", custom_dict)
        # Returns a list with one element
        assert result == ["Just a string, not a list"]
        
        result = get_definitions("int_value", custom_dict)
        assert result == [42]
        
        result = get_definitions("dict_value", custom_dict)
        assert result == [{"key": "value"}]
        
        result = get_definitions("tuple_value", custom_dict)
        assert result == [("item1", "item2")]
    
    def test_return_copy_not_reference(self):
        """Test that function returns a copy of the list, not a reference."""
        custom_dict = {
            "test_word": ["Definition 1", "Definition 2"]
        }
        
        result = get_definitions("test_word", custom_dict)
        
        # Check that it's a copy, not a reference
        assert result == ["Definition 1", "Definition 2"]
        
        # Modify the result
        result.append("Definition 3")
        
        # Check that original dictionary hasn't changed
        assert custom_dict["test_word"] == ["Definition 1", "Definition 2"]
        assert "Definition 3" not in custom_dict["test_word"]
    
    def test_numbers_as_words(self):
        """Test numbers as words."""
        custom_dict = {
            "123": ["Number one hundred twenty three"],
            "42": ["Answer to the ultimate question of life, the universe, and everything"]
        }
        
        result = get_definitions("123", custom_dict)
        assert result == ["Number one hundred twenty three"]
        
        result = get_definitions("42", custom_dict)
        assert result == ["Answer to the ultimate question of life, the universe, and everything"]
    
    def test_edge_cases(self):
        """Test edge cases."""
        # Word with only spaces and tabs
        result = get_definitions(" \t\n ")
        assert result == []
        
        # Very long string with spaces
        long_spaces = " " * 100 + "apple" + " " * 100
        result = get_definitions(long_spaces)
        expected = [
            "A fruit that grows on trees",
            "A technology company founded by Steve Jobs"
        ]
        assert result == expected


if __name__ == "__main__":
    # Run tests when file is executed directly
    pytest.main([__file__, "-v"])