# SESSION 01 — ANALYSIS AND REQUIREMENTS

Continue using the Master Prompt.

## Objective
Analyze the supplied HTML form before writing automation code.

## Step 0 — Locate every ground truth source, not just the HTML

Per the Master Prompt's "Ground truth sources" section: before reading the
HTML in detail, check the workspace (and any related zip/package, even one
extracted in a different session or location) for an FSD, a formal QA
workflow package (Scope/Analyze Requirements/Test Plan/Test Case
Design/Test Suite Organization/Test Execution/Defect Reporting), and an
official `TS01.xlsx`..`TS0N.xlsx` test case library. State explicitly,
before proceeding, which of these exist and where each was found (or that
none exist and analysis will be HTML-only).

## Tasks
1. Inspect the actual HTML.
2. Identify the form, fields, labels, placeholders, selects, radio buttons, checkboxes, textarea, submit button, validation, JavaScript behavior, and success/result behavior.
3. Build a field/control inventory. If an FSD exists, cross-reference every field against its field table (data type/max length/mandatory/UI element/validation) and note every mismatch explicitly — a mismatch is a finding, not an error to silently resolve one way or the other.
4. Identify stable locators.
5. Determine whether direct `file://` loading works or a local server is required.
6. Identify realistic test scenarios. If an official test case library exists, this step is: transcribe its test cases faithfully (do not re-derive scenarios from scratch when an authoritative list already exists) and note its own recorded Pass/Fail/Blocked status per case, since Session 04 will need it.
7. Define expected results strictly from observable behavior — unless an official test case library exists and a specific case's own recorded result already documents an FSD-vs-build divergence (see Master Prompt's "Reconciling..." section), in which case record both: what the build actually does, and what the FSD requires.

## Required output

Create/update documentation containing:

- ground truth sources found (Step 0) and where each was located;
- application under test;
- field/control inventory (cross-referenced against the FSD's field table when one exists);
- candidate locators;
- validation behavior;
- submission behavior;
- test scenarios;
- expected results;
- assumptions.

Create:

| ID | Scenario | Preconditions | Test Data | Expected Result |
|---|---|---|---|---|

At minimum identify a valid submission scenario and relevant negative scenarios if supported. If an official test case library exists, this table is the full transcribed list (one row per official TC ID), not a hand-picked subset.

## Rules
Do not implement the final tests yet.
Do not invent expected results — except as explicitly permitted above when reconciling against an official, already-executed test case library.
Do not modify the supplied application unless necessary.

Finish with a clear implementation plan for Session 02.
