"""Actual malformed positive records and universal-bridge boundary controls."""
import argparse,csv,json
from pathlib import Path
from check import check_row,require,label,char
def rejected(row):
    try:check_row(row)
    except (ValueError,StopIteration):return True
    return False
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);args=ap.parse_args()
    rows=[list(map(int,r)) for r in csv.reader(Path(args.input).read_text().splitlines())]
    fixture=next(r for r in rows if r[0]==1 and r[1]==0)
    require(not rejected(fixture),'true constant fixture')
    mutations=[]
    r=fixture[:-1];mutations.append(('missing_coordinate',r))
    r=fixture.copy();r[0]=0;mutations.append(('zero_scale',r))
    r=fixture.copy();r[1]=1;mutations.append(('palette_gauge',r))
    r=fixture.copy();r[3]=0;mutations.append(('zero_step',r))
    r=fixture.copy();r[3]=51;mutations.append(('unproved_step51_bound',r))
    r=fixture.copy();r[2]=103;mutations.append(('noncanonical_start',r))
    r=fixture.copy();r[2:4]=[0,1];mutations.append(('original_free_column',r))
    r=fixture.copy();r[4:6]=r[2:4];mutations.append(('overlapping_support',r))
    r=fixture.copy()
    labels={label((r[2]+j*r[3])%103,0,1) for j in range(7)}
    require(len(labels)>1,'damage fixture labels')
    k=next(k for k in sorted(labels) if k!=0)
    r[1]=1<<k;mutations.append(('actual_nonmonochromatic_colors',r))
    require(all(rejected(r) for name,r in mutations),'accepted damaged actual witness')
    # Every finite residue of m, including noncoprime m, is inspected.
    inverses=[]
    for residue in range(103):
        inv=[k for k in range(103) if residue*k%103==1]
        require(len(inv)==(residue!=0),'coprime CRT boundary')
        if inv:inverses.append(inv[0])
    require(set(inverses)==set(range(1,103)),'inverse bijection')
    for u in range(1,103):
        transformed=[sum(((w>>(k^(7*char(u))))&1)<<k for k in range(8)) for w in range(0,256,2)]
        gauged=[w^255 if w&1 else w for w in transformed]
        require(set(gauged)==set(range(0,256,2)),'complete truth-table absorption')
    print(json.dumps({'true_fixture':True,'damage_names':[n for n,r in mutations],
        'damages_rejected':len(mutations),'all103modulus_residues':True,
        'all102truth_table_bijections':True},sort_keys=True))
if __name__=='__main__':main()
