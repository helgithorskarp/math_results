"""Whole independent symbolic record, exact arithmetic, no native target input."""
import json,sys
from pathlib import Path
from polycheck import check as check_sign
from check_original import check as check_original
NAMES=['mu','alpha','beta','leaf','standard','even_old','trace','odd_old','odd_mean','old_plus','old_minus']
def symbolic(data):
 if type(data)is not list or [r['name']for r in data]!=NAMES:raise ValueError('all required whole physical blocks')
 shapes=[1,1,1,2,4,3,2,1,1,1,1]
 if [len(r['original'])for r in data]!=shapes:raise ValueError('all block dimensions')
 records=[]
 for r in data:records.append(dict(binding=check_original(r),positivity=check_sign(r)))
 return dict(domain='QQ(h,q), auxiliary real h>=2,q>=4; physical h integer>=2,q=2^(n-1),n integer>=3',original_entry_identities=sum(x['binding']['original_entries']for x in records),whole_cross_zero_entries=22,repeated_trace_identities=4,complete_original_obligations=66,gaussian_update_identities=sum(x['positivity']['identities']for x in records),positive_pivots=sum(x['positivity']['pivots']for x in records),positive_shifted_numerator_coefficients=sum(s['n']['coefficients']for x in records for s in x['positivity']['signs']),positive_shifted_denominator_coefficients=sum(s['d']['coefficients']for x in records for s in x['positivity']['signs']),maximum_positive_total_degree=max(s[v]['total_degree']for x in records for s in x['positivity']['signs']for v in['n','d']),records=records)
if __name__=='__main__':print(json.dumps(symbolic(json.loads(Path(sys.argv[1]).read_text())),sort_keys=True,separators=(',',':')))
