"""Late native corroboration; neither author computation is reviewer premise."""
import pathlib,sys,json,copy,collections
P=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(P/'author'));import producer,oracle
sys.path.insert(0,str(P/'core'));import audit as a

def convert(t):
    a.need(t[10]==t[0]+t[1]-t[8],'native redundant hub weight')
    return tuple(t[:5])+(t[5],t[8],t[6],t[9],t[7])
def key(c):return tuple(c[k] for k in ('N5','T','X','tau','Q','E','K','margin_budget'))
def validate(native,own):
    stars=json.loads((P/'core/fixtures.json').read_text())['stars'];oldstars=json.loads((P/'five_hub_pair_total36/fixtures.json').read_text())['stars']
    a.need(stars==oldstars,'every literal23 block array')
    raw,sel,types=a.c.raw_and_types(stars)
    def theirs(rs):return {(r['fixture'],tuple(r['hub_high'])):convert(r['coordinates']) for r in rs}
    def ours(rs):return {(r['star'],tuple(r['hubs'])):tuple(r[k] for k in ('e','k','q','eligible','h','g1','sigma','psi','I5','margin')) for r in rs}
    a.need(theirs(native['actual_marks'])==ours(raw),'every426 raw mark coordinate')
    a.need(theirs(native['conservative_marks'])==ours(sel),'every410 capped mark coordinate')
    a.need(sorted(map(convert,native['types']))==types,'all51 physical types')
    lookup={key(c):c for c in own['all_cases']}
    a.need(native['scalar_cases']==a.independent_scalars(),'all136 exact scalar cases')
    a.need(len(native['branches'])==len(lookup),'complete136 branches')
    reasonmap={'9538_EXCEPTIONAL_SURCHARGE':'isolated_exception_radius','COMPLEMENT_TRIANGLE_TYPE20_CAP':'complement_triangle_n20',
      'T1_HUB_DELTA_CAP':'T1_hub_weight','T1_ELIGIBLE_SINGLE_HUB_CAP':'T1_n20','T1_DEGREE_ONE_SINGLE_HUB_CAP':'T1_n22','9538_ELIGIBLE_UNIT_ROOT_CAPACITY':'eligible_unit_plus_root'}
    oldmap={'UNIT_NEIGHBOR_CAPACITY':'unit_endpoint','DISTINCT_RADIUS_TWO_CROSSINGS':'distinct_crossing','ALL_COLORS_CLOSED_PARTITION':'all_color_closure'}
    count=0;matched=[]
    for b in native['branches']:
      case=lookup.pop(key(b['case']));ours={tuple((tuple(t),n) for t,n in r['population']):r for r in case['vectors']}
      a.need(len(ours)==len(b['rows']),'complete per-branch population counts')
      for r in b['rows']:
       sparse=tuple(sorted((convert(t),n) for t,n in zip(native['types'],r['vector']) if n))
       a.need(sparse in ours,'unique native full population belongs to sealed carrier')
       o=ours.pop(sparse);m=o['metrics'];cert=r['certificate'];reason=cert['reason']
       if reason=='OLD_FROZEN_CUT':
        cert=cert['cut'];a.need(oldmap[cert['reason']] in o['all_failures'],'native OLD full cut independently true')
        for f in ('D','I','C1','C2','B2'):a.need(cert[f]==m[f],'native old exact endpoint coordinate')
       else:
        a.need(reasonmap[reason] in o['all_failures'],'native new certificate independently true')
        if reason=='9538_ELIGIBLE_UNIT_ROOT_CAPACITY':
         for k,k0 in [('R','R'),('D_A','DA'),('D_V','DV'),('I_even','I_even'),('C1','C1')]:a.need(cert[k]==m[k0],'native every root-certificate coordinate')
         a.need(cert['required']==m['DV']+max(m['R'],m['DA']-m['I_even']),'native root requirement exact')
       matched.append([b['case'],sparse,reason]);count+=1
      a.need(not ours,'no omitted sealed population')
    a.need(not lookup,'no omitted scalar branch')
    controls=[];totalassign=0
    a.need(len(native['deficit_calibration'])==5985,'all calibration column totals')
    for row,D in zip(native['deficit_calibration'],a.compositions(17,5)):
      a.need(tuple(row['D'])==D,'every ordered column composition')
      ok=all(D[u]+D[v]<=10 for u,v in a.it.combinations(range(5),2))
      want=[]
      if ok:
       for n in a.it.product(*(range(D[j]//2+1) for j in range(5))):
        if all(not n[j] or D[j]>=max(2*n[j],4+n[j]) for j in range(5)):want.append(n)
      a.need(row['pair_cap_valid']==ok and [tuple(x) for x in row['eligible_counts']]==want,'EVERY eligible column-support assignment')
      totalassign+=len(want);controls.append([D,want])
    return dict(full_vectors=count,whole_native_to_sealed_mapping_sha256=a.digest(matched),all_5985_column_totals_and_2325_assignments=True,assignments=totalassign,full_column_assignment_sha256=a.digest(controls))

def run():
    own=json.loads((P/'core/core-record.json').read_text());native,_=producer.build();other,_=oracle.build()
    a.need(native==other,'entire native producer/oracle records')
    a.need(producer.digest(native)==json.loads((P/'author/EXPECTED.json').read_text())['whole_record_sha256'],'native full expected record')
    record=validate(native,own);record.update(agent='six-reviewer-5',role='independent mathematical reviewer',after_independent_seals=True,native_whole_sha256=producer.digest(native),own_sealed_sha256=a.digest(own))
    # Scope/coverage corruption controls: explicit non-native validator checks.
    damages=[]
    for kind in ('missing_branch','missing_vector','duplicated_vector','altered_eligibility','altered_hub_weight','altered_root_C1','altered_column_assignment'):
      d=copy.deepcopy(native)
      if kind=='missing_branch':d['branches'].pop()
      elif kind=='missing_vector':next(b for b in d['branches'] if b['rows'])['rows'].pop()
      elif kind=='duplicated_vector':
       b=next(b for b in d['branches'] if b['rows']);b['rows'].append(copy.deepcopy(b['rows'][0]))
      elif kind=='altered_eligibility':d['actual_marks'][0]['coordinates'][3]=not d['actual_marks'][0]['coordinates'][3]
      elif kind=='altered_hub_weight':d['actual_marks'][0]['coordinates'][10]+=1
      elif kind=='altered_root_C1':
       r=next(r for b in d['branches'] for r in b['rows'] if r['certificate']['reason']=='9538_ELIGIBLE_UNIT_ROOT_CAPACITY');r['certificate']['C1']+=1
      else:next(r for r in d['deficit_calibration'] if r['eligible_counts'])['eligible_counts'].pop()
      try:validate(d,own)
      except (ValueError,KeyError):damages.append(kind)
      else:raise ValueError('unrejected coverage/semantic alteration:'+kind)
    record['seven_detected_coverage_semantic_alterations']=damages
    (P/'CORROBORATION.json').write_bytes(a.encode(record));print(json.dumps(record,indent=2))
if __name__=='__main__':run()
