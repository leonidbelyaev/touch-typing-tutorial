MODES: set[str] = {"course", "random", "words", "texts"}

MODE_NAMES: dict[str, str] = {
    "course": "Basic Course",
    "random": "Random Typing",
    "words": "Words Typing",
    "texts": "Real Texts",
}

# Include all languages and layouts here
INDEX: dict[str, list[str]] = {
    "languages": ["en-US"],
    "layouts": ["qwerty"],
}
