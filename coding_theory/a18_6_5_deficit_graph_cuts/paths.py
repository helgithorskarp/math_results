from pathlib import Path
import os
BASE = Path(__file__).resolve().parent
WORK = Path(os.environ.get("CWC_DEFICIT_WORK", str(BASE / ".work")))
WORK.mkdir(parents=True, exist_ok=True)
