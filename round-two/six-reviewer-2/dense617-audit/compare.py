"""Post-seal whole-entry native correspondence; not primary proof input."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from model import bits, canon, graph, increasing, require
from primary import domains

ROOT=Path(__file__).resolve().parent

def native(directory):
    pins=json.loads((ROOT/"NATIVE_INPUTS.json").read_text())["files"]
    for name,pin in pins.items():
        raw=(directory/name).read_bytes()
        require(len(raw)==pin["bytes"] and hashlib.sha256(raw).hexdigest()==pin["sha256"],
                "whole pinned native source "+name)
    spec=importlib.util.spec_from_file_location("dense617_late_native",directory/"generate.py")
    n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
    return n

def parents(n,lattice,cores):
    S,T,rows,columns,supports=graph()
    levels,_=increasing(rows)
    own=[]
    for b in {b for level in levels for a,b in level}:
        a=[S[q] for q,r in enumerate(rows) if b&r==b]
        own.append({"A":a,"B":[T[j] for j in bits(b)]})
    own.sort(key=lambda x:x["B"])
    require(lattice["records"]==own,"every11092 full literal state/closure")
    ownf=[{"A0":[S[q]for q in a],"C":[T[j]for j in bits(c)]}
          for a,c in levels[5]]
    ownf.sort(key=lambda x:x["A0"])
    require(cores["five_records"]==ownf,"every1685 literal five-core")
    raw=domains()[-1]
    chosen=[c for c in raw if 11-len(c[2])+sum(w for w,q in c[3][:6])<=11]
    ownb=[{"A0":[S[q]for q in a],"B0":[T[j]for j in b],
           "C":[T[j]for j in bits(C)],
           "lower_missing":11-len(b)+sum(w for w,q in costs[:6])}
          for a,C,b,costs in chosen]
    require(cores["balanced_records"]==ownb,"all515 labeled survivor cores")
    sq,ns,ends,D,neighbors=n.graph()
    require(tuple(sq)==S and tuple(ns)==T,"native field labels")
    require(ends==[{"step":d,"support":list(x)}for d,x in supports],"six whole supports")
    require(all(neighbors[s]=={T[j]for j in bits(rows[i])}
                for i,s in enumerate(S)),"entire308x308 adjacency")
    expected=json.loads((ROOT/"EXPECTED.json").read_text())["cores"]
    for case,key in zip(cores["part_cases"],("original10x12","original11x11")):
        require(case["core_cases"]==expected[key]["count"] and
                case["lower_missing_histogram"]==expected[key]["lower_histogram"],
                "whole initial core histogram")
    return dict(full_states=11092,full_fives=1685,full_survivors=515,
                full_adjacencies=308*308,all_literal_parent_entries_equal=True)

class Capture:
    def __init__(self,buffer):
        self.buffer=buffer;self.real=hashlib.sha256()
    def update(self,data):
        self.real.update(data)
        raw=data.removesuffix(b"\\n").removesuffix(b"\n")
        self.buffer.append(json.loads(raw))
    def hexdigest(self):return self.real.hexdigest()

def extension(n,cores,start,stop,stream,native_record):
    S,T,rows,columns,supports=graph()
    expected=json.loads((ROOT/"EXPECTED.json").read_text())["balanced"]
    pin=next(x for x in expected if x["range"]==[start,stop])
    require(hashlib.sha256(stream.read_bytes()).hexdigest()==pin["stream_sha256"],
            "whole sealed independent stream")
    captured=[]
    class Proxy:
        @staticmethod
        def sha256(*args):
            if args:return hashlib.sha256(*args)
            buf=[];captured.append(buf);return Capture(buf)
    real=n.hashlib
    try:
        n.hashlib=Proxy
        data=n.extend(cores,start,stop)
    finally:n.hashlib=real
    require(data==native_record,"whole independently regenerated native certificate")
    require(len(captured)==stop-start,"one native transcript per complete core")
    expected_records={}
    with stream.open()as f:
        for line in f:
            A0,B0,rest,g,best,missing=json.loads(line)
            key=(tuple(S[q]for q in A0),tuple(T[j]for j in B0))
            expected_records.setdefault(key,[]).append(
                [[S[q]for q in rest],g,[[w,T[j]]for w,j in best],missing])
    compared=0
    for number,record,full in zip(range(start,stop),data["records"],captured):
        core=cores["balanced_records"][number]
        key=(tuple(core["A0"]),tuple(core["B0"]))
        require(expected_records.pop(key)==full,"every complete native row/cost/best/missing entry")
        h=hashlib.sha256()
        for x in full:
            h.update(json.dumps(x,sort_keys=True,separators=(",",":")).encode()+b"\n")
        require(h.hexdigest()==record["extension_transcript_sha256"],"whole native literal-delimiter transcript")
        mask=sum(1<<T.index(t)for t in core["B0"])
        independent={str(k):[S[q]for q,r in enumerate(rows)
                            if S[q]not in core["A0"] and (mask&~r).bit_count()==k]
                     for k in range(3)}
        require(record["groups"]==independent,"every native cost group")
        compared+=len(full)
    require(not expected_records and compared==pin["count"],"entire batch coverage")
    return dict(range=[start,stop],full_row_entries=compared,
                every_row_cost_best_column_and_missing_equal=True,
                all_native_transcript_and_group_fields_equal=True,
                native_delimiter="one real newline byte, independently checked from pinned source AST")

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--native-source",type=Path,required=True)
    ap.add_argument("--lattice",type=Path,required=True)
    ap.add_argument("--cores",type=Path,required=True)
    ap.add_argument("--start",type=int)
    ap.add_argument("--stop",type=int)
    ap.add_argument("--stream",type=Path)
    ap.add_argument("--native-record",type=Path)
    x=ap.parse_args();n=native(x.native_source)
    lattice=json.loads(x.lattice.read_text());cores=json.loads(x.cores.read_text())
    if x.start is None:
        result=parents(n,lattice,cores)
    else:
        require(x.stop is not None and x.stream is not None and x.native_record is not None,"extension args")
        result=extension(n,cores,x.start,x.stop,x.stream,json.loads(x.native_record.read_text()))
    print(canon(result),end="")
