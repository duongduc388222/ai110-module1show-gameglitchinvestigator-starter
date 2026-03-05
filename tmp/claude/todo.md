# Todo: Fix Game Glitch Investigator

## Phase 1: Fix bugs in app.py (Bugs 1-10)

- [ ] **Step 1: Bug 1 — Swap hint messages in `check_guess()`**
  - Swap "Go HIGHER!" and "Go LOWER!" so hints match the outcome
  - **Test:** Run app, guess higher than secret → should say "Go LOWER!"

- [ ] **Step 2: Bug 2 — Remove type coercion sabotage**
  - Remove the `if attempts % 2 == 0: secret = str(...)` block (lines 158-161)
  - Always use `secret = st.session_state.secret`
  - Remove the `try/except TypeError` block in `check_guess()`
  - **Test:** Hints should be correct on both odd and even attempts

- [ ] **Step 3: Bug 3 — Fix Hard difficulty range**
  - Change Hard range from `(1, 50)` to `(1, 500)`
  - **Test:** Select Hard → sidebar should show "Range: 1 to 500"

- [ ] **Step 4: Bug 4 — Fix attempt counter init**
  - Change `st.session_state.attempts = 1` to `= 0`
  - **Test:** First guess should show as attempt 1, not 2

- [ ] **Step 5: Bug 5 + 6 — Fix New Game reset**
  - Reset `status`, `history`, `score` on new game
  - Use `random.randint(low, high)` instead of hardcoded `(1, 100)`
  - **Test:** Win a game, click New Game → should be playable again

- [ ] **Step 6: Bug 7 — Fix info text**
  - Replace hardcoded "between 1 and 100" with `{low}` and `{high}`
  - **Test:** Change difficulty → info text should reflect correct range

- [ ] **Step 7: Bug 8 — Fix win score formula**
  - Remove `+ 1` from `100 - 10 * (attempt_number + 1)`
  - **Test:** Win on attempt 1 → score should be 90

- [ ] **Step 8: Bug 9 — Fix "Too High" scoring**
  - Remove parity-based branching, always deduct 5 points
  - **Test:** "Too High" on any attempt should deduct 5 points

- [ ] **Step 9: Bug 10 — Don't consume attempts on invalid input**
  - Move `attempts += 1` after validation succeeds
  - Stop appending invalid guesses to history
  - **Test:** Enter "abc" → attempts count should not change

## Phase 2: Refactor into logic_utils.py (Bug 12)

- [ ] **Step 10: Bug 12 — Move fixed functions to `logic_utils.py`**
  - Copy fixed `get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score` into `logic_utils.py`
  - Update `app.py` to import from `logic_utils`
  - Remove function definitions from `app.py`

## Phase 3: Fix tests (Bug 11)

- [ ] **Step 11: Bug 11 — Fix test assertions**
  - Unpack tuple return from `check_guess()` in tests
  - Run `pytest` to verify all tests pass

## Phase 4: Update documentation

- [ ] **Step 12: Complete unanswered questions in `reflection.md`**
- [ ] **Step 13: Update `README.md` with bug fixes explanation**
- [ ] **Step 14: Update `FIX_PLAN.md` checkboxes**

---

## Review
*(To be filled after all steps are complete)*
