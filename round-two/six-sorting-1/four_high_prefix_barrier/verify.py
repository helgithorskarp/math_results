#!/usr/bin/env python3
"""Scalar original-domain checker; imports no producer/profiler/solver."""
from copy import deepcopy
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT=Path(__file__).resolve().parent
METRICS={"original_free_assignments":0,"scalar_gate_evaluations":0,"full_boolean_controls":0}
FAMILIES=[("one_minimum",1,0),("one_maximum",0,1),("two_minima",2,0),
          ("two_maxima",0,2),("mixed_pair",1,1),("four_maxima",0,4)]


def need(test,message):
    if not test:raise ValueError(message)


def sha(value):
    return hashlib.sha256(json.dumps(value,separators=(",",":")).encode()).hexdigest()


def mask(xs):
    return sum(1<<i for i in xs)


def marked(value):
    return value<0 or value>1


def ports(values):
    return mask(i for i,v in enumerate(values) if v<0),mask(i for i,v in enumerate(values) if v>1)


def summary(records):
    env={}
    for _,_,lo,hi,d,r,_ in records:
        old=env.get((lo,hi),(0,0));env[lo,hi]=(max(old[0],d),max(old[1],d+r))
    envelope=[[lo,hi,d,c] for (lo,hi),(d,c) in sorted(env.items())]
    info={"ordinary_mass":sum(1<<r[2] for r in envelope),"semantic_mass":sum(1<<r[3] for r in envelope),
          "maximum_deletions":max(r[4] for r in records),"maximum_semantic_deletions":max(r[4]+r[5] for r in records),
          "maximum_redundancies":max(r[5] for r in records),"port_classes":len(envelope)}
    return info,envelope


def scalar_family(gates,lo_count,hi_count,with_trace=False):
    histories=[[] for _ in range(len(gates)+1)] if with_trace else None
    records=[]
    for lows in combinations(range(13),lo_count):
        for highs in combinations([i for i in range(13) if i not in lows],hi_count):
            free=[i for i in range(13) if i not in lows and i not in highs]
            template=[0]*13
            for j,i in enumerate(lows):template[i]=j-len(lows)
            for j,i in enumerate(highs):template[i]=2+j
            reference=list(template);touched=0;reference_ports=[ports(reference)]
            for index,(a,b) in enumerate(gates):
                if marked(reference[a]) or marked(reference[b]):touched|=1<<index
                if reference[a]>reference[b]:reference[a],reference[b]=reference[b],reference[a]
                reference_ports.append(ports(reference))
            active=0
            for assignment in range(1<<len(free)):
                values=list(template)
                for j,i in enumerate(free):values[i]=(assignment>>j)&1
                for index,(a,b) in enumerate(gates):
                    hit=marked(values[a]) or marked(values[b])
                    need(hit==bool((touched>>index)&1),"marker trajectory depends on free assignment")
                    if values[a]>values[b]:
                        if not hit:active|=1<<index
                        values[a],values[b]=values[b],values[a]
                need(ports(values)==reference_ports[-1],"final marked ports differ")
                METRICS["original_free_assignments"]+=1
                METRICS["scalar_gate_evaluations"]+=len(gates)
            cuts=range(len(gates)+1) if with_trace else [len(gates)]
            last=None
            for cut in cuts:
                allowed=(1<<cut)-1
                d=(touched&allowed).bit_count();redundant=allowed&~touched&~active
                lp,hp=reference_ports[cut]
                row=[mask(lows),mask(highs),lp,hp,d,redundant.bit_count(),redundant]
                if with_trace:histories[cut].append(row)
                last=row
            records.append(last)
    records.sort();info,envelope=summary(records)
    result={"low_count":lo_count,"high_count":hi_count,"records":records,"envelope":envelope,"summary":info}
    trace=None
    if with_trace:
        trace=[]
        for rows in histories:
            rows.sort();info,_=summary(rows)
            trace.append({k:info[k] for k in ("ordinary_mass","semantic_mass","port_classes")})
        need(all(a["semantic_mass"]<=b["semantic_mass"] for a,b in zip(trace,trace[1:])),"semantic potential decreased")
    return result,trace


def original_anchors(data):
    answer={}
    for side,unary,paired in [("low","one_minimum","two_minima"),("high","one_maximum","two_maxima")]:
        column=0 if side=="low" else 1;units=0
        for entry in data[unary]["envelope"]:
            port=entry[column];value=16*(1<<entry[3])
            for name in (paired,"mixed_pair"):
                mass=sum(1<<r[3] for r in data[name]["envelope"] if r[column]&port)
                value=max(value,1<<(mass-1).bit_length())
            units+=value
        answer[side]=units
    return answer


def execute(values,gates):
    values=list(values)
    for a,b in gates:
        if values[a]>values[b]:values[a],values[b]=values[b],values[a]
    return values


def main():
    start=time.monotonic();fixture=json.loads((ROOT/"fixture.json").read_text())
    prefix=fixture["prefix38"];need(len(prefix)==38,"wrong prefix size")
    control=fixture["control45"];need(len(control)==45,"wrong positive control size")
    for word in (prefix,control):need(all(0<=a<b<13 for a,b in word),"invalid comparator")
    data={};four_trace=None
    for name,lo,hi in FAMILIES:
        data[name],trace=scalar_family(prefix,lo,hi,name=="four_maxima")
        if trace is not None:four_trace=trace
    positive,_=scalar_family(control,0,4)
    for x in range(8192):
        values=[(x>>i)&1 for i in range(13)]
        need(execute(values,control)==sorted(values),"known45 positive control fails")
        METRICS["full_boolean_controls"]+=1
    expected={"schema":"four-high-prefix38-v1","agent":"six-sorting-1","role":"researcher",
              "prefix_sha256":sha(prefix),"prefix_size":38,"families":data,
              "original_anchor_units":original_anchors(data),"four_high_trace":four_trace,
              "control45_four_high":positive}
    raw=(ROOT/"certificate.json").read_bytes();certificate=json.loads(raw)
    need(expected==certificate,"entry-level independent certificate reconstruction differs")
    need(max(expected["original_anchor_units"].values())<=512,"old anchor comparison fails")
    need(data["four_maxima"]["summary"]["semantic_mass"]==589824,"four-high obstruction differs")
    need(four_trace[37]["semantic_mass"]<=1<<19,"crossing already occurs before gate38")
    need(positive["summary"]["semantic_mass"]<=1<<20,"actual45 control exceeds its ceiling")
    damaged=[]
    bad=deepcopy(certificate);bad["families"]["four_maxima"]["records"].pop();damaged.append(bad)
    bad=deepcopy(certificate);bad["families"]["four_maxima"]["records"][0][4]+=1;damaged.append(bad)
    bad=deepcopy(certificate);bad["four_high_trace"][38]["semantic_mass"]-=1;damaged.append(bad)
    need(all(bad!=expected for bad in damaged),"damaged certificate accepted")
    print(json.dumps({"status":"ALL_FOUR_HIGH_PREFIX_CHECKS_PASSED","agent":"six-sorting-1","role":"researcher",
                      "certificate_sha256":hashlib.sha256(raw).hexdigest(),"four_high_mass":589824,
                      "ordinary_four_high_mass":data["four_maxima"]["summary"]["ordinary_mass"],
                      "anchor_units":expected["original_anchor_units"],"corruptions_rejected":len(damaged),
                      "seconds":time.monotonic()-start,"maximum_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      **METRICS},sort_keys=True),flush=True)


if __name__=="__main__":main()
