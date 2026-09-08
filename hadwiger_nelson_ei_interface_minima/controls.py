"""Small exhaustive comparison and malformed-certificate controls."""
import copy
import itertools
import json
import tempfile
from pathlib import Path
import verify

def main():
    small=0
    for n in range(2,5):
        pairs=list(itertools.combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            edges=[p for j,p in enumerate(pairs) if mask>>j&1]
            for triple in [None]+list(itertools.combinations(range(n),3)):
                constraints=edges+([] if triple is None else [triple])
                for equal in (False,True):
                    brute=any(word[0]==0 and word[1]==(0 if equal else 1)
                              and all(len({word[v] for v in t})>1 for t in constraints)
                              for word in itertools.product(range(4),repeat=n))
                    actual,_=verify.decide(n,constraints,equal)
                    verify.require(actual==brute,'small-case disagreement')
                    small+=1
    original=json.loads((verify.ROOT/'certificate.json').read_text())
    corruptions=[]
    c=copy.deepcopy(original);c['g40']['essential_words'][0]='0'*40;corruptions.append(c)
    c=copy.deepcopy(original);c['g49']['essential_words'][0]=c['g49']['essential_words'][0][:-1];corruptions.append(c)
    c=copy.deepcopy(original);c['g40']['patterns'][0]['mask']^=1024;corruptions.append(c)
    c=copy.deepcopy(original);c['g49']['essential'].pop();c['g49']['essential_words'].pop();corruptions.append(c)
    c=copy.deepcopy(original);c['g40']['minimal_covers'].pop();corruptions.append(c)
    c=copy.deepcopy(original);c['g40']['disjoint_obstructions'][0]=c['g40']['disjoint_obstructions'][1];corruptions.append(c)
    c=copy.deepcopy(original);c['g40']['optional'].reverse();corruptions.append(c)
    rejected=0
    for c in corruptions:
        try:verify.check(c)
        except (ValueError,KeyError,IndexError):rejected+=1
        else:raise ValueError('accepted corrupted certificate')
    saved=verify.ROOT
    with tempfile.TemporaryDirectory(prefix='hn-ei-control-') as tmp:
        verify.ROOT=Path(tmp)
        data=json.loads((saved/'g40.json').read_text());data[0][0]+=1
        (verify.ROOT/'g40.json').write_text(json.dumps(data))
        try:verify.geometric_graph('g40')
        except ValueError:rejected+=1
        else:raise ValueError('accepted corrupted source')
        finally:verify.ROOT=saved
    print(json.dumps({'small_complete_cases':small,'malformed_controls_rejected':rejected},sort_keys=True))

if __name__=='__main__':main()
