"""Independent original dual/complete-orbit checks, one bounded phase at a time."""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,signal
from affine import family,matrices,table,repair,parameters,mix,quad,pair,orbit_data,orbit_form,representative_form
from linear import need,mv,psd,digest,canonical
from sectors import full_sectors

def vectors(S,Z):
    non=S[1:];one=[F(1)]*len(non)
    y=[F(A&7==1 and A.bit_count()==2)for A in non]
    yz=[a*F(bool(A&Z))for a,A in zip(y,non)];yw=[a-b for a,b in zip(y,yz)]
    extra=[F(A&7 in [2,4,3,5] and (A&~7).bit_count()==1)for A in non]
    sa=[F(bool(A&1))for A in non]
    z=[1-F(bool(A&2))-F(bool(A&4))+F(A.bit_count()==3 or A in [3,5,6])for A in non]
    return one,y,yz,yw,extra,sa,z

def dual(q,k):
    S,Z,C,D,R,U=matrices(q,k);p=parameters(q,k);one,y,yz,yw,extra,sa,z=vectors(S,Z)
    need(not any(mv(C,z))and not any(mv(R,z)),'literal lower zero action and repair zero')
    need(quad(D,z)==p['alpha']>0,'literal lower derivative on actual z')
    gram2=[[pair(U,a,b)for b in [one,y]]for a in [one,y]]
    derivative2=[[pair(D,a,b)for b in [one,y]]for a in [one,y]]
    need(gram2==[[p['e'],p['a0']],[p['a0'],p['T']]],'every original mean/pair Gram entry')
    need(derivative2==[[p['S'],q*p['h']],[q*p['h'],0]],'every original mean/pair derivative entry')
    cols=[one]+([yz]if k else[])+([yw]if q-k else[])+[extra]
    counts=([k]if k else[])+([q-k]if q-k else[])
    actions=([p['az']]if k else[])+([p['aw']]if q-k else[])
    size=len(cols);expected=[[F(0)]*size for _ in range(size)];expected[0][0]=p['e']
    expectedD=[[F(0)]*size for _ in range(size)];expectedD[0][0]=p['S']
    for i,(count,action)in enumerate(zip(counts,actions),1):
        expected[0][i]=expected[i][0]=count*action;expected[i][i]=count*p['gap']
        expectedD[0][i]=expectedD[i][0]=count*p['h']
    expected[0][-1]=expected[-1][0]=4*q*(1-k);expected[-1][-1]=4*q*p['d']
    expectedD[0][-1]=expectedD[-1][0]=4*q*p['h']
    literal=[[pair(U,a,b)for b in cols]for a in cols]
    literalD=[[pair(D,a,b)for b in cols]for a in cols]
    need(literal==expected and literalD==expectedD,'entire original diagonal Schur Gram/derivative')
    need(all(pair(R,a,b)==0 for a in cols for b in cols),'entire repair vanishes bilinearly')
    w=[a-p['az']/p['gap']*b-p['aw']/p['gap']*c-F(1-k)/p['d']*d for a,b,c,d in zip(one,yz,yw,extra)]
    need(quad(U,w)==p['Q0']and quad(D,w)==p['D4']and quad(R,w)==0,'original rational four-vector dual pairings')
    F0=p['T']*p['e']-p['a0']**2
    polynomial=q**3*(q*q+7*q+8-2*k)*(q*q+(13-6*k)*q+2*k*k-10*k+14)-4*((2*k+1)*q*q+k*q-2*k)**2
    need(polynomial==4*q*q*F0,'original determinant versus displayed integer polynomial')
    need(p['Q0']==F0/p['T']-F(k*(q-k))*p['ww']**2/(q*p['gap'])-F(4*q*(1-k)**2)/p['d'],'complete improvement identity')
    if k:
        need(p['D4']>=p['B']/p['T']>0 and p['c4']>0 and p['gap']>=22 and p['g']>0,'full admissible domain signs calibrated')
        lower=F(q*(q+1)*(3*q**3+20*q*q+49*q+24),4*(3*q+5))
        need(p['B']/q>lower>0,'quantified all-q decreasing coefficient bound')
        for kap in [F(-2),F(0),F(1,4),F(3,7)]:
            vv=p['e']-kap*p['S']-(k*(p['az']-kap*p['h'])**2+(q-k)*(p['aw']-kap*p['h'])**2)/p['gap']-4*q*(1-k-kap*p['h'])**2/p['d']
            need(vv==p['Q0']-kap*p['D4']-kap*kap*p['c4'],'exact expanded quadratic controls')
    return {'q':q,'k':k,'N':len(S),'mean_pair_Gram':gram2,'four_Gram':literal,'four_derivative':literalD,
            'lower_alpha':p['alpha'],'F0':F0,'Q0':p['Q0'],'D4':p['D4'],'c4':p['c4'],
            'whole_domain_sha256':digest(S),'four_dual_sha256':digest(w)},(S,Z,C,D,R,U,p,one,y,yz,yw,extra,sa,z)

