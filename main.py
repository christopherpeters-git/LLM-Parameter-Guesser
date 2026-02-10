import random
from llm_communication import get_normal_response_openai, sanitize_number_openai
from speech_to_text import record_audio, speech_to_text_google

# Prompts to guess the parameters for
PROMPTS = [
    "Write a short poem about time.",
    "Explain recursion in one paragraph.",
    "Give three creative uses for a brick.",
    "Describe a sunset in two sentences.",
    "Tell a short joke.",
    "Tell the favorite animal of Batman."
]

# Guessable parameters and their ranges
PARAM_RANGES = {
    "temperature": (0.0, 2.0),
    "top_p": (0.1, 1.0),
}

def random_param(low, high):
    return round(random.uniform(low, high), 2)

def generate_random_params():
    return {k: random_param(*v) for k, v in PARAM_RANGES.items()}

def sanitize_number(number_string):
    cleaned = sanitize_number_openai(number_string).strip()

    if cleaned.upper() == "ERROR":
        raise ValueError("No number detected")

    return float(cleaned)


def get_user_guess(mode):
    guess = {}

    for param in PARAM_RANGES:
        while True:
            try:
                print(f"\nGuess the models parameter '{param}'!:")
                if mode == "2":
                    wav = record_audio()
                    spoken = speech_to_text_google(wav)

                    if spoken is None:
                        print("Could not understand speech. Try again.")
                        continue

                    #print(f"Raw STT: {spoken}")
                    value = sanitize_number(spoken)
                    print(f"Sanitized value: {value}")

                else:
                    value = float(sanitize_number_openai(input()))

                guess[param] = value
                break

            except ValueError:
                print("Could not extract a valid number. Try again.")

    return guess


def evaluate_guess(actual, guess):
    errors = {}
    for k in actual:
        errors[k] = round(abs(actual[k] - guess[k]), 2)
    return errors

def play_round():
    print("Choose input mode:")
    print("1 = text")
    print("2 = voice")
    mode = input(">> ").strip()

    prompt = random.choice(PROMPTS)
    params = generate_random_params()

    print("\n==============================")
    print("New round.")
    print("==============================")
    print("\nPrompt:")
    print(f"> {prompt}\n")

    response = get_normal_response_openai(prompt,params["temperature"], params["top_p"])

    print("\n==============================")
    print("Model output:\n")
    print(response)
    print("==============================")

    guess = get_user_guess(mode)
    errors = evaluate_guess(params, guess)

    print("\n--- RESULTS ---")
    for k in params:
        print(f"{k}: actual={params[k]}, guessed={guess[k]}, error={errors[k]}")

    total_error = round(sum(errors.values()), 2)
    print(f"\nTotal error score: {total_error}")

def main():
    print("LLM Parameter Guessing Game")
    print("Press ENTER to play a round")
    print("Type 'q' or 'exit' to quit\n")

    while True:
        choice = input(">> ").strip().lower()
        if choice in ("q", "exit"):
            print("\nGoodbye")
            break

        play_round()

        print("\nPlay again? (ENTER = yes, q = quit)")

if __name__ == "__main__":
    main()
