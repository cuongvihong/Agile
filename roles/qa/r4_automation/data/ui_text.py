"""Characters and fixed UI texts of the prototype. The file is UTF-8 (the Python 3 default),
so open it with an editor that reads UTF-8."""

MIDDOT = "·"      # separator used in the view switch and sub titles
EMDASH = "—"      # a table cell without a value shows this dash
ENDASH = "–"      # period ranges such as 01/08/2026 - 31/12/2026
LE = "≤"          # "less than or equal" in the limits
TIMES = "×"       # the close button of the drawer and the dialogs
WARN = "⚠"        # warning mark on a wizard step with errors
CROSS = "✕"       # remove button of a fee component column

VIEW_HQ = "Admin Portal " + MIDDOT + " MOE HQ"
VIEW_SCHOOL = "Admin Portal " + MIDDOT + " School user"
VIEW_PARENT = "e-Service Portal " + MIDDOT + " Parent"

SIGN_IN_HQ = "Sign in with MOE account"
HQ_USER = "Mei Lin Tan"
HQ_ROLE = "MOE HQ Administrator"

SEARCH_PLACEHOLDER = "Search student, NRIC/FIN or Application ID"
NO_RESULT = "No applications found."

TOAST_FORM_CLOSED = "Form closed. Applications were ranked by need and assessed."
TOAST_SUBSIDY = "Subsidy applied to the student's EA fees."
TOAST_REJECTED = "Application rejected. Parent notified by email."
TOAST_DRAFT = "Draft saved."
TOAST_PUBLISHED = "Scheme published. It is now view-only."
TOAST_FEES_ADDED = "Fee components added to the scheme."

ERR_NAME = "Enter a scheme name."
ERR_CELLS = "Enter 0" + ENDASH + "100 % for every new cell."
ERR_NATIONALITY = "Select at least one nationality."
ERR_BAND = "Use at least one income band (GHI or PCI)."
