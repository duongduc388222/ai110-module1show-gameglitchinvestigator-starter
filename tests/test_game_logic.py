# FIX: Updated tests to unpack tuple returns from check_guess() — identified by Claude Code
from logic_utils import (
    check_guess,
    parse_guess,
    get_range_for_difficulty,
    update_score,
)


# --- check_guess tests ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Edge-case tests generated with Claude Code ---

def test_parse_guess_non_numeric_string():
    """Non-numeric input like 'abc' should fail gracefully."""
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_parse_guess_empty_input():
    """Empty string should prompt the user to enter a guess."""
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_guess_none_input():
    """None input (no submission) should be handled the same as empty."""
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_guess_negative_number():
    """Negative numbers are valid integers and should parse successfully."""
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert err is None


def test_parse_guess_float_string():
    """Floating-point strings like '3.7' should be truncated to int."""
    ok, value, err = parse_guess("3.7")
    assert ok is True
    assert value == 3
    assert err is None


def test_parse_guess_special_characters():
    """Special characters like '!@#' should fail gracefully."""
    ok, value, err = parse_guess("!@#")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_hard_difficulty_harder_than_normal():
    """Hard range must be wider than Normal to be genuinely harder."""
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high


def test_update_score_win_first_attempt():
    """Winning on attempt 1 should award 90 points (100 - 10*1)."""
    score = update_score(current_score=0, outcome="Win", attempt_number=1)
    assert score == 90


def test_update_score_too_high_always_deducts():
    """Too High should always deduct 5, regardless of attempt parity."""
    score_even = update_score(current_score=50, outcome="Too High", attempt_number=2)
    score_odd = update_score(current_score=50, outcome="Too High", attempt_number=3)
    assert score_even == 45
    assert score_odd == 45


def test_update_score_win_floor_at_10():
    """Win points should never drop below 10 even on late attempts."""
    score = update_score(current_score=0, outcome="Win", attempt_number=20)
    assert score == 10
