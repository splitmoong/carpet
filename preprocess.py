'''static class'''

import re

class CleanPdfs:
    
    def clean_text(text: str) -> str:
        # Normalize invisible characters
        text = text.replace("\r", " ").replace("\f", " ")

        # Collapse all whitespace (spaces, tabs, newlines, Unicode spaces) into one
        text = re.sub(r'\s+', ' ', text, flags=re.UNICODE)

        # Remove isolated digits or page numbers
        text = re.sub(r'\b\d+\b', '', text)

        # Normalize punctuation
        text = text.replace("“", '"').replace("”", '"').replace("’", "'")

        # Trim edges
        return text.strip()
