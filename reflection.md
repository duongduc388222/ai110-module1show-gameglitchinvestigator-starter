# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

  The UI looks fine at first, but after more careful looking, there are inconsistency in various place in terms of the range we're supposed to be guessing and the number of attempts allowed. The winning animation for guessing secret number generally works, but I cannot click new game to play a new game and have to reload the file instead. There were actually error handling for non-integer values so that was a surprised. However, I think that a non-integer guess should not have counted as one attempt.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

  1. Show hint button is giving the wrong hint.
  2. Inconsistency parameters like range of numbers and number of attempts we want to guess depending on different levels
  3. Wasn't able to start a new game and was stuck. Have to reload.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  I'm currently using Claude Code on the terminal while in Cursor.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  Below is Claude's response.
  1. Hints are backwards (line 37-40)                              
                                                                    
    if guess > secret:                                               
        return "Too High", "📈 Go HIGHER!"   # Should say Go LOWER
    else:                                                          
        return "Too Low", "📉 Go LOWER!"     # Should say Go HIGHER
    The hint messages are swapped — when the guess is too high, it
    tells you to go higher.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  There was actually none in the 4 suggestions Claude gave me because I made Claude reference my experience by giving it context of the first question. By doing so, Claude is more focused and aware of these bugs.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  I asked Claude to create test cases (making sure that covering even edge cases). Also, after me and Claude fixes those bugs, I gave the game a final sanity check and repaly the game.
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.

  I ran `pytest tests/test_game_logic.py` which contains three tests: `test_winning_guess`, `test_guess_too_high`, and `test_guess_too_low`. Before fixes, the tests failed because they expected `check_guess()` to return a plain string like `"Win"`, but the function actually returned a tuple `("Win", "Correct!")`. After fixing the tests to unpack the tuple (`outcome, message = check_guess(50, 50)`), all three tests passed. This showed me that even when the game logic is correct, mismatched return type expectations in tests can cause false failures.

- Did AI help you design or understand any tests? How?
  Yes, it did help me design the edge cases that I think normally I would miss. Claude identified that the original tests were checking for a string return value when the function actually returned a tuple, which is why they always failed regardless of whether the logic was correct.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

  Streamlit reruns the entire script from top to bottom every time the user interacts with any widget (button click, text input, etc.). Without `session_state`, any variable like `secret = random.randint(1, 100)` would be regenerated on every rerun, giving a new secret each time. By storing the secret in `st.session_state.secret` and only setting it when the key doesn't already exist (`if "secret" not in st.session_state`), the value persists across reruns.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  Imagine every time you click a button on a webpage, the entire page gets rebuilt from scratch — that's how Streamlit works. Normally this means all your variables get reset. But `session_state` is like a sticky note that survives the rebuild: you write a value on it once, and every time the page rebuilds, it checks the sticky note instead of creating a new value. This is how the game remembers the secret number, your score, and how many attempts you've used.

- What change did you make that finally gave the game a stable secret number?

  The original code already used `st.session_state.secret` for initialization, which kept the number stable during gameplay. The real stability issue was in the "New Game" button — it used `random.randint(1, 100)` hardcoded instead of `random.randint(low, high)` based on the current difficulty, and it also failed to reset `status`, `history`, and `score`. Fixing the New Game handler to fully reset all state with the correct range made the game properly restartable.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?

  Next time I would start by giving the AI context about what I've already observed (which I did here and it worked well), but I would also ask it to generate a comprehensive test suite *before* fixing bugs. Having tests first would let me verify each fix immediately and catch regressions. Writing tests after the fact means you might miss edge cases.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

  This project showed me that AI-generated code can look clean and functional on the surface while hiding subtle bugs — like swapped hint messages, parity-based sabotage, or off-by-one errors — that only surface during actual gameplay. It reinforced that AI is a powerful collaborator but its output always needs testing and critical review.
