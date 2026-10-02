"""Additional dependency audit: independently close P20 using same row/graph engine.
Written after main9535 audit seal, before inspecting author source; P20 defining
9436/9313 mathematics already read. This is a separate credited boundary replay.
"""
from independent import *

def compute():
    physical=json.loads((P/'independent-physical.json').read_text());types=physical['types'];hist=physical['histograms'];admissible=set(map(int,physical['accepted_types']));cases_out=[];counts=collections.Counter();generic=[];generic_counts=collections.Counter()
    for Q,T,X,tau in it.product(range(5),range(3),range(3),range(2)):
        cost=Q+2*T+2*X+4*tau
        if cost>4:continue
        E=12-Q-T-2*tau;case={'Q':Q,'T':T,'X':X,'tau':tau,'E':E,'K':20-E+2*X,'budget':3*(4-cost)}
        vectors0,states0=census(types,case,None);generic_rows=[]
        for v in vectors0:
            check=graph_cut(expand_vertices(types,hist,v),case);generic_counts[check['stage']]+=1
            need(check['stage']!='survives','UNEXCLUDED raw generic P20 population')
            generic_rows.append({'counts':v,'graph':check})
        generic.append({'case':case,'count_states':states0,'records':generic_rows})
        vectors,states=census(types,case,admissible);rows=[]
        for v in vectors:
            check=graph_cut(expand_vertices(types,hist,v),case);counts[check['stage']]+=1
            need(check['stage']!='survives','UNEXCLUDED P20 population; dependency reduction incomplete')
            rows.append({'counts':v,'graph':check})
        cases_out.append({'case':case,'count_states':states,'records':rows})
    result={'scope':'Independent P20 exclusion from8323/8933/9249 and9313 P>=20, ordinary radius rederived; no9436 numerical premise required for independent9535 confirmation. No claim to rerun9436 native source.','all_cases':cases_out,'stage_totals':dict(counts),'generic_baseline_cases':generic,'generic_baseline_stage_totals':dict(generic_counts)}
    (P/'independent-boundary20.json').write_bytes(enc(result));print(json.dumps({'cases':len(cases_out),'generic_vectors':sum(len(c['records']) for c in generic),'generic_stages':dict(generic_counts),'vectors':sum(len(c['records']) for c in cases_out),'stages':dict(counts),'sha256':sha(result)}),flush=True)
    return result
if __name__=='__main__':compute()
