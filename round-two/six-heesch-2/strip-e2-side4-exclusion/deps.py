"""Prior published exact geometry; no numerical Heesch-value premise."""
from pathlib import Path
import sys
H=Path(__file__).absolute().parent
OPS=Path('/scratch/research-team-sol61-six-20260929/state')
for n in ['parametric-strip-obstruction','strip-contact-domains']:
    sys.path.append(str(H.parent/n))
def paused():
    return any((OPS/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER.json'))
