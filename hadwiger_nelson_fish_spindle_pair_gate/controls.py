"""Corruption controls check mathematical conditions, not only hashes."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import json
from model import fish,build
from verify import relations
HERE=Path(__file__).resolve().parent

def reject(call):
    try:call()
    except ValueError:return
    raise RuntimeError('corrupted input accepted')

def run():
    original=json.loads((HERE/'geometry_certificate.json').read_text())
    with TemporaryDirectory() as t:
        p=Path(t)/'bad.json'
        for change in range(4):
            c=deepcopy(original)
            if change==0:c['inverse_numerators']=[[0]*38 for _ in range(38)]
            if change==1:c['midpoint_numerators'][3][0]+=c['midpoint_denominator']
            if change==2:c['edges'].pop()
            if change==3:c['radius_denominator']=1
            p.write_text(json.dumps(c));reject(lambda:fish(p))
    graph,summary=build(HERE/'geometry_certificate.json')
    cert=json.loads((HERE/'relation_certificate.json').read_text())
    for change in range(4):
        c=deepcopy(cert)
        if change==0:c['words']=['0'*len(graph['classes'])]
        if change==1:c['words']=c['words'][:1]
        if change==2:c['words'][0]='4'+c['words'][0][1:]
        if change==3:c['forced']=[{'pair':[0,1],'impossible':'same'}]
        reject(lambda:relations(graph,summary,c))
    return {'mathematical_corruptions_rejected':8,'hash_rejection_used':False}
if __name__=='__main__':print(json.dumps(run()))
