"""
Unit tests for HOI4 Clausewitz Semantic Integrity.
Ensures no triggers (such as is_puppet, has_tech, ROOT) exist inside country modifier blocks,
and that deprecated HOI3/early HOI4 modifiers (such as offence, defence, crypto_strength,
army_morale, MONTHLY_POPULATION) are eliminated in favor of modern 1.19+ equivalents.
"""
import os
import unittest
import re

MOD_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

FORBIDDEN_TRIGGERS_IN_COUNTRY_MODIFIERS = {
    "is_puppet", "has_tech", "has_global_flag", "has_country_flag",
    "has_offensive_war", "has_defensive_war", "check_variable",
    "any_country", "ROOT", "OVERLORD", "FROM", "PREV"
}

DEPRECATED_MODIFIERS = {
    "army_morale": "army_org_regain_factor",
    "MONTHLY_POPULATION": "monthly_population",
    "offence": "army_attack_factor",
    "defence": "army_defence_factor",
    "crypto_strength": "encryption",
    "recruitable_population": "conscription or recruitable_population_factor",
}


def audit_file_modifiers(filepath: str, relpath: str):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    lines = content.splitlines()
    cleaned_lines = [re.sub(r"#.*", "", l) for l in lines]

    tokens = []
    token_pattern = re.compile(r'([a-zA-Z0-9_@\.\:\-]+)|([={}\[\]])')
    for line_idx, line in enumerate(cleaned_lines, 1):
        for match in token_pattern.finditer(line):
            tokens.append((match.group(0), line_idx))

    stack = []
    i = 0
    n = len(tokens)
    violations = []

    while i < n:
        tok, line_num = tokens[i]
        if tok == "{":
            stack.append(("block", line_num))
            i += 1
        elif tok == "}":
            if stack:
                stack.pop()
            i += 1
        elif i + 1 < n and tokens[i+1][0] == "=":
            key = tok
            if i + 2 < n and tokens[i+2][0] == "{":
                stack.append((key, line_num))
                i += 3
            else:
                if stack:
                    current_block = stack[-1][0]
                    if current_block == "modifier":
                        parents = [s[0] for s in stack]
                        is_ai = any(p in ("ai_will_do", "ai_weights", "ai_chance", "mtth", "mean_time_to_happen") for p in parents)
                        if not is_ai:
                            if key in FORBIDDEN_TRIGGERS_IN_COUNTRY_MODIFIERS:
                                violations.append((relpath, line_num, f"Trigger in country modifier: '{key}'"))
                            if key in DEPRECATED_MODIFIERS:
                                violations.append((relpath, line_num, f"Deprecated modifier: '{key}' (use '{DEPRECATED_MODIFIERS[key]}')"))
                i += 2
                if i < n and tokens[i][0] not in ("{", "}", "="):
                    i += 1
        else:
            i += 1

    return violations


class TestSemanticIntegrity(unittest.TestCase):
    def test_no_triggers_or_deprecated_tokens_in_ideas(self):
        ideas_dir = os.path.join(MOD_ROOT, "common", "ideas")
        self.assertTrue(os.path.exists(ideas_dir))
        violations = []

        for root, dirs, files in os.walk(ideas_dir):
            for file in sorted(files):
                if file.endswith(".txt"):
                    fp = os.path.join(root, file)
                    rel = os.path.relpath(fp, MOD_ROOT)
                    v = audit_file_modifiers(fp, rel)
                    violations.extend(v)

        if violations:
            msg = "\n".join([f"  {v[0]}:{v[1]} -> {v[2]}" for v in violations[:30]])
            self.fail(f"Found {len(violations)} semantic modifier violations in common/ideas/:\n{msg}")


if __name__ == "__main__":
    unittest.main()
