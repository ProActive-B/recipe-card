from app.tasks import translate_text


def test_translate_text():
    result = translate_text("Hello world", "en", "de")
    assert isinstance(result, str)
    assert len(result) > 0
