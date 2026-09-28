"""Make a complete source word and position masks for domain_score.cpp."""
import argparse
import json
from pathlib import Path

from check import defects
from encode import HERE


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--case',required=True)
    p.add_argument('--start',required=True)
    p.add_argument('--word-out',type=Path,required=True)
    p.add_argument('--mask-out',type=Path,required=True)
    a=p.parse_args()
    sources=json.loads((HERE/'sources.json').read_text(encoding='ascii'))
    cases=json.loads((HERE/'cases.json').read_text(encoding='ascii'))
    aligned=[]
    start=None
    for name,perm in cases[a.case]:
        word=''.join(perm[int(d)-1] for d in sources[name]['word'])
        aligned.append(word)
        if name==a.start and start is None: start=word
    assert start is not None
    domains=[{int(word[v]) for word in aligned} for v in range(537)]
    assert all(len(domain)>=2 for domain in domains),\
        'domain_score.cpp requires at least two choices at each position'
    masks=[sum(1<<(c-1) for c in domain) for domain in domains]
    assert all(mask&(1<<(int(start[v])-1)) for v,mask in enumerate(masks))
    a.word_out.write_text(start+'\n',encoding='ascii')
    a.mask_out.write_text(' '.join(map(str,masks))+'\n',encoding='ascii')
    print(f'case={a.case} start={a.start} initial_defects={defects(start)} '
          f'mask_count={len(masks)} domain_histogram='
          f'{[sum(len(d)==k for d in domains) for k in range(1,7)]}')


if __name__=='__main__': main()
