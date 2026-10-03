"""Post-seal DATA-only translation; never imports target executable code.

Usage: python3 compare_native.py /path/to/pinned/native/CERTIFICATE.json
Entire native typed certificate is compared, not aggregate counts.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import hashlib
import json
import sys
import audit


def patch(faces, whole_triangles):
    graph = set().union(*(audit.edges(t) for t in faces))
    rem = audit.residual_cycle(graph, whole_triangles)
    earlier = set(faces[0]); fresh = []
    for t in faces[1:]:
        new = set(t)-earlier
        audit.require(len(new) == 1, 'translated fresh corner')
        fresh.extend(sorted(new));earlier.update(t)
    return {'faces':[list(t) for t in faces],'support':sorted(earlier),
            'edges':[list(e) for e in sorted(graph)],
            'tree_edges':[[i,j] for i,j in combinations(range(len(faces)),2)
                          if len(set(faces[i])&set(faces[j])) == 2],
            'fresh_attachment_corners':fresh,'boundary':list(audit.unoriented(rem))}


def translated_primary():
    r = audit.whole_record()
    ts,rem = audit.coherent_faces(audit.G20,audit.A+audit.B,(audit.P,))
    out = {'schema':'g20-five-cycle-routing-v1','local_band':['1/2','3/5'],
           'separated_profile_band':r['profile_screen_band'],
           'patch_A':patch(audit.A,ts[:4]),'patch_B':patch(audit.B,ts[4:]),
           'G20_edges':r['G20']['edges'],'G20_VEF':[12,20,10],
           'P':list(audit.P),'R':list(audit.R)}
    out['boundary_pairings']=[{'lengths':sorted(map(len,x)),'cycles':x} for x in r['annulus_pairings']]
    names={'strict7-9':'strict-internal-noncontact-7-9','crossing':'alternating-endpoints',
           'degree6at5':'six-neighbors-at5','five-triangle-star-at5':'five-triangles-at5',
           'a-b-rhombus-at10':'U-quad-angle-star-at10'}
    rows=[]
    for x in sorted(r['pentagon_cases'],key=lambda x:(len(x['chords']),x['chords'])):
        chords=[tuple(e) for e in x['chords']]
        reason=x['reason']
        if reason=='necessary-survivor':name='possible-V' if chords else 'possible-empty'
        elif reason=='gamma-rhombus':
            name='W-quad-partner-below-alpha' if (7,10) in chords else 'Z-quad-partner-below-alpha'
        else:name=names[reason]
        rows.append({'diagonals':x['chords'],'crossing_pairs':[[list(e),list(f)] for e,f in combinations(chords,2)
                                                             if audit.alternating(e,f)],
                     'reason':name,'retained':reason=='necessary-survivor'})
    out['all_diagonal_subsets']=rows
    # Original-band scalar arithmetic independently evaluated here, after seal;
    # wider primary margins remain separate and unchanged.
    lo,hi=F(1,2),F(3,5)
    scalar={'lo':lo,'hi':hi,'lo_minus_half':lo-F(1,2),
            'lo_squared_minus_one_fifth':lo**2-F(1,5),
            'three_eighths_minus_upper_angle_cosine':F(3,8)-hi/(1+hi),
            'sqrt2_upper_squared_gap':F(23,16)**2-2,
            'sqrt5_upper_squared_gap':F(7,3)**2-5,
            'sqrt5_lower_squared_gap':5-F(11,5)**2,
            'nine_c_squared_minus_two_c_minus_one_at_lo':9*lo**2-2*lo-1,
            'derivative_lower':18*lo-2,'one_minus_hi':1-hi}
    out['parameter_checks']={k:str(v) for k,v in scalar.items()}
    degrees=dict(r['V']['degrees']);vgraph={tuple(e) for e in r['V']['edges']}
    out['V_degree_restrictions']=[{'vertex':v,'required_neighbors':sorted(b if a==v else a for a,b in vgraph if v in (a,b)),
                                  'minimum_degree':degrees[v],'maximum_degree':cap}
                                 for v,cap in [(5,5),(9,4),(10,5),(12,4)]]
    out['V_degree10_five_forced_faces']=[[2,10,'x'],[9,10,'x']]
    reasons={0:'degree-seven',11:'degree-six',4:'strict-4-10-at1-two-alpha',
             6:'strict-6-9-at11-three-alpha',8:'strict-8-10-at2-three-alpha',
             5:'excluded-U',7:'excluded-W'}
    core_rows=[]
    for v,why in r['fresh_core_candidates']:
        if why in ('self','existing10neighbor'):continue
        graph=vgraph|{audit.edge(v,w) for w in (2,9,10)}
        core_rows.append({'candidate':v,'required_neighbors':sorted(b if a==v else a for a,b in graph if v in (a,b)),
                          'reason':reasons[v]})
    out['V_degree10_five_noncore_check']=core_rows
    order=audit.A+((5,7,12),)+audit.B+((2,10,3),(9,10,3))
    primary_order=audit.A+audit.B+((5,7,12),(2,10,3),(9,10,3))
    mapping={i:next(j for j,t in enumerate(order) if frozenset(t)==frozenset(face))
             for i,face in enumerate(primary_order)}
    dual=sorted(sorted((mapping[i],mapping[j])) for i,j in r['G24_triangle_dual_edges'])
    components=sorted(sorted(mapping[i] for i in part) for part in r['G24_triangle_components'])
    out['V_degree10_five_required_G24']={'fresh_symbol':3,'edges':r['G24']['edges'],
                                       'faces':[list(t) for t in order],'full_TT_edges':dual,'components':components}
    out['disk_allocations']=[{'branch':x['branch'],'TQP':x['TQP'],'boundary_vertices':11,
                             'interior_vertices':x['interior_points'],'interior_edges':x['inner_contacts'],
                             'inner_faces':x['faces']} for x in r['residual_budgets'][:2]]
    out['all_partitions_checked']=len(r['profiles']['cohort_partitions'])
    out['separated_profiles']=sorted({tuple(x['profile']) for x in r['profiles']['assignments']})
    out['separated_profiles']=[list(x) for x in out['separated_profiles']]
    out['oriented_component_assignments']=[{'profile':x['profile'],'e':x['eNN'],'A':x['A'],'B':x['B'],'other':x['others'],
                                          'P_branch_retained':True,'V_branch_retained':x['V_possible'],
                                          'V_degree10_five_retained':x['V_and_degree10five_possible']}
                                         for x in r['profiles']['assignments']]
    return out


def main():
    certificate=Path(sys.argv[1]);native=json.loads(certificate.read_text())
    expected=translated_primary()
    audit.require(audit.canonical(native)==audit.canonical(expected), 'whole native typed mathematical correspondence')
    seal=json.loads((Path(__file__).resolve().parent/'SEAL.json').read_text())
    for name,entry in seal['primary_files'].items():
        b=(Path(__file__).resolve().parent/name).read_bytes()
        audit.require(len(b)==entry['bytes'] and hashlib.sha256(b).hexdigest()==entry['sha256'], 'unchanged primary seal '+name)
    print(json.dumps({'status':'PASS','postseal_DATA_only':True,'target_code_imported':False,
                      'entire_typed_native_certificate_equal':True,'native_fields':len(expected),
                      'native_certificate_bytes':certificate.stat().st_size,
                      'native_certificate_sha256':hashlib.sha256(certificate.read_bytes()).hexdigest(),
                      'all8_primary_seals_unchanged':True,
                      'extra_independent_theorems':'widerK+[7/15,8/13]; retained physical[7/15,19/31]; G24 residual0T2Q3P/two points/six contacts/five faces'},sort_keys=True))


if __name__=='__main__':main()