def negative(q):
    r,data=dual(q,5);S,Z,C,D,R,U,p,one,y,yz,yw,extra,sa,z=data
    if q<18:
        v=[18-a for a in y];expected=F(q**4+331*q**3-6302*q*q+4176*q+720,2*q)
        derivative=162*q*(q+1)+F(936*q-2268,3*q+5)
    else:
        v=[32-2*a-b+c for a,b,c in zip(yw,yz,extra)];expected=F(-8368,51);derivative=F(10381888,59)
        need(r['F0']==F(1905788,81)>0 and r['Q0']==F(-126891185,110844216)<0,'exception separates necessary tests')
    need(quad(U,v)==expected<0 and quad(D,v)==derivative>0 and quad(R,v)==0,'complete original all-real negative witness')
    need(not any(mv(C,sa))and not any(mv(R,sa)),'literal a-star kernel')
    return {**r,'negative_dual_values':sorted(set(v)),'negative_U0':expected,'positive_Delta':derivative,'R_pairing':0,'dual_sha256':digest(v)}

def positive(q,kap=F(1,4096)):
    need(19<=q<=23,'positive fixture domain');k=5;S,Z,C0,D,R,U0=matrices(q,k);N=len(S);s=3*q+4;m=N-1
    need(kap in [F(1,4096),F(1,1024)],'fixed positive parameter controls')
    sectors=[full_sectors(q,F(0)),full_sectors(q,kap)]
    C=mix(mix(C0,D,kap),R,4);U=mix(mix(U0,D,-kap),R,-4)
    keys,groups,weights=orbit_data(S,Z,q,k);need(len(groups)==23,'complete fixed-space dimension')
    G=orbit_form(C,groups);H=orbit_form(U,groups)
    need(G==representative_form(C,groups)and H==representative_form(U,groups),'all full weighted pair sums versus representative path')
    sa=[F(bool(A&1))for A in S[1:]];a=[F(bool(key[0]&1))for key in keys];weighted=[v*w for v,w in zip(a,weights)]
    eta=kap/F(1<<18);beta=F(1,1<<20)
    GP=[[G[i][j]-eta*(F(weights[i]*(i==j))-weighted[i]*weighted[j]/s)for j in range(23)]for i in range(23)]
    HP=[[H[i][j]-beta*weights[i]*(i==j)for j in range(23)]for i in range(23)]
    need(psd(GP)['rank']==22 and psd(HP)['rank']==23 and not any(mv(G,a)),'all complete positive weighted floors and a-star action')
    need(not any(mv(C,sa))and sum(sa)==s,'actual nonempty star kernel')
    rows=[sum(r)for r in C];energy=sum(rows);L=[[1+energy]+[1-r for r in rows]]
    L += [[1-rows[i]]+[1+x for x in row]for i,row in enumerate(C)]
    h=F(1,3*q+5);alpha=F(q*(q+1),2)+3*(q+1)*h
    need(energy==5*(s-5)+kap*(alpha-10*h),'independent actual empty energy')
    Q=table(q,kap);rho=[]
    for A in S[1:]:
        cc=(A&7).bit_count();action=1 if cc==0 else(h if cc<3 else -3*(q+1)*h)
        count=5 if A&6 else (A&Z).bit_count()
        deleted=-5 if count==5 else -count+(5-count)*(Q[tuple(sorted(((cc,(A&~7).bit_count()),(2,1))))]-1)
        rowR=2 if A==1 else(-1 if A in [3,5]else 0)
        rho.append(kap*action-deleted+4*rowR)
    need(rho==rows,'every actual nonempty row versus closed deleted-column formula')
    center=[F(bool(A&1))-F(s,N)for A in S];need(not any(mv(L,center)),'actual empty centered-star kernel')
    for i,A in enumerate(S):
        need(sum(L[i])==N,'actual whole row sums')
        for j,B in enumerate(S):
            need(L[i][j]==L[j][i],'actual whole symmetry')
            if A&B:need(L[i][j]==s*(i==j),'all original whole support')
    # New endpoint experiment: record actual feasibility, never infer exclusion.
    endpointC=mix(C0,R,4);endpointU=mix(U0,R,-4)
    EG=orbit_form(endpointC,groups);EH=orbit_form(endpointU,groups)
    endpoint={'kappa':0,'repair':4,'scope':'this fixed endpoint only; no ansatz nonexistence from failure'}
    try:
        er=psd(EG)['rank'];eh=psd([[EH[i][j]-beta*weights[i]*(i==j)for j in range(23)]for i in range(23)])['rank']
        need(eh==23,'endpoint cap strict floor');endpoint.update({'fixed_lower_PSD':True,'orbit_lower_rank':er,'cap_floor':beta,'cap_orbit_rank':eh,'interval':'proved from endpoints with independently checked complete finite undeleted forms'})
    except ValueError as error:endpoint.update({'fixed_lower_PSD':False,'check_failure':str(error)})
    return {'q':q,'k':5,'N':N,'s':s,'kappa':kap,'repair':4,'complete_orbit_keys':keys,'orbit_weights':weights,
            'orbit_Gram_sha256':digest(G),'orbit_cap_sha256':digest(H),'shifted_lower_rank':22,'shifted_cap_rank':23,
            'nonempty_lower_floor':eta,'physical_whole_cap_floor':beta,'complete_whole_entries':N*N,
            'lower_whole_rank':N-1,'cap_whole_rank':N-1,'actual_empty_L_loop':L[0][0],
            'actual_empty_M_loop':F(L[0][0]-s,N-s),'whole_L_sha256':digest(L),
            'actual_row_sha256':digest(rho),'zero_endpoint':endpoint,'finite_undeleted_sectors':sectors,'trust':'Complete finite old harmonic forms plus actual orbit/literal proof. Infinite tail explicitly retained separately; no literal dense PSD elimination.'}

def main():
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('fixed60s independent phase guard')));signal.alarm(60)
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['calibrations','negative','positive','stronger','controls']);p.add_argument('--q',type=int);p.add_argument('--expected');args=p.parse_args()
    if args.phase=='controls':
        from controls import controls
        rows=[controls()]
    elif args.phase=='calibrations':rows=[dual(q,k)[0]for q in range(4,9)for k in range(q+1)]
    elif args.phase=='negative':need(args.q is not None and 5<=args.q<=18,'negative q guard');rows=[negative(args.q)]
    else:rows=[positive(args.q,F(1,1024)if args.phase=='stronger'else F(1,4096))]
    out={'agent':'six-reviewer-2','role':'independent mathematical reviewer','phase':args.phase,'records':rows}
    if args.expected:
        frozen=json.loads(Path(args.expected).read_text())
        if 'cases'in frozen:frozen=frozen['cases'][str(args.q)]
        need(canonical(out)==frozen,'entire frozen independent phase')
    print(json.dumps(canonical(out),sort_keys=True,indent=2));signal.alarm(0)
if __name__=='__main__':main()
