## v0.3.0 (2021-10-30)

### Fix

- improve parsing method for evicting errors by fields aggregations

### Feat

- integrate pre-commit for avoid format errors
- split implementation in two classes

## v0.2.0 (2021-09-17)

### Fix

- add aclose method for async with and use run_until_complete
- remove user_id and paid_by_user_id properties from Transaction
- add type hint in __enter__ method of QvaPayClient class

### Feat

- add cache to GitHub Actions
- add context manager; updated README

## v0.1.0 (2021-09-05)

### Feat

- add post init validation to QvaPayAuth
- add not required status message to QvaPayError
- improve implementation

### Fix

- change UUID by str in remote_id of transaction model
- use python-dotenv for obtain authentication info from environment

### Perf

- remove pydantic dependency

## v0.0.3 (2021-08-30)

### Perf

- contributors
- contributors & deps
- added all contributors to README.md
- improved client
- preparing for publishing to pypi

### Fix

- switched from stage to production
- removed unused field
- improved imports
- improved imports
- removed unused code
- changed signed attr type
- fixed invoice model attrs
- fixed info model using alias values and str repr from datetimes
- path and pep8 fixes
- added vscode settings file
- error class for qvapay requests
- removed unused import

### Feat

- added github dependabot
- transaction endpoints
- fixed transaction model
- added alias to uuid field
- using json dataclass
- added link model
- renamed folder to better understanding of the project layout
- fixed info class and post init function
- using dataclass decorator, PEP 557 PEP 526
- qvapay client
