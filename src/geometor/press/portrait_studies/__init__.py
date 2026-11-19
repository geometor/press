"""Individual geometric portrait medallion studies for :mod:`geometor.press`."""

from __future__ import annotations

from .aristotle import build_aristotle_elements
from .durer import build_durer_elements
from .euclid import build_euclid_elements
from .euler import build_euler_elements
from .kepler import build_kepler_elements
from .pacioli import build_pacioli_elements
from .plato import build_plato_elements

__all__ = [
    "build_aristotle_elements",
    "build_durer_elements",
    "build_euclid_elements",
    "build_euler_elements",
    "build_kepler_elements",
    "build_pacioli_elements",
    "build_plato_elements",
]
