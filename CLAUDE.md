# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

A fully modular Othello (Reversi) game implementation in Python with PyQt6 GUI, following TDD practices.

**Project:** `othello-modular` v1.0.0 | **Python 3.10+** | **MIT License**

## Project Structure

```
src/othello/
├── main.py                          — Entry point (runs `othello` command)
├── core/                            — Game logic (no GUI dependencies)
│   ├── board.py                     — Board representation
│   ├── constants.py                 — Game constants
│   ├── engine.py                    — Game engine
│   ├── events.py                    — Event system for core
│   ├── game_state.py                — Game state management
│   ├── interfaces.py                — Player interface contracts
│   └── rules.py                     — Othello rules/validation
├── gui/                             — PyQt6 GUI components
│   ├── board_widget.py              — Visual board rendering
│   ├── events.py                    — Event system for GUI
│   ├── game_controller.py           — Mediates GUI ↔ core engine
│   ├── main_window.py               — MainWindow
│   ├── menu_widget.py               — Menu/UI controls
│   └── score_widget.py              — Score display
├── players/                         — AI and human player implementations
│   ├── ai_player.py                 — AI player
│   ├── human_adapter.py             — Human player ↔ player interface
│   ├── interfaces.py                — Player interface definition
│   └── random_player.py             — Random move player
└── utils/
    └── sounds.py                    — Sound effects (optional, requires pygame-ce)

tests/
├── conftest.py                      — Shared fixtures
├── core/                            — Tests for core modules
│   ├── test_board.py
│   ├── test_constants.py
│   ├── test_engine.py
│   └── test_rules.py
├── gui/                             — Tests for GUI modules
│   ├── test_game_controller.py
│   ├── test_main_window.py
│   └── test_pass_notification.py
└── players/                         — Tests for player modules
    ├── test_ai_player.py
    ├── test_human_adapter.py
    ├── test_player_integration.py
    └── test_random_player.py
```

## Commands

```bash
# Install dependencies (from othello_VIBE/)
pip install -e ".[sound]"        # Install with optional sound deps

# Testing
pytest                           # Run all tests (with coverage)
pytest -v                        # Verbose output
pytest tests/core/               # Run core tests only
pytest -k "test_name"            # Run matching tests
pytest --cov=src                 # With coverage report

# Code quality
ruff check src/ tests/           # Lint
black --check src/ tests/        # Check formatting
```

## Architecture

- **Event-driven**: `events.py` modules in both core and gui enable decoupled communication
- **Player interfaces**: All players (AI, random, human) implement a common interface (`players/interfaces.py`)
- **GameController**: Mediates between GUI widgets and the core game engine
- **Decoupled core**: Board state, rules, and logic are fully independent of the GUI

## Git Workflow

**Always commit and push regularly during work — never leave changes uncommitted for more than a few edits.** Commit after completing any meaningful step (a new feature, a fix, a visual update). Use clean, descriptive messages. Push immediately after each commit so progress is never lost.

```
git log           # view commit history
git show HEAD     # view latest changes
git revert HEAD   # undo the last commit
```

## Conventions

- Python 3.10+ target
- Black (88-char lines) + isort + ruff for formatting/linting
- pytest for all tests with coverage
- Keep core logic free of GUI imports
- Mirror test structure under `tests/` to match `src/othello/`
