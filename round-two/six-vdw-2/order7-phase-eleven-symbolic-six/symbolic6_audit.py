"""Independent literal-field and truth-table audit; never imports the generator."""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import resource
import time
from symbolic6_common import COMMIT, ROOT, VARIABLES, pins, require, sha, write


def field():
    require(all(617%d for d in range(2,25)), '617 not prime')
    require(len({pow(3,j,617) for j in range(616)})==616, 'root3 not primitive')
    H={pow(3,88*j,617) for j in range(7)}
    require(len(H)==7 and pow(3,19,617)==57, 'H7 or root57 incorrect')
    slots={}
    for i in range(88):
        coset={pow(3,i,617)*h%617 for h in H}
        require(not (set(slots)&coset), 'physical cosets overlap')
        slots.update({point:i for point in coset})
    require(set(slots)==set(range(1,617)) and slots[1]==0, 'actual616-point partition/gauge differs')
    require(all(slots[-point%617] == (index+44)%88 for point,index in slots.items()),'actual antipodal map fails')
    supports=set();kept=omitted=0
    for difference in range(1,617):
        for start in range(617):
            points=tuple((start+j*difference)%617 for j in range(7))
            if any(point==0 for point in points):
                omitted+=1;continue
            kept+=1
            supports.add(tuple(sorted({slots[point]+1 for point in points})))
    require((kept,omitted,len(supports))==(375760,4312,26488),'entire actual AP census differs')
    return slots,supports


def prime_clauses(relation, variables):
    allowed=[bits for bits in itertools.product((False,True),repeat=variables) if relation(bits)]
    result=[]
    for width in range(1,variables+1):
        for indices in itertools.combinations(range(variables),width):
            for signs in itertools.product((-1,1),repeat=width):
                row=tuple((index+1)*sign for index,sign in zip(indices,signs))
                if all(any(bits[abs(v)-1] == (v>0) for v in row) for bits in allowed):
                    if not any(set(old).issubset(row) for old in result):
                        result.append(row)
    return result


def gate_controls():
    gate=prime_clauses(lambda bits:bits[0] == (bits[1] or (bits[2] and bits[3])),4)
    xor=prime_clauses(lambda bits:bits[2] == (bits[0] != bits[1]),3)
    require(len(gate)==4 and sorted(map(len,gate))==[2,3,3,3] and len(xor)==4,'independent prime-implicate derivation differs')
    for values in itertools.product((False,True),repeat=4):
        require(all(any(values[abs(v)-1] == (v>0) for v in row) for row in gate)
                == (values[0] == (values[1] or (values[2] and values[3]))),'all16 counter truth rows fail')
    for values in itertools.product((False,True),repeat=3):
        require(all(any(values[abs(v)-1] == (v>0) for v in row) for row in xor)
                == (values[2] == (values[0] != values[1])),'all8 XOR truth rows fail')
    return gate,xor


def substitute(template, arguments):
    values=set()
    for literal in template:
        value=arguments[abs(literal)-1]
        if type(value) is bool:
            if value == (literal>0):
                return None
            continue
        require(type(value) is int and 1<=abs(value)<=VARIABLES,'invalid typed gate argument')
        value=value if literal>0 else -value
        if -value in values:
            return None
        values.add(value)
    return tuple(sorted(values))


