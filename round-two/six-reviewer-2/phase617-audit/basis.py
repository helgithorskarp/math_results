"""Literal Euler-character basis and occurrence/variable injection checks."""
import json

def need(ok,why):
    if not ok:raise ValueError(why)

def run():
    p=617;N=3704;roots=[n for n in range(N)if n%p in (0,1,4)];root_tags={n:49+i for i,n in enumerate(roots)};chi=[None]+[int(pow(r,308,p)==p-1)for r in range(1,p)];tags=[];slots=[{}for _ in range(6)]
    for n in range(N):
        if n in root_tags:tag=root_tags[n]
        else:
            k=4*chi[n%p]+2*chi[(n-1)%p]+chi[(n-4)%p];tag=6*k+n%6+1
            if n<632:slots[n%6].setdefault(k,n)
        tags.append(tag)
    need(all(set(v)==set(range(8))for v in slots),'all48 phase table slots actual by632')
    need(set(tags)==set(range(1,69)),'every68 actual variable realized')
    need(len(roots)==20 and len(set(root_tags.values()))==20,'independent root occurrences')
    need(tags[0]!=tags[617] and tags[1]!=tags[618] and tags[4]!=tags[621],'different same-column occurrences independent')
    for a in [0,1]:need(len(set(tags[a+j*617]for j in range(7)))==7,'every actual endpoint root AP independent')
    return dict(status='WHOLE_FIELD_BASIS_CHECKED',P=p,N=N,root_positions=roots,variable_tags=tags,regular_slot_witnesses=[[[k,n]for k,n in sorted(v.items())]for v in slots])
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,separators=(',',':')))
