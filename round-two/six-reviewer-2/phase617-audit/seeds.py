"""Definition-level complete actual progression checks of four endpoint words."""
import json,hashlib

def need(ok,why):
    if not ok:raise ValueError(why)

def run():
    N=3703;p=617;squares={r*r%p for r in range(1,p)};records=[]
    for root_one in [0,3702]:
        for flip in [0,1]:
            word=[(int(n%p not in squares)if n%p else int(n==root_one))^flip for n in range(N)]
            count=0
            for d in range(1,(N-1)//6+1):
                for a in range(N-6*d):
                    count+=1
                    vals={word[a+j*d]for j in range(7)}
                    need(len(vals)==2,'literal monochromatic actual AP')
            records.append(dict(root_one=root_one,palette=flip,APs=count,word_sha256=hashlib.sha256(''.join(map(str,word)).encode()).hexdigest()))
    # Removing the sole exceptional root value creates a real vertical AP.
    bad=[int(n%p not in squares)if n%p else 0 for n in range(N)]
    need({bad[j*p]for j in range(7)}=={0},'actual negative endpoint control')
    return dict(status='FOUR_COMPLETE_ENDPOINT_WORDS_CHECKED',N=N,words=records,damaged_seed_obstruction={'a':0,'d':617,'color':0})
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,separators=(',',':')))
