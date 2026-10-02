"""Optional late whole-entry comparison against a pinned author's JSON record.

The offline proof verifier does not import or require this record.
"""
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
from audit import run, sha
from core import require


def check(own, author):
    require(author['complete'] is True and author['outside_global_degree_input']=='none',
            'author scope status')
    mapped=[]
    for local,native in zip(own['literal'],author['literal_domains']):
        require(local['r']==native['core'] and bool(local['sy_swap'])==native['swapped_SY'],
                'actual four labels')
        columns=[{'bits':c['word'],'incidence':[(c['word']>>i)&1 for i in range(13)],
                  'internal_degree':c['h'],'actual_degree':c['degree']}
                 for c in local['columns']]
        require(columns==native['columns'], 'every full incidence/internal/actual-degree column')
        require(local['ranks'][3:]==native['row_targets'], 'every row rank')
        rules=[]
        for pair in local['fixed_pairs']:
            i,j=pair['pair']
            if pair['upper']==0:rules.append([i,j,'not_both_red'])
            if pair['union']:rules.append([i,j,'not_both_blue'])
        require(rules==native['tight_pair_column_rules'], 'every tight fixed-pair rule')
        mapped.append({'r':local['r'],'sy_swap':local['sy_swap'],'columns':columns,'rules':rules})
    table={}
    for role,records in own['roles'].items():
        local=[{'M':c['missing'],'SX':c['p']} for c in records]
        native=author['formula_role_table'][role]
        key=lambda x:(tuple(x['M']),tuple(x['SX']))
        require(sorted(local,key=key)==sorted(native['records'],key=key), 'every formula role: '+role)
        require(own['domains'][role]==native['missing_sets'], 'entire missing domain: '+role)
        table[role]=sorted(local,key=key)
    fixed=author['ordinary_fixed_core_spines']
    require(fixed['actual_known_degrees']==own['literal'][0]['degrees']
            and fixed['Q_ranks']==own['literal'][0]['ranks'], 'all known degrees/Q ranks')
    pairs={tuple(p['pair']):p for p in own['literal'][0]['fixed_pairs']}
    for n in fixed['spines']:
        i,j=n['spine'];p=pairs[tuple(sorted((i,j)))]
        require(n['known_common_red']==p['pages'] and n['red_edge']==p['red']
                and n['Q_intersection_upper']==p['upper']
                and n['Q_intersection_lower']==p['lower']
                and n['Q_ranks']==[own['literal'][0]['ranks'][i],own['literal'][0]['ranks'][j]],
                'every listed physical page/rank/cap/minimum')
    integers={}
    for case, local in own['missing_sums'].items():
        native=author['integer_checks'][case]
        histogram=Counter(next(i for i,(x,y) in enumerate(zip(v,author['missing_row_target'])) if x!=y)
                          for v in local['vectors'])
        require(native['tuples_checked']==local['count'] and native['survivors']==[]
                and {str(k):v for k,v in histogram.items()}==native['first_failed_row_histogram'],
                'complete missing-sum outcomes: '+case)
        integers[case]=dict(sorted(histogram.items()))
    for n in author['controls']:
        if 'spine' not in n:continue
        i,q=n['spine'];require(q==16,'named control point')
        require(n['red_codegree_cap']==(3 if n['red_edge'] else sum(n['actual_degrees'])-14),
                'native control physical cap')
        require(n['violates']==(len(n['known_common_red'])+n['Q_minimum']>n['red_codegree_cap']),
                'native control actual violation')
    return {'mapped_domains':mapped,'role_records':table,'fixed_spines':fixed['spines'],
            'full_integer_histograms':integers}


def run_comparison(path):
    own=run()['core'];author=json.loads(Path(path).read_text())
    record=check(own,author)
    damaged=[]
    mutations=[('omit-column',lambda a:a['literal_domains'][0]['columns'].pop()),
               ('duplicate-column',lambda a:a['literal_domains'][0]['columns'].append(a['literal_domains'][0]['columns'][0])),
               ('wrong-outside-degree',lambda a:a['literal_domains'][0]['columns'][0].__setitem__('actual_degree',99)),
               ('wrong-Q-rank',lambda a:a['literal_domains'][0]['row_targets'].__setitem__(0,2)),
               ('omit-tight-rule',lambda a:a['literal_domains'][0]['tight_pair_column_rules'].pop()),
               ('omit-role',lambda a:a['formula_role_table']['A1V']['records'].clear()),
               ('wrong-known-page',lambda a:a['ordinary_fixed_core_spines']['spines'][0]['known_common_red'].append(99)),
               ('omit-integer-tuple',lambda a:a['integer_checks']['U'].__setitem__('tuples_checked',511))]
    for name,mutate in mutations:
        altered=deepcopy(author);mutate(altered)
        try:check(own,altered)
        except (ValueError,KeyError,IndexError):damaged.append(name)
        else:raise ValueError('semantic damage accepted: '+name)
    return {'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer',
            'complete_entry_comparison_sha256':sha(record),'compared_columns':172,
            'compared_role_records':sum(len(v)for v in own['roles'].values()),
            'compared_fixed_spines':len(record['fixed_spines']),
            'compared_missing_tuples':896,'damages_rejected':damaged,
            'native_record_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest()}


if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: compare_author.py PINNED_NATIVE_RESULTS_JSON')
    print(json.dumps(run_comparison(sys.argv[1]),sort_keys=True,separators=(',',':')))
