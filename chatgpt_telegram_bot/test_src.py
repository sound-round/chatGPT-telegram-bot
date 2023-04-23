from .tokenizer import tokenize


def test_tokenizer():
    tokens = tokenize("Some text")
    assert tokens
    assert tokens == 2

    tokens = tokenize("Thisisthelongwordwithagreatnumberofcharacters")
    assert tokens
    assert tokens == 6