def components(background,slots,supports):
    require(type(background) is int and background in (0,1),'invalid background identity')
    rows={name:set() for name in ['field','color','xor','phase_units','adjacency','phase8','counter','terminal','gauge']}
    for support in supports:
        rows['field'].add(support);rows['field'].add(tuple(sorted(-v for v in support)))
    for end in range(88):
        start=pow(3,end,617)
        for points in [tuple(pow(3,end-j,617) for j in range(7)),
                       tuple(start*pow(57,j,617)%617 for j in range(8))]:
            ids={slots[point]+1 for point in points}
            rows['color'].add(tuple(sorted(ids)));rows['color'].add(tuple(sorted(-v for v in ids)))
    gate,xor=gate_controls()
    for i in range(44):
        for template in xor:
            row=substitute(template,[i+1,i+45,i+89])
            require(row is not None,'XOR unexpectedly tautological');rows['xor'].add(row)
    minorities=[(i+89)*(1-2*background) for i in range(44)]
    rows['phase_units'].update((v,) for v in minorities[:6])
    rows['phase_units'].update([(-minorities[6],),(-minorities[43],)])
    forbidden={(i,(i+1)%44) for i in range(44)}-{(i,i+1) for i in range(5)}
    rows['adjacency'].update(tuple(sorted([-minorities[a],-minorities[b]])) for a,b in forbidden)
    for end in range(44):
        ids={(end-j)%44+89 for j in range(8)}
        rows['phase8'].add(tuple(sorted(ids)));rows['phase8'].add(tuple(sorted(-v for v in ids)))
    def count(j,t):
        if t==0:return True
        if j==0:return False
        return 133+6*(j-1)+(t-1)
    for j in range(1,37):
        for t in range(1,7):
            args=[count(j,t),count(j-1,t),minorities[j+6],count(j-1,t-1)]
            for template in gate:
                row=substitute(template,args)
                if row is not None:rows['counter'].add(row)
    rows['terminal'].update([(347,),(-348,)])
    rows['gauge'].add((-1,))
    return rows


def read_cnf(path):
    lines=path.read_text().splitlines()
    require(lines and lines[0].split()[:2]==['p','cnf'] and len(lines[0].split())==4,'invalid DIMACS header')
    n,c=map(int,lines[0].split()[2:]);require(n==VARIABLES and len(lines)==c+1,'DIMACS dimensions differ')
    rows=[]
    for line in lines[1:]:
        entries=list(map(int,line.split()))
        require(entries and entries[-1]==0 and 0 not in entries[:-1]
                and all(1<=abs(v)<=VARIABLES for v in entries[:-1]),'invalid DIMACS literal')
        rows.append(tuple(sorted(entries[:-1])))
    return rows


def expected_record(background,cnf,groups):
    return dict(stem='symbolic6-bg%d'%background,background=background,phase_K=11+22*background,
        variables=348,color_variables=88,phase_variables=44,counter_variables=216,
        clauses=len(set().union(*groups.values())),cnf_sha256=sha(cnf),component_counts={k:len(v) for k,v in groups.items()},
        physical_supports=26488,literal_kept_APs=375760,omitted_zero_APs=4312,
        minority_profile=[6,1,1,1,1,1],normalized_minor_run=[0,1,2,3,4,5],
        tail_positions=list(range(7,43)),tail_weight=5,necessary_phase_heads=1876,
        maximum_background_gap=7,following_background_gap_cut=None,preceding_gap_cut=None,
        palette_gauge=[[-1]],only_global_y0_zero=True,color_zero_is_coset_of_one=True,
        threshold_definition='S(j,t) iff S(j-1,t) OR (U(j) AND S(j-1,t-1))',
        numerical_premises=[8664,8787,9069],private_gap_cut=False,foreign_family_cut=False,
        ordinary_classification_numerical_cut=False,source_commit=COMMIT,mathematical_exclusion=False)


def audit_case(record,cnf,slots,supports,groups=None):
    background=record['background']
    if groups is None:groups=components(background,slots,supports)
    expected=expected_record(background,cnf,groups)
    require(record==expected,'ENTIRE independent symbolic/physical metadata differs')
    wanted=sorted(set().union(*groups.values()),key=lambda row:(len(row),row))
    parsed=read_cnf(cnf)
    require(Counter(parsed)==Counter(wanted) and parsed==wanted,'ENTIRE signed physical/auxiliary CNF differs')
    require(set(abs(v) for row in parsed for v in row)==set(range(1,349)),'unaccounted-for variable domain')
    return expected


