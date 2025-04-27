Here’s a first draft of a clear and actionable `CONVENTIONS.md` file based on your provided instructions:

---

# CONVENTIONS.md

This document defines conventions and guidelines for contributing to **t3py**.

## Overview

`t3py` is a command-line and Python library interface to the Track & Trace Tools (T3) API. It is designed for both interactive CLI usage and programmatic imports in other Python scripts.

The OpenAPI specification (`openapi.json`) is included in the repo and must be used to align the client with the official API.

---

## Project Structure

- **CLI Application:**  
  - The CLI should launch via the `t3py` entry point.
  - Upon starting, the CLI should authenticate the user and present a menu-driven interface.
- **Python Library:**  
  - The library must expose modules and classes that wrap **all** T3 API endpoints.

---

## CLI Design Conventions

- **Authentication First:**  
  Always authenticate on CLI startup unless a non-authenticated routine is explicitly called.

- **Menu-driven Navigation:**  
  - Display a user menu with clear choices after authentication.
  - Organize commands into "routines" that group related API workflows.
  - For user inputs:
    - **Preload options** when available (e.g., licenses, states).
    - Use dropdowns, numbered selections, or autocomplete where possible.
    - **Provide sensible defaults** based on API documentation.

- **One-off Commands:**  
  Support "single-shot" CLI commands (e.g., `t3py authcheck`) without launching the full menu interface.

- **Reports:**  
  All "Reports" endpoints must be fully implemented as interactive CLI routines.

---

## Library (Importable Python Code) Conventions

- **Authentication Handling:**  
  - Centralize credential management and JWT refreshing.
  - Expose a simple method to authenticate and retrieve a valid access token.

- **API Wrapping:**  
  - Wrap the **entire** T3 API.
  - Organize code into logical groups (e.g., `auth.py`, `reports.py`, `packages.py`).
  - Follow the structure of the OpenAPI spec wherever possible.

- **Use `httpx`:**  
  All HTTP requests must use the `httpx` library.

- **Type Annotations:**  
  Use full Python 3 type annotations for all public methods and classes.

- **Error Handling:**  
  - Gracefully catch and report HTTP errors.
  - Provide helpful messages on authentication failure, missing data, or server errors.

---

## Coding Style

- Follow [PEP8](https://peps.python.org/pep-0008/) for Python code style.
- Prefer explicitness over implicitness.
- Use `async`/`await` if the code is async-compatible in the future, but initially build synchronous flows.
- Keep functions small, composable, and focused on a single responsibility.

---

## Miscellaneous

- **API Schema Awareness:**  
  When writing prompts or menus, pull field names, defaults, and descriptions from `openapi.json` when applicable.

- **Documentation:**  
  - All public functions, classes, and modules must have docstrings.
  - Keep CLI and library behaviors clearly documented.

- **Testing:**  
  - Add unit tests for critical logic.
  - Favor testable, modular code over monolithic scripts.

---

Would you also like me to make a slightly stricter version (for example, specifying naming rules like `snake_case` for files and classes, or even adding TODOs about later adding async support)?  
I can generate that too if you want a "full discipline" version. 🚀