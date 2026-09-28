import re
import unicodedata
from typing import Optional

# Standard English stop words
COMMON_STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", 
    "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", 
    "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", 
    "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", 
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", 
    "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", 
    "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", 
    "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", 
    "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", 
    "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", 
    "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", 
    "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", 
    "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", 
    "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", 
    "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", 
    "yourself", "yourselves", "will", "shall", "may", "might", "must", "can", "could"
}

# Standard resume section header patterns
SECTION_PATTERNS = {
    "summary": r"(?:professional\s+summary|profile|about\s+me|objective)",
    "skills": r"(?:technical\s+skills|core\s+competencies|skills|technologies|expertise)",
    "experience": r"(?:work\s+experience|professional\s+experience|employment\s+history|experience)",
    "education": r"(?:education|academic\s+background|degrees|qualifications)",
    "projects": r"(?:projects|key\s+projects|portfolio|personal\s+projects)",
    "certifications": r"(?:certifications|licenses|courses|awards)",
}

class TextPreprocessor:
    """Provides modular preprocessing and cleaning for resume & job description texts."""

    @staticmethod
    def normalize_text(text: str) -> str:
        """Cleans unicode, removes URLs, emails, phone numbers, and standardizes whitespace."""
        if not text:
            return ""
        
        # Unicode normalization
        text = unicodedata.normalize("NFKD", text)
        
        # Remove URLs
        text = re.sub(r"https?://\S+|www\.\S+", " ", text)
        
        # Remove emails
        text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", " ", text)
        
        # Remove phone numbers
        text = re.sub(r"\(?\b\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", " ", text)
        
        # Replace bullets, unusual quotes, special dashes with standard characters
        text = re.sub(r"[•●◆■▪►–—]", " ", text)
        
        # Collapse multiple spaces and newlines
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        
        return text.strip()

    @staticmethod
    def tokenize(text: str, remove_stopwords: bool = True) -> list[str]:
        """
        Tokenizes text into words, retaining technical characters like +, #, ., /
        e.g., c++, c#, .net, node.js, ci/cd
        """
        cleaned = TextPreprocessor.normalize_text(text).lower()
        
        # Pattern captures words including pluses (c++), hashes (c#), dots (node.js, .net), dashes/slashes (ci/cd)
        pattern = r"\b[a-z0-9]+(?:\.[a-z0-9]+|\+{2}|#|-[a-z0-9]+|/[a-z0-9]+)*\b"
        tokens = re.findall(pattern, cleaned)
        
        if remove_stopwords:
            tokens = [t for t in tokens if t not in COMMON_STOP_WORDS and len(t) > 1]
            
        return tokens

    @staticmethod
    def extract_sections(text: str) -> dict[str, str]:
        """Detects presence of key resume sections for structural evaluation."""
        found_sections = {}
        lines = text.split("\n")
        current_section = "general"
        section_buffers = {current_section: []}
        
        for line in lines:
            line_stripped = line.strip()
            matched_header = None
            
            # Check if line looks like a header (short, matches section keyword)
            if len(line_stripped) < 45:
                for section_name, pattern in SECTION_PATTERNS.items():
                    if re.match(rf"^#*\s*{pattern}[:\s]*$", line_stripped, re.IGNORECASE):
                        matched_header = section_name
                        break
            
            if matched_header:
                current_section = matched_header
                if current_section not in section_buffers:
                    section_buffers[current_section] = []
            else:
                section_buffers[current_section].append(line)
                
        for k, v in section_buffers.items():
            content = "\n".join(v).strip()
            if content:
                found_sections[k] = content
                
        return found_sections
