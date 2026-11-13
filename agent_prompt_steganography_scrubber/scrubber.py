"""Unicode and homoglyph prompt steganography scrubber."""
import unicodedata
from typing import Dict, List, Optional, Tuple, Any

# Common Cyrillic to Latin homoglyphs
HOMOGLYPH_MAP = {
    'а': 'a', 'с': 'c', 'е': 'e', 'о': 'o', 'р': 'p', 'х': 'x', 'у': 'y',
    'А': 'A', 'В': 'B', 'С': 'C', 'Е': 'E', 'Н': 'H', 'О': 'O', 'Р': 'P',
    'Т': 'T', 'Х': 'X'
}

ZERO_WIDTH_CODEPOINTS = {
    0x200B,  # Zero-width space
    0x200C,  # Zero-width non-joiner
    0x200D,  # Zero-width joiner
    0x200E,  # Left-to-right mark
    0x200F,  # Right-to-left mark
    0xFEFF,  # Zero-width no-break space
    0x202A, 0x202B, 0x202C, 0x202D, 0x202E  # BiDi overrides
}

class ScrubReport:
    def __init__(self, original_len: int, scrubbed_len: int, zero_width_removed: int, homoglyphs_mapped: int, clean_text: str):
        self.original_len = original_len
        self.scrubbed_len = scrubbed_len
        self.zero_width_removed = zero_width_removed
        self.homoglyphs_mapped = homoglyphs_mapped
        self.clean_text = clean_text

class PromptSteganographyScrubber:
    """Sanitizes text by stripping invisible zero-width chars and normalizing homoglyphs."""

    @staticmethod
    def scrub(text: str) -> ScrubReport:
        # Step 1: Normalize unicode to NFKC
        normalized = unicodedata.normalize("NFKC", text)

        zw_count = 0
        cleaned_chars = []
        for char in normalized:
            cp = ord(char)
            if cp in ZERO_WIDTH_CODEPOINTS or (0xE0000 <= cp <= 0xE007F):
                zw_count += 1
            else:
                cleaned_chars.append(char)

        # Step 2: Normalize homoglyphs
        homoglyph_count = 0
        final_chars = []
        for char in cleaned_chars:
            if char in HOMOGLYPH_MAP:
                final_chars.append(HOMOGLYPH_MAP[char])
                homoglyph_count += 1
            else:
                final_chars.append(char)

        clean_text = "".join(final_chars)
        return ScrubReport(
            original_len=len(text),
            scrubbed_len=len(clean_text),
            zero_width_removed=zw_count,
            homoglyphs_mapped=homoglyph_count,
            clean_text=clean_text
        )
