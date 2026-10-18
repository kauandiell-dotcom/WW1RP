"""
Baseline QA and Engine Integrity Tests for Baianagem-WW1-ROLEPLAY.
Validates Clausewitz bracket balance, UTF-8 BOM encoding, map files, and descriptors.
"""

import os
import re
import unittest

MOD_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestRoleplayBaseline(unittest.TestCase):
    def test_descriptor_mod(self):
        desc = os.path.join(MOD_ROOT, "descriptor.mod")
        self.assertTrue(os.path.exists(desc), "descriptor.mod must exist in root")
        with open(desc, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("name=", content)
        self.assertIn("supported_version=", content)

    def test_default_map_integrity(self):
        dmap = os.path.join(MOD_ROOT, "map", "default.map")
        self.assertTrue(os.path.exists(dmap), "map/default.map must exist")
        with open(dmap, "r", encoding="utf-8") as f:
            content = f.read()
        required_fields = ["definitions", "provinces", "adjacencies", "continent"]
        for field in required_fields:
            self.assertIn(f"{field} =", content, f"Field '{field}' must be declared in default.map")

    def test_syntax_and_braces_across_all_scripts(self):
        scan_dirs = ["common", "events", "history", "interface"]
        bad_files = []
        for sd in scan_dirs:
            dp = os.path.join(MOD_ROOT, sd)
            if not os.path.exists(dp):
                continue
            for root, _, files in os.walk(dp):
                for f in files:
                    if f.endswith((".txt", ".gui", ".gfx")):
                        fp = os.path.join(root, f)
                        try:
                            with open(fp, "r", encoding="utf-8", errors="ignore") as file_obj:
                                depth = 0
                                for line_num, line in enumerate(file_obj, 1):
                                    clean = re.sub(r"#.*", "", line)
                                    for ch in clean:
                                        if ch == "{":
                                            depth += 1
                                        elif ch == "}":
                                            depth -= 1
                                            if depth < 0:
                                                bad_files.append(f"{os.path.relpath(fp, MOD_ROOT)}: extra '}}' at line {line_num}")
                                                break
                                    if depth < 0:
                                        break
                                if depth > 0:
                                    bad_files.append(f"{os.path.relpath(fp, MOD_ROOT)}: unclosed {depth} brace(s)")
                        except Exception as e:
                            bad_files.append(f"{os.path.relpath(fp, MOD_ROOT)}: error {e}")
        self.assertEqual(len(bad_files), 0, f"Found bracket syntax errors in {len(bad_files)} files: {bad_files[:10]}")

    def test_bilingual_yaml_bom_encoding(self):
        loc_dir = os.path.join(MOD_ROOT, "localisation")
        missing_bom = []
        lua_comments = []
        if os.path.exists(loc_dir):
            for root, _, files in os.walk(loc_dir):
                for f in files:
                    if f.endswith(".yml"):
                        fp = os.path.join(root, f)
                        with open(fp, "rb") as bf:
                            header = bf.read(3)
                            if header != b"\xef\xbb\xbf":
                                missing_bom.append(os.path.relpath(fp, MOD_ROOT))
                        with open(fp, "r", encoding="utf-8", errors="ignore") as tf:
                            for idx, line in enumerate(tf, 1):
                                if "--" in line and not line.strip().startswith("#"):
                                    # check if lua comment outside quotes
                                    clean = re.sub(r'\"[^\"]*\"', '', line)
                                    if "--" in clean:
                                        lua_comments.append(f"{os.path.relpath(fp, MOD_ROOT)}:{idx}")
        self.assertEqual(len(lua_comments), 0, f"Forbidden Lua comments found: {lua_comments[:5]}")
        self.assertEqual(len(missing_bom), 0, f"Missing UTF-8 BOM in localisation files: {missing_bom[:5]}")

    def test_no_bom_in_gui_and_gfx(self):
        """Ensures .gui and .gfx files NEVER have UTF-8 BOM, which causes Unexpected token ?guiTypes crashes."""
        illegal_bom = []
        interface_dir = os.path.join(MOD_ROOT, "interface")
        if os.path.exists(interface_dir):
            for root, _, files in os.walk(interface_dir):
                for f in files:
                    if f.endswith((".gui", ".gfx")):
                        fp = os.path.join(root, f)
                        with open(fp, "rb") as bf:
                            if bf.read(3) == b"\xef\xbb\xbf":
                                illegal_bom.append(os.path.relpath(fp, MOD_ROOT))
        self.assertEqual(len(illegal_bom), 0, f"Illegal UTF-8 BOM found in GUI/GFX files: {illegal_bom}")

if __name__ == "__main__":
    unittest.main()
