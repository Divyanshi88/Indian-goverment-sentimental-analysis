from src.preprocessing.text_cleaner import clean_text


def test_clean_text_removes_noise():
    text = "Great policy update!!! Visit https://example.com <b>Now</b> 2026"

    cleaned = clean_text(text, lemmatize=False)

    assert "https" not in cleaned
    assert "2026" not in cleaned
    assert "great" in cleaned
    assert "policy" in cleaned
