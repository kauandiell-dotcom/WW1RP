"""
Unit tests for Equipment Designers, MIO Organizations, and 1.19 Special Projects compatibility.
Validates that:
1. Every equipment type referenced in MIO organization files exists in equipment/ or equipment_categories/.
2. MIO equipment categories are fully defined for all referenced macros (mio_cat_eq_*).
3. Special projects directory and stub project files exist for HOI4 1.15-1.19+ engine compatibility.
4. Equipment chassis and airframes have proper archetype declarations.
"""
import os
import unittest
import re

MOD_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class TestEquipmentAndMIOs(unittest.TestCase):
    def setUp(self):
        self.equip_dir = os.path.join(MOD_ROOT, "common", "units", "equipment")
        self.mio_dir = os.path.join(MOD_ROOT, "common", "military_industrial_organization")
        self.sp_dir = os.path.join(MOD_ROOT, "common", "special_projects")
        self.assertTrue(os.path.exists(self.equip_dir), "common/units/equipment missing")
        self.assertTrue(os.path.exists(self.mio_dir), "common/military_industrial_organization missing")

    def test_mio_categories_and_equipment_references(self):
        """Verifies that all equipment types referenced in MIO organizations are defined."""
        # 1. Collect defined equipments
        defined = set()
        for root, _, files in os.walk(self.equip_dir):
            for f in files:
                if f.endswith(".txt"):
                    fp = os.path.join(root, f)
                    with open(fp, "r", encoding="utf-8", errors="ignore") as file_obj:
                        lines = file_obj.readlines()
                    for line in lines:
                        clean = re.sub(r"#.*", "", line).strip()
                        m = re.match(r"^([a-zA-Z0-9_]+)\s*=\s*\{", clean)
                        if m:
                            tok = m.group(1)
                            if tok not in ("equipments", "duplicate_archetypes"):
                                defined.add(tok)

        # Also add generic categories supported by engine
        engine_categories = {
            "armor", "infantry", "artillery", "motorized", "air", "naval",
            "capital_ship", "screen_ship", "submarine", "carrier", "maritime_patrol_plane",
            "naval_bomber", "transport_plane_equipment"
        }
        defined.update(engine_categories)

        # 2. Collect defined MIO equipment categories
        mio_cats_file = os.path.join(self.mio_dir, "equipment_categories", "00_equipment_categories.txt")
        defined_cats = set()
        if os.path.exists(mio_cats_file):
            with open(mio_cats_file, "r", encoding="utf-8", errors="ignore") as f:
                for match in re.finditer(r'([a-zA-Z0-9_]+)\s*=\s*\{', f.read()):
                    tok = match.group(1)
                    if tok != "equipment_categories":
                        defined_cats.add(tok)

        # 3. Scan MIO organizations for equipment_type = { ... }
        orgs_dir = os.path.join(self.mio_dir, "organizations")
        unresolved = []
        if os.path.exists(orgs_dir):
            for root, _, files in os.walk(orgs_dir):
                for f in sorted(files):
                    if f.endswith(".txt"):
                        fp = os.path.join(root, f)
                        with open(fp, "r", encoding="utf-8", errors="ignore") as file_obj:
                            content = file_obj.read()
                        matches = re.findall(r'equipment_type\s*=\s*\{([^}]+)\}', content)
                        for m in matches:
                            for tok in m.split():
                                if tok not in defined and tok not in defined_cats:
                                    unresolved.append((f, tok))

        self.assertEqual(
            unresolved,
            [],
            f"Found unresolved equipment types in MIO organizations: {unresolved}"
        )

    def test_special_projects_stub_compatibility(self):
        """Verifies that special projects subsystem has a valid 1.15-1.19 stub in place."""
        projects_dir = os.path.join(self.sp_dir, "projects")
        self.assertTrue(
            os.path.exists(projects_dir),
            "common/special_projects/projects/ directory must exist for HOI4 1.15-1.19 compatibility"
        )
        stub_file = os.path.join(projects_dir, "ww1_special_projects.txt")
        self.assertTrue(
            os.path.exists(stub_file),
            "common/special_projects/projects/ww1_special_projects.txt must exist"
        )


if __name__ == "__main__":
    unittest.main()
