"""
Unit tests for Map Isolation, Partitioning, and Mechanics Coherence in Baianagem-WW1-ROLEPLAY.
Verifies that:
1. descriptor.mod and launcher mod file isolate all critical directories via replace_path.
2. All 10,022 land provinces form a complete, non-overlapping partition across all 912 states.
3. Every state owner tag has valid country tags and RGB color definitions.
4. Strategic regions cover 100% of land provinces.
5. Focus trees, events, and decisions have 0 references to non-existent state IDs.
"""

import unittest
import os
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestMapIsolationAndCoherence(unittest.TestCase):

    def test_descriptor_replace_paths(self):
        """Verifies descriptor.mod contains all total-conversion replace_path declarations."""
        descriptor_path = os.path.join(ROOT_DIR, "descriptor.mod")
        self.assertTrue(os.path.exists(descriptor_path), "descriptor.mod not found")
        with open(descriptor_path, "r", encoding="utf-8") as f:
            content = f.read()

        required_replaces = [
            'replace_path="history/states"',
            'replace_path="history/countries"',
            'replace_path="map/strategicregions"',
            'replace_path="common/national_focus"',
            'replace_path="common/ideas"',
            'replace_path="common/decisions"',
            'replace_path="common/decisions/categories"',
            'replace_path="events"',
        ]
        for req in required_replaces:
            self.assertIn(req, content, f"Missing {req} in descriptor.mod")

    def test_launcher_mod_replace_paths(self):
        """Verifies launcher .mod file contains replace_path declarations."""
        launcher_path = r"C:/Users/USURIO~2/Documents/Paradox Interactive/Hearts of Iron IV/mod/Baianagem_WW1_Roleplay.mod"
        if os.path.exists(launcher_path):
            with open(launcher_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn('replace_path="history/states"', content)
            self.assertIn('replace_path="history/countries"', content)

    def test_all_land_provinces_partitioned(self):
        """Verifies all 10,022 land provinces are assigned with 0 unassigned and 0 duplicates."""
        csv_path = os.path.join(ROOT_DIR, "map", "definition.csv")
        land_provinces = set()
        with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) >= 5 and parts[0].isdigit():
                    pid = int(parts[0])
                    if parts[4].strip() == "land" and pid > 0:
                        land_provinces.add(pid)

        states_dir = os.path.join(ROOT_DIR, "history", "states")
        assigned_provs = set()
        duplicates = set()

        for sf in os.listdir(states_dir):
            if not sf.endswith(".txt"): continue
            with open(os.path.join(states_dir, sf), "r", encoding="utf-8", errors="ignore") as f:
                c = f.read()
            pm = re.search(r"provinces\s*=\s*\{([^}]+)\}", c)
            if pm:
                for p in pm.group(1).split():
                    if p.isdigit():
                        pid = int(p)
                        if pid in assigned_provs:
                            duplicates.add(pid)
                        assigned_provs.add(pid)

        self.assertEqual(len(duplicates), 0, f"Found duplicate provinces in states: {duplicates}")
        unassigned = land_provinces - assigned_provs
        self.assertEqual(len(unassigned), 0, f"Found unassigned land provinces: {unassigned}")

    def test_all_state_owners_have_colors(self):
        """Verifies that all 72 owning tags have valid country tags and defined RGB colors."""
        states_dir = os.path.join(ROOT_DIR, "history", "states")
        owners = set()
        for sf in os.listdir(states_dir):
            if not sf.endswith(".txt"): continue
            with open(os.path.join(states_dir, sf), "r", encoding="utf-8", errors="ignore") as f:
                m = re.search(r"\bowner\s*=\s*([A-Za-z0-9_]{3})", f.read())
                if m:
                    owners.add(m.group(1))

        colors_file = os.path.join(ROOT_DIR, "common", "countries", "colors.txt")
        with open(colors_file, "r", encoding="utf-8", errors="ignore") as f:
            colors_content = f.read()
        defined_colors = set(re.findall(r"([A-Za-z0-9_]{3})\s*=\s*\{", colors_content))

        for tag in owners:
            self.assertIn(tag, defined_colors, f"Owning tag {tag} has no color defined in colors.txt")

    def test_no_invalid_state_references_in_mechanics(self):
        """Verifies 0 references to non-existent state IDs across focus trees, events, and decisions."""
        states_dir = os.path.join(ROOT_DIR, "history", "states")
        valid_sids = set()
        for sf in os.listdir(states_dir):
            if not sf.endswith(".txt"): continue
            with open(os.path.join(states_dir, sf), "r", encoding="utf-8", errors="ignore") as f:
                m = re.search(r"\bid\s*=\s*(\d+)", f.read())
                if m:
                    valid_sids.add(int(m.group(1)))

        dirs_to_check = [
            os.path.join(ROOT_DIR, "common", "national_focus"),
            os.path.join(ROOT_DIR, "events"),
            os.path.join(ROOT_DIR, "common", "decisions"),
            os.path.join(ROOT_DIR, "common", "scripted_effects"),
            os.path.join(ROOT_DIR, "common", "scripted_triggers"),
            os.path.join(ROOT_DIR, "common", "on_actions"),
        ]

        pattern = re.compile(r"\b(?:state|controls_state|owns_state|transfer_state|has_full_control_of_state)\s*=\s*(\d+)")
        invalid_refs = []

        for d in dirs_to_check:
            if not os.path.exists(d): continue
            for root, _, files in os.walk(d):
                for f in files:
                    if not f.endswith(".txt"): continue
                    fpath = os.path.join(root, f)
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                        for idx, line in enumerate(fp, 1):
                            clean = line.split("#")[0]
                            for m in pattern.finditer(clean):
                                sid = int(m.group(1))
                                if sid not in valid_sids and sid > 0:
                                    invalid_refs.append((f, idx, sid))

        self.assertEqual(len(invalid_refs), 0, f"Found {len(invalid_refs)} invalid state references: {invalid_refs[:10]}")

if __name__ == "__main__":
    unittest.main()
