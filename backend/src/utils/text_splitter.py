import re
from typing import List, Tuple
from .config import settings


class TextSplitter:
    def __init__(self, chunk_size: int = None, chunk_overlap: int = 50):
        self.chunk_size = chunk_size or settings.max_chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text: str) -> List[Tuple[str, int, int]]:
        """
        Split text into chunks of specified size with overlap.
        Returns list of tuples (chunk_text, start_pos, end_pos)
        """
        if len(text) <= self.chunk_size:
            return [(text, 0, len(text))]
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Determine the end position
            end = start + self.chunk_size
            
            # If we're at the end of the text
            if end >= len(text):
                chunks.append((text[start:], start, len(text)))
                break
            
            # Try to find a sentence boundary near the end
            chunk = text[start:end]
            last_sentence_end = max(
                chunk.rfind('. '),
                chunk.rfind('? '),
                chunk.rfind('! '),
                chunk.rfind('\n')
            )
            
            # If we found a sentence boundary and it's not too close to the start
            if last_sentence_end > len(chunk) // 2:
                actual_end = start + last_sentence_end + 1
                chunks.append((text[start:actual_end], start, actual_end))
                start = actual_end - self.chunk_overlap
            else:
                # If no good sentence boundary, just cut at the limit
                chunks.append((text[start:end], start, end))
                start = end - self.chunk_overlap
            
            # Ensure we're making progress
            if start <= 0:
                start = end
            elif start >= len(text):
                break
        
        return chunks


def count_tokens(text: str) -> int:
    """
    Rough estimation of token count.
    In practice, you might want to use a tokenizer specific to your model.
    """
    # Simple estimation: 1 token ~ 4 characters for English text
    return len(text) // 4


def validate_chunk_size(text: str, min_size: int = None, max_size: int = None) -> bool:
    """
    Validate that text chunk size is within acceptable limits
    """
    min_size = min_size or settings.min_chunk_size
    max_size = max_size or settings.max_chunk_size
    
    token_count = count_tokens(text)
    return min_size <= token_count <= max_size