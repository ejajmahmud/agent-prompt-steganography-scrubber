"""CLI for agent-prompt-steganography-scrubber."""
import sys
import argparse
from .scrubber import PromptSteganographyScrubber

def main():
    parser = argparse.ArgumentParser(description="Agent Prompt Steganography Scrubber CLI")
    parser.add_argument("--demo", action="store_true", help="Run prompt steganography scrubbing demo")
    args = parser.parse_args()

    if args.demo:
        scrubber = PromptSteganographyScrubber()
        # Cyrillic 'а' + zero width space
        tampered = "p​аssword"
        report = scrubber.scrub(tampered)
        print(f"[*] Tampered input: {tampered.encode('unicode_escape')}")
        print(f"[+] Clean output: '{report.clean_text}' (Removed {report.zero_width_removed} ZWSP, mapped {report.homoglyphs_mapped} homoglyphs)")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
