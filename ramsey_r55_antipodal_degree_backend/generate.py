"""One exact, certificate-aware SAT backend for the fixed H92 projection.

523 graph bits + 208 monotone residual bits. Binary full-adder circuits
encode 43 degree equations, two densities, three balances, and 45 cuts.
No graph symmetry and no extra full-K5 constraint is imposed.
"""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
PARENT = ROOT/'ramsey_r55_antipodal_degree_projection'
PINS = {'model.py':'f93bc5bdb33f920f4c1483652c6fa8478da76464f57d97ece7898f4bdafb7afd',
        'flow.py':'fa9aa09354729c704a5065b8dd7cbefe50a620c048533f23632c0173f2e8dab0',
        'H92.json':'926c18173764c02a45d6e6d46dc001eddff6a161570bdc3b1efcd8a24539f466',
        'PROOF.md':'f10926ef9d8c7a6f1b26825989c840ba9e8d72712dcdb776ca29bb1645f8a170'}
SOLVER_SHA = '2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45'
DRAT_SHA = '9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a'


def need(ok,message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path,data):
    with path.open('x') as f:
        json.dump(data,f,sort_keys=True,indent=2); f.write('\n')


def neg(x):
    return not x if type(x) is bool else -x


class Compiler:
    def __init__(self,variables,clauses):
        self.variables = variables; self.clauses = list(clauses)
        self.fulladders = []; self.counts = []; self.cache = {}; self.constraints = []

    def emit(self,row):
        if any(x is True for x in row):
            return
        xs = sorted(set(x for x in row if x is not False))
        if any(-x in xs for x in xs):
            return
        self.clauses.append(tuple(xs))

    def fulladder(self,a,b,c):
        self.variables += 2; s,t = self.variables-1,self.variables
        start = len(self.clauses)
        for values in it.product((False,True),repeat=3):
            row = [neg(x) if val else x for x,val in zip((a,b,c),values)]
            row.append(s if sum(values)%2 else -s)
            self.emit(row)
        self.emit([neg(a),neg(b),t]); self.emit([neg(a),neg(c),t]); self.emit([neg(b),neg(c),t])
        self.emit([a,b,-t]); self.emit([a,c,-t]); self.emit([b,c,-t])
        index = len(self.fulladders)
        self.fulladders.append({'inputs':[a,b,c],'sum':s,'carry':t,
                                'start':start,'end':len(self.clauses)})
        return s,t,index

    def add(self,left,right,carry=False):
        output = []; indices = []; initial = carry
        for i in range(max(len(left),len(right))):
            a = left[i] if i < len(left) else False
            b = right[i] if i < len(right) else False
            s,carry,index = self.fulladder(a,b,carry)
            output.append(s); indices.append(index)
        output.append(carry)
        return {'left':left,'right':right,'carry_in':initial,'output':output,'fulladders':indices}

    def count(self,literals):
        key = tuple(sorted(literals))
        if key in self.cache:
            return self.cache[key]
        words = [[x] for x in key]; additions = []
        while len(words) > 1:
            following = []
            for i in range(0,len(words),2):
                if i+1 == len(words):
                    following.append(words[i]); continue
                addition = self.add(words[i],words[i+1]); additions.append(addition)
                following.append(addition['output'])
            words = following
        index = len(self.counts)
        self.counts.append({'inputs':list(key),'additions':additions,'output':words[0] if words else []})
        self.cache[key] = index
        return index

    def enforce(self,definition):
        row = dict(definition); left = self.count(row['left']); row['left_count'] = left
        A = self.counts[left]['output']
        if row['kind'] == 'constant':
            k = row['equals']; start = len(self.clauses)
            if not 0 <= k < (1 << len(A)):
                self.emit([])
            else:
                for i,x in enumerate(A):
                    self.emit([x if k >> i & 1 else neg(x)])
            row['start'],row['end'] = start,len(self.clauses)
        else:
            right = self.count(row['right']); row['right_count'] = right
            B = self.counts[right]['output']; n = max(len(A),len(B))
            a = A+[False]*(n-len(A)); b = B+[False]*(n-len(B))
            if row['kind'] == 'balance':
                start = len(self.clauses)
                for x,y in zip(a,b):
                    self.emit([neg(x),y]); self.emit([x,neg(y)])
                row['start'],row['end'] = start,len(self.clauses)
            else:
                need(row['kind'] == 'cut','constraint kind')
                # A <= B iff B + complement(A) + 1 has unsigned carry out.
                addition = self.add(b,[neg(x) for x in a],True)
                row['comparison'] = addition
                row['start'] = len(self.clauses)
                self.emit([addition['output'][-1]])
                row['end'] = len(self.clauses)
        self.constraints.append(row)


