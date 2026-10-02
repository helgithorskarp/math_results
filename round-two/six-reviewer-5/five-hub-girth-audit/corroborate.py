"""Credited late author-schema adapter; imports no author mathematics."""
import hashlib,json
from collections import Counter
from itertools import combinations
from pathlib import Path
import first_check,rows

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def compute(proof,bridge,source):
    expected=json.loads((source/'EXPECTED.json').read_text())['mathematical_result']
    stars=json.loads((source/'fixtures.json').read_text())['stars']
    rows.need(stars==json.loads((Path(__file__).resolve().parent/'fixtures.json').read_text())['stars'],'all23 credited literal stars agree')
    adapted=[]
    for r in proof['rows']:
        adapted.append({'fixture':r['star'],'hub_high':r['hubs'],'h':r['h'],'e':r['e'],'k':r['k'],'q':r['q'],'eligible':r['eligible'],'g1_S':r['g1'],'ss_excess':r['sigma'],'hub_weight':sum(r['delta'][p] for p in r['hubs']),'psi':r['psi'],'margin':r['old_margin'],'I5':r['I5'],'corrected_margin':r['margin']})
    adapted.sort(key=lambda r:(r['fixture'],r['hub_high']))
    old=[{k:v for k,v in r.items() if k not in ['I5','corrected_margin']} for r in adapted]
    rows.need(digest(adapted)==expected['corrected_rows_sha256'] and digest(old)==expected['original_rows_sha256'],'all426 original and corrected row fields')
    exceptional=[r for r in adapted if r['I5']]
    catalog={'actual_rows':len(adapted),'exception_rows':len(exceptional),'minimum_corrected_margin':min(r['corrected_margin'] for r in adapted),'fixture_populations':[sum(r['fixture']==i for r in adapted) for i in range(23)],'all_exception_marks':[{'fixture':r['fixture'],'hub_high':r['hub_high'],'q':r['q'],'original_margin':r['margin'],'corrected_margin':r['corrected_margin']} for r in exceptional]}
    rows.need(catalog==expected['catalog'],'every corrected-catalog coordinate')
    fields=['e','k','q','eligible','h','g1_S','psi','corrected_margin','ss_excess'];branches=[]
    for b in proof['boundaries']:
        # Translate the complete independently computed category records.
        records=[dict(zip(rows.FIELDS,c)) for c in b['categories']]
        categories=[[r[k] for k in ['e','k','q','eligible','h','g1','psi','margin','sigma']] for r in records]
        branches.append({'E':b['E'],'K':b['K'],'N5':0,'Q':b['Q'],'T':1,'W':13,'X':0,'tau':0,'margin_budget':b['margin_budget'],'fields':fields,'categories':categories,'patterns':b['complete_population_vectors']})
    rows.need(branches==expected['boundary_branches'],'every complete boundary category and population')
    rows.need(bridge['coefficients']==expected['coefficients'],'every allm global coefficient')
    graph=expected['abstract_girth_validation'];own=proof['graphs']
    rows.need([graph[k] for k in ['literal_nine_edge_sets','labeled_cubic_six_graphs','triangle_free_cubic_six_graphs','girth_five_cubic_six_graphs']]==[own[k] for k in ['all_nine_edge_sets','cubic','trianglefree_cubic','girth_at_least_five_cubic']],'complete abstract cubic graph populations')
    A=[set() for _ in range(10)]
    for i in range(5):
        for a,b in [(i,(i+1)%5),(i,i+5),(i+5,(i+2)%5+5)]:A[a].add(b);A[b].add(a)
    peterson={'vertices':10,'edges':[[a,b] for a,b in combinations(range(10),2) if b in A[a]],'status':'POSITIVE_ABSTRACT_GRAPH_ONLY','all_root_layers':[{'root':p,'first':sorted(A[p]),'second':sorted({r for q in A[p] for r in A[q]}-{p}-A[p])} for p in range(10)]}
    rows.need(peterson==graph['petersen'],'allactual author Petersen layers')
    raw=(source/'BASELINE69.txt').read_bytes();lines=raw.decode('ascii').splitlines();words=[{i for i,b in enumerate(w) if b=='1'} for w in lines]
    rows.need(len(words)==len(set(map(frozenset,words)))==69 and all(len(w)==5 for w in words),'known primary69 literal words')
    rows.need(all(len(a&b)<=2 for a,b in combinations(words,2)),'known primary69 literal packing')
    distances=Counter(len(a^b) for a,b in combinations(words,2));triples={tuple(sorted(t)) for w in words for t in combinations(w,3)}
    baseline={'words':69,'weight':5,'length':18,'pair_checks':2346,'triple_owners':len(triples),'distance_histogram':{str(k):distances[k] for k in sorted(distances)},'sha256':hashlib.sha256(raw).hexdigest(),'status':'PRIOR69_REPRODUCTION_ONLY'}
    rows.need(baseline==expected['primary69'],'every known primary69 record field')
    return {'all426_original_and_corrected_rows_sha256':[digest(old),digest(adapted)],'every_author_catalog_coefficient_boundary_and_Petersen_field_compared':True,'primary69_known_baseline_compared':True,'all23_input_stars_match':True,'author_controls_are_native_late_corroboration_not_own_damages':True}
