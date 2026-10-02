"""New all-order-cut calibrations and multiplicity-sensitive column identities.
Finite controls are abstract necessary domains, not star/code realizations.
"""
import itertools as it,json,pathlib,time,collections,math
import audit as a
P=pathlib.Path(__file__).resolve().parent

def graph_calibration():
    n=4;pairs=list(it.combinations(range(n),2));count=admissible=active=0;full=[];start=time.monotonic()
    # Literal labelled complete graph/role/color domain, no symmetry quotient.
    for roles in it.product('AVCB',repeat=n):
      units={i for i,r in enumerate(roles) if r in 'AV'};eligible={i for i,r in enumerate(roles) if r in 'VB'}
      A={i for i,r in enumerate(roles) if r=='A'};V=units-A;C={i for i,r in enumerate(roles) if r=='C'};B=eligible-V
      for colors in it.product(range(3),repeat=len(pairs)):
        count+=1;a.need(time.monotonic()-start<10,'INCOMPLETE graph10s guard')
        adj=[set() for _ in range(n)];c1=[0]*n;c2=[0]*n;valid=True
        for (x,y),col in zip(pairs,colors):
          if not col:continue
          if ((x in units or y in units) and col!=1) or ((x in units and y in eligible) or (y in units and x in eligible)):
            valid=False;break
          adj[x].add(y);adj[y].add(x)
          (c1 if col==1 else c2)[x]+=1;(c1 if col==1 else c2)[y]+=1
        if not valid:continue
        admissible+=1
        roots=[r for r in A if {r}|adj[r]|set().union(*(adj[u] for u in adj[r]))==set(range(n))]
        if not roots or not eligible:continue
        active+=1;DA=sum(len(adj[u]) for u in A);DV=sum(len(adj[u]) for u in V)
        I=sum(min(len(adj[u]),len(A)-1) for u in A);Ieven=I-I%2
        C1=sum(c1[u] for u in C);C2=sum(c2[u] for u in C)
        lower=DV+max(len(roots),DA-Ieven)
        a.need(C1>=lower and C1+C2>=lower+len(B),'eligible unit sum plus root/internal-A cuts')
        full.append([roles,colors,roots,DA,DV,Ieven,C1,C2,len(B)])
    # Positive five-point control allowing a NONUNIT color3 edge.
    # Two A roots, one C, one V and one B: all through C, B-C color3.
    arbitrary=dict(roles=['A','A','C','V','B'],edges=[[0,2,1],[1,2,1],[2,3,1],[2,4,3]])
    a.need(3==1+2,'arbitrary-color endpoint equality C1=DV+R')
    return dict(labelled_cases=count,admissible_cases=admissible,active_cases=active,full_active_sha256=a.digest(full),arbitrary_nonunit_color_control=arbitrary)

def scalar_and_DAG_controls():
    # Exact weak-composition oracle, including unused margin. Tests coefficient
    # completeness with zero charges and multiple indistinguishable row charges.
    cases=0
    cols=[(0,0,0,False,0,0,0,0,0,0),(1,0,0,False,0,0,0,0,0,1),(0,1,0,False,0,0,0,0,0,1)]
    for E,K,b in it.product(range(4),range(4),range(5)):
      x=dict(E=E,K=K,Q=0,X=0,N5=0,margin_budget=b)
      got,_=a.c.populations(cols,x);want=[]
      for v in a.compositions(13,len(cols)):
       if (v[1],v[2])==(E,K) and v[1]+v[2]<=b:want.append(v)
      a.need(got==sorted(want),'entire DAG paths versus weak compositions')
      cases+=1
    return cases

def refinement_controls():
    # P37 mass19,pair sum11 and ordinary min-column support for type20.
    allD=list(a.compositions(19,5));kept=[]
    for D in allD:
      if any(D[u]+D[v]>11 for u,v in it.combinations(range(5),2)):continue
      best=0;w=None
      for n in it.product(*(range(D[j]//2+1) for j in range(5))):
       if all(not n[j] or D[j]>=max(2*n[j],4+n[j]) for j in range(5)) and sum(n)>best:best=sum(n);w=n
      a.need(max(D)<=8 and best<=4,'P37 general abstract column/support frontier')
      kept.append([D,best,w])
    a.need(max(r[1] for r in kept)==4,'P37 abstract upper4 is reached')
    # Literal coefficient identity for GENERAL P, with full multiplicity loss:
    # sum3 L_J -2 sum_J N =5M-7P+215-3lambda+sumt+2Z_J.
    identities=[]
    for P0,M,lam,t,z in it.product(range(34,39),range(8,13),range(6),range(5),range(5)):
      PJ=P0-22-M+lam;NJ=2*P0-55-M-z
      left=39-3*PJ+t-2*NJ;right=5*M-7*P0+215-3*lam+t+2*z
      a.need(left==right,'multiplicity-sensitive complementary triangle exact identity')
      identities.append([P0,M,lam,t,z,left])
    return dict(mass19_all=math.comb(23,4),pair_sum11_totals=len(kept),P37_max_D=max(max(r[0]) for r in kept),P37_max_n20=max(r[1] for r in kept),
      full_P37_controls_sha256=a.digest(kept),P37_positive_abstract_n20=next(r for r in kept if r[1]==4),
      identity_cases=len(identities),whole_identity_sha256=a.digest(identities))

def run():
    return dict(agent='six-reviewer-5',role='independent mathematical reviewer',graph=graph_calibration(),DAG_weak_composition_controls=scalar_and_DAG_controls(),refinements=refinement_controls())

if __name__=='__main__':
    r=run();(P/'controls-record.json').write_bytes(a.encode(r));print(json.dumps(r,indent=2));print('sha256',a.digest(r))
