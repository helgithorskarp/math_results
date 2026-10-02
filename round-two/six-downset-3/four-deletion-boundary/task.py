"""One finite mathematical phase, called serially by verify.py."""
import json,sys
from matrices import whole,require,digest
import negative,orbits


def positive(q):
    X,N,s,C,U,L,M,rec=whole(q)
    rec['orbit_certificate']=orbits.verify(q,C,U)
    rec.update(agent='six-downset-3',role='researcher',scope='original finite k4 certificate; full-rank bridge unformalized')
    rec['record_sha256']=digest(rec);return rec


if __name__=='__main__':
    if sys.argv[1]=='negative':rec=negative.run()
    elif sys.argv[1]=='positive':rec=positive(int(sys.argv[2]))
    elif sys.argv[1]=='controls':
        import controls;rec=controls.run()
    else:raise ValueError('unknown finite task')
    print(json.dumps(rec,sort_keys=True,indent=2))
