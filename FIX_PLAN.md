# Fix Plan: Game Glitch Investigator

## Progress Tracker

- [x] **Bug 1:** Hints are backwards in `check_guess()`
- [x] **Bug 2:** Even-attempt type coercion sabotages comparisons
- [x] **Bug 3:** Hard difficulty range is easier than Normal
- [x] **Bug 4:** Attempt counter initializes at 1 instead of 0
- [x] **Bug 5:** New Game button doesn't reset `status`, `history`, or `score`
- [x] **Bug 6:** New Game generates secret from hardcoded range (1, 100) instead of difficulty range
- [x] **Bug 7:** Info text hardcodes "between 1 and 100" regardless of difficulty
- [x] **Bug 8:** Win score formula double-penalizes with `attempt_number + 1`
- [x] **Bug 9:** "Too High" scoring inconsistently awards/penalizes based on attempt parity
- [x] **Bug 10:** Invalid guesses still consume an attempt
- [x] **Bug 11:** Tests in `test_game_logic.py` expect wrong return type & import from stub `logic_utils.py`
- [x] **Bug 12:** Refactor game logic functions from `app.py` into `logic_utils.py`

---

## Bug 1: Hints are backwards in `check_guess()`

**File:** `app.py` lines 37-40
**Problem:** When `guess > secret`, the message says "Go HIGHER!" but should say "Go LOWER!" (and vice versa). The emoji also contradicts: it shows a chart-going-up icon for "Too High".
**Root cause:** The hint messages are swapped between the two branches.

**Current code:**
```python
if guess > secret:
    return "Too High", "📈 Go HIGHER!"
else:
    return "Too Low", "📉 Go LOWER!"
```

**Fix:** Swap the messages so the hint matches the outcome:
```python
if guess > secret:
    return "Too High", "📉 Go LOWER!"
else:
    return "Too Low", "📈 Go HIGHER!"
```

---

## Bug 2: Even-attempt type coercion sabotages comparisons

**File:** `app.py` lines 158-161
**Problem:** On even-numbered attempts, the secret is cast to `str` before being passed to `check_guess()`. This causes the `>` comparison between an `int` guess and a `str` secret to raise a `TypeError`, falling into the except block which does **lexicographic** string comparison (e.g., `"9" > "50"` is `True` because `"9"` > `"5"` alphabetically). This makes hints wrong on every even attempt.
**Root cause:** Intentional sabotage code that converts secret to string on even attempts.

**Current code:**
```python
if st.session_state.attempts % 2 == 0:
    secret = str(st.session_state.secret)
else:
    secret = st.session_state.secret
```

**Fix:** Always pass the integer secret directly:
```python
secret = st.session_state.secret
```

Also simplify `check_guess()` by removing the `try/except TypeError` block since it's no longer needed:
```python
def check_guess(guess, secret):
    if guess == secret:
        return "Win", "Correct!"
    if guess > secret:
        return "Too High", "Go LOWER!"
    return "Too Low", "Go HIGHER!"
```

---

## Bug 3: Hard difficulty range is easier than Normal

**File:** `app.py` lines 4-11
**Problem:** `get_range_for_difficulty("Hard")` returns `(1, 50)` but Normal returns `(1, 100)`. A smaller range is *easier* to guess, so Hard is actually easier than Normal.
**Root cause:** The Hard range value is set too low.

**Current code:**
```python
if difficulty == "Hard":
    return 1, 50
```

**Fix:** Make Hard genuinely harder with a wider range:
```python
if difficulty == "Hard":
    return 1, 500
```

---

## Bug 4: Attempt counter initializes at 1 instead of 0

**File:** `app.py` line 96
**Problem:** `st.session_state.attempts` starts at `1`, so the first guess is counted as attempt 2 after the `+= 1` on line 148. This makes:
- "Attempts left" display wrong (off by one from the start)
- Score calculation wrong (uses inflated attempt number)
- Attempt limit reached one guess too early

**Current code:**
```python
st.session_state.attempts = 1
```

**Fix:**
```python
st.session_state.attempts = 0
```

---

## Bug 5: New Game button doesn't reset `status`, `history`, or `score`

**File:** `app.py` lines 134-138
**Problem:** Clicking "New Game" after winning or losing doesn't reset `status` back to `"playing"`. The status check on line 140 then immediately blocks the game with "You already won" or "Game over", making it impossible to play again without reloading the page. History and score also carry over.
**Root cause:** The new game handler only resets `attempts` and `secret`.

**Current code:**
```python
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(1, 100)
    st.success("New game started.")
    st.rerun()
```

