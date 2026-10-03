"""
Deterministic product-name normalization.

Turns a raw product title (as seen on a retailer page) into structured
components -- brand, RAM, storage, color -- and a comparable normalized
string. Pure pattern matching: no AI, no fuzzy/semantic matching, no
external API or dictionary lookup. This is a foundation and extension
point for future product matching (project-memory/ARCHITECTURE.md, OQ-3),
not a finished matcher -- it never guesses a field it found no evidence
for, and two genuinely-equivalent names written very differently (e.g.
different word order, abbreviations) may still normalize to different
strings. That's a known, accepted limitation for V0.2, not a bug.
"""

import re
from dataclasses import dataclass

# A short, deliberately incomplete list of brands sold in India, used only
# to anchor parsing. Extend as real listings reveal gaps -- this is not
# meant to be exhaustive, and an unrecognized brand simply returns None
# rather than a wrong guess.
KNOWN_BRANDS: tuple[str, ...] = (
    "Nothing", "Samsung", "Apple", "OnePlus", "Xiaomi", "Redmi", "Poco",
    "Realme", "Vivo", "Oppo", "Motorola", "Google", "iQOO", "Asus", "Nokia",
)

# Deliberately ordered longest-first so "midnight" doesn't get shadowed by
# a hypothetical shorter substring match, and so multi-word shades aren't
# needed for V0.2's scope.
KNOWN_COLORS: tuple[str, ...] = (
    "midnight", "starlight", "graphite", "titanium",
    "black", "white", "blue", "green", "red", "grey", "gray", "silver",
    "gold", "purple", "yellow", "pink", "orange",
)

_STORAGE_OR_RAM_RE = re.compile(r"(\d+)\s*GB\b", re.IGNORECASE)


def extract_brand(text: str) -> str | None:
    """Return the first known brand found in `text`, or None if none matched."""
    lowered = text.lower()
    for brand in KNOWN_BRANDS:
        if brand.lower() in lowered:
            return brand
    return None


def extract_ram_and_storage_gb(text: str) -> tuple[int | None, int | None]:
    """Parse patterns like '12GB 256GB' or '12/256GB' into (ram_gb, storage_gb).

    Heuristic, not a guarantee: when exactly two "NGB" numbers are found,
    the smaller is assumed to be RAM and the larger storage, since that
    ordering holds for essentially every phone sold today (storage always
    exceeds RAM). A single "NGB" number is ambiguous -- it's returned as
    storage only, since that's what's most often advertised alone (e.g.
    "256GB Black" with RAM omitted from the title). Three or more numbers
    aren't resolved at all (returns None, None) rather than guessing which
    two matter.
    """
    matches = [int(m.group(1)) for m in _STORAGE_OR_RAM_RE.finditer(text)]
    if len(matches) == 1:
        return None, matches[0]
    if len(matches) == 2:
        matches.sort()
        return matches[0], matches[1]
    return None, None


def extract_color(text: str) -> str | None:
    """Return the first known color word found in `text`, or None."""
    lowered = text.lower()
    for color in KNOWN_COLORS:
        if color in lowered:
            return color.capitalize()
    return None


def normalize_name(text: str) -> str:
    """A deterministic, comparable form of a name: lowercased, punctuation
    stripped, whitespace collapsed. This is a syntactic normalization, not
    a semantic one -- see the module docstring for what that does and
    doesn't guarantee."""
    cleaned = re.sub(r"[^\w\s]", " ", text.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


@dataclass(frozen=True)
class ParsedProductName:
    """Result of parse_product_name(). Every field except raw_text and
    normalized_name can be None -- that means "not found", never "empty"."""

    raw_text: str
    brand: str | None
    ram_gb: int | None
    storage_gb: int | None
    color: str | None
    normalized_name: str


def parse_product_name(text: str) -> ParsedProductName:
    """Best-effort, fully deterministic parse of a retailer-style product
    title into structured components."""
    ram_gb, storage_gb = extract_ram_and_storage_gb(text)
    return ParsedProductName(
        raw_text=text,
        brand=extract_brand(text),
        ram_gb=ram_gb,
        storage_gb=storage_gb,
        color=extract_color(text),
        normalized_name=normalize_name(text),
    )
