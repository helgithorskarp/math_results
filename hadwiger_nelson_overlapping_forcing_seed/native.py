"""Strict adapter for the native exhaustive checker."""
import json,subprocess

def solve(binary,n,edges,pins=()):
    data=f'{n} {len(edges)} {len(pins)}\n'+''.join(f'{a} {b}\n' for a,b in edges)+''.join(f'{v} {c}\n' for v,c in pins)
    p=subprocess.run([str(binary)],input=data,capture_output=True,text=True,check=True)
    x=json.loads(p.stdout)
    if type(x['satisfiable']) is not bool:raise ValueError('Malformed status')
    answer=x['colouring'] if x['satisfiable'] else None
    if answer is not None:
        if len(answer)!=n or any(type(c) is not int or not 0<=c<4 for c in answer):raise ValueError('Bad colour word')
        if any(answer[a]==answer[b] for a,b in edges) or any(answer[v]!=c for v,c in pins):raise ValueError('Bad positive witness')
    elif x['colouring']:raise ValueError('Colouring supplied with UNSAT')
    return answer,{k:x[k] for k in ('nodes','conflicts')}
