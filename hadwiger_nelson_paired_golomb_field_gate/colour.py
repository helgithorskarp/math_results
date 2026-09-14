from pathlib import Path
import json

def greedy(dom,adj):
 d=list(dom);n=len(d);live=(1<<n)-1;word=[-1]*n
 while live:
  v=min((j for j in range(n)if live>>j&1),key=lambda j:(d[j].bit_count(),-(adj[j]&live).bit_count(),j))
  if not d[v]:return None
  bit=d[v]&-d[v];word[v]=bit.bit_length()-1;live&=~(1<<v)
  for j in range(n):
   if live>>j&1 and adj[v]>>j&1:d[j]&=~bit
 return ''.join(map(str,word))

def checked(word,dom,adj):
 n=len(dom)
 if len(word)!=n or any(c not in '0123'for c in word):raise ValueError('word shape')
 if any(not(dom[i]>>int(word[i])&1)for i in range(n)):raise ValueError('domain colour')
 if any(word[i]==word[j]for i in range(n)for j in range(i)if adj[i]>>j&1):raise ValueError('edge colour')
