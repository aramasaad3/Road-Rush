# Road Rush: Line-by-Line Documentation
**Prepared for Development Teams & Academic Review**

---

## Part 3: `.gitignore` (The Source Control Filter)

When working on a team project, programmers use Git and GitHub to save their code and share it. However, games often generate massive temporary folders, secret password files, and garbage cache files. If you upload these to GitHub, it ruins the project. 

The `.gitignore` file acts like a bouncer at a club. It tells Git exactly which files are **forbidden** from being saved to the online repository. Here is the line-by-line breakdown of why we block certain files:

### Python Temporary Files
```text
1: # Python
2: __pycache__/
3: *.pyc
4: *.pyo
```
*   **Line 1:** Lines starting with `#` in this file are just human-readable comments. This section organizes Python rules.
*   **Line 2:** `__pycache__/` blocks the entire folder named `__pycache__`. When Python runs your game for the first time, it translates the human code into machine code to run faster next time. It stores that machine code in this folder. We block it because everyone's computer generates their own automatically, and tracking it on GitHub causes constant conflict errors.
*   **Line 3:** `*.pyc` blocks any file ending in `.pyc` (Compiled Python Files). The `*` is a wildcard, meaning "literally any name as long as it ends with .pyc".
*   **Line 4:** `*.pyo` blocks Optimized Python Files, which are an older format of `.pyc`.

### PC Builder Files (PyInstaller)
```text
6: # PyInstaller output
7: build/
8: dist/
9: *.spec
```
*   **Line 7 & 8:** To play the game without installing Python, we use PyInstaller to build a classic `exe` app. PyInstaller dumps massive chunks of data into the `build/` and `dist/` folders. An `exe` file can be hundreds of megabytes. GitHub is designed for thousands of tiny text files. We block these folders so we don't accidentally push a 200MB `exe` into our source code storage!
*   **Line 9:** `*.spec` blocks spec files (but wait!). *Note: In our actual project development, we bypassed this rule for `RoadRush.spec` by manually adding it, because we wanted to keep the specific setup instructions safe.* 

### Android Mobile Builder Files (Buildozer)
```text
11: # Buildozer build artifacts
12: .buildozer/
13: bin/
```
*   **Line 12:** `.buildozer/` is the hidden folder where the mobile converter downloads immense amounts of Android Studio tools to compile the `APK`. It can exceed gigabytes of space. This is absolutely blocked.
*   **Line 13:** `bin/` is the final destination folder where the finished Android `APK` is dumped. Similar to the Windows `exe`, we don't want giant phone apps polluting our source code history.

### Historical Project Files
```text
15: # Extracted pptx text
16: extracted_text.txt
17: read_pptx.py
```
*   **Line 16 & 17:** Early in the project's lifespan, there was a PowerPoint presentation explaining the architecture, and a script written to extract the text from it. Since they were one-off throwaway scripts, we instruct Git to ignore them forever so they don't clutter the final project repo.

### Operating System Garbage
```text
19: # OS
20: .DS_Store
21: Thumbs.db
```
*   **Line 20:** `.DS_Store` stands for "Desktop Services Store". It is a hidden file automatically created by Apple Mac computers in almost every folder to remember where to place the icons. If a Mac user joined the team, their computer would secretly try to upload these files everywhere. We block it permanently here.
*   **Line 21:** `Thumbs.db` is the exact same concept, but for Windows computers protecting the image thumbnail caching. We block it to keep the repository strictly focused on Game Code only.
