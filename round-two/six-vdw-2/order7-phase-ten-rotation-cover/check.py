"""Independent transfer/Burnside counts and actual selected-position cover audit."""
import argparse
from collections import Counter
from fractions import Fraction
import itertools
import json
from math import comb,gcd
from pathlib import Path
import resource
import time
from common import HERE,pins,require,sha

def rooted(n,total,cap,head):
    states={(sum(head),head[-1]):1}
    for _ in range(n-len(head)):
        next_states=Counter()
        for (subtotal,last),ways in states.items():
            for value in range(cap+1):
                if subtotal+value<=total and (last!=0 or value<=1):
                    next_states[subtotal+value,value]+=ways
        states=next_states
    return sum(ways for (s,last),ways in states.items()
               if s==total and (last!=0 or head[0]<=1))

def indexed(n,total,cap):
    result=0
    for first in range(cap+1):
        states={(first,first,first==0):1}
        for _ in range(n-1):
            next_states=Counter()
            for (subtotal,last,zero),ways in states.items():
                for value in range(cap+1):
                    if subtotal+value<=total and (last!=0 or value<=1):
                        next_states[subtotal+value,value,zero or value==0]+=ways
            states=next_states
        result+=sum(ways for (s,last,zero),ways in states.items()
                    if s==total and zero and (last!=0 or first<=1))
    return result

