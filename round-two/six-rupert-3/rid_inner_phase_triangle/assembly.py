"""Assemble all six disjoint products; recheck every actual field control."""
from pathlib import Path
from collections import Counter
import copy,json
from kernel import F,Q,Z,need,digest,structural
HERE=Path(__file__).resolve().parent
RUNTIME={'seconds','peak_kib','optimized','python'}

def assemble(parts,forest):
    need(len(parts)==6 and sorted(r['part'] for r in parts)==list(range(6)),'missing/duplicate complete18-root product')
    entries=structural(forest);common=None;counts=Counter();records=[];minimum=None;location=None;roots=set()
    for record in sorted(parts,key=lambda r:r['part']):
        part=record['part'];lo,hi=18*part,18*(part+1)
        need(record['root_interval']==[lo,hi] and record['complete_root_visitation'],'false complete source interval')
        row={k:record[k] for k in ['domain','geometry','forest_sha256','literal_complete_forest_counts']}
        need(common is None or common==row,'part source/receiver hypotheses differ');common=row
        actual=record['all_leaf_control_records'];need(digest(actual)==record['all_leaf_control_records_sha256'],'actual control record hash differs')
        visits=set();local=Counter();localmin=None
        for leaf in actual:
            ri,path,kind=leaf[:3];key=(ri,path)
            need(lo<=ri<hi and key in entries and key not in visits,'incorrect or duplicate leaf address')
            visits.add(key);expected=entries[key];roots.add(ri)
            if kind=='branch':
                need(expected['edge']==leaf[3:5],'midpoint branch differs');local['internal']+=1;continue
            need(kind==expected['kind'] and leaf[3]==expected['cut'],'literal selected cut differs')
            values=[F(Q(a),Q(b)) for a,b in leaf[4]]
            need(len(values)==(40 if kind=='support' else 90),'missing or duplicate degree control')
            need(all(v>F(Q(1,100000)) for v in values),'nonpositive or below-margin actual exact source control')
            local[kind]+=1;local['tensor_coefficients']+=len(values)
            m=min(values);localmin=m if localmin is None else min(localmin,m)
            if minimum is None or m<minimum:
                minimum=m;location={'root':ri,'path':path,'kind':kind,'cut':leaf[3],'coefficient':values.index(m)}
        need(visits=={key for key in entries if lo<=key[0]<hi},'complete product omits a source node')
        need(dict(local)==record['counts'] and localmin==F(*map(Q,record['minimum'])),'actual product count or minimum mismatch')
        counts.update(local);records.extend(actual)
    need(roots==set(range(108)),'whole source domain not covered')
    need(counts['support']+counts['gauge']==108+counts['internal'],'whole closed binary forest count fails')
    return {'agent':'six-rupert-3','role':'researcher','status':'complete exact whole closed receiving-cell source-cover certificate',
            **common,'counts':dict(counts),'minimum':minimum.encode(),'minimum_location':location,
            'margin':'1/100000','all108_roots_covered':True,'all_closed_children_retained':True,
            'all_actual_controls_reparsed_and_rechecked':True,'whole_actual_records_sha256':digest(records),
            'all_source_classification':'lambda=1,physical t=0,original R in G union H_n G on stated ENTIRE closed receiving cell',
            'ordinary_geometric_bridge':'unformalized; PROOF.md supplies the annular collar, original finite fold and closed-cover bridges',
            'independent_review':'NOT RECEIVED for this new result','global_RID':'OPEN'}
