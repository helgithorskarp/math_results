"""Optional bounded discovery replay. Raw state remains in out/."""
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
for args in [
    ['compose.py'],
    ['reduce.py','inequality_union','equal'],
    ['g40_kernel.py'],
    ['outer.py'],
    ['reduce.py','equality_union','different','1193'],
    ['freeze.py'],
    ['mandatory.py'],
    ['export.py'],
]:
    subprocess.run([sys.executable,str(ROOT/args[0]),*args[1:]],cwd=ROOT,check=True)
