"""Exact closed receiver cover, local collar, original scope and old-P join."""
from pins import verify_pins
verify_pins()
from pathlib import Path
from collections import Counter
import argparse,copy,json
from kernel import F,Q,Z,O,phi,need,digest
from check_cell import CELLS
from check_collar import BOUNDS
HERE=Path(__file__).resolve().parent
CLASSIFICATION='lambda=1,physical t=0,original R in G union H_n G on stated ENTIRE closed receiving cell'

def join(cells,collars):
    need(len(cells)==8 and {r['cell'] for r in cells}==set(CELLS),'all eight distinct entire closed cells required')
    expected=json.loads((HERE/'expected.json').read_text())
    counts=Counter();minimum=None;mincell=None;geometry=None;rows=[]
    for r in cells:
        name=r['cell'];need(r['domain']['receiving_rectangle_in_s_units']==list(CELLS[name]),'changed closed cell bounds')
        need(r['all108_roots_covered'] and r['all_closed_children_retained'] and r['all_actual_controls_reparsed_and_rechecked'],'incomplete source continuum coverage')
        need(r['all_source_classification']==CLASSIFICATION,'original source/translation/scale/central branch changed')
        need(r['all_expected_source_control_streams_match'],'actual source stream not fully compared')
        need(all(r[k]==v for k,v in expected['cells'][name].items() if k!='parts'),'actual whole-cell mathematical record differs')
        need(geometry is None or geometry==r['geometry'],'source geometry differs across cells');geometry=r['geometry']
        m=F(*map(Q,r['minimum']));need(m>F(Q(1,100000)),'nonpositive or insufficient exact source margin')
        if minimum is None or m<minimum:minimum=m;mincell=name
        c=r['counts'];need(c['support']+c['gauge']==108+c['internal'] and c['tensor_coefficients']==40*c['support']+90*c['gauge'],'whole source tree/degree count differs')
        counts.update(c)
        rows.append({k:r[k] for k in ['cell','domain','counts','minimum','minimum_location','forest_sha256','whole_actual_records_sha256']})
    need(len(collars)==3 and {r['layer'] for r in collars}==set(range(3)),'all three complete closed receiving collar layers required')
    rectangles=[];physical=None;zeros=0;controls=0;dual_records=[]
    for r in sorted(collars,key=lambda r:r['layer']):
        need(r['actual_body_geometry_sha256']==geometry['actual_body_geometry_sha256'],'collar/source actual body differs')
        need(r['all_original_gap_corner_controls']==4320 and r['full_phase_norm_controls']==162,'collar physical inventory differs')
        need(physical is None or physical==r['whole_full_phase_supports'],'full support checks differ across collar layers');physical=r['whole_full_phase_supports']
        need(len(physical)==18 and {a['support'] for a in physical}==set(range(18)),'incomplete entire phase support inventory')
        for ar in physical:
            need(len(ar['height_controls'])==4 and all(F(*map(Q,a))>Z for a in ar['height_controls']),'nonpositive entire phase support height')
            nc=ar['norm_controls'];need(len(nc)==9 and {tuple(a['index']) for a in nc}=={(u,v) for u in range(3) for v in range(3)},'incomplete support norm controls')
            need(all(F(*map(Q,a['value']))>Z for a in nc) and ar['all240_original_gap_controls_nonnegative'],'whole phase support/norm control failed')
        need(len(r['closed_rectangles'])==2,'closed layer is missing a half')
        layer=r['layer']
        for half,row in enumerate(r['closed_rectangles']):
            bounds=(*BOUNDS[layer],*([('0','1/2'),('1/2','1')][half]))
            need(row['name']=='annulus'+str(layer)+str(half) and row['bounds']==list(bounds),'collar closed receiving seam differs')
            need(len(row['axes'])==6 and {(a['axis'],a['sign']) for a in row['axes']}=={(j,s) for j in range(3) for s in [-1,1]},'collar is missing a signed dual')
            for ar in row['axes']:
                for name,entries in ar['controls'].items():
                    need(name in ['determinant','num0','num1','num2','mass'] and len(entries)==16,'incomplete bicubic dual controls')
                    need({tuple(e['index']) for e in entries}=={(u,v) for u in range(4) for v in range(4)},'missing or duplicate bicubic index')
                    for e in entries:
                        a=F(*map(Q,e['value']));need(a>=Z if name.startswith('num') else a>Z,'actual signed dual control failed')
                        controls+=1;zeros+=int(a==Z)
                need(set(ar['controls'])=={'determinant','num0','num1','num2','mass'},'missing dual polynomial')
            need(row['coordinate_mass_bounds']==[max(a['mass'] for a in row['axes'] if a['axis']==j) for j in range(3)],'incorrect coordinate mass summary')
            rectangles.append(row);dual_records.append(row)
    masses=[max(r['coordinate_mass_bounds'][j] for r in rectangles) for j in range(3)]
    need(masses==[19,42,7] and controls==2880,'whole annulus mass or dual inventory differs')
    closure=F(Q(81,64))*F(sum(m*m for m in masses))/F(53**2)
    need(closure==F(Q(88047,89888))<O and (39-24*phi)/484<F(Q(1,53**2)),'closed core/collar contraction failed')
    intervals=[(Q(1,8),Q(3,16)),(Q(3,16),Q(1,4)),(Q(1,4),Q(3,8)),(Q(3,8),Q(1,2))]
    halves=[(Q(0),Q(1,2)),(Q(1,2),Q(1))]
    need({tuple(map(Q,b)) for b in CELLS.values()}=={(*x,*y) for x in intervals for y in halves},'closed receiving Cartesian product cover differs')
    need(all(intervals[j][1]==intervals[j+1][0] for j in range(3)) and halves[0][1]==halves[1][0],'closed receiving cover has a gap')
    s=2-phi;need(Z<s<F(Q(1,2)) and s/8<F(Q(1,20))<s/2 and s*s==5-3*phi,'published P overlap or entire raw triangle join failed')
    need(dict(counts)==expected['aggregate_counts'] and minimum.encode()==expected['minimum'] and mincell==expected['minimum_cell'],'whole inner-phase counts or minimum differ')
    return {'agent':'six-rupert-3','role':'researcher','status':'author-checked exact regional rigidity lemma; ordinary proof unformalized; independently UNREVIEWED',
        'closed_raw_receiving_triangle':[['0','0','1'],['s/2','0','1'],['s/2','s^2/2','1']],
        'classification':'lambda P_n R K+t subseteq P_n K iff lambda=1,t=0,R in G union H_n G',
        'original_scope':'EVERY original R in SO(3), physical t in n-perp, lambda>=1; all signed/projective G receiver images, arbitrary rolls, original halfturns and closed ties',
        'geometry':geometry,'cells':rows,'counts':dict(counts),'minimum':minimum.encode(),'minimum_cell':mincell,
        'margin':'1/100000','annular_collar':{'radius':'1/53','mass_bounds':masses,'closure':closure.encode(),
            'source_core_alpha':'1/22','actual_dual_controls':controls,'legitimate_zero_numerators':zeros,
            'whole_exact_dual_records_sha256':digest(dual_records)},
        'old_P_dependency':{'height':9037,'artifactRef':'bafkreiga3tnen3tjbmd36lgpveyfxcta6zyvnecje7gt2rxogdf7s7ebki',
            'source_commit':'49504817cd4e23b52419dbb91ca6970ec3554dd1',
            'reader_url':'https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_cauchy_transition_cones/PROOF.md',
            'old_checker_newly_replayed':False,'old_review_transferred':False},
        'whole_eight_cells_and_closed_P_overlap':True,'outer_x_greater_than_s_over_2':'OPEN','global_RID':'OPEN'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--cells',type=Path,nargs=8,required=True)
    p.add_argument('--collars',type=Path,nargs=3,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    need(not a.output.exists(),'fresh whole inner-phase record required')
    cells=[json.loads(x.read_text()) for x in a.cells];collars=[json.loads(x.read_text()) for x in a.collars]
    result=join(cells,collars);damages=[]
    tests=[('omit a closed receiving cell',lambda c,k:c.pop()),
           ('alter the closed receiving seam',lambda c,k:c[1]['domain']['receiving_rectangle_in_s_units'].__setitem__(0,'9/64')),
           ('negative actual source margin',lambda c,k:c[1].__setitem__('minimum',['-1','0'])),
           ('alter the actual source geometry',lambda c,k:c[1]['geometry'].__setitem__('new_source_closed_roots_sha256','wrong')),
           ('discard original H_n G branch',lambda c,k:c[1].__setitem__('all_source_classification','G only')),
           ('omit a complete closed collar layer',lambda c,k:k.pop()),
           ('negative exact Cramer numerator',lambda c,k:k[0]['closed_rectangles'][0]['axes'][0]['controls']['num0'][0].__setitem__('value',['-1','0'])),
           ('zero exact determinant control',lambda c,k:k[0]['closed_rectangles'][0]['axes'][0]['controls']['determinant'][0].__setitem__('value',['0','0'])),
           ('discard a signed collar dual',lambda c,k:k[0]['closed_rectangles'][0]['axes'].pop())]
    for title,mutation in tests:
        c,k=copy.deepcopy(cells),copy.deepcopy(collars);mutation(c,k)
        try:join(c,k)
        except ValueError as e:damages.append({'control':title,'rejected':str(e)});continue
        raise ValueError('damaged mathematical join accepted')
    result['nine_semantic_closed_join_controls']=damages
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','counts','minimum','annular_collar','global_RID']}),flush=True)

if __name__=='__main__':main()
