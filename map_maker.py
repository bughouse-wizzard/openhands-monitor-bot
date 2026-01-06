"""
Module for creating maps and getting definitions.
"""

def get_definitions(word, dictionary=None):
    """
    Get definitions for a given word from a dictionary.
    
    Args:
        word (str): The word to look up.
        dictionary (dict, optional): A dictionary mapping words to definitions.
            If None, uses a default dictionary.
    
    Returns:
        list: A list of definitions for the word. Returns empty list if word not found.
    
    Examples:
        >>> get_definitions("apple")
        ['A fruit that grows on trees', 'A technology company']
        
        >>> get_definitions("unknown")
        []
    """
    if dictionary is None:
        # Default dictionary with some example definitions
        dictionary = {
            "apple": ["A fruit that grows on trees", "A technology company"],
            "banana": ["A yellow curved fruit", "Slang for crazy"],
            "computer": ["An electronic device for processing data", "A person who computes"],
            "python": ["A programming language", "A type of snake"],
            "test": ["A procedure to check quality", "An examination"],
        }
    
    # Handle None or non-string words
    if word is None:
        return []
    
    # Convert to string and strip whitespace
    word_str = str(word).strip()
    if not word_str:
        return []
    
    # Convert word to lowercase for case-insensitive lookup
    word_lower = word_str.lower()
    
    # Get definitions from dictionary
    definitions = dictionary.get(word_lower)
    
    # Ensure we always return a list
    if definitions is None:
        return []
    
    # Convert to list if it's not already a list
    if not isinstance(definitions, list):
        return [definitions]
    
    return definitions