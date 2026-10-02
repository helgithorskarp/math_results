"""Compact exact missing-edge certificates and an exhaustive local-lemma test.

Family coverage is supplied separately by the complete four-promotion census.
Markers certify pointwise blue-B7 saturation of every q9 boundary graph.
"""
from collections import Counter
from copy import deepcopy
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import sys
import time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import literal
import model as m


def book_free(rows,b):
    return all(sum(w in rows[u] and w in rows[v] for w in range(len(rows))) < b
               for u,v in combinations(range(len(rows)),2) if v in rows[u])


def local_marker(blue,u,v,b):
    common=sorted(blue[u]&blue[v])
    if len(common)>=b:
        return [u,v,-1,-1]
    for w in common:
        for endpoint in (u,v):
            if len(blue[endpoint]&blue[w])==b-1:
                return [u,v,w,endpoint]
    return None


def local_lemma_test():
    graphs,eligible,flips=0,0,0
    for n in range(1,6):
        pairs=list(combinations(range(n),2))
        for mask in range(1 << len(pairs)):
            rows=[set() for _ in range(n)]
            for i,(u,v) in enumerate(pairs):
                if mask >> i & 1:
                    rows[u].add(v);rows[v].add(u)
            graphs+=1
            for b in range(1,6):
                if not book_free(rows,b):
                    continue
                eligible+=1
                for u,v in pairs:
                    if v in rows[u]:
                        continue
                    marker=local_marker(rows,u,v,b)
                    changed=[set(row) for row in rows]
                    changed[u].add(v);changed[v].add(u)
                    m.need((marker is None)==book_free(changed,b),'local lemma vs all literal spines')
                    flips+=1
    return dict(graphs=graphs,book_free_graph_threshold_pairs=eligible,
                literal_missing_edge_flips=flips,orders=[1,2,3,4,5],page_thresholds=[1,2,3,4,5])


def action(u):
    return 21 if u==21 else 3*(u//3)+(u+1)%3


def edge_orbit(u,v):
    out=[]
    for t in range(3):
        out.append(tuple(sorted((u,v))));u,v=action(u),action(v)
    m.need(len(set(out))==3,'free edge orbit')
    return out


def check(controls):
    geometry=literal.geometry()
    counts=Counter()
    seen=set()
    for control in controls:
        J,P,D=control['J'],control['P'],control['D']
        for values,size,high in ((J,3,7),(P,4,35),(D,9,35)):
            m.need(type(values) is list and len(values)==size and
                   all(type(v) is int and 0<=v<high for v in values) and
                   values==sorted(set(values)), 'boundary recipe domain')
        m.need(type(control['index']) is int and 0<=control['index']<305874 and
               type(control['weight']) is int and control['weight'] in (1,2,3,6), 'boundary case/weight')
        m.need(len(D)==9 and tuple(sorted(set(D)))==tuple(D),'boundary deletion domain')
        key=(tuple(J),tuple(P),tuple(D))
        m.need(key not in seen,'duplicate boundary graph recipe')
        seen.add(key)
        red=literal.rows(geometry,J,P,D)
        blue=[set(range(22))-row-{u} for u,row in enumerate(red)]
        m.need(book_free(blue,7) and sum(map(len,red))==198,'actual boundary blue cap/99 edges')
        representatives={min(edge_orbit(u,v)) for u,v in m.PAIRS if v in red[u]}
        m.need(len(representatives)==33,'33 remaining red edge orbits')
        m.need(len(control['markers'])==33 and
               {tuple(x[:2]) for x in control['markers']}==representatives,'complete orbit marker coverage')
        covered=set()
        for marker in control['markers']:
            m.need(type(marker) is list and len(marker)==4 and all(type(x) is int for x in marker),
                   'marker encoding')
            u,v,w,endpoint=marker
            m.need(0<=u<v<22 and (w==-1 and endpoint==-1 or
                   0<=w<22 and endpoint in (u,v)), 'marker domain')
            for step in range(3):
                pair=tuple(sorted((u,v)))
                m.need(pair not in covered and v in red[u],'expanded red edge/domain')
                covered.add(pair)
                common=blue[u]&blue[v]
                if w==-1:
                    m.need(len(common)>=7,'new spine marker pages')
                    counts['new_spine_markers']+=1
                else:
                    m.need(w in common and len(blue[endpoint]&blue[w])==6,'existing spine marker pages')
                    counts['existing_spine_markers']+=1
                # Independent direct changed-graph audit of every expanded edge.
                changed=[set(row) for row in blue]
                changed[u].add(v);changed[v].add(u)
                m.need(not book_free(changed,7),'literal expanded missing-edge addition')
                u,v=action(u),action(v)
                if w!=-1:
                    w,endpoint=action(w),action(endpoint)
            counts['orbit_markers']+=1
        m.need(covered=={(u,v) for u,v in m.PAIRS if v in red[u]},'all 99 literal red spines covered')
        counts['controls']+=1
        counts['labeled_controls']+=control['weight']
    m.need(counts['controls']==28 and counts['labeled_controls']==168,'complete supplied boundary inventory')
    return dict(counts)


def main():
    started=time.monotonic()
    work=Path(sys.argv[1])
    geometry=literal.geometry()
    controls=[]
    for path in sorted(work.glob('positive-*.jsonl')):
        with path.open() as stream:
            for line in stream:
                item=json.loads(line)
                if len(item['D'])!=9:
                    continue
                red=literal.rows(geometry,item['J'],item['P'],item['D'])
                blue=[set(range(22))-row-{u} for u,row in enumerate(red)]
                representatives=sorted({min(edge_orbit(u,v)) for u,v in m.PAIRS if v in red[u]})
                markers=[local_marker(blue,u,v,7) for u,v in representatives]
                m.need(all(x is not None for x in markers),'unsaturated boundary edge')
                controls.append(dict(index=item['index'],J=item['J'],P=item['P'],D=item['D'],
                                     weight=item['weight'],markers=markers))
    marker_file=work/'saturation-markers.json'
    marker_file.write_text(json.dumps(controls,separators=(',',':'))+'\n')
    # Decode a fresh serialization, then verify all expanded edges by definitions.
    counts=check(json.loads(marker_file.read_text()))
    lemma=local_lemma_test()
    damages=0
    for damage in ('missing_control','duplicate_control','missing_orbit','wrong_edge','wrong_page'):
        bad=deepcopy(controls)
        if damage=='missing_control':bad.pop()
        elif damage=='duplicate_control':bad.append(deepcopy(bad[0]))
        elif damage=='missing_orbit':bad[0]['markers'].pop()
        elif damage=='wrong_edge':bad[0]['markers'][0][0]=22
        else:
            marker=next(x for x in bad[0]['markers'] if x[2]!=-1)
            marker[2]=marker[0]
        try:
            check(bad)
        except (ValueError,KeyError,IndexError,TypeError):
            damages+=1
        else:
            raise ValueError('corrupted saturation certificate accepted: '+damage)
    m.need(damages==5,'all certificate damages rejected')
    report=dict(status='EXACT_POINTWISE_Q9_BLUE_EDGE_SATURATION',counts=counts,
        local_lemma_test=lemma,damage_rejections=damages,
        markers_bytes=marker_file.stat().st_size,
        markers_sha256=hashlib.sha256(marker_file.read_bytes()).hexdigest(),
        seconds=time.monotonic()-started,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        scope='Pointwise certificates; universal boundary coverage comes separately from the family census. Same author, unformalized.')
    (work/'saturation-summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
