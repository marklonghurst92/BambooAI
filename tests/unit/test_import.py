"""Basic import tests for the bambooai package."""


def test_import():
    """Ensure core modules can be imported."""
    import bambooai
    from bambooai import models  # noqa: F401

    # The package should expose the BambooAI class at top-level
    assert hasattr(bambooai, "BambooAI")
