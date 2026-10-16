"""
Unit tests for Performance and Decision Fast-Failing (Padrão Roleplay Fluído).
Verifies that:
1. Every country-specific decision category has an allowed = { ... } block restricting it
   to its valid nation(s) (original_tag = TAG or tag = TAG).
2. No country-specific decision category has an empty allowed = { } block or missing allowed block,
   preventing daily tick lag caused by 200+ AI nations evaluating foreign decisions.
"""
import os
import unittest
import re

MOD_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Recognized valid cross-tag mappings for revolutionary / emergent tags
SPECIAL_TAG_ALLOWANCES = {
    "SOV": {"RUS", "SOV"},
    "TUR": {"TUR", "TRR", "OTT"},
    "CHI": {"CHI", "QIN", "SHX", "GXC", "YUN", "XSM", "SIK"},
    "SPR": {"SPR", "SPB"},
}


def parse_top_level_categories(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    categories = []
    depth = 0
    current_name = None
    current_lines = []
    start_line = 0

    for idx, line in enumerate(lines, 1):
        clean = re.sub(r"#.*", "", line)
        if not clean.strip():
            continue

        if depth == 0:
            m = re.match(r'^\s*([a-zA-Z0-9_]+)\s*=\s*\{', clean)
            if m:
                current_name = m.group(1)
                start_line = idx
                current_lines = [line]
                depth += clean.count("{") - clean.count("}")
                continue
        else:
            current_lines.append(line)
            depth += clean.count("{") - clean.count("}")
            if depth == 0:
                categories.append((current_name, start_line, idx, "".join(current_lines)))
                current_name = None
                current_lines = []

    return categories


class TestPerformanceAndFastFailing(unittest.TestCase):
    def setUp(self):
        self.cats_dir = os.path.join(MOD_ROOT, "common", "decisions", "categories")
        self.assertTrue(os.path.exists(self.cats_dir), "common/decisions/categories missing")

    def test_country_decision_categories_have_fast_failing_allowed(self):
        """Verifies all country-specific decision categories restrict evaluation to valid tag(s)."""
        country_files = []
        for f in sorted(os.listdir(self.cats_dir)):
            m = re.match(r"^([A-Z]{3})_decision_categories\.txt$", f)
            if m:
                tag = m.group(1)
                # Skip generic bundles like TGW or AGW
                if tag not in ("TGW", "AGW"):
                    country_files.append((tag, f))

        violations = []
        for tag, fname in country_files:
            fp = os.path.join(self.cats_dir, fname)
            cats = parse_top_level_categories(fp)
            valid_tags = SPECIAL_TAG_ALLOWANCES.get(tag, {tag})

            for cname, start_line, end_line, text in cats:
                allowed_match = re.search(r'\ballowed\s*=\s*\{([^}]*)\}', text)
                if not allowed_match:
                    violations.append((fname, start_line, cname, "Missing allowed = { } block"))
                    continue

                allowed_body = allowed_match.group(1).strip()
                if not allowed_body:
                    violations.append((fname, start_line, cname, "Empty allowed = { } block"))
                    continue

                # Check if at least one valid tag is checked
                has_tag_check = any(
                    re.search(rf'\b(original_tag|tag)\s*=\s*{t}\b', allowed_body)
                    for t in valid_tags
                )
                if not has_tag_check:
                    violations.append((fname, start_line, cname, f"Allowed block does not check tag {tag}: '{allowed_body}'"))

        if violations:
            msg = "\n".join([f"  {v[0]}:{v[1]} [{v[2]}] -> {v[3]}" for v in violations[:30]])
            self.fail(f"Found {len(violations)} decision categories missing fast-failing tag checks:\n{msg}")


if __name__ == "__main__":
    unittest.main()
