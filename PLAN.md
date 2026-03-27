The Swarm Orchestrator CLI

## 1. Core Objectives
* **Aesthetic Dominance:** Deliver a rich, responsive TUI with live-updating panels, syntax highlighting, and progress animations.
* **Parallel Execution:** Leverage Git worktrees to allow isolated, simultaneous code generation.
* **Agnostic Agent Adapters:** Abstract the specific tools (Cursor, Antigravity, Codex) so agents can be swapped, added, or removed hot via the UI.
* **Global State Management:** Maintain a single source of truth for the project roadmap, accessible by all agents.

## 2. Technology Stack
* **TUI Framework:** `Textual` (Python). It allows for CSS-like styling in the terminal, async UI updates, and complex layouts (drawers, modal dialogs, split panes).
* **Orchestration Logic:** `LangGraph`. Perfect for defining the cyclical graph of planning $\rightarrow$ delegating $\rightarrow$ executing $\rightarrow$ reviewing.
* **Version Control Magic:** `GitPython`. For programmatic creation and destruction of Git worktrees and branches.
* **Storage:** Local SQLite database or a persistent `state.json` at the root of the initialized repository.

## 3. UI/UX Architecture (The TUI)
When typing `forge`, the terminal takes over the full screen with the following layout:

* **Header:** Current project name, active branch, and global status (e.g., "3 Agents Active | 0 Merge Conflicts").
* **Left Sidebar (The Roster):** A live list of available/active agents.
    * 🟢 `Cursor (Main)`: Idle
    * 🟡 `Antigravity (Branch: feat/auth)`: Generating API routes...
    * 🔵 `Codex (Branch: docs/auth)`: Writing JSDoc...
* **Main Console (The Log):** The central chat interface where you issue commands to the Orchestrator ("Build a new login page and add tests for it").
* **Right Sidebar (The State Board):** A Kanban-style view of the `state.json` tasks (To Do, In Progress, Review, Done).
* **Footer/Command Palette:** A fuzzy-search input triggered by `Ctrl+P` to quickly execute commands like `spawn [agent]`, `kill [agent]`, or `sync`.

## 4. System Architecture & Modules

### Phase 1: The Git Worktree Engine (`git_manager.py`)
The foundation of the swarm. Agents cannot step on each other's toes.
* **`spawn_workspace(branch_name)`**: Creates a new Git worktree in a hidden directory (e.g., `.forge/worktrees/branch_name`).
* **`sync_state()`**: Rebase background worktrees onto the main branch to prevent massive merge conflicts later.
* **`merge_and_destroy(branch_name)`**: Squash-merges the agent's work into main and deletes the worktree.

### Phase 2: The Agent Adapters (`adapters/`)
Since Cursor and Antigravity don't have open APIs for remote control, the orchestrator controls them via workspace initialization and context injection.
* **`cursor_adapter.py`**: Triggers Cursor via CLI (`cursor /path/to/worktree`) and writes an `.instructions.md` file for its Composer to read.
* **`antigravity_adapter.py`**: Similar injection, setting up the environment variables or context files it requires.
* **`codex_adapter.py`**: Directly wraps the Codex CLI commands, passing stdout/stderr back to the TUI.

### Phase 3: The LangGraph Brain (`orchestrator.py`)
The logic layer that processes your natural language input.
* **Task Breakdown:** You type "Refactor the database schema." The graph calls a fast LLM (like Gemini Flash) to break this into: 1. Update models (Assign: Antigravity), 2. Write migrations (Assign: Cursor), 3. Update tests (Assign: Codex).
* **Routing & Delegation:** The graph calls the Git Engine to spin up worktrees, assigns the tasks to the adapters, and updates the UI State Board.
* **Review Node:** Before code is merged back to the main branch, the graph triggers a validation step (linting/testing) in the worktree.

## 5. Implementation Roadmap

### Milestone 1: TUI Prototype & Git Logic (Week 1)
* [ ] Initialize Python project with `uv` or `poetry`.
* [ ] Build the basic Textual UI layout (Header, Log, Sidebar).
* [ ] Implement the `git_manager.py` to programmatically create and delete worktrees from Python.
* [ ] Test spawning a dummy process in a new worktree and watching it complete.

### Milestone 2: Single Agent Integration (Week 2)
* [ ] Build the `state.json` parser to populate the UI's task list.
* [ ] Implement the `codex_adapter.py` (easiest to start with since it's CLI based).
* [ ] Create the workflow: Type command $\rightarrow$ Create Worktree $\rightarrow$ Run Codex $\rightarrow$ Merge back.

### Milestone 3: The LangGraph Orchestrator (Week 3)
* [ ] Define the Graph state (messages, active_worktrees, task_list).
* [ ] Build the Planner Node (breaks down user prompts into discrete agent tasks).
* [ ] Implement multi-agent routing (dispatching tasks to Codex and mock Cursor/Antigravity concurrently).

### Milestone 4: Polish & Advanced Adapters (Week 4)
* [ ] Finalize the Cursor and Antigravity hand-offs (opening the respective editors in the targeted worktrees).
* [ ] Add beautiful Textual animations (spinners, color-coded log streams).
* [ ] Implement conflict detection (alerting you in the UI if two agents are modifying the same underlying architecture).