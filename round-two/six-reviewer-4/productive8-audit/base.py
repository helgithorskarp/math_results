"""Fresh physical-period bitmaps for every BASE marginal, no target imports."""
import argparse,hashlib,json
PERIOD=2520
FIXED=[(8,0),(9,0),(10,1),(14,0),(12,10),(28,4)]
def need(ok,why):
    if not ok:raise ValueError(why)
def digest(obj):return hashlib.sha256((json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
def generate():
    full=(1<<PERIOD)-1
    classes=lambda m,a:sum(1<<n for n in range(a,PERIOD,m))
    R=full
    for m,a in FIXED:R&=full^classes(m,a)
    labels=[m for m in range(8,PERIOD+1) if PERIOD%m==0 and m not in {v[0] for v in FIXED}]
    need(len(labels)==35 and 15 in labels and 18 in labels and 21 in labels,'complete unused BASE originals')
    other=[m for m in labels if m not in (15,18)]
    masks={m:[classes(m,c) for c in range(m)] for m in labels};rows=[]
    for a in range(15):
        for b in range(18):
            F=R&(masks[15][a]|masks[18][b]);remaining=R^F
            marginal=[max((remaining&c).bit_count() for c in masks[m]) for m in other]
            rows.append([a,b,F.bit_count(),marginal,F.bit_count()+sum(marginal)])
    return dict(fixed=[list(v) for v in FIXED],period=PERIOD,initial_holes=R.bit_count(),original_labels=labels,remaining_original_labels=other,raw_phase_pairs=270,rows=rows)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();data=generate();open(a.output,'w').write(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(dict(record_sha256=digest(data),whole_row_sha256=digest(data['rows']),initial_holes=data['initial_holes'],complete_original_marginals=270*33,phase_intersections=270*sum(data['remaining_original_labels']),minimum_union_upper=min(r[-1] for r in data['rows']),maximum_union_upper=max(r[-1] for r in data['rows']),base_hole_lower=data['initial_holes']-max(r[-1] for r in data['rows'])),sort_keys=True))
if __name__=='__main__':main()
