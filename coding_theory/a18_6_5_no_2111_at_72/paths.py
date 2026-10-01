import os
from pathlib import Path
BASE = Path(__file__).resolve().parent
WORK = Path(os.environ.get("CWC2111_PAIR_WORK", str(BASE / ".work"))).resolve()
