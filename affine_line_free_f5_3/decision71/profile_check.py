"""Check all field-label normalizations of the low parallel-class profiles."""
from itertools import product
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def check_profiles():
    profiles=[];raw_counts=[]
    for m in range(7,11):
        normalized=set();raw=0
        for tail in product(range(13,17),repeat=4):
            p=(m,)+tail
            if sum(p)!=71:
                continue
            raw+=1
            normalized.add(min(tuple(p[(pow(a,-1,5)*j)%5] for j in range(5))
                               for a in range(1,5)))
        profiles.extend(sorted(normalized));raw_counts.append(raw)
    pairs=[(i,j) for i in range(5) for j in range(i,10) if j<5 or i==0]
    data=json.loads((HERE/'profiles.json').read_text())
    if profiles!=list(map(tuple,data['profiles'])) or pairs!=list(map(tuple,data['pairs'])):
        raise RuntimeError("profile or pair normalizations disagree")
    if raw_counts!=[1,4,10,20] or len(profiles)!=10 or len(pairs)!=20:
        raise RuntimeError("incomplete low-profile cover")
    header='#pragma once\n#include <array>\nconstexpr int N=71;\n'
    header+='constexpr std::array<std::array<int,5>,10> PROFILES{{'+','.join('{{'+','.join(map(str,x))+'}}' for x in profiles)+'}};\n'
    header+='constexpr std::array<std::array<int,2>,20> PAIRS{{'+','.join('{{'+','.join(map(str,x))+'}}' for x in pairs)+'}};\n'
    if ''.join(header.split())!=''.join((HERE/'profiles.hpp').read_text().split()):
        raise RuntimeError("C++ profile table differs from the exact normalization")
    return {'raw_profile_counts_by_minimum':raw_counts,'normalized_profiles':10,'pair_types':20}
