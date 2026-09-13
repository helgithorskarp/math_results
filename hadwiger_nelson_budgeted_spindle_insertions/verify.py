"""Solver-free physical certificate replay, including complete placement generation."""
from geometry51 import *
from build_host_only import run as build_host
from shell_search import checked_colouring,reject_bad_colouring
HERE=Path(__file__).resolve().parent

def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def check_obstruction(cert):
 s,P,seedword,seededges=seed(cert['tag']);added=[(tuple(map(F,p[:4])),tuple(map(F,p[4:])))for p in cert['added_points']];Q=P+added;es=Geometry51(W/'sparse_geometry.so').graph(Q,s,audit=True)
 require(len(Q)==cert['vertices']and len(es)==cert['edges'],'fixture census');checked_colouring(cert['word'],len(Q),es);reject_bad_colouring('0'*len(Q),len(Q),es)
 # Independent exhaustive extension check on the at-most-five newly added points.
 boundary=[(a,b-490)for a,b in es if a<490<=b];internal=[(a-490,b-490)for a,b in es if a>=490];count=0
 for c in product('0123',repeat=len(added)):
  count+=all(seedword[a]!=c[b]for a,b in boundary)and all(c[a]!=c[b]for a,b in internal)
 require(count==0,'fixed seed colouring unexpectedly extends')
 return {'vertices':len(Q),'edges':len(es),'new_points':len(added),'seed_word_extensions':count,'proper_alternative_four_colouring':True}

def run():
 st=time.time();cert=json.loads((HERE/'certificate.json').read_text());expected=json.loads((HERE/'EXPECTED.json').read_text());small=check_obstruction(cert['colour_obstruction_fixture']);tag=cert['dense_host']['tag']
 generate(tag);boundary(tag);build_host(tag)
 p=json.loads((W/f'placements_{tag}.json').read_text());h=json.loads((W/f'host_edges_{tag}.json').read_text());c=cert['dense_host'];n=490+len(h['new_point_ids']);es=h['edges'];pts=p['seed_points']+[p['new_points'][i]for i in h['new_point_ids']]
 require(n==c['vertices']and len(es)==c['edges']and len(h['placements'])==c['admitted_placements'],'dense census');require(digest(h['new_point_ids'])==c['new_point_ids_sha256'],'new point IDs');require(digest(pts)==c['points_sha256'],'physical point stream');require(digest(es)==c['edges_sha256'],'physical edge stream');checked_colouring(c['word'],n,es);reject_bad_colouring('0'*n,n,es);reject_bad_colouring(c['word'][:-1],n,es)
 require(p['raw_placements']==expected['dense']['raw_placements']and len(p['placements'])==expected['dense']['unique_nonempty_additions']and len(p['new_points'])==expected['dense']['all_new_points'],'placement counts')
 out={'status':'PASS','dense_host_vertices':n,'dense_host_edges':len(es),'admitted_placements':len(h['placements']),'dense_pair_instances_audited_twice':n*(n-1)//2,'colour_obstruction':small,'record_improvement':False,'field_host_status':'UNKNOWN','seconds':time.time()-st};(W/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
if __name__=='__main__':run()
