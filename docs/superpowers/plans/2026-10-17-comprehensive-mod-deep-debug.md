# Comprehensive Mod Deep Debug & Legacy Repair Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Perform an exhaustive, deep debug across all subsystems of the mod (focus trees, events, decisions, ideas, characters, mechanics, and GUI) to resolve all broken references, restore broken progression trees, and ensure 100% bug-free execution under Hearts of Iron IV 1.19.

**Architecture:** Systematic diagnosis and correction using static AST analysis and automated test assertion. Every broken prerequisite, event call, missing idea, and unregistered category is cataloged, repaired with authentic historical content matching the WW1 era, and sealed with regression unit tests in 	ests/.

**Tech Stack:** Hearts of Iron IV Clausewitz Script (PDXScript), Python 3.11 test runner, Git.

**Spec:** In-repository diagnosis report (scratch/deep_scan_report.txt and scratch/refined_mod_deep_scan.py).

## Global Constraints
- All Clausewitz script edits must strictly maintain bracket balance (stack == 0).
- All .yml localisation files must maintain UTF-8 with BOM (\xef\xbb\xbf).
- Total conversion isolation: descriptor.mod replace_paths must be preserved.
- Zero reliance on user machine configuration; all fixes must live entirely inside the mod repository.

## Review Focus
- Chile focus tree prerequisite progression without crashing or deadlock.
- Event triggers from focuses (
ussia.txt, chile.txt, serbia.txt) resolving without 'event does not exist' console errors.
- Ideas granted via dd_ideas in focuses/events existing in either common/ideas/ or character advisor tokens.
- Decision categories globally available for all countries (e.g. highlight_states).
- Full passing test suite (python tests/test_runner.py) with 0 failures.

---

### Task 1: Chile National Focus Tree Restoration & Prefix Normalization
### Task 2: Missing Events & Broken Focus/Decision Event Calls
### Task 3: Missing Ideas & Advisor Tokens Compatibility Layer
### Task 4: Decision Categories, Resource Prospecting & Global QA Verification
