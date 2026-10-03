"""LATE correspondence to the pinned9954 whole record; no target code imports.
Primary seal predates this file and target executable/data exposure.
The comparison uses independently reconstructed exact primitives, not native hashes
as mathematical premises. Supply the pinned native EXPECTED.json as the argument.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib
import core as c
import controls as g
import check

def main(path):
    target=json.loads(path.read_text(),object_pairs_hook=check.object_pairs)
    need=c.need;own=check.build();rows=[]
    def same(name,left,right):
        check.strict_equal(left,right,name);rows.append(name)
    budgets=target['fresh_complete_budgets'];m=own['core']['maps'];r=m['receiving_whole_budgets']
    same('complete coefficient A',m['receiving_A'],budgets['all_coefficient_A'])
    same('complete coefficient B',m['receiving_B'],budgets['all_coefficient_B'])
    same('complete full derivative budget',r['cd'],budgets['derivative_coefficient'])
    same('complete full root divisor',r['bd'],budgets['full_root_divisor'])
    for branch in budgets['branches']:
        b=F(branch['displacement_scale']);a=F(11999,12000);s=F(r['s']);cd=F(r['cd'])
        fresh=4*s**7*b*b/a**8+b*cd/(9*a**8)
        same('nonlinear '+branch['name'],str(fresh),branch['full_nonlinear_cost'])
        if branch['name']=='cube':
            same('cube numerator',r['nc'],branch['N'])
            same('complete paired cube normal',r['pair'],branch['pair_cost'])
            same('complete individual cube normal',r['individual'],branch['individual_cost'])
        else:
            same('all9 numerator',r['n'],branch['N'])
    same('full R3',str(F(63401,3600)),budgets['complete_paired_R3_cost'])
    same('full noncubic R4',str(F(47809,1800)),budgets['complete_paired_R4_noncubic_cost'])
    for name in ['physical','objective']:
        route=next(z for z in budgets['routes'] if z['name']==name)
        same(name+' PSD a0',m[name+'_costs']['a0'],route['a0'])
        same(name+' PSD b0',m[name+'_costs']['b0'],route['b0'])
        same(name+' complete original cost',m[name+'_costs']['cost'],budgets['complete_'+name+'_cost'])
    boot=target['complete_actual_entry_to_LC_budgets']
    same('broad paired full cost',m['broad_whole_budgets']['pair'],boot['broad_pair_cost'])
    same('broad individual full cost',m['broad_whole_budgets']['individual'],boot['broad_individual_cost'])
    same('preliminary paired full cost',m['fine_preliminary_whole_budgets']['pair'],boot['preliminary_fine_pair_cost'])
    same('preliminary individual full cost',m['fine_preliminary_whole_budgets']['individual'],boot['preliminary_fine_individual_cost'])
    for stage in boot['two_square_forward_stages']:
        name=stage['prior_V_cap']+'_to'+stage['new_V_cap']
        const=m[name+'_constants']
        for key,k in [('K','whole_K'),('G','whole_G'),('B','complete_square_cost'),('divisor','whole_divisor')]:
            same(name+' '+key,const[key],stage[k])
    # ALL126 six-coordinate field vectors, including zeros.
    tables=target['whole_phase_maps']['whole_nine_phase_tables']
    need(len(tables)==9,'entire native nine-phase table')
    for table in tables:
        k=str(table['phase']);need(len(table['all_seven_lower_degrees'])==7,'entire native seven lower degrees')
        for row in table['all_seven_lower_degrees']:
            j=str(row['degree']);our=own['core']['all9_phase_maps'][k][j]
            disp=[str(-F(v)/9) for v in our['displacement']]
            same('phase'+k+' d'+j+' whole displacement',disp,row['complete_displacement_field'])
            same('phase'+k+' d'+j+' whole paired normal',our['paired'],row['complete_pair_normal_field'])
    # Five complete native input multisets, integrated here without target helpers.
    for control in target['complete_arbitrary_critical_controls']:
        z=[tuple(F(t)for t in pair)for pair in control['complete_critical_multiset']]
        need(len(z)==8,'all eight control multiplicities')
        mean=g.scale(g.add(*z),F(1,8));nu=[g.add(t,g.scale(mean,-1))for t in z]
        u=g.add(g.ga(F(11999,12000)),g.scale(mean,-1));V=sum((g.norm(t)for t in nu),F(0))
        T=g.add(*(g.power(t,2)for t in nu));U=g.add(*(g.power(t,3)for t in nu))
        QJ=g.mul(T,g.mul(g.cj(u),g.inv(u)));E=(V+QJ[0])/2
        product=g.polynomial(nu);p=[g.ga()]+[g.scale(t,F(9,j+1))for j,t in enumerate(product)]
        p[0]=g.scale(g.at(p,u),-1)
        enc=lambda pair:list(map(str,pair))
        ix=str(control['index'])
        for name,fresh in [('complete_centered_multiset',list(map(enc,nu))),('mean',enc(mean)),('u',enc(u)),
                           ('centered_energy',str(V)),('rotated_real_energy',str(E)),('rotated_trace',enc(QJ)),
                           ('whole_T',enc(T)),('whole_U3',enc(U)),('complete_centered_primitive',list(map(enc,p))),
                           ('complete_derivative_product',[enc(g.scale(t,9))for t in product])]:
            same('nativecontrol'+ix+' '+name,fresh,control[name])
        motions=control['all_nine_linear_motions'];need(len(motions)==9,'native all-nine control motions')
        for motion in motions:
            k=motion['phase'];value=g.embed(p[0])
            for j in range(1,10):
                value=g.ea(value,g.em(g.embed(g.mul(p[j],g.power(u,j))),g.ep(k*j)))
            raw=g.em(g.es(value,F(-1,9)),g.em(g.embed(g.power(u,-8)),g.ep(-8*k)))
            cleared=g.es(raw,g.norm(u)**8)
            same('nativecontrol'+ix+' complete12 motion'+str(k),g.encoded(cleared),motion['FULL_clear_r16_displacement'])
        same('control feasibility scope'+ix,False,control['actual_original_disk_feasibility_claimed'])
        same('control receiving scope'+ix,False,control['receiving_hypotheses_or_objective_cuts_claimed'])
    seal=json.loads(Path(__file__).with_name('PRIMARY_SEAL.json').read_text())
    unchanged=all(hashlib.sha256(Path(__file__).with_name(n).read_bytes()).hexdigest()==v for n,v in seal['files'].items())
    need(unchanged,'six primary files remain unchanged after target access')
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'late_comparison_after_native_access':True,'target_code_imported':False,
            'six_primary_files_unchanged':unchanged,'comparisons':rows,
            'comparison_count':len(rows),'all126_phase_field_vectors_equal':True,
            'all5_full_native_control_records_and45_twelve_coordinate_motions_equal':True}

if __name__=='__main__':
    out=main(Path(sys.argv[1]));Path(__file__).with_name('CORRESPONDENCE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items()if k!='comparisons'},sort_keys=True))
