"""Standard-library check of the exact physical graph and its literal 4-word.
No producer or solver import. Sparse square-free-radical arithmetic.
"""
from pathlib import Path
from hashlib import sha256
from itertools import combinations
from math import gcd
import copy,json
HERE=Path(__file__).resolve().parent
RAD=(1,3,5,15,11,33,55,165)
D=(102,109,293,296,299,302,305,308,569,578)
ADDED=(399,576)
def need(ok,reason):
    if not ok:raise ValueError(reason)
def points(raw):
    rows=[tuple(map(int,line.split(','))) for line in raw.decode('ascii').splitlines()]
    need(all(len(r)==16 for r in rows),'coordinate dimensions')
    return [({r:x for r,x in zip(RAD,row[:8]) if x},{r:x for r,x in zip(RAD,row[8:]) if x}) for row in rows],rows

def sqdist(p,q):
    answer={r:0 for r in RAD}
    for a,b in zip(p,q):
        delta=[(r,a.get(r,0)-b.get(r,0)) for r in sorted(a.keys()|b.keys()) if a.get(r,0)!=b.get(r,0)]
        for r,c in delta:answer[1]+=r*c*c
        for (r,c),(s,d) in combinations(delta,2):
            g=gcd(r,s);answer[r*s//(g*g)]+=2*c*d*g
    return tuple(answer[r] for r in RAD)

def graph(P):
    return [(u,v) for u,v in combinations(range(len(P)),2) if sqdist(P[u],P[v])==(9216,0,0,0,0,0,0,0)]

def verify_certificate(c,P,E,labels,newcontacts,point_hash,edge_hash):
    need(c['labels']==labels,'physical label map')
    need(c['removed']==list(D) and c['added']==list(ADDED),'literal exchange')
    need(c['vertices']==508 and c['unit_edges']==len(E)==2506,'graph order and size')
    need(c['complete_pair_count']==128778,'pair coverage')
    need(c['new_old_contacts']==newcontacts,'all old-new contacts')
    need(c['point_sha256']==point_hash and c['edge_sha256']==edge_hash,'graph bytes')
    need(c['status']=='SAT_FOUR' and c['colour_queries']==1 and c['record_certified'] is False,'claim status')
    word=c['four_word'];need(len(word)==508 and set(word)<=set('0123'),'word domain')
    need(all(word[u]!=word[v] for u,v in E),'proper four-colouring')
    witness=c['moser_witness'];need(len(witness)==len(set(witness))==7 and all(type(x)is int and 0<=x<508 for x in witness),'Moser labels')
    o,t,a,b,s,d,e=witness
    required=[(o,a),(o,b),(t,a),(t,b),(a,b),(o,d),(o,e),(s,d),(s,e),(d,e),(t,s)]
    edgeset=set(E);need(all(tuple(sorted(edge)) in edgeset for edge in required),'Moser unit edges')
    # In any three-colouring each K4-minus-edge diamond forces o=t and o=s;
    # the checked t-s edge contradicts equality. Thus chi>=4, independently of SAT.
    need(c['chromatic_number']==4,'exact chromatic number')
    for v in ADDED:need(len(newcontacts[str(v)])>=3,'private point old contacts')
    need(tuple(sorted(labels.index(v) for v in ADDED)) in edgeset,'new-new interaction')

def main():
    prov=json.loads((HERE/'PROVENANCE.json').read_text());arch=(HERE/'ARCHITECTURE.json').read_bytes()
    need(sha256(arch).hexdigest()==prov['architecture_sha256'],'frozen architecture hash')
    need(json.loads(arch)['removed_host_labels']==list(D),'frozen deletions')
    raw=(HERE/'h632.csv').read_bytes();need(sha256(raw).hexdigest()==prov['h632_sha256'],'H632 bytes')
    P,rows=points(raw);need(len(P)==len(set(rows))==632,'exact H632 collisions')
    full=graph(P);need(len(full)==3112,'complete H632 edges')
    B=set(prov['base_labels']);H=set(prov['host560_labels'])
    need(len(B)==516 and len(H)==560 and B<=H<=set(range(632)),'parent sets')
    adj=[set() for _ in P]
    for u,v in full:adj[u].add(v);adj[v].add(u)
    need(sum(u in B and v in B for u,v in full)==2538,'parent unit graph')
    need(sorted(v for v in B if len(adj[v]&B)==4)==list(D),'all degree-four vertices')
    need(sqdist(P[293],P[299])==(9*9216,0,0,0,0,0,0,0),'distributed deletion witness')
    retained=B-set(D)
    first=next(((u,v) for u,v in full if u not in H and v not in H and len(adj[u]&retained)>=3 and len(adj[v]&retained)>=3),None)
    need(first==ADDED,'first admissible geometric pair')
    need(not set(ADDED)&H,'outside fixed H560 and B')
    labels=sorted(retained|set(ADDED));need(len(labels)==508,'physical cap')
    qraw=(HERE/'points.csv').read_bytes();Q,qrows=points(qraw)
    need(qrows==[rows[v] for v in labels] and len(set(qrows))==508,'literal merged support')
    E=graph(Q);eraw=''.join(f'{u},{v}\n' for u,v in E).encode('ascii')
    need(eraw==(HERE/'edges.csv').read_bytes(),'complete physical edge bytes')
    contacts={str(v):sorted(adj[v]&retained) for v in ADDED}
    c=json.loads((HERE/'certificate.json').read_text());need(c['architecture_sha256']==prov['architecture_sha256'],'certificate architecture')
    def run(x):verify_certificate(x,Q,E,labels,contacts,sha256(qraw).hexdigest(),sha256(eraw).hexdigest())
    run(c)
    # Meaningful corruption controls on the checked mathematical data.
    bad=[]
    z=copy.deepcopy(c);w=list(z['four_word']);w[E[0][1]]=w[E[0][0]];z['four_word']=''.join(w);bad.append(('monochromatic edge',z))
    z=copy.deepcopy(c);z['four_word']=z['four_word'][:-1];bad.append(('short word',z))
    z=copy.deepcopy(c);z['removed']=list(D[:-1]);bad.append(('wrong deletion',z))
    z=copy.deepcopy(c);z['added']=[399,575];bad.append(('wrong addition',z))
    z=copy.deepcopy(c);z['labels'][0]=1;bad.append(('wrong label map',z))
    z=copy.deepcopy(c);z['unit_edges']-=1;bad.append(('edge omission claim',z))
    z=copy.deepcopy(c);z['point_sha256']='0'*64;bad.append(('point identity',z))
    z=copy.deepcopy(c);z['new_old_contacts']['399']=[];bad.append(('contact loss',z))
    z=copy.deepcopy(c);z['vertices']=507;bad.append(('false cap',z))
    z=copy.deepcopy(c);z['moser_witness'][1]=z['moser_witness'][0];bad.append(('lower bound collision',z))
    for name,z in bad:
        try:run(z)
        except (ValueError,IndexError,KeyError):continue
        raise ValueError('accepted malformed certificate: '+name)
    out={'verified':True,'vertices':508,'unit_edges':2506,'chromatic_number':4,'complete_support_pairs':128778,'H632_pairs':199396,'new_points':list(ADDED),'new_old_contacts':contacts,'point_sha256':sha256(qraw).hexdigest(),'edge_sha256':sha256(eraw).hexdigest(),'malformed_certificates_rejected':[n for n,z in bad],'scope':'one frozen physical exchange; no record improvement'}
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
