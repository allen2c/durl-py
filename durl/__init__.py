from pathlib import Path

from .core import DURL

__version__ = Path(__file__).parent.joinpath("VERSION").read_text().strip()

__all__ = ["DURL", "__version__"]
