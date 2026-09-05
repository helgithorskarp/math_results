#!/usr/bin/env python3
"""Append all forty four-bit fixed-signature units, preserving the entire base."""
import shutil
from classify import ROOT,info,require

BASE_PIN='f3a99ee8b211cfcf134f26670ada6fcdce9dc765b92dce3812a5bfdb16f971eb'


def make(base,output,case):
    require(info(base)['sha256']==BASE_PIN,'full core194 pin')
    with base.open('rb') as f,output.open('wb') as g:
        require(f.readline()==b'p cnf 34320 616138\n','base header')
        g.write(b'p cnf 34320 616178\n');shutil.copyfileobj(f,g)
        for f,prefix in enumerate(case['prefixes']):
            for i,b in enumerate(prefix):
                v=211+11*f+i;g.write(f'{v if b else -v} 0\n'.encode())
    return info(output)