def burnside(n,total,cap):
    numerator=0
    for shift in range(n):
        period=gcd(n,shift)
        if (total*period)%n==0:
            numerator+=indexed(period,total*period//n,cap)
    require(numerator%n==0,'Burnside divisibility failed')
    return numerator//n

def positive_coeff(n,total,cap):
    if total<0:return 0
    poly=Counter({0:1})
    for _ in range(n):
        poly=Counter({t:sum(poly[t-value] for value in range(2,cap+1))
                      for t in range(total+1)})
    return poly[total]

def distinguished_zero_run(n,total,cap):
    # Distinguish the last zero before a one, rather than an arbitrary zero.
    result=Fraction()
    for zeros in range(1,n):
        positives=n-zeros
        for ones in range(1,positives+1):
            arrays=comb(positives,ones)*positive_coeff(positives-ones,total-ones,cap)
            result+=Fraction(arrays*ones*comb(zeros+ones-2,ones-1),positives)
    require(result.denominator==1,'nonintegral distinguished zero-run count')
    return result.numerator

def actual_phase_key(gaps):
    require(len(gaps)==10 and sum(gaps)==44 and all(2<=x<=8 for x in gaps),
            'wrong literal selected-position domain')
    points=[0]
    for distance in gaps[:-1]:points.append(points[-1]+distance)
    selected=set(points)
    require(len(selected)==10 and max(selected)<44,'wrong actual phase support')
    # Reconstruct rooted gaps from actual phase positions, not deficit rotations.
    candidates=[]
    for origin in selected:
        if (origin+2)%44 not in selected or (origin+5)%44 not in selected:continue
        positions=sorted((point-origin)%44 for point in selected)
        distances=tuple((positions[(i+1)%10]-point)%44
                        for i,point in enumerate(positions))
        if distances[:2]==(2,3):candidates.append(distances)
    require(candidates,'missing mandatory gap-(2,3) root')
    require(all(distance!=2 or gaps[(i+1)%10] in (2,3)
                for i,distance in enumerate(gaps)),'successor rule violated')
    period22={((point+22)%44) for point in selected}==selected
    return min(candidates),period22

def controls():
    indexed_inputs=count_comparisons=literal_classes=0
    for n in range(2,8):
        words=Counter();roots=Counter();orbits={}
        for word in itertools.product(range(4),repeat=n):
            if 0 not in word or sum(word)==0:continue
            if any(value==0 and word[(i+1)%n]>1 for i,value in enumerate(word)):continue
            total=sum(word);words[total]+=1;indexed_inputs+=1
            require(any(word[i]==0 and word[(i+1)%n]==1 for i in range(n)),
                    'tiny mandatory root missing')
            key=min(word[i:]+word[:i] for i in range(n))
            orbits.setdefault(total,set()).add(key)
            if word[:2]==(0,1):roots[total]+=1
        for total in range(1,3*n+1):
            literal=len(orbits.get(total,()))
            require(indexed(n,total,3)==words[total]
                    and burnside(n,total,3)==literal
                    and rooted(n,total,3,(0,1))==roots[total]
                    and distinguished_zero_run(n,total,3)==roots[total],
                    'tiny literal/transfer/Burnside/zero-run counts differ')
            count_comparisons+=1;literal_classes+=literal
    # Full phase-word rotations on small cycles check gap classes against binary classes.
    binary_words=binary_classes=signed_rotations=0
    for length in range(8,15):
        by_gap={};by_binary={}
        for bits in itertools.product((0,1),repeat=length):
            for background in (0,1):
                points=[i for i,value in enumerate(bits) if value!=background]
                if len(points)<3:continue
                gaps=tuple((points[(i+1)%len(points)]-x)%length
                           for i,x in enumerate(points))
                if min(gaps)!=2 or max(gaps)>8 or all(x==2 for x in gaps):continue
                if any(x==2 and gaps[(i+1)%len(gaps)] not in (2,3)
                       for i,x in enumerate(gaps)):continue
                roots=[gaps[i:]+gaps[:i] for i,x in enumerate(gaps)
                       if x==2 and gaps[(i+1)%len(gaps)]==3]
                require(roots,'tiny binary mandatory root missing')
                gap_key=min(roots)
                binary_key=min(bits[i:]+bits[:i] for i in range(length))
                group=(length,len(points),background)
                old=by_gap.setdefault(group,{}).setdefault(gap_key,binary_key)
                require(old==binary_key,'gap rotation identifies different phase orbits')
                by_binary.setdefault(group,set()).add(binary_key);binary_words+=1
        require(all(len(keys)==len(by_binary[group]) for group,keys in by_gap.items()),
                'gap and literal binary orbit counts differ')
        binary_classes+=sum(len(keys) for keys in by_gap.values())
    for half in range(2,7):
        for y in itertools.product((0,1),repeat=2*half):
            phase=[y[i]^y[i+half] for i in range(half)]
            for shift in range(2*half):
                moved=[y[(i+shift)%(2*half)]^y[shift] for i in range(2*half)]
                require(moved[0]==0 and all(moved[i]^moved[i+half]
                        ==phase[(i+shift)%half] for i in range(half)),
                        'scalar rotation/global-color gauge lost a phase orientation')
                signed_rotations+=1
    return dict(tiny_indexed_words=indexed_inputs,count_comparisons=count_comparisons,
                tiny_gap_classes=literal_classes,tiny_binary_words=binary_words,
                tiny_binary_classes=binary_classes,signed_rotation_controls=signed_rotations)

def audit(work,expected=None,run_controls=True):
    began=time.monotonic();pins()
    expected=expected or json.loads((HERE/'EXPECTED.json').read_text())
    require(expected['selected_count']==10 and expected['cycle_length']==44
            and expected['deficit_total']==24 and expected['deficit_cap']==6
            and expected['backgrounds']==[0,1] and expected['lower_orientation_variables']==44
            and expected['orientation_invariance_imposed'] is False
            and expected['field_coloring_count'] is False,'changed mathematical scope')
    t10=indexed(10,24,6);t5=indexed(5,12,6)
    classes=burnside(10,24,6);root23=rooted(10,24,6,(0,1))
    require(root23==distinguished_zero_run(10,24,6),'independent rooted counts differ')
    derived=dict(indexed_gap_words=t10,indexed_period5_base_words=t5,
                 rooted_gap2_profiles=rooted(10,24,6,(0,)),rooted_23_profiles=root23,
                 phase_rotation_classes=classes,period22_phase_classes=t5//5,
                 period44_phase_classes=(t10-t5)//10,
                 both_background_phase_classes=2*classes)
    require(all(expected[k]==value for k,value in derived.items()),'changed exact count expectation')
    path=work/'representatives.txt'
    require(sha(path)==expected['corpus_sha256'],'changed corpus bytes')
    checked=short=0;previous=None
    for line in path.read_text().splitlines():
        row=tuple(map(int,line.split()))
        require(line==' '.join(map(str,row)),'noncanonical corpus encoding')
        key,period22=actual_phase_key(row)
        require(row==key,'noncanonical actual phase root')
        require(previous is None or previous<row,'duplicate or unordered phase representative')
        previous=row;short+=int(period22);checked+=1
    require(checked==classes and short==t5//5,'incomplete or wrong-period phase cover')
    result=dict(agent='six-vdw-2',role='researcher',status='EXACT_CANONICAL_PHASE10_ROTATION_COVER',
                **derived,checked_representatives=checked,corpus_sha256=sha(path),
                controls=controls() if run_controls else None,
                seconds=time.monotonic()-began,
                maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                global_W_bound=False,admissible_field_coloring_count=False,
                external_review=False,formalization=False)
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True)
    args=parser.parse_args();result=audit(args.work.absolute())
    (args.work/('check-normal.json' if __debug__ else 'check-optimized.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
