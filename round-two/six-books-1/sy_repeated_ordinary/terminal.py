"""Literal seven BLUE page witnesses, all Q role labels and free T0 Q rows."""
from itertools import combinations, product
import literal as L
import reference as R
from reduction import core

def check_pages(require,neighbors,bits,claimed):
    require(15 not in neighbors[0] and 14 not in neighbors[1],'terminal spine must be BLUE')
    pages=[z for z in range(22) if z not in (14,15) and all(z not in row for row in neighbors)]
    bitpages=[z for z in range(22) if z not in (14,15) and all(not(w>>z&1) for w in bits)]
    require(len(claimed)==7 and len(set(claimed))==7 and claimed==pages==bitpages,
            'SEVEN physical distinct common BLUE pages')

def run(require,guard,digest):
    cases=L.terminal_cases()
    require(cases==R.terminal_cases() and len(cases)==14,'whole independent fourteen-core catalogue')
    known=[];witnesses=[];damages=[]
    universe=set(range(16,22))
    for x,y,u,v in cases:
        n,d,q,c,bits=core(require,(L.C,x,y),(u,v))
        require(q[9:]==(4,4,2,2,4,2,2),'all derived endpoint Q ranks')
        require(c[11,12]==0 and all(c[s,t]==0 for s,t in product((11,12),(14,15))),
                'actual blue SY and four red SY-T spines saturated')
        known.append({'T_X':[L.C,x,y],'SY_X':[u,v],'original16':[sorted(z) for z in n],
                      'actual_degrees':d,'Q_ranks':q,'all120_allowances':[[i,j,a] for (i,j),a in sorted(c.items())]})
        for aa in combinations(range(16,22),2):
            for bb in combinations(sorted(universe-set(aa)),2):
                Aq,Bq=set(aa),set(bb);Cq=universe-Aq-Bq
                for tt in combinations(range(16,22),4):
                    graph=[set(z) for z in n]+[set() for _ in range(6)]
                    roles={1:universe,11:Aq,12:Bq,13:set(tt),14:Cq,15:Cq}
                    for i,row in roles.items():
                        for z in row:graph[i].add(z);graph[z].add(i)
                    Ti=[bits[i]|sum(1<<z for z in Cq) for i in (14,15)]
                    expected=sorted({0,1,13}|Aq|Bq)
                    check_pages(require,(graph[14],graph[15]),Ti,expected)
                    require(all(len(graph[i])==d[i] for i in (11,12,13,14,15)),
                            'all endpoint neighborhoods complete; other free edges irrelevant')
                    witnesses.append([x,y,u,v,aa,bb,tt,expected])
                    if aa==(16,17) and bb==(18,19) and tt==(16,17,18,19):
                        tests=[]
                        duplicate=expected[:];duplicate[-1]=duplicate[-2]
                        selfpage=expected[:];selfpage[-1]=14
                        redpage=expected[:];redpage[-1]=20
                        tests.extend([('duplicate',duplicate,None),('endpoint-page',selfpage,None),
                                      ('red-Q-page',redpage,None),('six-pages',expected[:-1],None),
                                      ('new-red-u',expected,0),('red-spine',expected,15)])
                        for name,claim,add in tests:
                            nn=[set(graph[i]) for i in (14,15)];nb=Ti[:]
                            if add is not None:nn[0].add(add);nb[0]|=1<<add
                            try:check_pages(require,nn,nb,claim)
                            except ValueError:damages.append([x,y,u,v,name])
                            else:raise ValueError('semantic terminal damage accepted: '+name)
            guard()
    require(len(witnesses)==14*90*15,'all14 cores/all90 SY Q roles/all15 T0 Q rows')
    require(len(damages)==84,'six semantic original-page damages rejected at EVERY core')
    return {'complete':True,'whole14_original16_models':known,
            'all18900_literal_bit_seven_BLUE_witnesses':[len(witnesses),digest(witnesses)],
            'all84_semantic_witness_damages_rejected':[len(damages),digest(damages)],
            'arbitrary_T0_Q_rank4_rows':15,'ordered_disjoint_SY_Q_roles':90,
            'any_Q_X_SX_or_Q_Q_completion_can_change_TT_pages':False,
            'old_density_terminal_or_review_verdict_used':False}