def build():
    for name,digest in PINS.items():
        need(sha(PARENT/name) == digest,'parent source identity: '+name)
    sys.path.insert(0,str(PARENT)); from model import Model
    model = Model(); descriptor = model.descriptor()
    physical = ('p cnf 523 70848\n'+''.join(' '.join(map(str,c))+' 0\n' for c in model.clauses)).encode()
    descriptor['neighborhood_cnf_sha256'] = hashlib.sha256(physical).hexdigest()
    upper = {}
    for L,R in model.blocks:
        upper.update({v:len(R) for v in L}); upper.update({v:len(L) for v in R})
    margin = {}; last = 523
    for v in sorted(upper):
        margin[v] = list(range(last+1,last+1+upper[v])); last += upper[v]
    need(last == 731,'208 margin bits')
    enc = Compiler(last,model.clauses); base = len(enc.clauses)
    for v in sorted(margin):
        for a,b in zip(margin[v],margin[v][1:]):
            enc.emit([-b,a])
    monotone_end = len(enc.clauses)
    for row in model.residuals:
        v = row['vertex']
        enc.enforce({'tag':f'degree-{v}','kind':'constant',
                     'left':row['subtract_variables']+margin.get(v,[]),'equals':row['constant']})
    for row in model.densities:
        enc.enforce({'tag':f'density-{row["root"]}','kind':'constant',
                     'left':row['sum_variables'],'equals':row['equals']})
    for block,(L,R) in enumerate(model.blocks):
        left = [x for v in L for x in margin[v]]; right = [x for v in R for x in margin[v]]
        enc.enforce({'tag':f'balance-{block}','kind':'balance','left':left,'right':right})
        for mask in range(1,16):
            S = [L[i] for i in range(4) if mask>>i&1]
            enc.enforce({'tag':f'cut-{block}-{mask}','kind':'cut',
                         'left':[x for v in S for x in margin[v]],
                         'right':[x for v in R for x in margin[v][:len(S)]]})
    meta = {'format':'r55-projected-binary-backend-v1','physical_variables':523,
            'margin_variables':208,'variables':enc.variables,'clauses':len(enc.clauses),
            'base_clauses':base,'monotone_end':monotone_end,'margins':margin,
            'fulladders':enc.fulladders,'counts':enc.counts,'constraints':enc.constraints,
            'parent_source_pins':PINS,'projection':descriptor}
    return model,enc,meta


def status(code,output):
    expected = {0:'s UNKNOWN',10:'s SATISFIABLE',20:'s UNSATISFIABLE'}
    need(code in expected,'solver exit code')
    need([s for s in output.splitlines() if s.startswith('s ')] == [expected[code]],'exact solver status')
    return {0:'UNKNOWN',10:'SAT_PENDING_LIFT_AUDIT',20:'UNSAT_PENDING_PROOF'}[code]


