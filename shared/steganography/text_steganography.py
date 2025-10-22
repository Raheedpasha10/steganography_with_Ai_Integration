"""
Text Steganography Module with AI Integration
"""

import random
import string
from typing import Optional

class TextSteganography:
    """Text steganography implementation with AI enhancement"""
    
    def __init__(self):
        """Initialize the text steganography module"""
        self.ai_model = None  # Placeholder for AI model
        
    def embed_message(self, cover_text: str, secret_message: str, method: str = "whitespace") -> str:
        """
        Embed a secret message into cover text using specified method
        
        Args:
            cover_text (str): The text to hide the message in
            secret_message (str): The secret message to hide
            method (str): The steganography method to use
            
        Returns:
            str: The steganographic text with hidden message
        """
        if method == "whitespace":
            return self._embed_whitespace(cover_text, secret_message)
        elif method == "synonym":
            return self._embed_synonym(cover_text, secret_message)
        elif method == "binary":
            return self._embed_binary(cover_text, secret_message)
        else:
            raise ValueError(f"Unsupported method: {method}")
            
    def extract_message(self, stego_text: str, method: str = "whitespace") -> str:
        """
        Extract a secret message from steganographic text
        
        Args:
            stego_text (str): The text containing the hidden message
            method (str): The steganography method used
            
        Returns:
            str: The extracted secret message
        """
        if method == "whitespace":
            return self._extract_whitespace(stego_text)
        elif method == "synonym":
            return self._extract_synonym(stego_text)
        elif method == "binary":
            return self._extract_binary(stego_text)
        else:
            raise ValueError(f"Unsupported method: {method}")
            
    def _embed_whitespace(self, cover_text: str, secret_message: str) -> str:
        """
        Embed message using whitespace variation technique (tabs and spaces)
        
        Args:
            cover_text (str): The text to hide the message in
            secret_message (str): The secret message to hide
            
        Returns:
            str: The steganographic text with hidden message
        """
        # Convert message to binary
        binary_message = ''.join(format(ord(char), '08b') for char in secret_message)
        binary_message += '00000000'  # End of message marker
        
        # Split text into words
        words = cover_text.split()
        
        # We need at least as many spaces as bits in our message
        if len(words) - 1 < len(binary_message):
            # If not enough spaces, duplicate words to create more spaces
            while len(words) - 1 < len(binary_message):
                # Add duplicate words at the end
                words.append(words[len(words) % len(cover_text.split())])
        
        # Encode each bit in the whitespace using different space characters
        stego_words = []
        
        for i in range(len(words)):
            stego_words.append(words[i])
            if i < len(words) - 1:  # Don't add space after last word
                if i < len(binary_message):
                    # If bit is 1, use tab, if 0, use single space
                    space = '\t' if binary_message[i] == '1' else ' '
                    stego_words.append(space)
                else:
                    # Use regular space for remaining positions
                    stego_words.append(' ')
            
        return ''.join(stego_words)
        
    def _extract_whitespace(self, stego_text: str) -> str:
        """
        Extract message from whitespace variation (tabs and spaces)
        
        Args:
            stego_text (str): The text containing the hidden message
            
        Returns:
            str: The extracted secret message
        """
        # Parse the text to find tabs and spaces between words
        binary_message = ""
        parts = []
        current_part = ""
        
        for char in stego_text:
            if char in [' ', '\t']:
                if current_part:  # If we have accumulated a word
                    parts.append(current_part)
                    current_part = ""
                parts.append(char)  # Add the whitespace character
            else:
                current_part += char
                
        if current_part:  # Don't forget the last word
            parts.append(current_part)
        
        # Now extract bits from whitespace characters
        for part in parts:
            if part == '\t':
                binary_message += '1'
            elif part == ' ':
                binary_message += '0'
                
        # Convert binary to text
        message = ""
        # Process in 8-bit chunks
        for i in range(0, len(binary_message), 8):
            if i + 8 <= len(binary_message):
                byte = binary_message[i:i+8]
                if byte == '00000000':  # End of message marker
                    break
                try:
                    char = chr(int(byte, 2))
                    message += char
                except ValueError:
                    # Skip invalid bytes
                    continue
                    
        return message
        
    def _embed_synonym(self, cover_text: str, secret_message: str) -> str:
        """
        Embed message using synonym substitution technique with punctuation variation
        
        Args:
            cover_text (str): The text to hide the message in
            secret_message (str): The secret message to hide
            
        Returns:
            str: The steganographic text with hidden message
        """
        # Extended synonyms with more options
        synonyms = {
            'the': ['the', 'this', 'that', 'these', 'those'],
            'and': ['and', 'also', 'plus', 'furthermore', 'moreover'],
            'or': ['or', 'either', 'else', 'alternatively', 'otherwise'],
            'but': ['but', 'however', 'yet', 'nevertheless', 'nonetheless'],
            'is': ['is', 'exists', 'appears', 'seems', 'represents'],
            'are': ['are', 'exist', 'seem', 'appear', 'represent'],
            'was': ['was', 'were', 'existed', 'occurred', 'happened'],
            'were': ['were', 'was', 'seemed', 'appeared', 'occurred'],
            'have': ['have', 'possess', 'own', 'contain', 'hold'],
            'has': ['has', 'possesses', 'owns', 'contains', 'holds'],
            'had': ['had', 'possessed', 'owned', 'contained', 'held'],
            'do': ['do', 'perform', 'execute', 'accomplish', 'achieve'],
            'does': ['does', 'performs', 'executes', 'accomplishes', 'achieves'],
            'did': ['did', 'performed', 'executed', 'accomplished', 'achieved'],
            'will': ['will', 'shall', 'going to', 'intend to', 'plan to'],
            'would': ['would', 'should', 'going to', 'intend to', 'plan to'],
            'could': ['could', 'might', 'possibly', 'potentially', 'perhaps'],
            'should': ['should', 'ought to', 'must', 'need to', 'have to'],
            'may': ['may', 'might', 'possibly', 'potentially', 'perhaps'],
            'can': ['can', 'could', 'able to', 'capable of', 'permitted to'],
            'be': ['be', 'exist', 'become', 'appear', 'seem']
        }
        
        # Convert message to binary
        binary_message = ''.join(format(ord(char), '08b') for char in secret_message)
        binary_message += '00000000'  # End of message marker
        
        words = cover_text.split()
        stego_words = []
        bit_index = 0
        
        # Process each word and substitute synonyms to encode bits
        for i, word in enumerate(words):
            # Extract clean word and punctuation
            clean_word = word.lower().strip('.,!?;:"()[]{}')
            punctuation = ''.join(c for c in word if c in '.,!?;:"()[]{}')
            is_capitalized = word[0].isupper() if word else False
            
            # Check if this word can be used for synonym substitution
            if clean_word in synonyms and bit_index < len(binary_message):
                # Get the bit to encode
                bit = binary_message[bit_index]
                bit_index += 1
                
                # Choose synonym based on bit value
                options = synonyms[clean_word]
                if bit == '1':
                    # Use second synonym for 1
                    synonym = options[1] if len(options) > 1 else options[0]
                else:
                    # Use first synonym for 0
                    synonym = options[0]
                    
                # Preserve original capitalization and punctuation
                if is_capitalized:
                    synonym = synonym.capitalize()
                synonym += punctuation
                    
                stego_words.append(synonym)
            else:
                stego_words.append(word)
                
        # If we still have bits to encode and ran out of words, add dummy words
        while bit_index < len(binary_message):
            bit = binary_message[bit_index]
            bit_index += 1
            
            # Create a dummy word with appropriate encoding
            if bit == '1':
                dummy_word = 'Furthermore'
            else:
                dummy_word = 'and'
                
            stego_words.append(dummy_word)
            
        return ' '.join(stego_words)
        
    def _extract_synonym(self, stego_text: str) -> str:
        """
        Extract message from synonym substitution with punctuation variation
        
        Args:
            stego_text (str): The text containing the hidden message
            
        Returns:
            str: The extracted secret message
        """
        # Extended synonyms with more options
        synonyms = {
            'the': ['the', 'this', 'that', 'these', 'those'],
            'and': ['and', 'also', 'plus', 'furthermore', 'moreover'],
            'or': ['or', 'either', 'else', 'alternatively', 'otherwise'],
            'but': ['but', 'however', 'yet', 'nevertheless', 'nonetheless'],
            'is': ['is', 'exists', 'appears', 'seems', 'represents'],
            'are': ['are', 'exist', 'seem', 'appear', 'represent'],
            'was': ['was', 'were', 'existed', 'occurred', 'happened'],
            'were': ['were', 'was', 'seemed', 'appeared', 'occurred'],
            'have': ['have', 'possess', 'own', 'contain', 'hold'],
            'has': ['has', 'possesses', 'owns', 'contains', 'holds'],
            'had': ['had', 'possessed', 'owned', 'contained', 'held'],
            'do': ['do', 'perform', 'execute', 'accomplish', 'achieve'],
            'does': ['does', 'performs', 'executes', 'accomplishes', 'achieves'],
            'did': ['did', 'performed', 'executed', 'accomplished', 'achieved'],
            'will': ['will', 'shall', 'going to', 'intend to', 'plan to'],
            'would': ['would', 'should', 'going to', 'intend to', 'plan to'],
            'could': ['could', 'might', 'possibly', 'potentially', 'perhaps'],
            'should': ['should', 'ought to', 'must', 'need to', 'have to'],
            'may': ['may', 'might', 'possibly', 'potentially', 'perhaps'],
            'can': ['can', 'could', 'able to', 'capable of', 'permitted to'],
            'be': ['be', 'exist', 'become', 'appear', 'seem']
        }
        
        words = stego_text.split()
        binary_message = ""
        
        for word in words:
            clean_word = word.lower().strip('.,!?;:"()[]{}')
            # Check if this word is a synonym of a common word
            found = False
            for base_word, options in synonyms.items():
                if clean_word == options[0]:
                    binary_message += '0'
                    found = True
                    break
                elif len(options) > 1 and clean_word == options[1]:
                    binary_message += '1'
                    found = True
                    break
            
            # Check for dummy words used for encoding
            if not found:
                if clean_word == 'furthermore':
                    binary_message += '1'
                elif clean_word == 'and':
                    binary_message += '0'
        
        # Convert binary to text
        message = ""
        # Process in 8-bit chunks, stopping at the end marker
        for i in range(0, len(binary_message), 8):
            if i + 8 <= len(binary_message):
                byte = binary_message[i:i+8]
                if byte == '00000000':  # End of message marker
                    break
                try:
                    char = chr(int(byte, 2))
                    message += char
                except ValueError:
                    # Skip invalid bytes
                    continue
                    
        return message

    def _embed_binary(self, cover_text: str, secret_message: str) -> str:
        """
        Embed message using binary encoding in word capitalization
        
        Args:
            cover_text (str): The text to hide the message in
            secret_message (str): The secret message to hide
            
        Returns:
            str: The steganographic text with hidden message
        """
        # Convert message to binary
        binary_message = ''.join(format(ord(char), '08b') for char in secret_message)
        binary_message += '00000000'  # End of message marker
        
        words = cover_text.split()
        stego_words = []
        bit_index = 0
        
        # Process each word and adjust capitalization to encode bits
        for i, word in enumerate(words):
            if bit_index < len(binary_message):
                # Get the bit to encode
                bit = binary_message[bit_index]
                bit_index += 1
                
                # Extract clean word and punctuation
                clean_word = ''.join(c for c in word if c.isalpha())
                punctuation = ''.join(c for c in word if not c.isalpha())
                
                # Encode bit using capitalization
                if bit == '1':
                    # Capitalize first letter for 1
                    if clean_word:
                        processed_word = clean_word[0].upper() + clean_word[1:].lower() if len(clean_word) > 1 else clean_word.upper()
                    else:
                        processed_word = clean_word
                else:
                    # Lowercase for 0
                    processed_word = clean_word.lower()
                    
                stego_words.append(processed_word + punctuation)
            else:
                # No more bits to encode, keep original word
                stego_words.append(word)
                
        # If we still have bits to encode and ran out of words, add dummy words
        while bit_index < len(binary_message):
            bit = binary_message[bit_index]
            bit_index += 1
            
            # Create a dummy word with appropriate encoding
            if bit == '1':
                dummy_word = 'Data'
            else:
                dummy_word = 'data'
                
            stego_words.append(dummy_word)
            
        return ' '.join(stego_words)
        
    def _extract_binary(self, stego_text: str) -> str:
        """
        Extract message from binary encoding in word capitalization
        
        Args:
            stego_text (str): The text containing the hidden message
            
        Returns:
            str: The extracted secret message
        """
        words = stego_text.split()
        binary_message = ""
        
        # Extract bits from word capitalization
        for word in words:
            clean_word = ''.join(c for c in word if c.isalpha())
            # Check if first letter is capitalized
            if clean_word and clean_word[0].isupper():
                binary_message += '1'
            else:
                binary_message += '0'
                
        # Convert binary to text
        message = ""
        # Process in 8-bit chunks, stopping at the end marker
        for i in range(0, len(binary_message), 8):
            if i + 8 <= len(binary_message):
                byte = binary_message[i:i+8]
                if byte == '00000000':  # End of message marker
                    break
                try:
                    char = chr(int(byte, 2))
                    message += char
                except ValueError:
                    # Skip invalid bytes
                    continue
                    
        return message

    def analyze_text(self, text: str) -> dict:
        """
        Analyze text using AI to determine optimal steganography method
        
        Args:
            text (str): The text to analyze
            
        Returns:
            dict: Analysis results with recommendations
        """
        # Placeholder for AI analysis
        # In a real implementation, this would use an AI model to analyze:
        # - Text complexity
        # - Word frequency distribution
        # - Syntactic structure
        # - Semantic content
        
        word_count = len(text.split())
        char_count = len(text)
        
        # Simple heuristic for method selection
        if word_count < 50:
            recommended_method = "whitespace"
        else:
            recommended_method = "synonym"
            
        return {
            "word_count": word_count,
            "char_count": char_count,
            "recommended_method": recommended_method,
            "confidence": 0.75
        }