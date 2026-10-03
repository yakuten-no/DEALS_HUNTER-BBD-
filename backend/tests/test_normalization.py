"""Tests for app.normalization -- deterministic, no database needed."""

from app.normalization import (
    extract_brand,
    extract_color,
    extract_ram_and_storage_gb,
    normalize_name,
    parse_product_name,
)


def test_parse_product_name_matches_the_documented_example():
    """The exact example from the V0.2 brief."""
    result = parse_product_name("Nothing Phone 3a Pro 12GB 256GB Black")
    assert result.brand == "Nothing"
    assert result.ram_gb == 12
    assert result.storage_gb == 256
    assert result.color == "Black"
    assert result.normalized_name == "nothing phone 3a pro 12gb 256gb black"


def test_extract_brand_is_case_insensitive():
    assert extract_brand("SAMSUNG Galaxy S24 Ultra") == "Samsung"
    assert extract_brand("apple iphone 15") == "Apple"


def test_extract_brand_returns_none_when_unrecognized():
    assert extract_brand("Definitely Not A Real Brand X200") is None


def test_extract_ram_and_storage_with_two_numbers_smaller_is_ram():
    assert extract_ram_and_storage_gb("Phone 8GB 128GB") == (8, 128)
    # Order in the text shouldn't matter -- the smaller number is always
    # treated as RAM, per the documented heuristic.
    assert extract_ram_and_storage_gb("Phone 128GB 8GB") == (8, 128)


def test_extract_storage_with_single_number_is_ambiguous_treated_as_storage():
    ram, storage = extract_ram_and_storage_gb("Phone 256GB Black")
    assert ram is None
    assert storage == 256


def test_extract_ram_and_storage_returns_none_when_absent():
    assert extract_ram_and_storage_gb("Phone Black Edition") == (None, None)


def test_extract_ram_and_storage_does_not_guess_with_three_numbers():
    """Three GB-numbers is genuinely ambiguous -- return (None, None)
    rather than guessing which two are RAM/storage."""
    assert extract_ram_and_storage_gb("Phone 8GB 128GB 512GB variant") == (None, None)


def test_extract_color_finds_known_color():
    assert extract_color("Phone 128GB Midnight Black Edition") in ("Midnight", "Black")


def test_extract_color_returns_none_when_absent():
    assert extract_color("Phone 128GB 8GB") is None


def test_normalize_name_strips_punctuation_and_collapses_whitespace():
    assert normalize_name("Nothing Phone (3a) Pro!!  12GB/256GB") == "nothing phone 3a pro 12gb 256gb"


def test_normalize_name_is_deterministic():
    """Same input always produces the same output -- no randomness, no AI."""
    text = "Nothing Phone (3a) Pro 12GB 256GB Black"
    assert normalize_name(text) == normalize_name(text)


def test_parse_product_name_never_guesses_a_missing_field():
    result = parse_product_name("Some Unknown Device")
    assert result.brand is None
    assert result.ram_gb is None
    assert result.storage_gb is None
    assert result.color is None
    # normalized_name is always produced, even with nothing else recognized.
    assert result.normalized_name == "some unknown device"
