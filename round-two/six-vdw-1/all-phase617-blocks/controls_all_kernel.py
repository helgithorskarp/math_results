"""Real compact physical/domain/positive-RUP damages, including repaired hashes."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
from check_all_kernel import check_kernel


def reject(function):
    try:
        function()
    except (ValueError,KeyError,TypeError,IndexError):
        return
    raise ValueError('real damaged standalone mathematical certificate accepted')


if __name__=='__main__':
    h=Path(__file__).resolve().parent
    record=json.loads((h/'kernel.json').read_bytes())
    plan=json.loads((h/'ALL_PHASE_BLOCKS_NEXT_PLAN.json').read_bytes())
    cnf=h/'kernel.cnf';proof=h/'kernel.lrat';positive=check_kernel(record,cnf,proof,plan)
    ap=next(i for i,x in enumerate(record['leaves']) if x['kind']=='actual_original_AP')
    choice=next(i for i,x in enumerate(record['leaves']) if x['kind']=='proved_necessary_local_row_choice')
    root_leaf=next(i for i,x in enumerate(record['leaves']) if x['kind']=='actual_original_AP'
                   and any(577<=abs(v)<=602 for v in x['literals']))
    root_at=next(j for j,v in enumerate(record['leaves'][root_leaf]['literals']) if 577<=abs(v)<=602)
    bads=[]
    for name,mutate in [
        ('wrong_prime',lambda r:r.__setitem__('q',619)),
        ('wrong_free_root_quantifier',lambda r:r.__setitem__('actual_root_bits',4)),
        ('literal_endpoint_outside_interval',lambda r:r['leaves'][ap].__setitem__('original_AP',[3703,1])),
        ('actual_AP_polarity_reversed',lambda r:r['leaves'][ap].__setitem__('polarity',-r['leaves'][ap]['polarity'])),
        ('actual_color_helper_changed',lambda r:r['leaves'][ap]['literals'].__setitem__(0,r['leaves'][ap]['literals'][0]+1)),
        ('necessary_local_clause_index_changed',lambda r:r['leaves'][choice].__setitem__('choice_clause_index',
                 (r['leaves'][choice]['choice_clause_index']+1)%29502)),
        ('foreign_leaf',lambda r:r['leaves'][choice].__setitem__('kind','solver_assumption')),
        ('actual_root_occurrence_aliased',lambda r:r['leaves'][root_leaf]['literals'].__setitem__(root_at,
                 (1 if r['leaves'][root_leaf]['literals'][root_at]>0 else -1)*
                 (578 if abs(r['leaves'][root_leaf]['literals'][root_at])==577 else 577)))]:
        bad=copy.deepcopy(record);mutate(bad)
        reject(lambda:check_kernel(bad,cnf,proof,plan));bads.append(name)
    with tempfile.TemporaryDirectory(dir=h) as tmp:
        tmp=Path(tmp)
        damaged=cnf.read_bytes().replace(b' 0\n',b' 1\n',1)
        cp=tmp/'damaged.cnf';cp.write_bytes(damaged)
        bad=copy.deepcopy(record);bad['kernel_cnf_sha256']=hashlib.sha256(damaged).hexdigest()
        reject(lambda:check_kernel(bad,cp,proof,plan));bads.append('real_signed_CNF_repaired_hash')
        lines=proof.read_text().splitlines();first=lines[0].split();zero=first.index('0')
        first[zero+1]='999999';changed=' '.join(first)+'\n'+'\n'.join(lines[1:])+'\n'
        pp=tmp/'damaged.lrat';pp.write_text(changed)
        bad=copy.deepcopy(record);bad['kernel_lrat_sha256']=hashlib.sha256(pp.read_bytes()).hexdigest()
        reject(lambda:check_kernel(bad,cnf,pp,plan));bads.append('real_positive_hint_repaired_hash')
        pp.write_text('\n'.join(lines[:-1])+'\n')
        bad=copy.deepcopy(record);bad['kernel_lrat_sha256']=hashlib.sha256(pp.read_bytes()).hexdigest()
        reject(lambda:check_kernel(bad,cnf,pp,plan));bads.append('final_checked_empty_removed_repaired_hash')
    print(json.dumps({'author':'six-vdw-1','role':'researcher',
                      'status':'GENUINE_COMPACT_ALL_BLOCK_PHYSICAL_DOMAIN_RUP_DAMAGES_REJECTED',
                      'positive_actual_APs':positive['distinct_actual_APs'],
                      'positive_RUP_additions':positive['strict_compact_RUP']['checked_additions'],
                      'damage_count':len(bads),'damages':bads},sort_keys=True))
