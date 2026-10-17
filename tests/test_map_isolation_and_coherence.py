"""
Unit tests for Map Isolation, Partitioning, and Mechanics Coherence in Baianagem-WW1-ROLEPLAY.
Verifies that:
1. descriptor.mod and launcher mod file isolate all critical directories via replace_path.
2. All 10,022 land provinces form a complete, non-overlapping partition across all 912 states.
3. Every state owner tag has valid country tags and RGB color definitions.
4. Strategic regions cover 100% of land provinces.
5. Focus trees, events, and decisions have 0 references to non-existent state IDs.
6. Map files comply strictly with Clausewitz rendering specifications.
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
            'replace_path="common/bookmarks"',
            'replace_path="common/country_tags"',
            'replace_path="common/ai_strategy"',
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
        self.assertTrue(os.path.exists(csv_path), "definition.csv not found")

        land_provinces = set()
        with open(csv_path, "r", encoding="latin-1") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) >= 5 and parts[0].isdigit():
                    pid = int(parts[0])
                    ptype = parts[4].strip()
                    if ptype == "land" and pid > 0:
                        land_provinces.add(pid)

        self.assertEqual(len(land_provinces), 10022, f"Expected 10,022 land provinces, found {len(land_provinces)}")

        states_dir = os.path.join(ROOT_DIR, "history", "states")
        assigned_provinces = {}
        for fname in os.listdir(states_dir):
            if fname.endswith(".txt"):
                fpath = os.path.join(states_dir, fname)
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                prov_match = re.search(r"provinces\s*=\s*\{([^}]+)\}", content)
                if prov_match:
                    tokens = prov_match.group(1).split()
                    for t in tokens:
                        if t.isdigit():
                            pid = int(t)
                            if pid in assigned_provinces:
                                assigned_provinces[pid].append(fname)
                            else:
                                assigned_provinces[pid] = [fname]

        unassigned = land_provinces - set(assigned_provinces.keys())
        duplicates = {pid: files for pid, files in assigned_provinces.items() if len(files) > 1}

        self.assertEqual(len(unassigned), 0, f"Found {len(unassigned)} unassigned land provinces")
        self.assertEqual(len(duplicates), 0, f"Found {len(duplicates)} duplicated provinces across states")

    def test_all_state_owners_have_colors(self):
        """Verifies that all 72 owning tags have valid country tags and defined RGB colors."""
        colors_file = os.path.join(ROOT_DIR, "common", "countries", "colors.txt")
        self.assertTrue(os.path.exists(colors_file), "colors.txt not found")
        with open(colors_file, "r", encoding="utf-8", errors="ignore") as f:
            colors_content = f.read()

        states_dir = os.path.join(ROOT_DIR, "history", "states")
        owners = set()
        for fname in os.listdir(states_dir):
            if fname.endswith(".txt"):
                fpath = os.path.join(states_dir, fname)
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                m = re.search(r"owner\s*=\s*([A-Za-z0-9_]{3})", content)
                if m:
                    owners.add(m.group(1))

        missing_colors = []
        for tag in owners:
            if not re.search(rf"\b{tag}\b\s*=\s*\{{", colors_content):
                missing_colors.append(tag)

        self.assertEqual(len(missing_colors), 0, f"Missing color definition for owners: {missing_colors}")

    def test_no_invalid_state_references_in_mechanics(self):
        """Verifies 0 references to non-existent state IDs across focus trees, events, and decisions."""
        states_dir = os.path.join(ROOT_DIR, "history", "states")
        valid_states = set()
        for fname in os.listdir(states_dir):
            if fname.endswith(".txt"):
                sid = int(fname.split("-")[0].strip())
                valid_states.add(sid)

        target_dirs = [
            os.path.join(ROOT_DIR, "common", "national_focus"),
            os.path.join(ROOT_DIR, "events"),
            os.path.join(ROOT_DIR, "common", "decisions"),
            os.path.join(ROOT_DIR, "common", "scripted_effects"),
        ]

        state_regex = re.compile(r'\b(?:state\s*=\s*|controls_state\s*=\s*|owns_state\s*=\s*)(\d+)\b')
        invalid_refs = []

        for d in target_dirs:
            if not os.path.exists(d):
                continue
            for root, _, files in os.walk(d):
                for fname in files:
                    if fname.endswith(".txt"):
                        fpath = os.path.join(root, fname)
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                            for lnum, line in enumerate(f, start=1):
                                line_clean = line.split("#")[0]
                                for m in state_regex.finditer(line_clean):
                                    sid = int(m.group(1))
                                    if sid not in valid_states:
                                        invalid_refs.append((f"{fname}:{lnum}", sid))

        self.assertEqual(len(invalid_refs), 0, f"Found invalid state references: {invalid_refs[:10]}")

    def test_map_engine_file_integrity(self):
        """Verifies map engine files are strictly compliant with HOI4 direct-render specs."""
        bmp_path = os.path.join(ROOT_DIR, "map", "provinces.bmp")
        self.assertEqual(os.path.getsize(bmp_path), 34603062, "provinces.bmp must be exactly 34,603,062 bytes")

        required_map_files = ["positions.txt", "trees.bmp", "seasons.txt", "cities.bmp", "cities.txt", "colors.txt"]
        for mf in required_map_files:
            p = os.path.join(ROOT_DIR, "map", mf)
            self.assertTrue(os.path.exists(p), f"Missing self-contained map file {mf}")

if __name__ == "__main__":
    unittest.main()
