"""
Happy Curiosity Hurricane AI - Core Implementation

This file re-exports from the installable package for backwards compatibility.
The canonical source is src/biogrid/hgai.py.

    pip install -e .
    from biogrid.hgai import ResonantHurricaneAI
"""
from src.biogrid.hgai import *  # noqa: F401,F403
from src.biogrid.hgai import __all__  # noqa: F401
