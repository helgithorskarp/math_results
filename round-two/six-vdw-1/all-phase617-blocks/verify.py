"""Sequential source-only complete mathematical verification, no external tools."""
import hashlib
import json
from pathlib import Path
from check_all_kernel import check_kernel
from check_attainment import check as attainment
from check_metric import check as metric


def need(ok,message):
    if not ok:
        raise ValueError(message)


if __name__=='__main__':
    h=Path(__file__).resolve().parent
    manifest=json.loads((h/'SOURCE_MANIFEST.json').read_bytes())
    for name,pin in manifest['files'].items():
        path=h/name
        need(path.parent==h and path.is_file(),'plain source-packet file path')
        raw=path.read_bytes()
        need(len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256'],
             'changed source-packet file:'+name)
    proof=check_kernel(json.loads((h/'kernel.json').read_bytes()),h/'kernel.cnf',h/'kernel.lrat',
                       json.loads((h/'ALL_PHASE_BLOCKS_NEXT_PLAN.json').read_bytes()))
    known=attainment();geometry=metric()
    need(proof['family_exclusion_at3704'] is True and known['family_membership_proved'] is True,
         'exact upper restriction and separately checked actual attainment')
    value={'author':'six-vdw-1','role':'researcher','status':'EXACT_FOUR_CHARACTER617_BLOCK_PHASE_FAMILY_MAXIMUM_3703',
           'family_maximum_AP7_free_length':3703,'proof':proof,'attainment':known,'metric':geometry,
           'ordinary_bridges_formalized':False,'external_person_review_claimed':False,
           'unrestricted_W_upper_or_exact_value_claimed':False,'new_W_lower_bound_claimed':False,
           'radius_one_exclusion_claimed':False}
    encoded=json.dumps(value,sort_keys=True)
    need(json.loads(encoded)==json.loads((h/'EXPECTED.json').read_bytes()),
         'whole expected mathematical record')
    print(encoded)
