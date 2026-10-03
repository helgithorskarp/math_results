"""Lossless eight-core partition of a whole primary32-core transcript."""
import hashlib
import json
from pathlib import Path
from primary import domains
from model import require

def split_stream(which, first, last, stream, directory):
    cores=domains()[-1]
    a,b,cap=(11,11,11) if which=="balanced" else (10,12,12)
    domain=[c for c in cores if len(c[2])>=b-(5*cap//a)
            and b-len(c[2])+sum(w for w,q in c[3][:a-5])<=cap]
    index={(c[0],c[2]):i for i,c in enumerate(domain)}
    ranges=[(i,min(i+8,last)) for i in range(first,last,8)]
    paths=[directory/f"{which}-{i:04d}-check.jsonl" for i,j in ranges]
    require(all(not p.exists() for p in paths),"fresh partition files")
    handles=[p.open("w") for p in paths]
    try:
        with stream.open() as source:
            for line in source:
                x=json.loads(line)
                require(isinstance(x,list) and len(x)==6,"partition schema")
                key=(tuple(x[0]),tuple(x[1]))
                require(key in index and first<=index[key]<last,"partition core range")
                handles[(index[key]-first)//8].write(line)
    finally:
        for f in handles:f.close()
    h=hashlib.sha256()
    for p in paths:h.update(p.read_bytes())
    require(h.hexdigest()==hashlib.sha256(stream.read_bytes()).hexdigest(),
            "whole partition concatenation")
    return [(i,j,p) for (i,j),p in zip(ranges,paths)]
