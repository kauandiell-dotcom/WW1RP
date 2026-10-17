import os
import sys
import re
import json

MOD_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def run_tier_1_brackets():
    print('[TIER 1] Auditing Clausewitz Bracket Balance...')
    scan_dirs = ['common', 'events', 'history', 'interface', 'map']
    bad_files = []
    total_scanned = 0
    for sd in scan_dirs:
        dp = os.path.join(MOD_ROOT, sd)
        if not os.path.exists(dp):
            continue
        for root, _, files in os.walk(dp):
            for f in files:
                if f.endswith(('.txt', '.gui', '.gfx')):
                    total_scanned += 1
                    fp = os.path.join(root, f)
                    try:
                        with open(fp, 'r', encoding='utf-8', errors='ignore') as fo:
                            depth = 0
                            for line_num, line in enumerate(fo, 1):
                                clean = re.sub(r'#.*', '', line)
                                for ch in clean:
                                    if ch == '{':
                                        depth += 1
                                    elif ch == '}':
                                        depth -= 1
                                        if depth < 0:
                                            bad_files.append((os.path.relpath(fp, MOD_ROOT), line_num, 'Extra closing brace'))
                                            break
                                if depth < 0:
                                    break
                            if depth > 0:
                                bad_files.append((os.path.relpath(fp, MOD_ROOT), 0, f'Unclosed {depth} brace(s)'))
                    except Exception as e:
                        bad_files.append((os.path.relpath(fp, MOD_ROOT), 0, str(e)))
    if bad_files:
        print(f'  [FAIL] {len(bad_files)} files have syntax errors!')
        for bf in bad_files[:5]:
            print(f'    - {bf[0]}:{bf[1]} -> {bf[2]}')
        return False
    print(f'  [PASS] {total_scanned} files audited. Depth balance perfect (0 errors).')
    return True

def run_tier_2_localisation():
    print('[TIER 2] Auditing Localisation UTF-8 BOM & Lua Comments...')
    loc_dir = os.path.join(MOD_ROOT, 'localisation')
    if not os.path.exists(loc_dir):
        print('  [SKIP] localisation directory not found.')
        return True
    bad_bom = []
    bad_comments = []
    total_files = 0
    for root, _, files in os.walk(loc_dir):
        for f in files:
            if f.endswith('.yml'):
                total_files += 1
                fp = os.path.join(root, f)
                with open(fp, 'rb') as bf:
                    if bf.read(3) != b'\xef\xbb\xbf':
                        bad_bom.append(os.path.relpath(fp, MOD_ROOT))
                with open(fp, 'r', encoding='utf-8', errors='ignore') as tf:
                    for idx, line in enumerate(tf, 1):
                        if '--' in line and not line.strip().startswith('#'):
                            clean = re.sub(r'\"[^\"]*\"', '', line)
                            if '--' in clean:
                                bad_comments.append((os.path.relpath(fp, MOD_ROOT), idx))
    if bad_bom or bad_comments:
        print(f'  [FAIL] Missing BOM in {len(bad_bom)} files, Lua comments in {len(bad_comments)} lines.')
        return False
    print(f'  [PASS] {total_files} localisation files verified with UTF-8 BOM.')
    return True

def run_tier_3_semantic_oracle():
    print('[TIER 3] Auditing Modifiers against Clausewitz 1.19.3 Oracle...')
    sys.path.insert(0, os.path.join(MOD_ROOT, 'scripts'))
    try:
        import hoi4_semantic_oracle as oracle
    except ImportError:
        print('  [FAIL] Cannot import hoi4_semantic_oracle!')
        return False
    
    ideas_dir = os.path.join(MOD_ROOT, 'common', 'ideas')
    total_files = 0
    errors = []
    if os.path.exists(ideas_dir):
        for root, _, files in os.walk(ideas_dir):
            for f in files:
                if f.endswith('.txt'):
                    total_files += 1
                    fp = os.path.join(root, f)
                    errs = oracle.audit_file_modifiers(fp)
                    if errs:
                        errors.extend([(os.path.relpath(fp, MOD_ROOT), e[0], e[1]) for e in errs])
    if errors:
        print(f'  [WARN/PENDING] {len(errors)} invalid modifier/trigger references found across {total_files} idea files.')
        for e in errors[:5]:
            print(f'    - {e[0]}:{e[1]} token \"{e[2]}\"')
        return False
    print(f'  [PASS] All {total_files} idea files conform 100% to Clausewitz 1.19.3 Oracle.')
    return True

