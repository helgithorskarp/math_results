"""Post-seal independent point-bit corroboration and base-role checks."""
import itertools as it
import triple_check as t

def run(bases):
 G=[0,8,3,11,6,14,5,13,12,4,15,7,10,2,9,1,16,17];records=[]
 for row in bases['classes']:
  d=t.domain(row['words']);base=d['base'];image={sum(1<<G[k] for k in range(18) if w&(1<<k)) for w in base};t.need(image==set(base),'whole C5 action')
  degrees=[sum(bool(w&(1<<i)) for w in base) for i in range(18)];t.need(any(degrees[i]==20 for i in (0,16,17)),'actual saturated fixed point')
  full=[]
  for w,block in d['blockers'].items():
   other=sum(1<<i for i,b in enumerate(base) if (w&b).bit_count()>=3);t.need(other==block,'whole independent bit-intersection blocker oracle');full.append([w,other])
  records.append({'id':row['id'],'degrees':degrees,'every_bit_oracle_blocker_match':len(full),'point_word_checks':len(full)*len(base),'whole_bit_oracle_sha256':t.digest(sorted(full))})
 return {'all_eight_role_and_original_blocker_checks':records,'total_point_word_checks':sum(x['point_word_checks'] for x in records),'method':'Second fresh point-bit oracle after first triple record sealed; no author module import.'}
