#!/usr/bin/env python3
"""Fresh exact origin-pencil census and odd-valuation projection filter."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import argparse,json,subprocess,sys
import projection as P
PREV=P.ROOT/'hadwiger_nelson_ramified_a159_bridge_orbits/field_filter.py'

def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);args=p.parse_args();W=args.work;W.mkdir(parents=True,exist_ok=True)
 P.need(sha256(PREV.read_bytes()).hexdigest()=='d4864a53a0fa87f170c0f3064d094d6b6783bf962a1c3a56e12f83e7669dab57','previous filter dependency')
 subprocess.run([sys.executable,'-B',str(PREV),'--work',str(W/'previous')],check=True,stdout=subprocess.DEVNULL)
 rows=json.loads((W/'previous/field-rows.json').read_text());summary=json.loads((W/'previous/field-summary.json').read_text());additional=[];remaining=[];odd_total=0
 for r in rows:
  d=tuple(map(F,r['D']));vp=P.valuation_real(d,1);vm=P.valuation_real(d,-1);P.need(vp==r['plus']['valuation'] and vm==r['minus']['valuation'],'valuation implementation mismatch');odd=vp%2==1 or vm%2==1;odd_total+=odd;prior=r['embeds_plus'] or r['embeds_minus']
  if odd and not prior:
   sign=1 if vp%2 else -1;P.certify_radicand(d,sign);additional.append(r|{'projection_embedding':sign})
  if not odd and not prior:remaining.append(r)
 fields=[r for r in summary['remaining_fields'] if not(r['example']['plus']['valuation']%2 or r['example']['minus']['valuation']%2)]
 out={'classes':len(rows),'previous_square_embedding_exclusions':summary['embeddable_classes'],'odd_valuation_classes':odd_total,'additional_projection_exclusions':len(additional),'total_whole_field_exclusions':len(rows)-len(remaining),'unresolved_classes':len(remaining),'unresolved_fields':[{'D':r['D'],'classes':r['classes'],'max_edges':r['max_edges']} for r in fields],'remaining_max_contacts':max(r['edges'] for r in remaining),'remaining_is_not_nonfour_evidence':True}
 P.need((out['classes'],out['odd_valuation_classes'],len(additional),len(remaining))==(1490,218,146,84),'filter count');P.need(sum(r['classes'] for r in fields)==84,'field partition')
 (W/'additional.json').write_text(json.dumps(additional,separators=(',',':'))+'\n');(W/'remaining.json').write_text(json.dumps(remaining,separators=(',',':'))+'\n');(W/'filter.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
