"""Actual defining-factor, original-scope and signed-radical failures."""
import copy,json
from pathlib import Path
from fractions import Fraction as F
from digit import T,Z,prove_zero
from geometry import model
from bindings import decode,scope,compile,require

def binding(data,system):
    m=model();f=decode(data,m['R']);compile(m,f,system)
    Q=m['a']*m['D']*Z*Z-2*m['D']*Z+2*T*T-T+1
    h=f['bound2'].q*f['bound2'].q*m['R']-f['bound2'].p*f['bound2'].p
    prove_zero(h+8*m['a']**4*m['b']**4*m['c']**2*m['J']*Q*f['bound2_square_factor'].p)

def signed(A,B,R,w,guard):
    A,B,R,w=map(F,[A,B,R,w]);require(w>0 and w*w==R,'actual positive root guard')
    H=B*B*R-A*A
    tests={'A+B+':A>0 and B>0,'B+H+':B>0 and H>0,'A+H-':A>0 and H<0}
    require(guard in tests and tests[guard],'full signed guard')
    require(A+B*w>0,'claimed affine positivity')

def check():
    original=json.loads(Path('FACTORS.json').read_text());system=json.loads(Path('SYSTEM.json').read_text());records=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError,KeyError):records.append({'name':name,'rejected':True})
        else:raise ValueError('actual mathematical damage accepted: '+name)
    for name in original['rows']:
        damaged=copy.deepcopy(original);row=damaged['rows'][name][0];row[3]=str(int(row[3])+7)
        reject('coefficient_'+name,lambda d=damaged:binding(d,system))
    for name,field,value in [
        ('missing_contact','original_contacts',system['original_contacts'][:-1]),
        ('additional_1_7','original_contacts',system['original_contacts']+[[1,7]]),
        ('alias_label','required_labels',[0,1,2,4,5,6,8,8,9,10,11,12]),
        ('unsigned_root','root','w*w=R'),('closed_endpoint_omitted','intervals_closed',False),
        ('changed_t_endpoint','t_interval',['14/25','594/1000']),
        ('changed_inner_endpoint','z_interval',['6/5','1399/1000']),
        ('prescribed_added_points','other_points','fixed_contacts'),
        ('extra_contact_hypothesis','additional_hypotheses',['5-12']),
        ('wrong_sheet','sheet',[1,1]),('nonstrict_regular','regularity','2G-a^4 C^2>=0'),
        ('dropped_actual_triple','residual_triples',system['residual_triples'][1:]),
        ('duplicated_actual_triple','residual_triples',[system['residual_triples'][0]]+system['residual_triples'][:-1]),
        ('cap_pair_not_excluded','incompatible_pairs',system['incompatible_pairs'][:-1]),
        ('equilateral_clique_dropped','equilateral_short_triples',system['equilateral_short_triples'][:-1])]:
        d=copy.deepcopy(system);d[field]=value;reject(name,lambda d=d:scope(d))
    for label in [98,99]:
        d=copy.deepcopy(system);d['cap_planes'][label-98]['normal'][0]+=1;reject('actual_cap_normal_'+str(label),lambda d=d:scope(d))
    for name in ['C0','delta']:
        d=copy.deepcopy(system);d['Farkas_positive_factors'][name]=d['Farkas_positive_factors'][name][:-1];reject('missing_positive_clearing_'+name,lambda d=d:binding(original,d))
    d=copy.deepcopy(original);d['rows']['bound0'][0][2]=2;reject('unsigned_radical_tag',lambda:binding(d,system))
    d=copy.deepcopy(original);d['variable_order']=['z','t','w'];reject('changed_variable_order',lambda:binding(d,system))
    for name,values in [('negative_root',(-2,1,9,-3,'B+H+')),('nonstrict_square',(1,1,1,1,'A+H-')),
        ('wrong_A',(-4,1,9,3,'A+H-')),('wrong_B',(-2,-1,9,3,'B+H+'))]:reject(name,lambda v=values:signed(*v))
    for values in [(1,1,1,1,'A+B+'),(-2,1,9,3,'B+H+'),(4,-1,9,3,'A+H-')]:signed(*values)
    return {'actual_damage_records':records,'all_damage_count':len(records),'valid_signed_radical_controls':3,
            'full_guard_failures_not_solver_statuses':True}

if __name__=='__main__':print(json.dumps(check(),sort_keys=True,separators=(',',':')))
