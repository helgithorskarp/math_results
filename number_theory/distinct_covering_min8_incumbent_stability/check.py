"""Exact 51-of-53 incumbent stability certificate checker; stdlib only.

Author: six-covering-1, researcher. No solver result or search completeness
is assumed. Every remaining eligible divisor is charged in each case.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
B = 5040


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rows_checked(rows, period):
    require(isinstance(rows, list) and rows, 'empty or invalid class list')
    require(all(isinstance(row, list) and len(row)==2
                and all(type(v) is int for v in row) for row in rows), 'invalid class entries')
    require(len({m for a,m in rows})==len(rows), 'repeated modulus')
    require(all(m>=8 and period%m==0 and 0<=a<m for a,m in rows), 'invalid congruence')
    require(rows==sorted(rows,key=lambda row:row[1]), 'unsorted moduli')
    return rows


def residual(prefix):
    covered=bytearray(B)
    for a,m in prefix:
        for x in range(a,B,m):covered[x]=1
    return [x for x,c in enumerate(covered) if not c]


def budget(period, free, points, weights):
    histograms={}
    capacities=[]
    for m in free:
        g=math.gcd(B,m)
        if g not in histograms:
            histogram=[0]*g
            for x,w in zip(points,weights):histogram[x%g]+=w
            histograms[g]=max(histogram,default=0)
        capacities.append([m,period//math.lcm(B,m)*histograms[g]])
    return period//B*sum(weights),capacities


def compute(core_data, upper_data, weight_data):
    require(core_data.get('base')==B and core_data.get('format_version')==1,'invalid core format')
    core=rows_checked(core_data.get('congruences'),B)
    require([m for a,m in core]==[m for m in range(8,B+1) if B%m==0], 'core must contain all 53 eligible divisors')
    require(len(core)==53,'wrong core size')
    # Three disjoint forcing pairs prove every 51-class subset has LCM B.
    forcing=[[16,315],[144,35],[80,63]]
    require(len(set(sum(forcing,[])))==6,'forcing pairs not disjoint')
    require(all(math.lcm(*pair)==B and set(pair)<=set(m for a,m in core) for pair in forcing),'invalid forcing pairs')
    require(upper_data.get('lcm')==20160 and upper_data.get('format_version')==1,'wrong upper period')
    upper=rows_checked(upper_data.get('congruences'),20160)
    require(min(m for a,m in upper)==8 and math.lcm(*(m for a,m in upper))==20160,'wrong upper minimum or actual LCM')
    require(set(map(tuple,core))<=set(map(tuple,upper)),'upper does not retain the core')
    counts=[0]*20160
    for a,m in upper:
        for x in range(a,20160,m):counts[x]+=1
    require(all(counts),'upper does not cover')
    require(weight_data.get('format_version')==1 and weight_data.get('base')==B,'invalid weight format')
    cuts={}
    for item in weight_data.get('cuts',[]):
        period=item.get('period')
        pair=item.get('removed')
        require(period in (10080,15120) and isinstance(pair,list) and len(pair)==2
                and all(type(m) is int for m in pair) and pair[0]<pair[1],'invalid weight case')
        key=period,tuple(pair)
        require(key not in cuts,'duplicate weight case')
        cuts[key]=item
    used=set()
    events=hashlib.sha256()
    reports=[]
    total_weight_points=0
    for period in (10080,15120):
        eligible=[m for m in range(8,period+1) if period%m==0]
        uniform_count=weighted_count=0
        uniform_gaps=[];weighted_gaps=[]
        for pair in itertools.combinations([m for a,m in core],2):
            prefix=[row for row in core if row[1] not in pair]
            require(len(prefix)==51 and math.lcm(*(m for a,m in prefix))==B,'prefix LCM failure')
            assigned={m for a,m in prefix}
            free=[m for m in eligible if m not in assigned]
            points=residual(prefix)
            demand,capacities=budget(period,free,points,[1]*len(points))
            key=period,pair
            kind='uniform'
            if demand>sum(c for m,c in capacities):
                require(key not in cuts,'unused weighted record on uniform case')
                uniform_count+=1;uniform_gaps.append(demand-sum(c for m,c in capacities))
            else:
                require(key in cuts,'missing nonuniform certificate')
                item=cuts[key]
                values=item.get('weights')
                require(isinstance(values,list) and values and all(isinstance(row,list) and len(row)==2
                        and all(type(v) is int for v in row) for row in values),'invalid weight entries')
                require(values==sorted(values) and len({x for x,w in values})==len(values),'repeated/unsorted weight points')
                uncovered=set(points)
                require(all(x in uncovered and w>0 for x,w in values),'weight outside residual or nonpositive')
                demand,capacities=budget(period,free,[x for x,w in values],[w for x,w in values])
                require(item.get('demand')==demand and item.get('capacities')==capacities,'declared demand or resource capacities disagree')
                require(demand>sum(c for m,c in capacities),'nonstrict capacity certificate')
                used.add(key);weighted_count+=1;kind='weighted'
                weighted_gaps.append(demand-sum(c for m,c in capacities))
                total_weight_points+=len(values)
            event=[period,list(pair),kind,demand,capacities]
            events.update((json.dumps(event,separators=(',',':'))+'\n').encode())
        require(uniform_count+weighted_count==1378,'incomplete pair cases')
        reports.append({'period':period,'pair_cases':1378,'uniform_cuts':uniform_count,
                        'weighted_cuts':weighted_count,'minimum_uniform_gap':min(uniform_gaps),
                        'minimum_weighted_gap':min(weighted_gaps)})
    require(used==set(cuts),'unused or extra weight records')
    return {'agent':'six-covering-1','role':'researcher',
            'status':'COMPLETE_EXACT_LOCAL_MINIMUM','core_classes':53,'minimum_retained':51,
            'exact_family_minimum_lcm':20160,'cases':reports,
            'weighted_base_points':total_weight_points,
            'ordered_events_sha256':events.hexdigest(),
            'upper_classes':len(upper),'upper_lcm':20160,'upper_minimum':8,
            'upper_uncovered':0,'upper_coverage_histogram':{str(k):v for k,v in sorted(Counter(counts).items())},
            'upper_multiplicity_sha256':hashlib.sha256(bytes(counts)).hexdigest()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true',help='regenerate expected metadata after exact checks')
    args=parser.parse_args()
    result=compute(*(json.loads((ROOT/name).read_text())
                     for name in ('core.json','upper_cover.json','weights.json')))
    if args.write:(ROOT/'expected.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        expected=json.loads((ROOT/'expected.json').read_text())
        require(result==expected,'expected metadata mismatch')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
