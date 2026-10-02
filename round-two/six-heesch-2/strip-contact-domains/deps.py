"""Read only the adjacent already-published exact geometry modules."""
import os
from pathlib import Path
import sys

HERE=Path(__file__).absolute().parent
GEOMETRY=HERE.parent/'parametric-strip-obstruction'
if not (GEOMETRY/'strip_parametric_geometry.py').is_file():
    raise RuntimeError('The adjacent published parametric-strip-obstruction directory is required')
sys.path.insert(1,str(GEOMETRY))
OPS=Path(os.environ['DISCOVERY_RESEARCH_TEAM_ROOT']) if os.environ.get('DISCOVERY_RESEARCH_TEAM_ROOT') else None

def paused():
    return OPS is not None and any((OPS/n).exists() for n in ['PAUSED','PAUSED.json','HANDOVER.json'])
