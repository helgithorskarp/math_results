"""Independent rational-root controls, reversal symmetry and rejected faults."""
import argparse
import copy
import json
from pathlib import Path
import random
import shutil
import tempfile
import sympy as s
import algebra as A
import verify as V


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work',type=Path,required=True)
    args=parser.parse_args()
    geometry=V.independent_contacts()
    M,addresses,generic,unit,collision=geometry
    factors,pieces,identities=V.verify_proposals(args.work,*geometry)
    reverse=lambda v:49*(v%7)+7*((v//7)%7)+v//49
    reversal_pairs=0
    for family in (unit,collision):
        for p,pairs in family.items():
            reflected=A.canonical([((-1)**i*a,(-1)**i*b)for i,(a,b)in enumerate(p)])
            images={tuple(sorted((reverse(a),reverse(b))))for a,b in pairs}
            V.require(reflected in family and images=={tuple(e)for e in family[reflected]},
                      'complete parameter-reversal incidence')
            reversal_pairs+=len(pairs)
    for a in range(-8,9):
        for b in range(-8,9):
            V.require(A.sign((a,b))==int(s.sign(a+b*s.sqrt(33))),'quadratic sign control')
    roots={f:A.real_roots(f)for f in factors}
    chosen=random.Random(343508).sample(factors,200)
    T=s.Symbol('t')
    for f in chosen:
        conjugate=tuple((a,-b)for a,b in f)
        norm=A.multiply(f,conjugate)
        V.require(all(b==0 for a,b in norm),'rational polynomial norm')
        rational=s.Poly.from_list([a for a,b in norm[::-1]],gens=T,domain=s.QQ).sqf_part()
        shared=A.pgcd(f,conjugate)
        predicted=roots[f]+A.real_roots(conjugate)-A.real_roots(shared)
        V.require(predicted==rational.count_roots(-s.oo,s.oo),'independent rational root count')
    fixtures=[([(1,0)],0),([(-1,0),(0,0),(1,0)],2),
              ([(1,0),(0,0),(1,0)],0),([(0,0),(-1,0),(0,0),(1,0)],3),
              ([(1,0),(-4,0),(6,0),(-4,0),(1,0)],1),
              ([(-33,0),(0,0),(0,0),(0,0),(1,0)],2)]
    for p,n in fixtures:V.require(A.real_roots(p)==n,'root multiplicity fixture')

    rejected=[]
    def rejection(name,call):
        try:call()
        except ValueError as error:rejected.append({'case':name,'reason':str(error)})
        else:raise RuntimeError('fault accepted: '+name)
    with tempfile.TemporaryDirectory(prefix='moser-cube-controls-')as temp:
        work=Path(temp)
        for name in ('contacts.json','factorizations.json'):
            shutil.copyfile(args.work/name,work/name)
        def proposal_fault(name,file,mutate):
            path=work/file;before=path.read_bytes();d=json.loads(before);mutate(d)
            path.write_text(json.dumps(d))
            try:rejection(name,lambda:V.verify_proposals(work,*geometry))
            finally:path.write_bytes(before)
        proposal_fault('changed coordinate','contacts.json',lambda d:d['M'][0].__setitem__(0,1))
        proposal_fault('missing generic edge','contacts.json',lambda d:d['generic_edges'].pop())
        proposal_fault('missing unit polynomial','contacts.json',lambda d:d['contacts'].pop())
        proposal_fault('missing incidence','contacts.json',lambda d:d['contacts'][0]['pairs'].pop())
        proposal_fault('boolean coefficient','contacts.json',lambda d:d['contacts'][0]['poly'][0].__setitem__(0,True))
        proposal_fault('missing factor row','factorizations.json',lambda d:d.pop())
        proposal_fault('wrong multiplicity','factorizations.json',lambda d:d[0]['factors'][0].__setitem__(1,3))
        proposal_fault('duplicate factor','factorizations.json',lambda d:d[0]['factors'].append(copy.deepcopy(d[0]['factors'][0])))
        def lose_collision(d):
            next(r for r in d if r['kind']=='collision'and r['factors'])['factors']=[]
        proposal_fault('lost collision root','factorizations.json',lose_collision)
        rejection('repeated modular piece',lambda:V.modular_separation([factors[0],factors[0]]))
        rejection('distinct noncoprime pieces',lambda:V.modular_separation([factors[0],A.canonical(A.multiply(factors[0],factors[1]))]))
        rejection('modular degree drop',lambda:V.modular_separation([((1,0),(2**61-1,0))]))

        # Cache only the already independently verified mathematical prefix.
        # These remaining faults concern the separately supplied colour data.
        original=(V.independent_contacts,V.verify_proposals,V.modular_separation,A.real_roots)
        modular=V.modular_separation(factors)
        V.independent_contacts=lambda:geometry
        V.verify_proposals=lambda *unused:(factors,pieces,identities)
        V.modular_separation=lambda unused:modular
        A.real_roots=lambda f:roots[tuple(f)]
        good=json.loads((V.HERE/'certificate.json').read_text())
        cert=work/'certificate.json'
        def colour_fault(name,mutate):
            data=copy.deepcopy(good);mutate(data);cert.write_text(json.dumps(data))
            rejection(name,lambda:V.verify(work,cert))
        try:
            colour_fault('wrong version',lambda d:d.__setitem__('version','wrong'))
            colour_fault('short word',lambda d:d['words'].__setitem__(0,d['words'][0][:-1]))
            colour_fault('monochromatic generic graph',lambda d:d['words'].__setitem__(0,'0'*343))
            colour_fault('missing angle',lambda d:d['assignment'].pop())
            real=next(i for i,f in enumerate(factors)if roots[f])
            nonreal=next(i for i,f in enumerate(factors)if not roots[f])
            colour_fault('real case skipped',lambda d:d['assignment'].__setitem__(real,-1))
            colour_fault('nonreal marker corrupted',lambda d:d['assignment'].__setitem__(nonreal,0))
            colour_fault('boolean word index',lambda d:d['assignment'].__setitem__(real,True))
            colour_fault('infinity case skipped',lambda d:d['assignment'].__setitem__(-1,-1))
            for kind in ('extra_edges',):
                witness=None
                for i,f in enumerate(factors):
                    if not roots[f]:continue
                    c=pieces[f]
                    for j,w in enumerate(good['words']):
                        wrong=(any(w[a]==w[b]for a,b in c['extra_edges'])if kind=='extra_edges'
                               else all(w[a]!=w[b]for a,b in c['extra_edges'])and any(w[a]!=w[b]for a,b in c['equalities']))
                        if wrong:witness=(i,j);break
                    if witness:break
                V.require(witness is not None,'semantic fault witness exists')
                i,j=witness
                colour_fault('wrong '+kind+' colouring',lambda d:d['assignment'].__setitem__(i,j))
            f=factors[real];saved=pieces[f]
            pieces[f]=copy.deepcopy(saved)
            pieces[f]['equalities'].append([0,49])
            cert.write_text(json.dumps(good))
            try:rejection('spurious collision constraint',lambda:V.verify(work,cert))
            finally:pieces[f]=saved
        finally:
            V.independent_contacts,V.verify_proposals,V.modular_separation,A.real_roots=original
    print(json.dumps({'verified':True,'reversal_pair_incidences':reversal_pairs,
        'quadratic_sign_controls':289,'independent_rational_root_controls':200,
        'root_multiplicity_fixtures':len(fixtures),'rejected_faults':rejected,
        'rejection_count':len(rejected),'solver_calls':0},sort_keys=True))


if __name__=='__main__':main()
