# Copilot Instructions for imagerecog

Dearest Copilot,
this project is a Python Phoenix (wxPython) app which organizes e-Learning content.

When generating code snippets or explanations, please follow these guidelines:

1. Output always in Markdown.
2. When referring to a file in this repo, link using `#file:<relative_path>`.
   - Phoenix app: [Dateiablage.py](#file:Dateiablage.py)
   - Creating an e-Learning folder structure: [src/creator.py](#file:src/creator.py)
   - File panel: [src/files.py](#file:src/files.py)
   - Global variables setting: [src/globals.py](#file:src/globals.py)
   - e-Learning panel: [src/learning.py](#file:src/learning.py)
   - Various methods: [src/methods.py](#file:src/methods.py)
   - Preferences menu: [src/preferences.py](#file:src/preferences.py)
   - Tasks panel [src/tasks.py](#file:src/tasks.py)

3. Code‑block format for changes or new files:
    ````python
    // filepath: #file:<relative_path>
    # ...existing code...
    def my_new_function(...):
        ...
    # ...existing code...
    ````

4. Comments format:
   - Use `#` for comments
   - Start comments with 'Setting', 'Creating', 'Adding', 'Updating' etc.
     (always the gerund form)

5. Adhere to PEP 8:
   - 4‑space indentation, snake_case names
   - Imports at the top of the file
   - Docstrings in Google or NumPy style

6. Preserve existing patterns:
   - Use `@st.cache_resource` for expensive initializations
   - Store and retrieve state via `st.session_state.get("key", default)`

7. File I/O:
   - Use `os.path.join(...)` and `os.makedirs(..., exist_ok=True)`
   - Handle missing directories before writing files

8. Error handling & logging:
   - Import and configure `logger = logging.getLogger(__name__)`
   - Raise clear exceptions on invalid inputs

9. Testing:
    - Add or update tests under `tests/`
    - Use `pytest` fixtures to mock `st.session_state`