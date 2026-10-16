"""
HOI4 Clausewitz Semantic Oracle.
Provides definitive validation for country modifier tokens against
the official Hearts of Iron IV 1.19.3 engine definitions and dynamic synthesis rules.
"""
import os
import json
import re
from typing import Set, List, Dict, Tuple, Optional

MOD_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CACHE_FILE = os.path.join(MOD_ROOT, "data", "hoi4_valid_country_modifiers.json")

_VALID_MODIFIERS: Optional[Set[str]] = None


def get_valid_modifiers() -> Set[str]:
    """Returns the set of all valid Clausewitz HOI4 country modifier tokens."""
    global _VALID_MODIFIERS
    if _VALID_MODIFIERS is not None:
        return _VALID_MODIFIERS

    valid = set()
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            valid.update(json.load(f))

    # 1. Dynamically load custom modifier definitions from mod
    mod_defs_dir = os.path.join(MOD_ROOT, "common", "modifier_definitions")
    if os.path.exists(mod_defs_dir):
        for fname in os.listdir(mod_defs_dir):
            if fname.endswith(".txt"):
                def_path = os.path.join(mod_defs_dir, fname)
                with open(def_path, "r", encoding="utf-8", errors="ignore") as f:
                    for m in re.finditer(r'^\s*([a-zA-Z0-9_]+)\s*=\s*\{', f.read(), re.M):
                        valid.add(m.group(1))

    # 2. Dynamically load building modifiers from mod
    bld_dir = os.path.join(MOD_ROOT, "common", "buildings")
    if os.path.exists(bld_dir):
        for fname in os.listdir(bld_dir):
            if fname.endswith(".txt"):
                bld_path = os.path.join(bld_dir, fname)
                with open(bld_path, "r", encoding="utf-8", errors="ignore") as f:
                    for m in re.finditer(r'^\s*([a-zA-Z0-9_]+)\s*=\s*\{', f.read(), re.M):
                        bname = m.group(1)
                        if bname != "buildings":
                            valid.add(f"production_speed_{bname}_factor")
                            valid.add(f"max_levels_{bname}")
                            valid.add(f"repair_speed_{bname}_factor")

    # 3. Dynamically load AI focuses from mod
    ai_dir = os.path.join(MOD_ROOT, "common", "ai_focuses")
    if os.path.exists(ai_dir):
        for fname in os.listdir(ai_dir):
            if fname.endswith(".txt"):
                ai_path = os.path.join(ai_dir, fname)
                with open(ai_path, "r", encoding="utf-8", errors="ignore") as f:
                    for m in re.finditer(r'^\s*([a-zA-Z0-9_]+)\s*=\s*\{', f.read(), re.M):
                        valid.add(f"{m.group(1)}_factor")

    # 4. Known Clausewitz engine modifiers valid in ideas/spirits/doctrines
    known_engine_modifiers = {
        "land_night_attack", "special_forces_no_supply_grace", "sub_retreat_speed",
        "naval_mines_effect_reduction", "air_interception_detect_factor",
        "equipment_upgrade_xp_cost", "commando_trait_chance_factor",
        "terrain_penalty_reduction", "unit_upkeep_attrition_factor",
        "local_factory_sabotage", "industrial_factory_donations", "dockyard_donations",
        "army_org_regain_factor",
    }
    valid.update(known_engine_modifiers)

    _VALID_MODIFIERS = valid
    return _VALID_MODIFIERS


def is_valid_country_modifier(token: str) -> bool:
    """Checks whether a modifier key is recognized by the Clausewitz engine."""
    valid_set = get_valid_modifiers()
    if token in valid_set:
        return True

    # Regex patterns for dynamically generated Clausewitz tokens
    if re.match(r"^modifier_army_sub_unit_[a-zA-Z0-9_]+$", token):
        return True
    if re.match(r"^trait_[a-zA-Z0-9_]+_xp_gain_factor$", token):
        return True
    if re.match(r"^tactic_[a-zA-Z0-9_]+_preferred_weight_factor$", token):
        return True
    if re.match(r"^(army|navy|air)_leader_start_[a-zA-Z0-9_]+_level$", token):
        return True
    if re.match(r"^ai_focus_[a-zA-Z0-9_]+_factor$", token):
        return True
    if re.match(r"^operation_[a-zA-Z0-9_]+$", token):
        return True
    if re.match(r"^defense_impact_on_[a-zA-Z0-9_]+$", token):
        return True

    return False


def audit_modifier_dict(mod_dict: Dict[str, any]) -> List[str]:
    """Returns a list of keys in the dict that are NOT recognized country modifiers."""
    invalid = []
    for k in mod_dict.keys():
        if not is_valid_country_modifier(k):
            invalid.append(k)
    return invalid


def audit_file_modifiers(filepath: str) -> List[Tuple[int, str, str]]:
    """
    Parses a Clausewitz file and extracts all modifier = { ... } blocks,
    returning a list of (line_num, token_name, idea_or_context_id) that are invalid.
    Correctly distinguishes country modifier blocks from ai_will_do/ai_chance trigger modifiers.
    """
    if not os.path.exists(filepath):
        return []

    errors = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    stack = []
    for line_idx, raw_line in enumerate(lines, start=1):
        clean = raw_line.split("#")[0].strip()
        if not clean:
            continue

        for m in re.finditer(r'([a-zA-Z0-9_]+)\s*=\s*\{|\{|\}|([a-zA-Z0-9_]+)\s*=\s*([^\{\}]+)', clean):
            full = m.group(0)
            if full.endswith("{"):
                key = m.group(1) or "block"
                stack.append(key)
            elif full == "}":
                if stack:
                    stack.pop()
            else:
                key = m.group(2)
                if stack and stack[-1] == "modifier":
                    parents = [s for s in stack]
                    if any(p in ("ai_will_do", "ai_chance", "ai_weights", "mtth", "mean_time_to_happen") for p in parents):
                        continue
                    if key in ("custom_effect_tooltip", "modifier"):
                        continue
                    if not is_valid_country_modifier(key):
                        parent = stack[-2] if len(stack) >= 2 else ""
                        errors.append((line_idx, key, parent))

    return errors


if __name__ == "__main__":
    mods = get_valid_modifiers()
    print(f"Clausewitz Semantic Oracle initialized with {len(mods)} valid modifiers.")
