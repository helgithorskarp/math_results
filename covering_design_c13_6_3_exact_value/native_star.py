"""Small ctypes boundary for the exact native star solver."""
import ctypes
from itertools import combinations
from pathlib import Path

class Result(ctypes.Structure):
    _fields_=[('status',ctypes.c_int),('witness_size',ctypes.c_int),
              ('point_states',ctypes.c_uint64),('bundle_states',ctypes.c_uint64),
              ('witness',ctypes.c_uint16*21)]

LIB=ctypes.CDLL(str(Path(__file__).with_name('star_audit.so')))
LIB.cover_solve.argtypes=[ctypes.c_int]*6+[ctypes.POINTER(ctypes.c_uint16),ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int),ctypes.POINTER(Result)]
LIB.cover_solve.restype=ctypes.c_int
PAIR_MASKS=tuple(sum(1<<x for x in t) for t in combinations(range(13),2))

class Space:
    def __init__(self,p,r):self.p=p;self.r=r

def solve(space,fixed,h,q,total_blocks=20,target_degrees=None,pair_bounds=None):
    if any(type(b) is not int or not 0<=b<8192 for b in fixed):raise ValueError('block mask outside thirteen points')
    if target_degrees is None:target_degrees=[11 if p==h else 10 if p==q else 9 for p in range(13)]
    if pair_bounds is None:pair_bounds={t:(20 if t==((1<<h)|(1<<q)) else 5) for t in PAIR_MASKS}
    f=(ctypes.c_uint16*len(fixed))(*fixed);d=(ctypes.c_int*13)(*target_degrees)
    bounds=(ctypes.c_int*78)(*(pair_bounds[t] for t in PAIR_MASKS));result=Result()
    status=LIB.cover_solve(space.p,space.r,total_blocks,h,q,len(fixed),f,d,bounds,ctypes.byref(result))
    if status or result.status not in (0,1):raise RuntimeError('native search rejected input, allocation, or counter overflow')
    answer=dict(status='SAT' if result.status else 'UNSAT',point_states=int(result.point_states),bundle_states=int(result.bundle_states))
    if result.status:answer['witness']=list(result.witness[:result.witness_size])
    return answer
