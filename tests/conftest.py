from pathlib import Path

import pytest

repo_root = Path(__file__).parent.parent

@pytest.fixture
def mandelbrot_area(monkeypatch):
    monkeypatch.syspath_prepend(repo_root / "src")
    from mandelbrot_area import mandelbrot_area
    return mandelbrot_area