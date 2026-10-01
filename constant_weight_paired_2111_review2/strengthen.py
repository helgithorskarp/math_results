"""Transport the source's better center-swapped partition: upper66 -> upper65."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
from audit import BASE, CERT_SHA, check_partition, digest, points, union_check
from incidence import canonical, image, inverse, need


def run(work,target,compare=True):
    audited=json.loads((work/'audit.json').read_text())
    frozen=json.loads((BASE/'expected.json').read_text())
    need(digest(audited)==frozen['audit_record_sha256'],'required complete independent audit mismatch')
    classes=json.loads((work/'joint-classes.json').read_text())
    need(digest(classes)==audited['ordered_class_sha256'] and len(classes)==128,'complete joint-class input mismatch')
    raw=(target/'certificates.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==CERT_SHA,'source certificate provenance mismatch')
    certificates=json.loads(raw)['color_certificates']
    first,second=classes[127],classes[114]
    need([first['first'],first['second'],second['first'],second['second']]==[7,6,6,7],'wrong center-swap types')
    source=union_check(first['left'],first['right'])
    destination=union_check(second['left'],second['right'])
    colors=((0,17),tuple(range(1,17)))
    a=canonical(source,18,colors);b=canonical(destination,18,colors)
    need(a['canonical']==b['canonical'],'the two classes are not center-set isomorphic')
    inverse_target=inverse(b['to_canonical'])
    transport=tuple(inverse_target[a['to_canonical'][z]] for z in range(18))
    need(sorted(transport)==list(range(18)) and transport[0]==17 and transport[17]==0,'transport is not a center exchange')
    need(image(source,transport)==destination and image(destination,inverse(transport))==source,'literal37-word transport mismatch')
    def candidates(words):
        literal=[points(w) for w in words]
        return [frozenset(q) for q in combinations(range(1,17),5) if all(len(set(q)&w)<=2 for w in literal)]
    src,dst=candidates(source),candidates(destination)
    need(len(src)==len(dst)==118,'wrong complete residual domains')
    lookup={w:i for i,w in enumerate(dst)}
    moved=[frozenset(transport[z] for z in w) for w in src]
    need(len(set(moved))==118 and set(moved)==set(dst),'transport does not biject the whole residual domain')
    indices=[lookup[w] for w in moved]
    source_partition=certificates[127]['partition']
    need(check_partition(src,source_partition)==28,'source partition not independently verified')
    replacement=[[indices[z] for z in c] for c in source_partition]
    need(check_partition(dst,replacement)==28,'transported partition fails literal conflicts/coverage')
    uppers=[]
    for i,c in enumerate(certificates):
        uppers.append(37+(28 if i==114 else c['certified_residual_upper']))
    need(len(uppers)==128 and max(uppers)==65 and sum(u==66 for u in uppers)==0,'complete revised code bound differs')
    result=dict(agent='six-reviewer-2',role='independent mathematical reviewer',status='PROVED paired2111 bound65 by literal certificate transport',
                source_class=127,target_class=114,source_templates=[7,6],target_templates=[6,7],
                source_certificate_sha256=CERT_SHA,point_transport=list(transport),center_exchange=[17,0],
                fixed_words=37,source_domain=118,target_domain=118,complete_candidate_bijection=indices,
                old_target_partition_classes=29,new_target_partition_classes=28,
                source_partition_classes=28,replacement_partition=replacement,
                source_joint_words_sha256=digest(source),target_joint_words_sha256=digest(destination),
                literal_replacement_conflict_pairs=sum(len(c)*(len(c)-1)//2 for c in replacement),
                complete_joint_classes=128,maximum_code_upper=65,
                remaining_ordered_classes_at_upper65=[i for i,u in enumerate(uppers) if u==65],
                sharpness_established=False,global_code_interval_changed=False)
    if compare:
        expected=json.loads((BASE/'improvement.json').read_text())
        need(result==expected,'independent strengthening record differs')
    (work/'strengthening.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','source_class','target_class','new_target_partition_classes','maximum_code_upper','remaining_ordered_classes_at_upper65')}),flush=True)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--target',type=Path,required=True);a=p.parse_args();run(a.work.resolve(),a.target.resolve())
