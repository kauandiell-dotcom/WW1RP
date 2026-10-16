"""
Unit tests for HOI4 Map, States, Supply Nodes, and Railway Infrastructure.
Validates:
1. All 13,278 provinces in map/definition.csv conform to Clausewitz bounds.
2. All 912 states have valid, non-overlapping province definitions.
3. All supply hubs in map/supply_nodes.txt are stationed on valid land provinces.
4. All railway segments in map/railways.txt traverse valid land provinces.
"""
import os
import unittest
import csv
import re

MOD_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class TestMapAndStates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.def_file = os.path.join(MOD_ROOT, "map", "definition.csv")
        cls.states_dir = os.path.join(MOD_ROOT, "history", "states")
        cls.supply_file = os.path.join(MOD_ROOT, "map", "supply_nodes.txt")
        cls.railway_file = os.path.join(MOD_ROOT, "map", "railways.txt")

        # Load provinces
        cls.provinces = {}
        if os.path.exists(cls.def_file):
            with open(cls.def_file, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f, delimiter=';')
                for row in reader:
                    if not row or not row[0].strip().isdigit():
                        continue
                    pid = int(row[0].strip())
                    ptype = row[4].strip() if len(row) > 4 else "land"
                    cls.provinces[pid] = ptype

    def test_definition_csv_bounds(self):
        """Verifies definition.csv max province ID is <= 13278."""
        self.assertTrue(len(self.provinces) > 0, "map/definition.csv empty or missing")
        max_pid = max(self.provinces.keys())
        self.assertLessEqual(max_pid, 13278, f"Max province ID {max_pid} exceeds 13278")

    def test_all_states_provinces_valid_and_unique(self):
        """Verifies that all provinces assigned across states are valid and non-overlapping."""
        self.assertTrue(os.path.exists(self.states_dir), "history/states/ missing")
        assigned = {}
        duplicates = []
        out_of_bounds = []

        for root, _, files in os.walk(self.states_dir):
            for file in files:
                if file.endswith(".txt"):
                    fp = os.path.join(root, file)
                    with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                        c = f.read()
                    sid_match = re.search(r'id\s*=\s*([0-9]+)', c)
                    if not sid_match:
                        continue
                    sid = int(sid_match.group(1))
                    provs_match = re.search(r'provinces\s*=\s*\{([^}]+)\}', c)
                    if provs_match:
                        for tok in provs_match.group(1).split():
                            if tok.isdigit():
                                pid = int(tok)
                                if pid not in self.provinces:
                                    out_of_bounds.append((file, sid, pid))
                                elif pid in assigned:
                                    duplicates.append((pid, assigned[pid], sid))
                                else:
                                    assigned[pid] = sid

        self.assertEqual(out_of_bounds, [], f"Found out of bounds provinces: {out_of_bounds}")
        self.assertEqual(duplicates, [], f"Found overlapping provinces: {duplicates[:10]}")

    def test_supply_nodes_on_land(self):
        """Verifies all supply nodes are on valid land provinces."""
        if not os.path.exists(self.supply_file):
            self.skipTest("map/supply_nodes.txt not present")

        invalid = []
        with open(self.supply_file, "r", encoding="utf-8", errors="ignore") as f:
            for idx, line in enumerate(f, 1):
                clean = re.sub(r"#.*", "", line).strip()
                if not clean:
                    continue
                tokens = clean.split()
                if len(tokens) >= 2 and tokens[1].isdigit():
                    pid = int(tokens[1])
                    if pid not in self.provinces or self.provinces[pid] != "land":
                        invalid.append((idx, pid, self.provinces.get(pid, "UNKNOWN")))

        self.assertEqual(invalid, [], f"Invalid supply nodes found: {invalid}")

    def test_railways_on_land(self):
        """Verifies all railway path nodes are on valid land provinces."""
        if not os.path.exists(self.railway_file):
            self.skipTest("map/railways.txt not present")

        invalid = []
        with open(self.railway_file, "r", encoding="utf-8", errors="ignore") as f:
            for idx, line in enumerate(f, 1):
                clean = re.sub(r"#.*", "", line).strip()
                if not clean:
                    continue
                tokens = clean.split()
                if len(tokens) >= 3 and tokens[0].isdigit() and tokens[1].isdigit():
                    for tok in tokens[2:]:
                        if tok.isdigit():
                            pid = int(tok)
                            if pid not in self.provinces or self.provinces[pid] != "land":
                                invalid.append((idx, pid, self.provinces.get(pid, "UNKNOWN")))

        self.assertEqual(invalid, [], f"Invalid railway nodes found: {invalid}")


if __name__ == "__main__":
    unittest.main()
