def get_input_type(char: str) -> str:
    """Classifies the character for the ATM PIN DFA transition table."""
    if char.isdigit():
        return 'digit'
    else:
        return 'invalid'

def simulate_atm_pin_dfa(pin_string: str) -> tuple[bool, list]:
    """
    Simulates the ATM PIN DFA character by character.

    Rules:
    - PIN must contain exactly 4 digits.
    - Allowed alphabet: Sigma = { 0-9 } (no letters or special characters).
    - Each digit advances exactly one state: q0 -> q1 -> q2 -> q3 -> q4.
    - Accept only when exactly four digits are entered (final state q4).
    - Any non-digit, or a fifth digit, goes to the dead state.

    Returns a tuple: (is_accepted_boolean, transition_history_list)
    """
    # This directly represents your TOA Transition Table
    transitions = {
        'q0': {'digit': 'q1'},   # Start state expects the 1st digit
        'q1': {'digit': 'q2'},   # Read 1 digit, expects the 2nd digit
        'q2': {'digit': 'q3'},   # Read 2 digits, expects the 3rd digit
        'q3': {'digit': 'q4'},   # Read 3 digits, expects the 4th digit
        'q4': {}                 # Accept state (4 digits); nothing is valid next
    }

    current_state = 'q0'
    accept_state = 'q4'
    transition_log = []

    for char in pin_string:
        char_type = get_input_type(char)

        # Any non-digit, or a 5th digit from q4, has no valid path -> Dead State
        if char_type not in transitions.get(current_state, {}):
            transition_log.append({
                'char': char,
                'from_state': current_state,
                'to_state': 'Dead State / Error',
                'status': 'REJECTED'
            })
            return False, transition_log

        next_state = transitions[current_state][char_type]

        # Record the step so the GUI can animate it later
        transition_log.append({
            'char': char,
            'from_state': current_state,
            'to_state': next_state,
            'status': 'PROCESSING'
        })

        current_state = next_state

    is_accepted = (current_state == accept_state)
    return is_accepted, transition_log


# --- TESTING BLOCK ---
if __name__ == "__main__":
    test_pins = ["1234", "123", "12345", "12a4"]

    for pin in test_pins:
        print(f"\nSimulating DFA for: {pin}")
        accepted, log = simulate_atm_pin_dfa(pin)

        for step in log:
            print(f"Read '{step['char']}' | {step['from_state']} ---> {step['to_state']}")

        print("-" * 33)
        if accepted:
            print("FINAL RESULT: PIN ACCEPTED (Final State Reached)")
        else:
            print("FINAL RESULT: PIN REJECTED")
        print("-" * 33)
