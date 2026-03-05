# FIX: Refactored game logic from app.py into logic_utils.py using Claude Code in terminal


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard".

    Returns:
        Tuple of (low, high) integers defining the guessing range.
    """
    # FIX: Changed Hard range from (1, 50) to (1, 500) — identified by Claude Code
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 500
    return 1, 100


def parse_guess(raw: str):
    """Parse user input into an int guess.

    Args:
        raw: The raw string from the text input.

    Returns:
        Tuple of (ok: bool, guess_int: int | None, error_message: str | None).
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """Compare guess to secret and return (outcome, message).

    Args:
        guess: The player's integer guess.
        secret: The secret integer to guess.

    Returns:
        Tuple of (outcome, message) where outcome is "Win", "Too High", or "Too Low".
    """
    if guess == secret:
        return "Win", "Correct!"

    # FIX: Swapped hint messages — originally "Go HIGHER!" for Too High, identified by Claude Code
    if guess > secret:
        return "Too High", "Go LOWER!"
    return "Too Low", "Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number.

    Args:
        current_score: The player's current score.
        outcome: One of "Win", "Too High", or "Too Low".
        attempt_number: The current attempt number (1-indexed).

    Returns:
        The updated score as an integer.
    """
    if outcome == "Win":
        # FIX: Removed extra +1 that double-penalized — identified by Claude Code
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    # FIX: Too High now always deducts 5 (was parity-based) — identified by Claude Code
    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
