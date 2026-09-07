"""Reproduce the negative certificate without SAT, catalogs, or private files."""
from itertools import combinations
from pathlib import Path
import hashlib,json,sys,time
import verify,check_literal
HERE=Path(__file__).resolve().parent


def reproduce():
    start=time.monotonic();graph=json.loads((HERE/'graph.json').read_text());expected=json.loads((HERE/'CERTIFICATE.json').read_text())
    if verify.certify(graph)!=expected or check_literal.certify(graph)!=expected:raise ValueError('Independent certificate mismatch')
    # Decode the separately supplied graph6 record, using its standard column order.
    g6=(HERE/'graph.g6').read_text().strip()
    if ord(g6[0])-63!=19:raise ValueError('graph6 order')
    stream=''.join(format(ord(c)-63,'06b') for c in g6[1:])
    if len(stream)!=174 or stream[171:]!='000':raise ValueError('graph6 padding')
    edges={pair for bit,pair in zip(stream,((i,j) for j in range(1,19) for i in range(j))) if bit=='1'}
    physical=sum(int(pair in edges)<<k for k,pair in enumerate(combinations(range(19),2)))
    if physical!=int(graph['red_hex'],16):raise ValueError('Two graph encodings disagree')
    complement={'n':19,'red_hex':format(((1<<171)-1)^physical,'043x')}
    c=verify.certify(complement)
    if c!=check_literal.certify(complement) or len(c['red_fours'])!=12 or len(c['blue_fours'])!=24:raise ValueError('Complement check')
    positions={p:k for k,p in enumerate(combinations(range(19),2))}
    def changed(groups):
        bits=physical
        for q in groups:
            for pair in combinations(q,2):bits|=1<<positions[pair]
        return {'n':19,'red_hex':format(bits,'043x')}
    invalid=[changed([range(5)]),changed([range(4),range(4,8)]),{'n':18,'red_hex':graph['red_hex']},{'n':19,'red_hex':'f'*43},{**graph,'extra':0}]
    rejected=0
    for bad in invalid:
        for checker in (verify.certify,check_literal.certify):
            try:checker(bad)
            except ValueError:rejected+=1
            else:raise ValueError('Invalid certificate accepted')
    return {'status':'VERIFIED_NEGATIVE_GOOD19_PACKING_BRIDGE','vertices':19,'red_edges':86,'red_fours':24,'blue_fours':12,
            'monochromatic_fives':0,'literal_four_subsets':3876,'literal_five_subsets':11628,'four_pair_intersections':630,
            'negative_checker_calls':rejected,'graph6_transport':True,'complement_checked':True,
            'graph_sha256':hashlib.sha256((HERE/'graph.json').read_bytes()).hexdigest(),
            'certificate_sha256':hashlib.sha256((HERE/'CERTIFICATE.json').read_bytes()).hexdigest()}

if __name__=='__main__':
    result=reproduce()
    if result!=json.loads((HERE/'EXPECTED.json').read_text()):raise ValueError('Expected replay differs')
    print(json.dumps(result,indent=2,sort_keys=True))
