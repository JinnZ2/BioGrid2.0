"""Allow running sensors as: python -m biogrid.sensors --prompt '...' """
from .analyze_cli import main

raise SystemExit(main())
