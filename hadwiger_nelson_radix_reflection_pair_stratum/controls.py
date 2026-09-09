#!/usr/bin/env python3
"""Corruption controls for the exact algebra, modular lift, and physical data."""
from copy import deepcopy
from pathlib import Path
import json,tempfile
import geometry as G
import colour as C
import verify,physical
X=C.X;HERE=Path(__file__).resolve().parent

def rejected(name,call):
    try:call()
    except ValueError:return name
    raise ValueError('corrupt proof input accepted: '+name)

def run():
    cert=json.loads((HERE/'certificate.json').read_text());data=G.compile(cert['pair_rows']);bad=C.inventory();results=[]
    results.append(rejected('wrong colour on complete projected physical edge set',lambda:C.check(data['components'][0],{'prime':cert['prime'],'colour':0},bad)))
    p=cert['prime']
    results.append(rejected('degree-dropping modular parameter polynomial',lambda:C.check(([1,p],['0'],['0']),{'prime':p,'colour':0},bad)))
    # A reducible coefficient algebra must never silently invert a zero divisor.
    u=G.Q([0,1]);q=G.Q([0,-1,1])
    results.append(rejected('zero-divisor leading coefficient in fibre Euclid',lambda:G.monic_gcd([G.Q([1]),u],[G.Q([1]),u],q)))
    # A vanished resultant need not supply a root when source degrees drop.
    f=[G.Z([1]),G.Z([0,1])];g=[G.Z([-1]),G.Z([0,1])]
    X.need(G.resultant(f,g)==G.Z([0,-2]),'hand-checked leading-drop resultant')
    X.need(len(G.monic_gcd(f,g,G.Q([0,1])))==1,'extraneous resultant fibre correctly proved empty')
    with tempfile.TemporaryDirectory(prefix='hn-reflection-controls-') as temp:
        temp=Path(temp);wrong=deepcopy(cert);wrong['prime']=4;(temp/'composite.json').write_text(json.dumps(wrong))
        results.append(rejected('composite proof modulus',lambda:verify.run(temp/'composite.json')))
        wrong=deepcopy(cert);wrong['cover_sha256']='0'*64;(temp/'cover.json').write_text(json.dumps(wrong))
        results.append(rejected('incomplete algebraic cover transcript',lambda:verify.run(temp/'cover.json')))
        wrong=json.loads((HERE/'physical.json').read_text());wrong['vertices'][0][0]+=wrong['vertices'][0][-1];(temp/'coordinate.json').write_text(json.dumps(wrong))
        results.append(rejected('false physical vertex coordinate',lambda:physical.run(temp/'coordinate.json')))
        wrong=json.loads((HERE/'physical.json').read_text());wrong['embeddings'][0]['isolating_interval']=['10','11'];(temp/'embedding.json').write_text(json.dumps(wrong))
        results.append(rejected('nonexistent real embedding',lambda:physical.run(temp/'embedding.json')))
    return {'verified':True,'rejected':results,'extraneous_resultant_fibre_control':True,'uses_assert_for_correctness':False}

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
