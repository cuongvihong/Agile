# SESSION 03 — PAGE OBJECTS AND LOCATORS

Continue from Sessions 01–02.

## Objective
Implement the Page Object Model for the actual HTML form.

## BasePage

Create `pages/base_page.py`.

Provide only reusable browser/page operations, such as:
- page storage;
- navigation;
- screenshot helper;
- URL/title helpers when useful.

## FormPage

Create `pages/form_page.py`.

It must represent the actual form and contain:
- centralized locators;
- field interaction methods;
- selection/check methods;
- submit action;
- result/validation readers.

Prefer readable methods such as:

```python
open()
fill_form(data)
submit()
verify_success()
```

Add specialized methods only where they improve readability.

## Locator rules

Use the actual HTML and prefer:

```python
page.get_by_role(...)
page.get_by_label(...)
page.get_by_text(...)
page.get_by_placeholder(...)
page.get_by_test_id(...)
```

Use CSS/XPath only when needed.

Do not invent selectors.

**Verify the locator strategy empirically before committing to it** — do
not assume `get_by_role`/`get_by_label` will resolve correctly just
because a field looks labeled. Two real gotchas to check for on any new
form:
- `get_by_label()` requires a real `for`/id association or the input
  being nested inside the `<label>` — many forms have visually-labeled
  fields with neither, so `get_by_label()` silently fails to resolve them.
  A CSS id-based fallback is legitimate here (and should be documented as
  such), since the app's own script usually depends on the same ids.
- `get_by_role(..., name=...)` does a **substring** match by default, not
  exact. Two options whose text contains one another as a substring (e.g.
  "Singapore" / "Non-Singapore") will both match a query for the shorter
  one unless `exact=True` is passed. Confirm this by actually running the
  selector, not by inspection alone.

If an official test case library's own data uses field/option names that
don't literally exist as build option text (e.g. the library says
"Employment Pass" but the build's dropdown only has "EP"), add an explicit
mapping table in `data/` with a one-line comment citing the underlying
defect/finding — do not silently substitute one string for another inside
a Page Object method.

Add a narrow escape-hatch method for setting a raw DOM value (bypassing
the browser's own `maxlength` enforcement) if any boundary test needs to
exceed an HTML length cap that coincides with the value under test —
`.fill()` respects `maxlength` exactly like real typing would, which can
make a boundary genuinely untestable through normal interaction. Use it
only for that narrow purpose, never as a general replacement for `.fill()`.

## Assertions

Page Object methods may expose state, but keep test intent in the test layer.

Example:

```python
def is_success_visible(self):
    return self.success_message.is_visible()
```

or use `expect` in the appropriate layer according to the project design.

## End condition
The Page Object should allow the main user workflow to be expressed in a few readable test lines.
Do not implement unrelated features.
