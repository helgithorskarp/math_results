"""Late complete comparison; target executables are never imported here."""
import argparse,json,hashlib
from pathlib import Path
from rows import need,encoded

def adapted(row):
 return {'fixture':row['fixture'],'hub_high':row['hubs'],'h':row['h'],'e':row['e'],'k':row['k'],'q':row['q'],
 'eligible':row['eligible'],'g1_S':row['g1'],'ss_excess':row['sigma'],
 'hub_weight':sum(5-row['replication'][v]for v in row['hubs']),
 'psi':row['psi'],'margin':row['margin3'],'ss_hist':row['colors']}

def compare(own,original,fixture):
 need(encoded(sorted((adapted(r)for r in own['physical']),key=lambda r:(r['fixture'],r['hub_high'])))==encoded(original['rows']),'every426 physical color field')
 original_types=original['inventory']['types']
 lookup={tuple([r['e'],r['k'],r['q'],r['eligible'],tuple(r['ss_hist']),r['psi'],r['margin']]):i for i,r in enumerate(original_types)}
 mapping={i:lookup[tuple(t[:4])+tuple([tuple(t[4])])+tuple(t[5:])]for i,t in enumerate(own['types'])}
 need(len(mapping)==len(set(mapping.values()))==len(original_types)==56,'all56 types')
 branchmap={(b['Q'],b['T'],b['X'],b['tau']):b for b in original['inventory']['branches']}
 n=0
 reason={'odd-color':'odd_weight_layer','distinct-endpoints':'too_few_weighted_partners','radius-two':'hub_complete_radius_two'}
 for b in own['branches']:
  old=branchmap[(b['Q'],b['T'],b['X'],b['tau'])]
  for f in ('E','K','margin_budget'):need(b[f]==old[f],'branch scalar')
  actual={tuple(sorted((mapping[i],c)for i,c in enumerate(r['counts'])if c)):r for r in b['records']}
  expected={tuple(tuple(x)for x in r['population']):r for r in old['templates']}
  need(set(actual)==set(expected),'EVERY raw population, independent of type order')
  for key,r in actual.items():
   fail=expected[key]['failures'];need((r['failure']is None)==(not fail),'necessary survival entry')
   if r['failure']is not None:need(reason[r['failure']['reason']]in fail,'independent first obstruction is a native obstruction')
   n+=1
 need(len(branchmap)==20 and n==118,'complete original domain')
 need(encoded(original['inventory'])==encoded(fixture),'whole native frozen inventory')
 return {'all_physical_rows':426,'all_types':56,'all_branches':20,'all_raw_populations':118,'every_necessary_survival_compared':True,'every_first_obstruction_corroborated':True,'all_native_failure_lists_claimed_equal':False,'target_executable_imported':False,
  'native_whole_record_sha256':hashlib.sha256(encoded(original)).hexdigest()}

def main():
 p=argparse.ArgumentParser();p.add_argument('--own',type=Path,required=True);p.add_argument('--original',type=Path,required=True);p.add_argument('--expected',type=Path,required=True);a=p.parse_args()
 print(json.dumps(compare(json.loads(a.own.read_bytes()),json.loads(a.original.read_bytes()),json.loads(a.expected.read_bytes())),sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
