"""Replay the authors' primary21 positive witness, including raw metadata."""
import hashlib,json
from pathlib import Path

def require(condition,message):
    if not condition:raise ValueError(message)

def main():
    raw=Path(__file__).with_name('primary21.txt').read_bytes()
    sha=hashlib.sha256(raw).hexdigest()
    require(sha=='3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55','primary source bytes changed')
    text=raw.decode();depth=0;end=None
    for i,char in enumerate(text):
        if char=='[':depth+=1
        if char==']':
            depth-=1
            if depth==0:end=i+1;break
    require(end is not None,'unclosed primary matrix')
    matrix=json.loads(text[:end]);n=len(matrix)
    require(n==21 and all(type(row) is list and len(row)==n for row in matrix),'wrong primary dimensions')
    require(all(type(v) is int and v in (0,1) for row in matrix for v in row),'nonbinary primary')
    require(all(matrix[i][j]==matrix[j][i] for i in range(n) for j in range(n)),'asymmetric primary')
    red=[set(j for j in range(n) if j!=i and matrix[i][j]==0) for i in range(n)]
    blue=[set(range(n))-{i}-red[i] for i in range(n)]
    rp=max(len(red[i]&red[j]) for i in range(n) for j in red[i]);bp=max(len(blue[i]&blue[j]) for i in range(n) for j in blue[i])
    edges=sum(map(len,red))//2
    require((edges,rp,bp)==(93,3,6),'known witness check failed')
    print(json.dumps({'order':n,'red_edges':edges,'blue_edges':210-edges,'checked_pairs':210,'red_pages':rp,'blue_pages':bp,'raw_sha256':sha,'primary_prior_art_not_new':True},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
