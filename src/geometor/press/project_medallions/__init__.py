"""Bespoke compass-and-straightedge project and catalog medallions for :mod:`geometor.press`."""

from __future__ import annotations

from .codes import build_codes_elements
from .constructions import build_constructions_elements
from .divine import build_divine_elements
from .elementarium import build_elementarium_elements
from .elements import build_elements_elements
from .explorer import build_explorer_elements
from .fundamentals import build_fundamentals_elements
from .geometor import build_geometor_elements
from .gibert import build_gibert_elements
from .heptadecagon import build_heptadecagon_elements
from .knott import build_knott_elements
from .levels import build_levels_elements
from .model import build_model_elements
from .phyllotaxis import build_phyllotaxis_elements
from .polyhedra import build_polyhedra_elements
from .posamentier import build_posamentier_elements
from .press import build_press_elements
from .seer import build_seer_elements
from .seer_navigator import build_seer_navigator_elements
from .seer_sessions import build_seer_sessions_elements
from .trees import build_trees_elements

__all__ = [
    "build_codes_elements",
    "build_constructions_elements",
    "build_divine_elements",
    "build_elementarium_elements",
    "build_elements_elements",
    "build_explorer_elements",
    "build_fundamentals_elements",
    "build_geometor_elements",
    "build_gibert_elements",
    "build_heptadecagon_elements",
    "build_knott_elements",
    "build_levels_elements",
    "build_model_elements",
    "build_phyllotaxis_elements",
    "build_polyhedra_elements",
    "build_posamentier_elements",
    "build_press_elements",
    "build_seer_elements",
    "build_seer_navigator_elements",
    "build_seer_sessions_elements",
    "build_trees_elements",
]
