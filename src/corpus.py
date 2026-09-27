PEP_NUMBERS = [
    8, 20, 257, 484, 526, 557, 563, 585, 589, 590,
    634, 635, 636, 647, 673, 695, 702, 709, 742, 8,
    498, 505, 518, 519, 525, 529, 530, 544, 567, 570,
    572, 573, 574, 579, 589, 591, 593, 600, 612, 613,
]
PEP_NUMBERS = sorted(set(PEP_NUMBERS))


def pep_url(number: int) -> str:
    return f"https://peps.python.org/pep-{number:04d}/"


def pep_title(number: int) -> str:
    known = {
        8: "Style Guide for Python Code",
        20: "The Zen of Python",
        257: "Docstring Conventions",
        484: "Type Hints",
        526: "Syntax for Variable Annotations",
        557: "Data Classes",
        563: "Postponed Evaluation of Annotations",
        585: "Type Hinting Generics In Standard Collections",
        589: "TypedDict",
        590: "PEP 590 — Vectorcall",
        634: "Structural Pattern Matching: Specification",
        635: "Structural Pattern Matching: Motivation and Rationale",
        636: "Structural Pattern Matching: Tutorial",
        647: "User-Defined Type Guards",
        673: "Self Type",
        695: "Type Parameter Syntax",
        702: "Deprecation Warnings as Errors",
        709: "Comprehensions in Python",
        742: "Narrowing Types with TypeIs",
    }
    return known.get(number, f"Python Enhancement Proposal {number}")
