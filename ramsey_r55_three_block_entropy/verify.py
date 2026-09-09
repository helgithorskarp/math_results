"""Independent census comparison and explicit entropy-cover certificate audit."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import argparse,hashlib,json,struct
HERE=Path(__file__).resolve().parent

def require(ok,why):
    if not ok:raise ValueError(why)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def verify(producer,checker,global_file):
    producer=Path(producer);checker=Path(checker)
    for pin in json.loads((HERE/'DEPENDENCIES.json').read_text()):
        root=HERE.parent/pin['directory'];manifest=root/pin['manifest'];require(sha(manifest)==pin['sha256'],'parent identity')
        contents=manifest.read_text();entries=json.loads(contents) if pin['manifest'].endswith('.json') else {name:digest for digest,name in (line.split('  ',1) for line in contents.splitlines())}
        for name,digest in entries.items():require(sha(root/name)==digest,'changed upstream '+name)
    local=json.loads((producer/'LOCAL.json').read_text());claim=json.loads(Path(global_file).read_text())
    require(local['status']=='COMPLETE_CENTRED_TRIPLE_CENSUS','complete local claim')
    require((producer/'HISTOGRAM.tsv').read_bytes()==(checker/'HISTOGRAM.tsv').read_bytes(),'entrywise histogram mismatch')
    require((producer/'PROFILE.tsv').read_bytes()==(checker/'PROFILE.tsv').read_bytes(),'entrywise profile mismatch')
    require(sha(producer/'HISTOGRAM.tsv')==local['histogram_sha256'] and sha(producer/'PROFILE.tsv')==local['profile_sha256'],'profile identities')
    hrows=(checker/'HISTOGRAM.tsv').read_text().splitlines();prows=(checker/'PROFILE.tsv').read_text().splitlines()
    require(len(hrows)==local['histogram_rows']==830 and len(prows)==local['profile_rows']==1039,'profile coverage')
    # Compare every literal domain state with the pinned parent's bitmap.
    old_domains=json.loads((HERE.parent/'ramsey_r55_global_clique_packing'/'DOMAINS.json').read_text())
    sizes={}
    for tag,left,right in (('RR','R4','R4'),('RB','R4','B4'),('BB','B4','B4')):
        raw=(checker/(tag+'.bin')).read_bytes();require(len(raw)%2==0,'domain bytes')
        values=list(struct.unpack('<'+str(len(raw)//2)+'H',raw));require(values==sorted(set(values)),'ordered domain states')
        item=next(x for x in old_domains if x['left']==left and x['right']==right)
        bitmap=int(item['allowed_bitmap_hex'],16)
        require(sum(1<<v for v in values)==bitmap,'parent palette differs')
        require(sha(checker/(tag+'.bin'))==local['domains'][tag]['sha256'] and len(values)==local['domains'][tag]['count']==item['count'],'domain metadata')
        sizes[tag]=len(values)
    # Uniform palette transport justifies every centre colour and block ordering.
    palettes={}
    for left in ('R4','B4'):
        for right in ('R4','B4'):
            item=next(x for x in old_domains if x['left']==left and x['right']==right)
            bits=int(item['allowed_bitmap_hex'],16)
            palettes[left,right]={x for x in range(65536) if (bits>>x)&1}
    transport=0
    for (left,right),values in palettes.items():
        transposed={sum(((x>>(4*i+j))&1)<<(4*j+i) for i in range(4) for j in range(4)) for x in values}
        require(transposed==palettes[right,left],'transpose palette transport')
        flipped=('B4' if left=='R4' else 'R4','B4' if right=='R4' else 'R4')
        require({65535^x for x in values}==palettes[flipped],'complement palette transport')
        transport+=2*len(values)
    computed=Counter()
    for line in prows:
        tag,code,weight,subtotal=line.split();computed[tag]+=int(weight)*int(subtotal)
    totals={tag:int(value) for tag,value in (line.split() for line in (checker/'TOTALS.tsv').read_text().splitlines())}
    require(dict(computed)==totals,'conditioned profile totals')
    denominators=dict(same=sizes['RR']**3,majority=sizes['RR']*sizes['RB']**2,minority=sizes['BB']*sizes['RB']**2)
    probabilities={}
    for tag in denominators:
        row=local['probabilities'][tag];require((row['allowed'],row['total'])==(totals[tag],denominators[tag]),'local exact count')
        probabilities[tag]=Fraction(totals[tag],denominators[tag])
    parent=json.loads((HERE.parent/'ramsey_r55_q9_core_contact_domains'/'EXPECTED.json').read_text())['census']
    expected_classes={(q,r) for q in range(7,11) for r in range(5,q+1)}
    require(len(claim['classes'])==18 and {(x['q'],x['r']) for x in claim['classes']}==expected_classes,'complete global classes')
    after=Fraction();before=0;all_occurrences=all_events=0
    for row in claim['classes']:
        q,r=row['q'],row['r'];blocks=list(range(1,q));incidence=Counter();kinds=Counter()
        for centre in blocks:
            colour=int(centre<r)
            for left,right in combinations([v for v in blocks if v!=centre],2):
                others=(int(left<r),int(right<r));kind='same' if others==(colour,colour) else 'minority' if others==(1-colour,1-colour) else 'majority';kinds[kind]+=1
                for edge in combinations(sorted((centre,left,right)),2):incidence[edge]+=1
        require(set(incidence)==set(combinations(blocks,2)) and set(incidence.values())=={row['read']},'exact independent-variable cover')
        require(kinds==Counter(same=3*row['same_triples'],majority=2*row['mixed_triples'],minority=row['mixed_triples']),'event colours')
        require(sum(kinds.values())==row['events'] and len(incidence)==row['matrix_coordinates'],'event cardinality')
        power=Fraction(1)
        for kind,exponent in kinds.items():power*=probabilities[kind]**exponent
        upper=Fraction(**row['probability_upper']);require(0<upper<1 and upper**row['read']>=power,'root upper certificate')
        scale=claim['root_scale'];require(type(scale) is int and scale==10**18 and (upper*scale).denominator==1,'rational grid')
        require((upper-Fraction(1,scale))**row['read']<power,'least grid upper')
        inherited=next(x for x in parent['classes'] if (x['q'],x['r'])==(q,r))
        require(row['before']==inherited['after'] and row['core_count']==inherited['core_count'],'class weight')
        contribution=inherited['after']*upper;require(contribution==Fraction(**row['after_upper']),'weighted class bound')
        before+=inherited['after'];after+=contribution;all_events+=sum(kinds.values());all_occurrences+=sum(incidence.values())
    require(before==parent['after']==claim['before'] and after==Fraction(**claim['after_upper']),'global census')
    require(Fraction(**claim['removed_lower'])==(before-after)/before,'global removed fraction')
    require(abs(Fraction(claim['removed_lower_decimal'])-(before-after)/before)<Fraction(1,10**39),'displayed removal')
    smallest=min(1-Fraction(**row['probability_upper']) for row in claim['classes'])
    require(abs(Fraction(claim['minimum_class_removal_lower_decimal'])-smallest)<Fraction(1,10**39),'displayed class bound')
    require(claim['gate']==('PASS' if 4*after<=3*before else 'FAIL'),'declared gate status')
    require(claim['affected_task_ids']==claim['task_ids']==2189178 and claim['new_task_decisions']==0 and not claim['target_found'],'scope')
    return dict(status='INDEPENDENT_CENTRED_CENSUS_AND_GLOBAL_COVER_VERIFIED',histogram_entries=830,profile_entries=1039,
                literal_pair_assignments=196608,palette_states=sum(sizes.values()),palette_transport_identities=transport,exact_primitive_counts=3,classes=18,
                abstract_events=all_events,coordinate_occurrences=all_occurrences,gate=claim['gate'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('producer');p.add_argument('checker');p.add_argument('global_file');a=p.parse_args()
    print(json.dumps(verify(a.producer,a.checker,a.global_file),sort_keys=True))