def main():
    p = argparse.ArgumentParser(); p.add_argument('--work',type=Path,required=True)
    p.add_argument('--kissat',type=Path); p.add_argument('--seconds',type=int,default=90)
    p.add_argument('--drat-trim',type=Path); p.add_argument('--emit-only',action='store_true')
    a = p.parse_args(); need(a.seconds > 0,'positive cap'); a.work.mkdir(exist_ok=False)
    t = time.monotonic(); model,enc,meta = build(); cnf = a.work/'case.cnf'
    with cnf.open('x') as f:
        f.write(f'p cnf {enc.variables} {len(enc.clauses)}\n')
        for row in enc.clauses:
            f.write(' '.join(map(str,row))+' 0\n')
    dump(a.work/'encoding.json',meta)
    report = {'status':'EMITTED','variables':enc.variables,'clauses':len(enc.clauses),
              'physical_variables':523,'margin_variables':208,
              'fulladder_count':len(enc.fulladders),'count_circuits':len(enc.counts),
              'constraint_count':len(enc.constraints),'source_sha256':sha(Path(__file__)),
              'formula_sha256':sha(cnf),'formula_bytes':cnf.stat().st_size,
              'encoding_sha256':sha(a.work/'encoding.json'),'build_seconds':time.monotonic()-t,
              'solver_cap_seconds':a.seconds,'scope':'exact projected six-neighborhood subsystem; not all full-K5 constraints'}
    dump(a.work/'interface.json',report); print(json.dumps(report),flush=True)
    if a.emit_only:
        return
    need(a.kissat is not None and sha(a.kissat) == SOLVER_SHA,'solver identity')
    need(a.drat_trim is not None and sha(a.drat_trim) == DRAT_SHA,'proof checker identity')
    log = a.work/'solver.log'; trace = a.work/'trace.drat'; started = time.monotonic()
    with log.open('x') as f:
        code = subprocess.run([str(a.kissat),f'--time={a.seconds}',str(cnf),str(trace)],
                              stdout=f,stderr=subprocess.STDOUT,timeout=a.seconds+30).returncode
    output = log.read_text()
    report.update(status=status(code,output),solver_exit=code,solver_seconds=time.monotonic()-started,
                  solver_sha256=SOLVER_SHA,trace_sha256=sha(trace),trace_bytes=trace.stat().st_size,
                  log_sha256=sha(log),max_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    # The pending record preserves a completed proof before the check starts.
    dump(a.work/'pending.json',report)
    if code == 10:
        values = {}
        for line in output.splitlines():
            if line.startswith('v '):
                for token in line.split()[1:]:
                    x = int(token)
                    if x:
                        need(abs(x) not in values or values[abs(x)] == (x>0),'consistent assignment')
                        values[abs(x)] = x>0
        need(set(values) == set(range(1,enc.variables+1)),'complete model')
        need(all(any(values[abs(x)] == (x>0) for x in row) for row in enc.clauses),'all CNF clauses')
        physical = [values[i] for i in range(1,524)]; evaluation = model.evaluate(physical)
        need(evaluation['satisfies_complete_projected_system'],'mixed-model semantic evaluation')
        graph = model.complete_degrees(physical)
        dump(a.work/'graph.json',graph); dump(a.work/'evaluation.json',evaluation)
        report['status'] = 'SAT_MODEL_AND_PROJECTED_CONDITIONS_CHECKED_LIFT_PENDING_INDEPENDENT_AUDIT'
        report['graph_sha256'] = sha(a.work/'graph.json')
    elif code == 20:
        started = time.monotonic()
        with (a.work/'drat.log').open('x') as f:
            checked = subprocess.run([str(a.drat_trim),str(cnf),str(trace)],stdout=f,stderr=subprocess.STDOUT,timeout=600)
        prooflog = (a.work/'drat.log').read_text()
        need(checked.returncode == 0 and 's VERIFIED' in prooflog and 'NOT VERIFIED' not in prooflog,'full DRAT verification')
        report.update(status='UNSAT_FULL_DRAT_CHECKED',drat_seconds=time.monotonic()-started,
                      drat_sha256=DRAT_SHA,drat_log_sha256=sha(a.work/'drat.log'))
    report['total_seconds'] = time.monotonic()-t
    dump(a.work/'result.json',report); print(json.dumps(report),flush=True)


if __name__ == '__main__':
    main()
