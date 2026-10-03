"""Strict full-record validation controls after a fresh complete direct audit."""
import copy,json,sys,hashlib

def wire(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def need(ok,why):
    if not ok:raise ValueError(why)
def validate(candidate,verified_reference):
    # Reference is accepted only after direct.py has checked its entire mathematics.
    need(type(candidate)is dict,'record mapping')
    need(wire(candidate)==wire(verified_reference),'whole already-audited mathematical record')
def controls(reference):
    validate(reference,reference);bad=[]
    def damage(name,change):
        v=copy.deepcopy(reference);change(v)
        try:validate(v,reference)
        except ValueError:bad.append(name)
        else:raise ValueError('accepted damage '+name)
    damage('wrong original14 phase',lambda v:v['scope']['prefix'][3].__setitem__(1,1))
    damage('drop essential32',lambda v:v['scope'].__setitem__('essential_32',False))
    damage('exact-LCM assumption',lambda v:v['scope'].__setitem__('actual_lcm','equals10080'))
    damage('at-least-eight minimum',lambda v:v['scope'].__setitem__('minimum','atleast8'))
    damage('drop last BASE original',lambda v:v['BASE_gluing'][0]['labels'].pop())
    damage('last BASE phase stream',lambda v:v['BASE_gluing'][-1].__setitem__('whole_phase_stream_sha256','0'*64))
    damage('false1156 budget',lambda v:v['BASE_gluing'][0].__setitem__('sum',1216))
    damage('inactive half falsely covers',lambda v:v['all_raw_local_types'][0][2][0].__setitem__(1,True))
    damage('drop final raw phase',lambda v:v['final_phases'][0].__setitem__('raw_count',46655))
    damage('wrong final original phase',lambda v:v['final_phases'][0]['qualifying'][0][0].__setitem__(0,18))
    damage('wrong mixed bound',lambda v:v['mixed_HQQ_HHQ_rows'][-1][-1].__setitem__(-1,0))
    damage('drop late H-union group',lambda v:v['all_exact_H_unions'].pop())
    damage('drop third-parent allocation',lambda v:v['three_parent_allocations'].pop())
    damage('false180 terminal type bound',lambda v:next(r for r in v['type_rows']if r[4]==180).__setitem__(4,176))
    damage('false ninth-to-tenth tail flag',lambda v:v['scope'].__setitem__('productive_count_lower',10))
    damage('unproved global bound flag',lambda v:v['scope'].__setitem__('global_L_min_8_improvement',True))
    damage('new unsupported claim key',lambda v:v.__setitem__('sharp_capacity',True))
    for malformed in (None,[],{},'record',{'scope':reference['scope']}):
        try:validate(malformed,reference)
        except ValueError:pass
        else:raise ValueError('malformed accepted')
    validate(copy.deepcopy(reference),reference)
    return {'status':'COMPLETE_CONTROLS','semantic_rejections':bad,'malformed_rejections':5,'restored_whole_positive':True,'whole_record_sha256':hashlib.sha256(wire(reference)).hexdigest(),'trust':'full reference is cached only after a fresh complete direct mathematical audit; damages test the validation interface, not new mathematical proofs'}

if __name__=='__main__':print(wire(controls(json.load(open(sys.argv[1])))).decode())