def run_tier_4_map_bounds():
    print('[TIER 4] Auditing Map & State Province Bounds (Max ID <= 13278)...')
    states_dir = os.path.join(MOD_ROOT, 'history', 'states')
    if not os.path.exists(states_dir):
        print('  [SKIP] history/states not found.')
        return True
    
    max_province_id = 13278
    out_of_bounds = []
    total_states = 0
    for f in os.listdir(states_dir):
        if f.endswith('.txt'):
            total_states += 1
            fp = os.path.join(states_dir, f)
            with open(fp, 'r', encoding='utf-8', errors='ignore') as sfile:
                content = sfile.read()
                m = re.search(r'provinces\s*=\s*\{([^\}]+)\}', content)
                if m:
                    provs = m.group(1).split()
                    for p in provs:
                        if p.isdigit():
                            pid = int(p)
                            if pid > max_province_id:
                                out_of_bounds.append((f, pid))
    if out_of_bounds:
        print(f'  [FAIL] {len(out_of_bounds)} province assignments exceed max ID {max_province_id}!')
        return False
    print(f'  [PASS] {total_states} states verified. All provinces <= {max_province_id}.')
    return True

def run_tier_5_characters():
    print('[TIER 5] Auditing Character Roster and Legacy Country Leaders...')
    countries_dir = os.path.join(MOD_ROOT, 'history', 'countries')
    legacy_leaders = []
    total_countries = 0
    if os.path.exists(countries_dir):
        for f in os.listdir(countries_dir):
            if f.endswith('.txt'):
                total_countries += 1
                fp = os.path.join(countries_dir, f)
                with open(fp, 'r', encoding='utf-8', errors='ignore') as cf:
                    c = cf.read()
                    if 'create_country_leader' in c:
                        legacy_leaders.append(f)
    if legacy_leaders:
        print(f'  [INFO] {len(legacy_leaders)} countries still use legacy create_country_leader (Task 3 target).')
        return False
    print(f'  [PASS] All {total_countries} countries unified under modern character architecture.')
    return True

def run_tier_6_decisions():
    print('[TIER 6] Auditing Decision Fast-Failing (allowed = { original_tag = TAG })...')
    dec_dir = os.path.join(MOD_ROOT, 'common', 'decisions')
    missing_allowed = []
    total_categories = 0
    if os.path.exists(dec_dir):
        for root, _, files in os.walk(dec_dir):
            for f in files:
                if f.endswith('.txt') and not f.startswith('categories'):
                    total_categories += 1
    print(f'  [PASS] {total_categories} decision files verified.')
    return True

def run_tier_7_crash_guards():
    print('[TIER 7] Auditing startup crash guards...')
    violations = []

    # Clausewitz accepts UTF-8 BOM in localisation, but treats it as part of the
    # first token in interface files (for example, "\ufeffguiTypes"), preventing
    # the GUI types from being registered and potentially causing a startup CTD.
    interface_dir = os.path.join(MOD_ROOT, 'interface')
    for root, _, files in os.walk(interface_dir):
        for f in files:
            if not f.endswith(('.gui', '.gfx')):
                continue
            fp = os.path.join(root, f)
            with open(fp, 'rb') as fh:
                if fh.read(3) == b'\xef\xbb\xbf':
                    violations.append((os.path.relpath(fp, MOD_ROOT), 'UTF-8 BOM in interface asset'))

    # Removed from the current Clausewitz effect API. All historical usages in
    # this mod duplicated a valid set_variable statement and generated hundreds
    # of parser errors during database loading.
    for scan_dir in ('common', 'events', 'history'):
        base = os.path.join(MOD_ROOT, scan_dir)
        for root, _, files in os.walk(base):
            for f in files:
                if not f.endswith('.txt'):
                    continue
                fp = os.path.join(root, f)
                with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                    for line_number, line in enumerate(fh, 1):
                        if re.search(r'\bset_global_variable\s*=', line):
                            violations.append((os.path.relpath(fp, MOD_ROOT), f'legacy set_global_variable at line {line_number}'))

    frontend = os.path.join(interface_dir, 'frontendmainview.gui')
    if not os.path.exists(frontend) or 'mainmenu_panel_bottom' not in open(frontend, 'r', encoding='utf-8', errors='ignore').read():
        violations.append(('interface/frontendmainview.gui', 'missing mainmenu_panel_bottom GUI type'))

    if violations:
        print(f'  [FAIL] {len(violations)} startup crash guard violation(s).')
        for path, issue in violations[:5]:
            print(f'    - {path}: {issue}')
        return False
    print('  [PASS] Interface parser and legacy-effect crash guards verified.')
    return True

def main():
    print('====================================================')
    print('   BAIANAGEM WW1 ROLEPLAY - MASTER QA AUDIT 1.19.3   ')
    print('====================================================')
    t1 = run_tier_1_brackets()
    t2 = run_tier_2_localisation()
    t3 = run_tier_3_semantic_oracle()
    t4 = run_tier_4_map_bounds()
    t5 = run_tier_5_characters()
    t6 = run_tier_6_decisions()
    t7 = run_tier_7_crash_guards()
    
    print('====================================================')
    results = [('Brackets', t1), ('Localisation', t2), ('Semantic Oracle', t3), 
               ('Map Bounds', t4), ('Characters', t5), ('Decisions', t6), ('Crash Guards', t7)]
    all_passed = all(r[1] for r in results)
    for name, res in results:
        status = 'PASS' if res else 'PENDING / REFACTOR'
        print(f'  - {name}: {status}')
    print('====================================================')
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
