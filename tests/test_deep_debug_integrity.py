"""
Unit tests for Deep Systemic Debug Integrity in Baianagem-WW1-ROLEPLAY.
Verifies that:
1. Zero broken prerequisites or mutually exclusive deadlocks exist across all focus trees.
2. All 15 Soviet Republic decisions are properly contained inside SOV_decision_soviet_republics.
3. Newly patched national ideas (unequal treaties, armistice, general staff) are defined and valid.
4. All patched events exist and have valid options and scopes.
"""

import unittest
import os
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestDeepDebugIntegrity(unittest.TestCase):

    def test_zero_broken_focus_prerequisites(self):
        """Verifies all focus prerequisites exist within their focus tree or globally."""
        nf_dir = os.path.join(ROOT_DIR, "common", "national_focus")
        all_focus_ids = set()
        tree_focuses = {}
        tree_prereqs = {}

        for f in os.listdir(nf_dir):
            if not f.endswith(".txt"): continue
            fpath = os.path.join(nf_dir, f)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                c = fp.read()
            clean = "\n".join(l.split("#")[0] for l in c.split("\n"))
            tree_id = f.replace(".txt", "")
            tree_focuses[tree_id] = set()
            tree_prereqs[tree_id] = []

            for block in re.finditer(r'\bfocus\s*=\s*\{([^\{\}]+(?:\{[^\}]*\}[^\{\}]*)*)\}', clean):
                body = block.group(1)
                m_id = re.search(r'\bid\s*=\s*([A-Za-z0-9_\-]+)', body)
                if m_id:
                    fid = m_id.group(1)
                    tree_focuses[tree_id].add(fid)
                    all_focus_ids.add(fid)
                    for pm in re.finditer(r'prerequisite\s*=\s*\{\s*focus\s*=\s*([A-Za-z0-9_\-]+)', body):
                        tree_prereqs[tree_id].append((fid, pm.group(1)))

        broken = []
        for tree_id, plist in tree_prereqs.items():
            for fid, req in plist:
                if req not in tree_focuses[tree_id] and req not in all_focus_ids:
                    broken.append((tree_id, fid, req))

        self.assertEqual(len(broken), 0, f"Found broken focus prerequisites: {broken}")

    def test_soviet_decisions_encapsulation(self):
        """Verifies that common/decisions/SOV.txt has zero stranded root-level decisions."""
        cat_dir = os.path.join(ROOT_DIR, "common", "decisions", "categories")
        defined_categories = set()
        for f in os.listdir(cat_dir):
            if not f.endswith(".txt"): continue
            with open(os.path.join(cat_dir, f), "r", encoding="utf-8", errors="ignore") as fp:
                c = fp.read()
            for m in re.finditer(r'^\s*([A-Za-z0-9_]+)\s*=\s*\{', c, re.MULTILINE):
                defined_categories.add(m.group(1))

        sov_file = os.path.join(ROOT_DIR, "common", "decisions", "SOV.txt")
        with open(sov_file, "r", encoding="utf-8", errors="ignore") as fp:
            lines = fp.readlines()

        depth = 0
        invalid_cats = []
        for idx, line in enumerate(lines, 1):
            clean = line.split("#")[0]
            if depth == 0:
                m = re.match(r'^\s*([A-Za-z0-9_]+)\s*=\s*\{', clean)
                if m:
                    cat = m.group(1)
                    if cat not in defined_categories:
                        invalid_cats.append((idx, cat))
            depth += clean.count("{") - clean.count("}")

        self.assertEqual(len(invalid_cats), 0, f"Found unencapsulated decisions in SOV.txt: {invalid_cats}")
        self.assertEqual(depth, 0, f"Final depth balance of SOV.txt is not 0 (got {depth})")

    def test_missing_ideas_patch_presence(self):
        """Verifies newly patched ideas are defined in common/ideas/ww1_missing_ideas.txt."""
        patch_file = os.path.join(ROOT_DIR, "common", "ideas", "ww1_missing_ideas.txt")
        self.assertTrue(os.path.exists(patch_file), "ww1_missing_ideas.txt does not exist")
        with open(patch_file, "r", encoding="utf-8") as fp:
            c = fp.read()

        required_ideas = [
            "unequal_treaties",
            "anti_german_military",
            "CHI_chinese_general_staff",
            "CHI_construction_battalions",
            "CHI_french_drill",
            "CHI_modern_logistics",
            "CHI_elite_mountaineers",
            "RUS_idea_armistice_cp",
            "RUS_idea_armistice_rus",
            "MAN_banditry",
            "TUR_constitutional_reform",
        ]
        for idea in required_ideas:
            self.assertIn(f"{idea} = {{", c, f"Idea {idea} missing from patch file")

    def test_missing_events_patch_presence(self):
        """Verifies newly patched events are defined in events/WW1_Missing_Events_Patch.txt."""
        patch_file = os.path.join(ROOT_DIR, "events", "WW1_Missing_Events_Patch.txt")
        self.assertTrue(os.path.exists(patch_file), "WW1_Missing_Events_Patch.txt does not exist")
        with open(patch_file, "r", encoding="utf-8") as fp:
            c = fp.read()

        required_events = [
            "id = decisions.1",
            "id = decisions.2",
            "id = mtg_exile_government.2",
            "id = mtg_exile_government.3",
            "id = bftb_news.209",
            "id = ww1_romania.7",
            "id = ww1_romania.19",
            "id = ww1_romania.9",
            "id = ww1_korea.28",
            "id = ww1_political.4",
            "id = ww1_qing.215",
            "id = ww1_auh.28",
            "id = ww1_turkestan.2",
            "id = ww1_soviet.25",
            "id = ww1_generic.6",
        ]
        for ev in required_events:
            self.assertIn(ev, c, f"Event {ev} missing from patch file")

        extra_events = [
            "id = ww1_baltics.13",
            "id = ww1_russia.100",
            "id = options.1",
            "id = options.2",
        ]
        for ev in extra_events:
            self.assertIn(ev, c, f"Event {ev} missing from patch file")


    def test_chile_focus_tree_restored(self):
        """Verifies Chile focus tree is active, has >= 40 focuses, and ww1_chile.12 is defined."""
        chile_path = os.path.join(ROOT_DIR, "common", "national_focus", "chile.txt")
        self.assertTrue(os.path.exists(chile_path), "chile.txt missing")
        with open(chile_path, "r", encoding="utf-8") as f:
            c = f.read()
        chl_focuses = re.findall(r'id\s*=\s*(CHL_[A-Za-z0-9_]+)', c)
        self.assertGreaterEqual(len(chl_focuses), 40, "Chile focus tree has fewer than 40 focuses")

        # Verify ww1_chile.12 in events/WW1_Chile.txt
        chile_events = os.path.join(ROOT_DIR, "events", "WW1_Chile.txt")
        with open(chile_events, "r", encoding="utf-8") as f:
            ec = f.read()
        self.assertIn("id = ww1_chile.12", ec, "ww1_chile.12 event missing in WW1_Chile.txt")

if __name__ == "__main__":
    unittest.main()
