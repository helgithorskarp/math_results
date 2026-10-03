"""Meaningful typed-record and arithmetic-source damages, on fresh results.

Fixtures use path copying from whole checked fresh records; equal may skip
identical unchanged fixture subtrees only after full independent validation.
"""
import json
from pathlib import Path
from semantic import equal,need

def replace(root,path,value):
    if not path:return value
    key=path[0];out=dict(root)if type(root)is dict else list(root);out[key]=replace(root[key],path[1:],value);return out

def record_controls(bundle):
    examples=[]
    def damage(name,key,path,value):
        original=bundle[key];bad=replace(original,path,value)
        try:equal(original,bad,fixtures=True)
        except ValueError as e:
            need(str(e).startswith(('type mismatch','keys at','length at','value at')),'unrelated damage rejection');examples.append({'name':name,'record':key,'path':list(path),'rejected':True,'reason':str(e)})
        else:raise ValueError('damage accepted: '+name)
    c=bundle['context'];f=bundle['first'];p=bundle['phases'];s=bundle['symmetry'];g=bundle['gluing']
    for name,path,value in(
        ('literal12phase',('literal_prefix',4,1),11),('essential-as-int',('essential16_32',),1),('actual-allocation',('productive_allocation',),[3,6]),('hole177',('BASE_holes_lower_bound',),176),('original-distinctness',('original_moduli_distinct',),False),('proper-divisorLCM',('proper_divisor_actual_LCM_allowed',),False),('unproductive-selected-freedom',('selected_unproductive_tails_allowed',),False)):
        damage(name,'context',path,value)
    for name,path,value in(
        ('initialRpoint',('initial_R',0),-1),('literalBASEphase',('domain','prefix',3,1),1),('essential-record',('domain','essential16_32_required'),False),('BASE-label-omitted',('domain','unused_BASE_originals'),f['domain']['unused_BASE_originals'][:-1]),('small-omission',('small_shadows',0,'omission_allowed'),False),('small-phase-lost',('small_shadows',0,'phase_populations','15'),f['small_shadows'][0]['phase_populations']['15'][:-1]),('pair-phase-population',('raw_pair_unions',0,'values',0),f['raw_pair_unions'][0]['values'][0]+1),('pair-label',('raw_pair_unions',0,'original_cofactors',0),3),('group-bound',('group_bounds',1),f['group_bounds'][1]+1),('missing-inventory',('inventories',0,'rows'),f['inventories'][0]['rows'][:-1]),('missing-phase-block',('phase_blocks',),f['phase_blocks'][:-1])):
        damage(name,'first',path,value)
    for name,path,value in(
        ('canonical-row-lost',(0,'rows'),p[0]['rows'][:-1]),('Q-original-phase',(0,'rows',0,'original_phases',3),p[0]['rows'][0]['original_phases'][3]+32),('Q-arm-omitted',(0,'rows',0,'Q_arms'),[10,10]),('orbit-weight',(0,'rows',0,'orbit_weight'),p[0]['rows'][0]['orbit_weight']+1),('repair-bitmap',(0,'rows',0,'repair_mask_hex'),'0'),('repair-population',(0,'rows',0,'repair_size'),p[0]['rows'][0]['repair_size']+1),('witness-bool-as-int',(0,'rows',0,'exclusive_initial_witness',0),int(p[0]['rows'][0]['exclusive_initial_witness'][0])),('necessary-test-bool',(0,'rows',0,'survives_necessary_tests'),not p[0]['rows'][0]['survives_necessary_tests']),('full-phase-weight',(0,'raw_weight'),p[0]['raw_weight']+1)):
        damage(name,'phases',path,value)
    for name,path,value in(
        ('generator-branch',('generators',0,'generator',0),9),('original-family-lost',('generators',0,'family_images'),s['generators'][0]['family_images'][:-1]),('original-image',('generators',0,'family_images',0,'phase_images',0),1),('fixed-literal',('generators',0,'placed_fixed',0,1),1),('membership-domain',('generators',0,'physical_membership_domain_size'),1)):
        damage(name,'symmetry',path,value)
    row=g['shapes'][0];br=row['BASE_phase_rows'][0]
    for name,path,value in(
        ('fixed-parent6-lost',('fixed_parent6',),g['fixed_parent6'][:-1]),('final-shadow-lost',('shapes',),g['shapes'][:-1]),('protected177-budget',('shapes',0,'protected_budget'),row['protected_budget']+1),('outside-needed',('shapes',0,'outside_need'),row['outside_need']-1),('final-original-lost',('shapes',0,'BASE_phase_rows'),row['BASE_phase_rows'][:-1]),('final-phase-lost',('shapes',0,'BASE_phase_rows',0,'phases'),br['phases'][:-1]),('protected-population',('shapes',0,'BASE_phase_rows',0,'phases',0,0),br['phases'][0][0]+1),('outside-population',('shapes',0,'BASE_phase_rows',0,'phases',0,1),br['phases'][0][1]+1),('omission-as-int',('shapes',0,'BASE_phase_rows',0,'omission_allowed'),1),('relaxed-max',('shapes',0,'BASE_phase_rows',0,'outside_max_with_omission'),br['outside_max_with_omission']+1),('positive-deficit',('shapes',0,'deficit'),row['deficit']+1)):
        damage(name,'gluing',path,value)
    # Key-order changes and exact copies preserve typed mathematical content.
    positives=[]
    for key in('context','first','symmetry','gluing'):
        obj=bundle[key];copy=dict(reversed(list(obj.items())));equal(obj,copy,fixtures=True);positives.append({'record':key,'key_order_preserved_math':True})
    return {'negative_controls':examples,'positive_controls':positives,'scope':'typed complete fresh reference channel, not a third arithmetic kernel; unchanged fixture subtrees may use identity only after whole fresh comparison'}

def source_controls(source,out,run,bundle,phase_reference):
    out=Path(out);out.mkdir();receipts=[]
    jobs=[('first-union-intersection','first_stage.py','union=lambda a,b:a|b','union=lambda a,b:a&b','first',['partition'],bundle['first']),('physical-lift-omitted','phase_rows.py','for k in range(4)','for k in range(3)','phases',['component',str(Path(phase_reference).resolve()),'0','5'],bundle['phases'][:5])]
    for name,file,old,new,key,args,reference in jobs:
        text=(source/file).read_text();need(old in text,'source fixture anchor');damaged=out/(name+'.py');damaged.write_text(text.replace(old,new,1));product=out/(name+'.json');run(damaged,args+[str(product)],'source-'+name)
        obj=json.loads(product.read_bytes())
        try:equal(reference,obj)
        except ValueError as e:receipts.append({'name':name,'completed_arithmetic':True,'rejected_by_fresh_math':True,'reason':str(e),'hash_gate_used':False})
        else:raise ValueError('source damage accepted: '+name)
    name='nonbranch-symmetry';text=(source/'symmetry.py').read_text();need('(9,(3,6))'in text,'symmetry fixture anchor');damaged=out/(name+'.py');damaged.write_text(text.replace('(9,(3,6))','(9,(3,5))',1));product=out/(name+'.json');p=run(damaged,['literal',str(product)],'source-'+name,allow_failure=True)
    need(p.returncode!=0 and 'ValueError: one SAME-original phase image'in p.stderr,'invalid branch must fail original-family mathematics');receipts.append({'name':name,'completed_rejection':True,'reason':'one SAME-original phase image','hash_gate_used':False,'timeout_used':False})
    return receipts
