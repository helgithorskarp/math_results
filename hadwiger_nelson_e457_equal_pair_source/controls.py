#!/usr/bin/env python3
"""Small mutation controls for the exact graph and colour-word checks."""
import json
from pathlib import Path
from build import edges

HERE=Path(__file__).resolve().parent
def valid(rows,word):
 if len(rows)!=457 or len({tuple(r) for r in rows})!=457:return False
 es=edges(rows)
 return len(es)==2329 and len(word)==457 and word[0]==word[1] and all(word[u]!=word[v] for u,v in es)
def main():
 x=json.loads((HERE/'core.json').read_text());rows=x['points'];word=x['equal_four_colouring'];assert valid(rows,word);rejected=0
 bad=[r[:] for r in rows];bad[2][0]+=1;rejected+=not valid(bad,word)
 bad=[r[:] for r in rows];bad[2]=bad[3][:];rejected+=not valid(bad,word)
 bad=word[:];bad[0]=(bad[0]+1)%4;rejected+=not valid(rows,bad)
 bad=word[:];u,v=edges(rows)[0];bad[v]=bad[u];rejected+=not valid(rows,bad)
 assert rejected==4;print(json.dumps({'positive_control':True,'mutations_rejected':rejected},sort_keys=True))
if __name__=='__main__':main()

