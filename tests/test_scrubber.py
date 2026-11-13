"""Unit tests for agent-prompt-steganography-scrubber."""
import unittest
from agent_prompt_steganography_scrubber.scrubber import PromptSteganographyScrubber

class TestPromptScrubber(unittest.TestCase):
    def test_zero_width_removal(self):
        text = "safe​code﻿"
        report = PromptSteganographyScrubber.scrub(text)
        self.assertEqual(report.clean_text, "safecode")
        self.assertEqual(report.zero_width_removed, 2)

    def test_homoglyph_mapping(self):
        # Cyrillic 'с' and 'а'
        text = "саt"
        report = PromptSteganographyScrubber.scrub(text)
        self.assertEqual(report.clean_text, "cat")
        self.assertEqual(report.homoglyphs_mapped, 2)

if __name__ == "__main__":
    unittest.main()
