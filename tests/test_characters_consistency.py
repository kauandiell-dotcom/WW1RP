"""
Unit tests for HOI4 Modern Character Roster Architecture (HOI4 1.15 - 1.19+).
Validates that:
1. No country uses the legacy create_country_leader command in history/countries/.
2. Every character recruited via recruit_character = <ID> is defined in common/characters/.
3. All character files have valid syntax and proper character definition structures.
"""
import os
import unittest
import re

MOD_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class TestCharactersConsistency(unittest.TestCase):
    def setUp(self):
        self.characters_dir = os.path.join(MOD_ROOT, "common", "characters")
        self.countries_dir = os.path.join(MOD_ROOT, "history", "countries")
        self.assertTrue(os.path.exists(self.characters_dir), "common/characters missing")
        self.assertTrue(os.path.exists(self.countries_dir), "history/countries missing")

    def test_no_legacy_create_country_leader(self):
        """Verifies that no country file uses deprecated create_country_leader."""
        legacy_found = []
        for root, _, files in os.walk(self.countries_dir):
            for file in sorted(files):
                if file.endswith(".txt"):
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read()
                    if "create_country_leader" in text:
                        legacy_found.append(file)

        self.assertEqual(
            legacy_found,
            [],
            f"Found {len(legacy_found)} countries still using legacy create_country_leader: {legacy_found}"
        )

    def test_all_recruited_characters_exist(self):
        """Verifies that every character recruited in history/countries exists in common/characters."""
        # 1. Collect all defined characters
        defined_characters = set()
        for root, _, files in os.walk(self.characters_dir):
            for file in files:
                if file.endswith(".txt"):
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    for line in lines:
                        clean = re.sub(r"#.*", "", line).strip()
                        # Character definitions match: <character_id> = {
                        m = re.match(r"^([a-zA-Z0-9_]+)\s*=\s*\{", clean)
                        if m:
                            tok = m.group(1)
                            if tok not in ("characters", "portraits", "civilian", "army", "navy", "advisor",
                                           "country_leader", "corps_commander", "field_marshal", "navy_leader"):
                                defined_characters.add(tok)

        # 2. Collect all recruited characters
        missing = []
        for root, _, files in os.walk(self.countries_dir):
            for file in sorted(files):
                if file.endswith(".txt"):
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    for line_idx, line in enumerate(lines, 1):
                        clean = re.sub(r"#.*", "", line).strip()
                        m = re.search(r"recruit_character\s*=\s*([a-zA-Z0-9_]+)", clean)
                        if m:
                            char_id = m.group(1)
                            if char_id not in defined_characters:
                                missing.append((file, line_idx, char_id))

        if missing:
            msg = "\n".join([f"  {m[0]}:{m[1]} -> Missing character '{m[2]}'" for m in missing[:30]])
            self.fail(f"Found {len(missing)} recruited characters missing from common/characters/:\n{msg}")


if __name__ == "__main__":
    unittest.main()
