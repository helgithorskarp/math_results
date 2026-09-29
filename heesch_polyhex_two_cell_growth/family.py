"""The complete free two-cell growth family of a fixed 16-hex."""
from geometry import halo,orientations,holes,normalize
SEED = ((-4,4),(-3,3),(-3,4),(-2,1),(-2,2),(-1,1),(-1,2),(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(1,3),(2,0),(2,2))
def family():
    shapes={min(orientations(SEED))}
    for _ in range(2):
        shapes={min(orientations(tuple(sorted(set(t)|{p})))) for t in shapes for p in halo(t)}
    return sorted(t for t in shapes if not holes(t))
