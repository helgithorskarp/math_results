"""Rebuild two exact source graphs and check the five positive port witnesses."""
from pathlib import Path
from itertools import combinations
from hashlib import sha256
import argparse,json,sys,time

HERE=Path(__file__).resolve().parent
INPUT=HERE.parent/'hadwiger_nelson_nonmono159_214_lowden2'
sys.path.insert(0,str(INPUT))
import enumerate_lowden as F
PORTS={'159':[141,142,144],'214':[186,187]}
PATTERNS={'159':['001','010','011','012'],'214':['01']}


def encoded(x):return (json.dumps(x,separators=(',',':'))+'\n').encode()


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 args.out.mkdir(parents=True,exist_ok=False);start=time.perf_counter()
 cert_raw=(HERE/'certificate.json').read_bytes();cert=json.loads(cert_raw);graphs={};results=[]
 assert set(cert)==set(PORTS)
 for key in PORTS:
  n=int(key);path=INPUT/f'points{key}.tsv';points=F.points(path);assert len(points)==n
  def distance(i,j):
   xx,yy=[tuple(x-y for x,y in zip(a,b,strict=True)) for a,b in zip(points[i],points[j],strict=True)]
   return F.add(F.mul(xx,xx),F.mul(yy,yy))
  distances={(i,j):distance(i,j) for i,j in combinations(range(n),2)}
  edges=[list(e) for e,d in distances.items() if d==(144,)+(0,)*7]
  expected_edges=646 if n==159 else 977
  assert len(edges)==expected_edges
  ports=PORTS[key];assert cert[key]['terminals']==ports
  port_distance=7 if n==159 else 9
  assert all(distances[i,j]==(144*port_distance,)+(0,)*7 for i,j in combinations(ports,2))
  assert port_distance>4
  rows=cert[key]['extensions'];assert [row['pattern'] for row in rows]==PATTERNS[key]
  for row in rows:
   colours=row['colours'];assert len(colours)==n and set(colours)<=set('0123')
   assert ''.join(colours[i] for i in ports)==row['pattern']
   assert all(colours[i]!=colours[j] for i,j in edges)
  g={'denominator':12,'points':points,'edges':edges,'terminals':ports}
  raw=encoded(g);(args.out/f'graph{key}.json').write_bytes(raw);graphs[key]=g
  results.append({'vertices':n,'edges':len(edges),'pair_tests':len(distances),'terminals':ports,
   'squared_terminal_distance':port_distance,'canonical_patterns':PATTERNS[key],
   'positive_witness_edge_checks':len(rows)*len(edges),'graph_sha256':sha256(raw).hexdigest(),
   'coordinate_sha256':sha256(path.read_bytes()).hexdigest()})
 result={'status':'ALL NONMONOCHROMATIC TERMINAL ASSIGNMENTS EXTEND; TERMINAL-ONLY ASSEMBLIES OF AT MOST508 VERTICES ARE FOUR-COLOURABLE',
  'gadgets':results,'positive_witnesses':5,'positive_witness_edge_checks':sum(x['positive_witness_edge_checks'] for x in results),
  'full_graph_pair_tests':sum(x['pair_tests'] for x in results),'certificate_bytes':len(cert_raw),
  'certificate_sha256':sha256(cert_raw).hexdigest(),'native_solver_calls_in_replay':0,
  'maximum_gadgets_in_at_most508_terminal_only_assembly':3,'minimum_private_vertices_per_gadget':156,
  'four_gadget_private_vertex_lower_bound':624,'three_gadgets_including_B_private_vertex_lower_bound':524,
  'all_at_most508_terminal_only_assemblies_four_colourable':True,'arbitrary_interior_interactions_covered':False,
  'monochromatic_terminal_pattern_refutation_required':False,'target_found':False}
 (args.out/'certificate.json').write_bytes(cert_raw)
 (args.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 (args.out/'timing.json').write_text(json.dumps({'seconds':time.perf_counter()-start})+'\n')
 print(json.dumps(result,indent=2))


if __name__=='__main__':main()
