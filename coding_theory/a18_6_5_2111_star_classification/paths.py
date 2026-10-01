"""Contribution-specific generated state; never part of the source artifact."""
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent
WORK = Path(os.environ.get('CWC2111_WORK', str(BASE / '.work'))).resolve()
WORK.mkdir(parents=True, exist_ok=True)
