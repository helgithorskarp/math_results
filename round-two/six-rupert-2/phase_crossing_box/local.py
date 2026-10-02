"""Exact conditional local bridge and both true closed J74 receiver phases.

Standard library only; original source/geometry pins are checked before import.
No private journal or numerical solver output is imported.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib,importlib.util,json,sys
HERE=Path(__file__).resolve().parent
DEPENDENCIES=json.loads((HERE/'DEPENDENCIES.json').read_text())
for relative,digest in DEPENDENCIES['sha256'].items():
 if hashlib.sha256((HERE/relative).read_bytes()).hexdigest()!=digest:
  raise ValueError('before-import exact prerequisite fingerprint: '+relative)
spec=importlib.util.spec_from_file_location('j74_cross_parent_forms',HERE.parent/'full_source_rectangle/forms.py')
parent=importlib.util.module_from_spec(spec);sys.modules[spec.name]=parent;spec.loader.exec_module(parent)
c,a,Q,p=parent.c,parent.a,parent.Q,parent.p
def squared(x):return x*x

def preflight(data):
 c.require(len(data['physical_rotation_bases'])==6,'six signed physical-coordinate bases')
 c.require(all(type(d['axis']) is int and type(d['sign']) is int for d in data['physical_rotation_bases']),'literal signed rotation coordinates')
 c.require({(d['axis'],d['sign']) for d in data['physical_rotation_bases']}=={(i,s) for i in range(3) for s in (-1,1)},'all signed rotation targets')
 u,oldcycle,oldN,R2=c.original_geometry();s=Q(0,1);r0=a.scale(-1/u[2],u);tau=(-3994+1792*s)/899
 raw=a.add(r0,(-tau,tau,Q()));eta=Q(F(1,1000))
 corners=[a.add(raw,(x*eta,y*eta,Q())) for x,y in ((-1,-1),(1,-1),(1,1),(-1,1))]
 oldedges=list(zip(oldcycle,oldcycle[1:]+oldcycle[:1]))
 common_edges=[e for i,e in enumerate(oldedges) if i not in (14,15)]
 E=[a.sub(c.V[j],c.V[i]) for i,j in common_edges]
 M=[[a.cross(e,r) for e in E] for r in (raw,p.EX,p.EY)]
 h=[[a.dot(m,c.V[i]) for m,(i,j) in zip(ms,common_edges)] for ms in M]
 N=[a.scale(1/x,m) for m,x in zip(M[0],h[0])]
 source_data=json.loads((c.HERE/'certificate.json').read_text())
 poses=[c.matrix(x['proper_matrix_rows']) for x in source_data['poses']]
 for g in poses:c.proper(g)
 aa=(s-1)/4;bb=(s+1)/4;cc=Q(1)/2;Z=Q()
 H=((Q(-1),Z,Z),(Z,Q(-1),Z),(Z,Z,Q(1)))
 A=((bb,aa,cc),(-aa,-cc,bb),(cc,-bb,-aa));B=((-aa,-cc,-bb),(cc,-bb,aa),(-bb,-aa,cc))
 c.require(set(poses)=={c.IDENTITY,H,A,c.matmul(A,H),B,c.matmul(B,H)},'six literal named proper base poses')
 supports_checked=0;strict_gaps=[];normratios=[]
 for i,j in common_edges:
  for r in corners:
   m=a.cross(a.sub(c.V[j],c.V[i]),r);height=a.dot(m,c.V[i]);c.require(height>0,'positive true common support height')
   for k,v in enumerate(c.V):
    gap=a.dot(m,a.sub(c.V[i],v));c.require(gap>=0,'full common original support');supports_checked+=1
    if k not in (i,j):c.require(gap>0,'strict common offendpoint receiver support');strict_gaps.append(gap)
   normratios.append(R2*a.dot(m,m)/(height*height))
 c.require(max(normratios)<Q(F(9,4)),'all common supports have R||N||<3/2')
 C=Q(F(5,4))
 duals=data['physical_rotation_bases']
 inverse=c.load_collar().inverse;families=[];masses=[Q(),Q(),Q()];rhos=[];weights_floor=[]
 def B(normals,contacts):
  return tuple(zip(*(tuple(a.cross(c.V[k],normals[common_edges.index((i,j))]))+tuple(normals[common_edges.index((i,j))][:2]) for i,j,k in contacts)))
 for d in duals:
  contacts=d['literal_original_contacts'];indices=[common_edges.index(tuple(x[:2])) for x in contacts]
  c.require(all(k in (i,j) for i,j,k in contacts),'selected common rows use literal persistent spatial endpoints')
  B0,Bx,By=[B(ms,contacts) for ms in M]
  inv=inverse(c,B0);Kx,Ky=c.matmul(inv,Bx),c.matmul(inv,By)
  target=tuple(Q(d['sign']*int(j==d['axis'])) for j in range(5))
  w0=c.act(inv,target)
  c.require(c.act(B0,w0)==target,'all exact point raw torque/force equations')
  D=tuple(tuple(eta*(c.absolute(x)+c.absolute(y)) for x,y in zip(row1,row2)) for row1,row2 in zip(Kx,Ky))
  rho=max(sum(row,Q()) for row in D);c.require(rho<1,'strict component Neumann norm')
  I=tuple(tuple(Q(int(i==j)) for j in range(5)) for i in range(5))
  repair=inverse(c,tuple(tuple(x-y for x,y in zip(row1,row2)) for row1,row2 in zip(I,D)))
  c.require(all(x>=0 for row in repair for x in row),'nonnegative entire comparison inverse')
  b=tuple(eta*(c.absolute(x)+c.absolute(y)) for x,y in zip(c.act(Kx,w0),c.act(Ky,w0)))
  error=c.act(repair,b);lower=tuple(x-y for x,y in zip(w0,error));c.require(min(lower)>0,'whole-box positive raw weights')
  mass0=sum((w*h[0][i] for w,i in zip(w0,indices)),Q())
  mass=mass0+sum((e*h[0][i]+eta*(w+e)*(c.absolute(h[1][i])+c.absolute(h[2][i])) for e,w,i in zip(error,w0,indices)),Q())
  masses[d['axis']]=max(masses[d['axis']],mass);rhos.append(rho);weights_floor.extend(lower)
  families.append({'axis':d['axis'],'sign':d['sign'],'literal_original_contacts':contacts,
                   'raw_point_weights':[c.enc(x) for x in w0],'component_error':[c.enc(x) for x in error],
                   'strict_raw_weight_lower':[c.enc(x) for x in lower],'strict_normalized_mass_upper':c.enc(mass)})
 mass_bounds=[next(k for k in range(1,201) if value<k) for value in masses]
 G=next(k for k in range(2,201) if C*C*sum(x*x for x in mass_bounds)<Q(F(9*k*k,10)))
 hole_den=next(k for k in range(G+1,G+401) if squared(Q(F(2,k))+6*eta)<Q(F(4,G*G+1)))
 c.require(C*C*sum(x*x for x in mass_bounds)/Q(G*G)<1,'complete nonlinear conditional Cayley closure')

 # True closed receiver phases separated by the actual old48->56/original40 wall.
 old_cycle=oldcycle;new_cycle=oldcycle.copy();new_cycle[new_cycle.index(56)]=40
 line_E=a.sub(c.V[56],c.V[48]);line_gap=a.sub(c.V[48],c.V[40])
 def phase_value(r):return a.dot(a.cross(line_E,r),line_gap)
 c.require(phase_value(raw)==0,'actual support phase seam passes exact box center')
 def clip(sign):
  output=[]
  for v,w in zip(corners,corners[1:]+corners[:1]):
   x,y=sign*phase_value(v),sign*phase_value(w)
   if x>=0:output.append(v)
   if (x<0<y) or (y<0<x):
    t=x/(x-y);output.append(a.add(v,a.scale(t,a.sub(w,v))))
  return output
 regions=[];full_receiver_comparisons=0;full_source_comparisons=0
 for sign,cycle in ((1,old_cycle),(-1,new_cycle)):
  polygon=clip(sign);c.require(len(polygon)>=3,'both closed receiver phases nonempty')
  # Every original is checked at every vertex of the exact clipped polygon.
  for r in polygon:
   for i,j in zip(cycle,cycle[1:]+cycle[:1]):
    m=a.cross(a.sub(c.V[j],c.V[i]),r);height=a.dot(m,c.V[i]);c.require(height>0,'positive actual phase heights')
    for v in c.V:c.require(a.dot(m,v)<=height,'all literal actual phase supports');full_receiver_comparisons+=1
    for g in poses:
     images=[c.act(g,v) for v in c.V]
     c.require(c.V[i] in images and c.V[j] in images,'actual full spatial corner preimages in every base pose')
     for image in images:c.require(a.dot(m,image)<=height,'whole actual source containment at all closed receiver polygon vertices');full_source_comparisons+=1
  regions.append({'phase':sign,'original_cycle':cycle,'raw_closed_polygon_vertices':[[c.enc(x) for x in r] for r in polygon]})
 # All chosen physical points really occur in every base source, at all receivers.
 for g in poses:
  images={c.act(g,v) for v in c.V}
  c.require(all(c.V[k] in images for f in families for i,j,k in f['literal_original_contacts']), 'every persistent physical source contact has literal preimage')
 Mn=tuple(tuple(c.IDENTITY[i][j]-2*raw[i]*raw[j]/a.dot(raw,raw) for j in range(3)) for i in range(3))
 Mx=((Q(-1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1)))
 c.require({c.act(Mx,v) for v in c.V}==set(c.V),'full-body x reflection')
 branches=[v for g in poses for v in (g,c.matmul(c.matmul(Mn,g),Mx))]
 c.require(len(set(branches))==12,'twelve distinct point equality branches')
 sep=min(sum((squared(g[i][j]-v[i][j]) for i in range(3) for j in range(3)),Q()) for k,g in enumerate(branches) for v in branches[k+1:])
 c.require(sep>Q(F(1,100)) and 18*eta<Q(F(1,10)),'all twelve branches stay distinct across the whole box')
 c.require(data['raw_center']==[c.enc(x) for x in raw] and data['raw_halfwidth']==['1/1000','0'],'literal entire phase-crossing receiver box')
 c.require(mass_bounds==[7,12,18] and G==30 and hole_den==33,'stated exact finite local constants')
 c.require(C*C*sum(x*x for x in mass_bounds)/Q(G*G)==Q(F(517,576)),'literal local absorption517/576')
 return {'agent':'six-rupert-2','role':'researcher','scope':'entire closed phase-crossing raw receiving box; conditional local rigidity only',
         'raw_center':[c.enc(x) for x in raw],'raw_halfwidth':c.enc(eta),'common_actual_original_edges':common_edges,
         'fifteen_common_receiver_corner_comparisons':supports_checked,'full_piecewise_receiver_comparisons':full_receiver_comparisons,
         'full_piecewise_source_comparisons':full_source_comparisons,'receiving_closed_phase_regions':regions,
         'uniform_common_contact_quadratic_constant':c.enc(C),'raw_families':families,
         'uniform_coordinate_contact_mass_bounds':mass_bounds,'maximum_component_Neumann_norm':c.enc(max(rhos)),
         'strict_common_raw_weight_lower':c.enc(min(weights_floor)),'closed_local_Cayley_Euclidean_gate':c.enc(Q(F(1,G))),
         'squared_local_absorption_bound':c.enc(C*C*sum(x*x for x in mass_bounds)/Q(G*G)),
         'point_reference_hole_Cayley_gate':c.enc(Q(F(1,hole_den))),
         'proper_point_pose_rows':[[[c.enc(x) for x in row] for row in g] for g in branches],
         'source_entry_hypothesis_still_required':True}
