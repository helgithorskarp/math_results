"""Offline verifier; frozen initial core plus explicit later radius/slack algebra.

The initial auxiliary slack identity formally sets g=a^-3. It is an algebra
diagnostic, not a uniform reciprocal bound. Here the actual g=r^-3 remains
independent until the written proof bounds |g-1|<4eta. This later explanatory
layer was written after author replay; its chronology is explicit.
"""
from pathlib import Path
import hashlib,importlib.util,json,sys
here=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('independent_energy_core',here/'audit.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)

def supplement():
    Q=c.Q;v={k:c.tok(k) for k in ['a','eta','V','Q','M2','E','tail','g','F','M']}
    a,e,V,q,m2,E,t,g,F,M=[v[k] for k in ['a','eta','V','Q','M2','E','tail','g','F','M']]
    rows={}
    def equal(name,l,r):c.need(l==r,name);rows[name]=c.pack(l)
    lower=c.add(c.sc(c.tok('a',-1),8),c.sc(c.mul(M,c.tok('a',-2)),8),c.sc(c.mul(m2,c.tok('a',-3)),-4),c.sc(c.mul(c.add(V,c.sc(q,3)),g),Q(1,4)),c.sc(t,-1))
    solved=c.sc(c.prod([c.pw(a,2),c.add(F,c.sc(c.tok('a',-1),-8),c.sc(c.mul(m2,c.tok('a',-3)),4),c.sc(c.mul(c.add(V,c.sc(q,3)),g),Q(-1,4)),t)]),Q(1,8))
    equal('actual-g-mean-convexity',c.sub(lower,{'M':solved}),F)
    slack=c.add(e,c.sc(c.pw(e,2),Q(-1,2)),c.sc(c.mul(a,M),Q(3,2)),c.sc(m2,Q(-3,2)),c.sc(q,Q(3,28)),E)
    exact=c.sub(c.sub(slack,{'M':solved}),{'F':c.add(c.cn(8),c.sc(e,3))})
    rhs=c.add(c.sc(e,Q(1,16)),c.sc(c.pw(e,2),Q(13,16)),c.sc(c.pw(e,3),Q(3,16)),c.sc(c.pw(e,4),Q(-9,16)),c.sc(m2,Q(-3,4)),c.sc(c.prod([c.pw(a,3),g,c.add(V,c.sc(q,3))]),Q(-3,64)),c.sc(q,Q(3,28)),c.sc(c.mul(c.pw(a,3),t),Q(3,16)),E)
    mapping={'a':c.add(c.cn(1),c.sc(e,-1))}
    equal('whole-actual-g-slack',c.sub(exact,mapping),c.sub(rhs,mapping))
    error=c.sc(c.prod([c.pw(a,3),c.add(g,c.cn(-1)),c.add(V,c.sc(q,3))]),Q(-3,64))
    equal('whole-radius-slack-error',c.add(rhs,c.sc(c.sub(rhs,{'g':c.cn(1)}),-1)),error)
    # Use F-8/a <= -5eta and |g-1|<4eta, |V+3Q|<=4V.
    weak=c.add(e,c.sc(c.pw(e,2),Q(-1,2)),c.sc(c.mul(c.pw(a,3),e),Q(-15,16)),c.sc(m2,Q(-3,4)),c.sc(c.mul(c.pw(a,3),c.add(V,c.sc(q,3))),Q(-3,64)),c.sc(q,Q(3,28)),c.sc(c.mul(c.pw(a,3),t),Q(3,16)),c.sc(c.prod([c.pw(a,3),e,V]),Q(3,4)),E)
    expanded=c.add(c.sc(e,Q(1,16)),c.sc(V,Q(-3,64)),c.sc(q,Q(-15,448)),c.sc(m2,Q(-3,4)),c.sc(c.mul(c.add(c.cn(1),c.sc(c.pw(a,3),-1)),e),Q(15,16)),c.sc(c.pw(e,2),Q(-1,2)),c.sc(c.mul(c.add(c.cn(1),c.sc(c.pw(a,3),-1)),c.add(V,c.sc(q,3))),Q(3,64)),c.sc(c.prod([c.pw(a,3),e,V]),Q(3,4)),c.sc(c.mul(c.pw(a,3),t),Q(3,16)),E)
    equal('whole-safe-actual-slack-decomposition',weak,expanded)
    return {'chronology':'later explanatory layer after author replay; original core/fixture unchanged','entire_identities':rows,'ordinary_majorant':'-P+E <= eta/16+45eta^2/16+21eta V/16+3tail/16+E, by actual-g convergence, positive a, |Q|<=V, 1-a^3<=3eta and the negative variance/mean-square terms. Not a formal inequality proof.'}

def main():
    seal=json.loads((here/'INDEPENDENCE.json').read_text())
    for f,h in seal['frozen_source_sha256'].items():c.need(hashlib.sha256((here/f).read_bytes()).hexdigest()==h,'initial sealed bytes '+f)
    original=c.build();c.typed(original,json.loads((here/'EXPECTED.json').read_text()))
    record=supplement();path=here/'SUPPLEMENT.json'
    if '--write' in sys.argv:path.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    else:c.typed(record,json.loads(path.read_text()))
    print(json.dumps({'status':'PASS','initial_record_sha256':c.digest(original),'supplement_sha256':c.digest(record),'whole_initial_identities':20,'later_actual_g_identities':len(record['entire_identities']),'strict_margins':55,'literal_controls':6},sort_keys=True))
if __name__=='__main__':main()
