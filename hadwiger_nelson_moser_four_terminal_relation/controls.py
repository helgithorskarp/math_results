"""Mathematical certificate corruption controls; no digest-based rejections."""
from copy import deepcopy
from pathlib import Path
import json
from verify import verify
from model import graph,POINTS,need

def main():
    base=json.loads((Path(__file__).resolve().parent/'certificate.json').read_text())
    verify(base)
    rejected=[]
    def trial(name,edit):
        c=deepcopy(base);edit(c)
        try:verify(c)
        except ValueError:rejected.append(name)
        else:raise ValueError('accepted corruption: '+name)
    trial('missing_positive_pattern',lambda c:c['positive_words'].pop())
    trial('duplicate_positive_pattern',lambda c:c['positive_words'].__setitem__(0,c['positive_words'][1]))
    trial('improper_full_word',lambda c:c['positive_words'].__setitem__(0,'0'*11))
    trial('missing_interior_deletion',lambda c:c['vertex_deletions'].pop())
    trial('wrong_deleted_vertex',lambda c:c['vertex_deletions'][0].__setitem__('deleted',1))
    trial('improper_deletion_word',lambda c:c['vertex_deletions'][0]['words'][0].__setitem__(1,0))
    trial('missing_failed_formula_pattern',lambda c:c['failed_formula_words'].pop())
    collision=list(POINTS);collision[10]=collision[9]
    try:graph(collision)
    except ValueError:rejected.append('physical_point_collision')
    else:raise ValueError('accepted physical collision')
    need(len(rejected)==8,'all corruption controls rejected')
    return {'status':'CORRUPTION CONTROLS PASS','rejected':rejected,'count':len(rejected)}

if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
