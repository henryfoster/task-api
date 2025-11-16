# Run
`uv run uvicorn app.main:app --reload`
`uv run fastapi dev`
`uv run ruff check app/ tests/`  # Lint
`uv run ruff check --fix app/ tests/`  # fixes
`uv run ruff format app/ tests/` # Format
`uv run mypy app/ tests/ `       # Type check
`uv run pytest`

# Ruff
## ruff.toml
[lint]
# Core rule sets most companies use
select = [
  "E",     # pycodestyle errors (PEP 8)
  "F",     # Pyflakes (unused imports, variables)
  "I",     # isort (import sorting)
  "UP",    # pyupgrade (modern Python syntax)
  "B",     # flake8-bugbear (bug-prone patterns)
  "C90",   # mccabe (complexity)
  "N",     # pep8-naming (naming conventions)
  "W",     # pycodestyle warnings
]

ignore = [
  "E501",  # Line too long (Black handles this)
  "B008",  # Do not perform function calls in argument defaults
]

## Common business settings
line-length = 88  # Black's default
target-version = "py311"  # Or your Python version

[lint.mccabe]
max-complexity = 10  # Cyclomatic complexity limit

[lint.per-file-ignores]
"tests/*" = ["F401", "F811"]  # Allow unused imports in tests

[format]
quote-style = "double"
indent-style = "space"

What Each Rule Set Does:

- E/W: PEP 8 compliance (spacing, naming)
- F: Catches actual bugs (unused variables, imports)
- I: Sorts imports consistently
- UP: Uses modern Python syntax (f-strings, type hints)
- B: Prevents dangerous patterns (mutable defaults, etc.)
- N: Enforces naming conventions (snake_case, etc.)




Next:
Relations
- add a Tags table 
- adding tags and fetching from tasks?

