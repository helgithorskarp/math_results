#!/usr/bin/env python3
"""LATE ONLY: sealed reviewer arithmetic checks every native coordinate/plane,
Cramer intersection and native closed cover. This does not edit primary evidence.
"""
import argparse,hashlib,importlib.util,itertools,json,pathlib,sys,time
P=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('sealed_reviewer',P/'audit.py');own=importlib.util.module_from_spec(spec);spec.loader.exec_module(own)
R=own.require

def poly(p):
 R(all(type(k)is tuple and len(k)==3 and k[1:]==(0,0) and type(k[0])is int and k[0]>=0 and type(v)is int for k,v in p.c.items()),'strict native polynomial data type/univariate boundary')
 return own.trim(p.c.get((i,0,0),0) for i in range(max((k[0] for k in p.c),default=-1)+1))
def exact_json(x):
 if isinstance(x,dict):
  R(all(type(k)is str for k in x),'string JSON keys')
  for v in x.values():exact_json(v)
 elif isinstance(x,list):
  for v in x:exact_json(v)
 else:R(type(x) in (str,int,bool,type(None)),'no float proof data')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native',required=True);ap.add_argument('--output',required=True);ap.add_argument('--damage');a=ap.parse_args();native=pathlib.Path(a.native).resolve()
 sys.path.insert(0,str(native));from polynomials import P as NP
 import model,algebra
 y,checks=own.reconstruct();t=NP.var(0);ny,no,_=model.make(t);planes,_,_=algebra.row_planes(t)
 R(tuple(model.LABELS)==own.LABELS and tuple(model.CONTACTS)==own.EDGES,'literal native labels/contacts')
 if a.damage=='coordinate':ny[7][0]+=no
 R(poly(no)==own.OMEGA,'whole native Omega identity')
 for i in own.LABELS:
  for j in range(3):R(poly(ny[i][j])==y[i][j],'all36 native coordinate polynomials')
 cert=json.loads((native/'CERTIFICATE.json').read_text());system=json.loads((native/'SYSTEM.json').read_text());exact_json(cert)
 R(set(cert)=={'system','boundedness_determinant_sign','records'} and cert['system']==system,'complete native literal scope')
 R(system['core_labels']==list(own.LABELS) and system['literal_contacts']==[list(e) for e in own.EDGES] and system['closed_parameter_interval']==[str(own.LO),str(own.HI)] and system['actual_extra_core_point_required'] is False and system['extra_contact_or_face_or_degree_premise_for_capacity'] is False,'native twelve arbitrary-point quantifier')
 R(system['all_additional_points']=='arbitrary unit vectors avoiding all12 core points' and system['global_Tammes_bound_claimed'] is False and system['optimizer_motif_occurrence_claimed'] is False,'no stronger hidden scope')
 mapped={99:98,98:99};orows,orhs=own.row_data(y);primal={}
 for k,(row,rhs) in planes.items():
  m=mapped.get(k,k);normal=orows[m];s=own.sum_poly(normal)
  expected=tuple(own.add(own.mul((1,-1),q),own.mul(own.T,s)) for q in normal)
  nr=tuple(poly(q) for q in row);nh=poly(rhs)
  for j in range(3):R(own.mul(nr[j],orhs[m])==own.mul(expected[j],nh),'all42 native primal row clearings')
  R(own.positive(own.strip(nh),own.LO,own.HI),'positive native row clearing')
  primal[k]=(nr,nh)
 records=cert['records']
 if a.damage=='missing-triple':records.pop()
 if a.damage=='duplicate-triple':records[1]=records[0]
 expected=set(itertools.combinations(own.LABELS+(98,99),3));seen=set();counts={'coordinate_polynomials':36,'row_polynomials':42,'triples':0,'singular':0,'cramer_ratio_identities':0,'leaves':0,'strict_signs':0}
 for record in records:
  keys=tuple(record['triple']);R(all(type(k)is int for k in keys) and keys in expected and keys not in seen,'all364 unique native triples');seen.add(keys);counts['triples']+=1
  rawd,raww=own.cram([primal[k][0] for k in keys],[primal[k][1] for k in keys]);nd,nw=algebra.vertex(planes,keys,t);d=poly(nd);w=tuple(poly(q) for q in nw)
  if record['type']=='S':R(not rawd and not d and set(record)=={'triple','type'},'singular physical Cramer');counts['singular']+=1;continue
  R(record['type']=='COVER' and rawd and d and len(w)==3 and set(record)=={'triple','type','leaves'},'complete nonsingular record')
  for j in range(3):R(own.mul(rawd,w[j])==own.mul(raww[j],d),'whole native Cramer intersection ratio');counts['cramer_ratio_identities']+=1
  for k in keys:R(own.pdot(primal[k][0],w)==own.mul(primal[k][1],d),'native reduced Cramer row identity')
  leaves=record['leaves'];paths=[''.join(map(str,l['path'])) for l in leaves]
  R(all(type(bit)is int and bit in (0,1) for l in leaves for bit in l['path']),'typed binary paths')
  if a.damage=='missing-cell' and len(leaves)>1:leaves=leaves[:-1];paths=paths[:-1];a.damage='applied'
  R(len(paths)==len(set(paths)) and sum((own.F(1,2**len(s)) for s in paths),own.F())==1,'complete exact native binary mass')
  for x,z in itertools.combinations(paths,2):R(not x.startswith(z) and not z.startswith(x),'prefix-free native cover')
  norm=own.strip(own.sub(own.scale(own.power(d,2),49),own.scale(own.add(own.mul((1,-1),own.sum_poly(own.power(q,2) for q in w)),own.mul(own.T,own.power(own.sum_poly(w),2))),50)))
  for leaf in leaves:
   lo,hi=own.LO,own.HI
   for bit in leaf['path']:
    mid=(lo+hi)/2
    if bit:lo=mid
    else:hi=mid
   counts['leaves']+=1
   if leaf['type']=='N':
    R(set(leaf)=={'path','type'} and own.positive(norm,lo,hi),'native norm leaf via reviewer Sturm');counts['strict_signs']+=1
   else:
    R(leaf['type']=='I2' and set(leaf)=={'path','type','positive_residual','negative_residual'},'complete native residual leaf')
    j,k=leaf['positive_residual'],leaf['negative_residual'];R(type(j)is int and type(k)is int and j!=k and j in primal and k in primal and j not in keys and k not in keys,'typed opposite inactive native planes')
    if a.damage=='swapped-sign':j,k=k,j;a.damage='applied'
    for lab,sgn in [(j,1),(k,-1)]:
     h=own.strip(own.sub(own.pdot(primal[lab][0],w),own.mul(primal[lab][1],d)))
     R(own.positive(own.scale(h,sgn),lo,hi),'native residual leaf via reviewer Sturm');counts['strict_signs']+=1
 R(seen==expected and counts['triples']==364 and counts['singular']==4 and counts['leaves']==367 and counts['strict_signs']==703,'whole native census/completion')
 # The other48 signs are independently regenerated from the whole normalized family.
 own.boundedness(y);s=own.sharpness(y);R(len(s['core_pairs'])==66,'all native-matched packing comparisons')
 counts['strict_signs_with_core_and_boundedness']=703+44+4
 result={'status':'PASS','method':'LATE native data alignment, complete Cramer ratio identities and every native closed cell using sealed reviewer Sturm','mapping':'native99=reviewer98 first cap; native98=reviewer99 second cap','counts':counts,'seconds':time.monotonic()-own.START,'primary_file_changed':False}
 pathlib.Path(a.output).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