**Fix:** Reset all game state:
```python
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.success("New game started.")
    st.rerun()
```

*(Note: this also fixes Bug 6's hardcoded range issue by using `low, high`.)*

---

## Bug 6: New Game generates secret from hardcoded range

**File:** `app.py` line 136
**Problem:** `random.randint(1, 100)` ignores the current difficulty setting. On Easy (1-20) or Hard, the secret could be out of range.
**Root cause:** Hardcoded values instead of using `low, high` from `get_range_for_difficulty()`.

**Fix:** Already covered in Bug 5's fix — use `random.randint(low, high)`.

---

## Bug 7: Info text hardcodes "between 1 and 100"

**File:** `app.py` lines 109-112
**Problem:** The info message always says "Guess a number between 1 and 100" regardless of difficulty. On Easy the range is 1-20, on Hard it should be 1-500.
**Root cause:** Hardcoded string instead of using the `low`/`high` variables.

**Current code:**
```python
st.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)
```

**Fix:**
```python
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)
```

---

## Bug 8: Win score formula double-penalizes

**File:** `app.py` lines 51-52
**Problem:** `points = 100 - 10 * (attempt_number + 1)`. The `+ 1` is unnecessary because `attempts` is already incremented before `update_score()` is called (line 148). So winning on your actual 1st guess gives `100 - 10*(2) = 80` instead of 90.
**Root cause:** Extra `+ 1` in the formula.

**Current code:**
```python
points = 100 - 10 * (attempt_number + 1)
```

**Fix:**
```python
points = 100 - 10 * attempt_number
```

---

## Bug 9: "Too High" scoring inconsistently awards/penalizes

**File:** `app.py` lines 57-60
**Problem:** On "Too High" outcomes, the player *gains* 5 points on even attempts but *loses* 5 on odd attempts. Wrong guesses should consistently lose points. "Too Low" always loses 5 — the two should be symmetric.
**Root cause:** Parity-based branching that sometimes rewards wrong guesses.

**Current code:**
```python
if outcome == "Too High":
    if attempt_number % 2 == 0:
        return current_score + 5
    return current_score - 5
```

**Fix:** Always deduct points for wrong guesses:
```python
if outcome == "Too High":
    return current_score - 5
```

---

## Bug 10: Invalid guesses still consume an attempt

**File:** `app.py` lines 148-154
**Problem:** `attempts += 1` runs on line 148 *before* checking whether the input is valid. If the user types garbage like "abc", they lose an attempt for nothing.
**Root cause:** Attempt increment happens before validation.

**Current code:**
```python
if submit:
    st.session_state.attempts += 1
    ok, guess_int, err = parse_guess(raw_guess)
    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
```

**Fix:** Only increment attempts after validation succeeds:
```python
if submit:
    ok, guess_int, err = parse_guess(raw_guess)
    if not ok:
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)
        ...
```

Also stop appending invalid guesses to history.

---

## Bug 11: Tests expect wrong return type

**File:** `tests/test_game_logic.py`
**Problem:** Tests do `assert result == "Win"` but `check_guess()` returns a tuple `("Win", "message")`. Tests will always fail even with correct logic.
**Root cause:** Tests check for a string but the function returns `(outcome, message)`.

**Current code:**
```python
result = check_guess(50, 50)
assert result == "Win"
```

**Fix:** Unpack the tuple:
```python
outcome, message = check_guess(50, 50)
assert outcome == "Win"
```

---

## Bug 12: Refactor game logic into `logic_utils.py`

**File:** `logic_utils.py`
**Problem:** All four functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) are stubs that raise `NotImplementedError`. The project expects these to hold the real (fixed) logic, and `app.py` should import from `logic_utils.py`.
**Root cause:** Refactoring hasn't been done yet.

**Fix:**
1. Copy the **fixed** versions of all four functions into `logic_utils.py`
2. Update `app.py` to import from `logic_utils`:
   ```python
   from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score
   ```
3. Remove the function definitions from `app.py`
4. Update test imports if needed (already imports from `logic_utils`)

---

## Suggested Fix Order

1. Bug 1 + Bug 2 (hints & type coercion — closely related)
2. Bug 3 (Hard difficulty range)
3. Bug 4 (attempt counter init)
4. Bug 5 + Bug 6 (new game reset)
5. Bug 7 (info text)
6. Bug 8 + Bug 9 (scoring fixes)
7. Bug 10 (invalid guess attempt consumption)
8. Bug 12 (refactor into logic_utils.py)
9. Bug 11 (fix tests)