def validate_manifest(produced):
    old,new=pins()
    require(set(produced)=={'agent','role','status','producer_sha256','models','covered_necessary_phase_heads','ordinary_classification','records'}
            and produced['agent']=='six-vdw-2' and produced['role']=='researcher' and produced['status']=='GENERATED_NOT_AUDITED'
            and produced['producer_sha256']==new['files']['symbolic6_generate.py']
            and produced['models']==2 and produced['covered_necessary_phase_heads']==3752
            and produced['ordinary_classification']=='10093/index1'
            and len(produced['records'])==2 and [r['background'] for r in produced['records']]==[0,1],
            'ENTIRE symbolic two-model coverage/provenance differs')
    require(len({r['cnf_sha256'] for r in produced['records']})==2
            and not {r['cnf_sha256'] for r in produced['records']}.intersection(old['frozen_prior_cnfs']),
            'identical frozen failed input')


def main(work,witness=None):
    began=time.monotonic();pins();produced=json.loads((work/'models.json').read_text());validate_manifest(produced)
    slots,supports=field()
    records=[audit_case(record,work/(record['stem']+'.cnf'),slots,supports) for record in produced['records']]
    mode='normal' if __debug__ else 'optimized'
    result=dict(agent='six-vdw-2',role='researcher',status='INDEPENDENT_ENTIRE_SYMBOLIC_TWO_MODELS_CHECKED',
        records=records,literal_field_points=616,literal_kept_APs=375760,omitted_zero_APs=4312,
        literal_supports=26488,gate_truth_rows=16,XOR_truth_rows=8,models=2,covered_necessary_phase_heads=3752,
        source_manifest_sha256=sha(ROOT/'symbolic6-source-pins.json'),mathematical_exclusion=False)
    if witness is not None:
        require(type(witness) is int and witness in (0,1),'invalid witness background')
        cnf=work/('symbolic6-bg%d.cnf'%witness)
        bits=json.loads(cnf.with_suffix('.model.json').read_text())
        require(len(bits)==348 and all(type(v) is int and v in (0,1) for v in bits) and bits[0]==0,'348-value assignment/gauge fails')
        require(all(any(bits[abs(v)-1]==int(v>0) for v in row) for row in read_cnf(cnf)),'whole original CNF witness fails')
        y=bits[:88];f=[y[i]^y[i+44] for i in range(44)]
        require(bits[88:132]==f and sum(f)==11+22*witness,'actual antipodal phase/weight differs')
        m=[v^witness for v in f];require(m[:6]==[1]*6 and m[6]==m[43]==0,'actual six-run normalization fails')
        require(sum(m[7:43])==5 and all(not(m[i] and m[(i+1)%44]) for i in range(5,44)), 'actual minority profile fails')
        require(all(len({f[(i+j)%44] for j in range(8)})==2 for i in range(44)), 'actual phase-eight windows fail')
        for j in range(1,37):
            for t in range(1,7):
                require(bits[132+(j-1)*6+t-1]==int(sum(m[7:j+7])>=t),'actual auxiliary threshold semantics fail')
        actual={point:y[index] for point,index in slots.items()}
        require(all(actual[point*pow(3,88*j,617)%617]==value for point,value in actual.items() for j in range(7)), 'actual H7 invariance fails')
        checked=0
        for difference in range(1,617):
            for start in range(617):
                points=[(start+j*difference)%617 for j in range(7)]
                if 0 in points:continue
                require(len({actual[point] for point in points})==2,'actual monochromatic field AP7')
                checked+=1
        require(checked==375760,'entire witness AP coverage incomplete')
        result.update(status='INDEPENDENT_ACTUAL_FIELD_WITNESS',background=witness,coset_colors=y,phase=f,
                      actual616_colors=[actual[x] for x in range(1,617)],checked_witness_APs=checked,
                      interval3704_witness=False,global_W_bound=False)
        destination=work/('symbolic6-bg%d-witness-%s.json'%(witness,mode))
    else:
        destination=work/('audit-%s.json'%mode)
    write(destination,result)
    print(json.dumps(dict(status=result['status'],receipt_sha256=sha(destination),seconds=time.monotonic()-began,
                         maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),sort_keys=True))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True);parser.add_argument('--witness',type=int)
    args=parser.parse_args();main(args.work.absolute(),args.witness)
