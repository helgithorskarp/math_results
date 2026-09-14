"""Discover a compact certificate using general finite domain search."""
from pathlib import Path
import argparse,json
import model as M

T=(5,6,7,8,12,13,14,15)
def produce():
    p=M.construction();e=M.edges(p);positive=[];negative=[]
    for w in M.patterns(8):
        key=''.join(map(str,w));ans=M.solve(16,e,zip(T,w))
        if ans is None:negative.append(key)
        else:positive.append([key,ans])
    ce=M.edges(M.cell())
    single=[[ ''.join(map(str,w)),M.solve(9,ce,zip(range(5,9),w))] for w in M.patterns(4)]
    bad='01020102'
    deleted=[]
    for k in range(8):
        ans=M.solve(16,e,[(v,int(c)) for j,(v,c) in enumerate(zip(T,bad)) if j!=k])
        deleted.append(ans)
    rows=[]
    for point in p:
        row=[c*8 for axis in point for c in axis]
        if any(c.denominator!=1 for c in row):raise ValueError('coordinate denominator')
        rows.append([int(c) for c in row])
    return {'schema':1,'denominator':8,'radicals':M.RAD,'points':rows,
            'single_cell_words':single,'three_colour_word':M.solve(16,e,colours=3),
            'positive':positive,'negative':negative,
            'irreducible_example':bad,'delete_one_pin_words':deleted}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);a=parser.parse_args()
    with a.output.open('x') as f:f.write(json.dumps(produce(),separators=(',',':'))+'\n')
