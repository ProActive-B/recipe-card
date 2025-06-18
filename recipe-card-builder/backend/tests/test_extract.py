from app.extract import parse_transcript


def test_parse_transcript():
    text = """Best Pancakes
Ingredients
flour
milk
Step
mix
cook"""
    data = parse_transcript(text)
    assert "flour" in data["ingredients"]
    assert "mix" in data["steps"]
