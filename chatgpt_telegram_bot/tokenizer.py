TOKEN_K = 4
WORD_K = 0.75


def tokenize(text: str):
    char_count = len(text)
    word_count = len(text.split())

    tokens_by_chars = int(char_count / TOKEN_K)
    tokens_by_words = int(word_count / WORD_K)

    return int((tokens_by_chars + tokens_by_words) / 2)
