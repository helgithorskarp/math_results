"""Bounded protocol for the separately implemented C++ clique checker."""
import json
from pathlib import Path
import select
import subprocess


def check(ok,message):
    if not ok:
        raise ValueError(message)


class Native:
    def __init__(self, executable, graphs):
        self.process=subprocess.Popen([str(Path(executable).resolve())],stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1)
        rows=[str(len(graphs))]
        for adjacent in graphs:
            rows.append(str(len(adjacent)))
            rows.extend(str(len(a))+' '+' '.join(map(str,sorted(a))) for a in adjacent)
        self.process.stdin.write('\n'.join(rows)+'\n')
        self.process.stdin.flush()

    def query(self,gid,vertices,target=9,node_cap=2000000,milliseconds=20000):
        vertices=sorted(vertices)
        text=' '.join(map(str,[gid,target,node_cap,milliseconds,len(vertices)]+vertices))+'\n'
        self.process.stdin.write(text);self.process.stdin.flush()
        ready,_,_=select.select([self.process.stdout],[],[],22)
        check(bool(ready),'INCOMPLETE native protocol timeout')
        line=self.process.stdout.readline()
        if not line:
            check(self.process.wait(timeout=3)==0,'INCOMPLETE native search: '+self.process.stderr.read())
            raise ValueError('missing native completion record')
        result=json.loads(line)
        check(result['status']=='COMPLETE' and type(result['nodes']) is int and result['nodes']<=node_cap,
              'native completion status')
        cliques=result['cliques']
        check(cliques==sorted(cliques) and len({tuple(q) for q in cliques})==len(cliques),'native duplicate solutions')
        check(all(len(q)==target and q==sorted(set(q)) and set(q)<=set(vertices) for q in cliques),
              'native solution domain')
        return cliques,result['nodes']

    def close(self):
        if self.process.stdin and not self.process.stdin.closed:
            self.process.stdin.close()
        if self.process.poll() is None:
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill();self.process.wait(timeout=3)
                raise ValueError('INCOMPLETE native shutdown')
        check(self.process.returncode==0,'INCOMPLETE native exit: '+self.process.stderr.read())

    def __enter__(self):
        return self

    def __exit__(self,kind,value,trace):
        if kind is not None:
            self.process.kill();self.process.wait(timeout=3)
        else:
            self.close()
