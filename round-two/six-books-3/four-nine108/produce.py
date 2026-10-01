#!/usr/bin/env python3
"""Exact four-nine Petersen census and complete static star certificates.

Standard-library exact integers only. No solver, branching, host automorphism,
other-root Petersen assumption, or private data. Default regenerates everything.
"""
import argparse
from collections import Counter, defaultdict
from itertools import combinations, combinations_with_replacement, permutations, product
import hashlib, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
DELTAS = (1,) * 4 + (0,) * 7
GROUND=list(combinations(range(5),2));A=1023
P=[sum(1<<j for j,y in enumerate(GROUND) if set(x).isdisjoint(y)) for x in GROUND]
STARS=[sum(1<<i for i,x in enumerate(GROUND) if t in x) for t in range(5)]
RED=[(i,j) for i,j in combinations(range(10),2) if P[i]>>j&1]
BLUE=[(i,j) for i,j in combinations(range(10),2) if not P[i]>>j&1]
BAD_BLUE=sum(1<<(3*t+2) for t in range(len(BLUE)))

def require(ok,msg):
 if not ok:raise ValueError(msg)

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def word_pool():
 out=[]
 for z in range(1024):
  k=z.bit_count()
  if not 5<=k<=7:continue
  c=A^z
  if any(k-1>8-(P[i]&c).bit_count() for i in range(10) if c>>i&1):continue
  if any((P[i]&z).bit_count()<k-7 for i in range(10) if z>>i&1):continue
  if any(k+1+(P[i]&c).bit_count()+(P[j]&c).bit_count()>12 for i,j in RED if z>>i&1 and z>>j&1):continue
  out.append(z)
 return out

def setup():
 pack=[sum(((z>>i)&1)<<(3*i) for i in range(10)) for z in range(1024)]
 red=[sum(1<<t for t,(i,j) in enumerate(RED) if z>>i&1 and z>>j&1) for z in range(1024)]
 blue=[sum(1<<(3*t) for t,(i,j) in enumerate(BLUE) if z>>i&1 and z>>j&1) for z in range(1024)]
 low=word_pool();table=defaultdict(list);stats=Counter()
 for a,b in combinations_with_replacement(low,2):
  if a.bit_count()+b.bit_count()>12:continue
  stats['low_pairs_within_budget']+=1
  if red[a]&red[b]:continue
  stats['low_pairs_red_capped']+=1
  table[pack[a]+pack[b]].append((a,b,red[a]|red[b],blue[a]+blue[b]))
 vectors=[]
 for v,entries in sorted(table.items()):
  counts=[(v>>(3*i))&7 for i in range(10)]
  require(max(counts)<=2,'pair column packing carry')
  union=sum(1<<i for i,x in enumerate(counts) if x)
  both=sum(1<<i for i,x in enumerate(counts) if x==2)
  vectors.append((v,union,both,entries))
 full={k:[z for z in range(1024) if z.bit_count()==k and all((P[i]&(A^z)).bit_count()<=1 for i in range(10) if not z>>i&1)] for k in (5,6)}
 choices=[()]+[(z,) for z in full[5]]+[(z,) for z in full[6]]+list(combinations_with_replacement(full[5],2))
 choices=[h for h in choices if len(h)<2 or not red[h[0]]&red[h[1]]]
 require(len(choices)==456,'full-large coverage changed')
 mu_by_count={count:[mu for mu in product(range(3),repeat=5) if sum(mu)==count] for count in (5,6,7)}
 info={'low_size_counts':dict(sorted(Counter(z.bit_count() for z in low).items())),'full_large_sizes':{k:len(v) for k,v in full.items()},'high_choices':len(choices),'pair_column_vectors':len(vectors),'mu_counts':{k:len(v) for k,v in mu_by_count.items()},**stats}
 return pack,red,blue,table,vectors,choices,mu_by_count,info

def one_choice(highs,data):
 pack,red,blue,table,vectors,choices,mu_by_count,info=data
 stats=Counter();keys=set()
 used=0
 for h in highs:used|=red[h]
 for mu in mu_by_count[7-len(highs)]:
  stats['high_multiplicities']+=1
  rows=list(highs)+[s for s,m in zip(STARS,mu) for _ in range(m)]
  require(len(rows)==7,'wrong full-row count')
  residual=[5-sum(z>>i&1 for z in rows) for i in range(10)]
  if any(not 0<=r<=4 for r in residual):continue
  hb=tuple(sum(bool(z>>i&1 and z>>j&1) for z in rows) for i,j in BLUE)
  if max(hb)>3:continue
  high_blue=sum(count<<(3*t) for t,count in enumerate(hb))
  stats['residual_vectors']+=1
  target=sum(r<<(3*i) for i,r in enumerate(residual))
  zero=sum(1<<i for i,r in enumerate(residual) if r==0)
  one=sum(1<<i for i,r in enumerate(residual) if r==1)
  three=sum(1<<i for i,r in enumerate(residual) if r==3)
  four=sum(1<<i for i,r in enumerate(residual) if r==4)
  for vector,union,both,left in vectors:
   if union&zero or both&one or union&three!=three or both&four!=four:continue
   # Coordinate-wise 0<=residual-pair<=2: no base8 borrow or carry.
   stats['valid_pair_column_splits']+=1
   right=table.get(target-vector)
   if right is None:continue
   stats['matched_pair_column_splits']+=1
   for a,b,lr,lb in left:
    if lr&used:continue
    for c,d,rr,rb in right:
     if b>c:continue
     stats['ordered_exact_column_joins']+=1
     if rr&(used|lr):continue
     stats['red_capped_joins']+=1
     # Each field is <=3+2+2=7, so base8 addition has no carry.
     if (high_blue+lb+rb)&BAD_BLUE:continue
     key=((a,b,c,d),tuple(highs),mu)
     require(key not in keys,'duplicate four-low incidence')
     keys.add(key)
 return sorted(keys),dict(sorted(stats.items()))


def canonical_json(value):
    return json.dumps(json.loads(json.dumps(value)), sort_keys=True, separators=(",", ":"))

def key_rows(key):
    lows, highs, mu = key
    return list(lows) + list(highs) + [s for s,m in zip(STARS,mu) for _ in range(m)]

def census():
    data=setup();keys=set();stats=Counter()
    for highs in data[5]:
        found,part=one_choice(highs,data)
        require(not keys.intersection(found),'overlapping full-large choices')
        keys.update(found);stats.update(part)
    patterns=Counter((tuple(sorted(z.bit_count() for z in lows)),tuple(h.bit_count() for h in highs)) for lows,highs,mu in keys)
    report={'deficits':DELTAS,'complete':True,'incidence_records':len(keys),
            'incidence_sha256':digest(sorted(keys)),'setup':data[7],
            'census':dict(sorted(stats.items())),
            'patterns':[{'low_sizes':l,'high_sizes':h,'records':n} for (l,h),n in sorted(patterns.items())]}
    return keys,report

def transformations():
    position = {x: i for i, x in enumerate(GROUND)}
    output = []
    for permutation in permutations(range(5)):
        mapping = [position[tuple(sorted(permutation[t] for t in x))] for x in GROUND]
        words = [sum(1 << mapping[i] for i in range(10) if z >> i & 1)
                 for z in range(1024)]
        output.append((permutation, words))
    return output

def transformed(key, permutation, words):
    lows, highs, mu = key
    moved_mu = [0] * 5
    for t in range(5):
        moved_mu[permutation[t]] = mu[t]
    return tuple(sorted(words[z] for z in lows)), tuple(sorted(words[h] for h in highs)), tuple(moved_mu)

def domains(rows):
    """Decomposed A/B page counts; verifier uses literal 22-vertex sets."""
    result = []
    outside = (1 << len(rows)) - 1
    for b, (z, delta) in enumerate(zip(rows, DELTAS)):
        degree = z.bit_count() - delta
        require(0 <= degree < len(rows), "outside degree out of range")
        rest = outside ^ (1 << b)
        columns = [sum(1 << c for c in range(len(rows)) if c != b and rows[c] >> i & 1)
                   for i in range(10)]
        accepted = []
        for picked in combinations([c for c in range(len(rows)) if c != b], degree):
            star = sum(1 << c for c in picked)
            if any((P[i] & (A ^ z)).bit_count() + (star & (rest ^ columns[i])).bit_count() > 3
                   for i in range(10) if not z >> i & 1):
                continue
            if any(z.bit_count() - 1 - (P[i] & z).bit_count()
                   + (columns[i] & (rest ^ star)).bit_count() > 6
                   for i in range(10) if z >> i & 1):
                continue
            accepted.append(star)
        result.append(sorted(accepted))
    return result

def compatible(rows, b, x, c, y):
    if (x >> c & 1) != (y >> b & 1):
        return False
    if x >> c & 1:
        return 10 - (rows[b] | rows[c]).bit_count() + (x & y).bit_count() <= 3
    outside = (1 << len(rows)) - 1
    bx = outside ^ (1 << b) ^ x
    by = outside ^ (1 << c) ^ y
    return 1 + (rows[b] & rows[c]).bit_count() + (bx & by).bit_count() <= 6
def exclusion(rows, stars):
    for b, domain in enumerate(stars):
        if not domain:
            return {"type": "empty_star", "point": b}
    # Use the complete initial domains only. Every star of one point must
    # lack pairwise support somewhere; no propagation or domain update.
    for b, domain in enumerate(stars):
        groups = {}
        for x in domain:
            for c in range(11):
                if c != b and not any(compatible(rows, b, x, c, y) for y in stars[c]):
                    groups.setdefault(c, []).append(x)
                    break
            else:
                break
        else:
            return {"type": "star_pair_cover", "point": b,
                    "covers": [{"against": c, "stars": sorted(xs)}
                               for c, xs in sorted(groups.items())]}
    raise ValueError('unexcluded incidence: no complete static obstruction')
def make_certificate():
    keys, result = census()
    maps = transformations()
    covered = set()
    entries = []
    histogram = Counter()
    for key in sorted(keys):
        if key in covered:
            continue
        orbit = {transformed(key, p, words) for p, words in maps}
        require(key == min(orbit), 'nonminimum orbit representative')
        require(orbit <= keys and not covered.intersection(orbit), 'invalid or overlapping orbit')
        covered.update(orbit)
        rows = key_rows(key)
        require(len(rows) == 11, 'wrong outside order')
        stars = domains(rows)
        entries.append({'key': key, 'orbit_size': len(orbit),
                        'domain_sizes': [len(domain) for domain in stars],
                        'domains_sha256': digest(stars), 'exclusion': exclusion(rows, stars)})
        histogram[len(orbit)] += 1
    require(covered == keys, 'incomplete raw orbit cover')
    certificate = {'schema': 1, 'order': 22, 'red_page_cap': 3, 'blue_page_cap': 6,
                   'outside_deficits': DELTAS, 'local_graph': 'KG(5,2)',
                   'incidence_records': len(keys), 'entries': entries}
    result.update({'orbits': len(entries), 'orbit_size_histogram': dict(sorted(histogram.items())),
                   'exclusion_types': dict(sorted(Counter(e['exclusion']['type'] for e in entries).items())),
                   'weighted_exclusion_types': dict(sorted((kind,sum(e['orbit_size'] for e in entries if e['exclusion']['type']==kind)) for kind in {e['exclusion']['type'] for e in entries})),
                   'star_pair_covers': sum(len(e['exclusion'].get('covers', [])) for e in entries),
                   'unsupported_stars': sum(len(c['stars']) for e in entries for c in e['exclusion'].get('covers', [])),
                   'certificate_sha256': digest(certificate)})
    return certificate, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--derive", action="store_true", help="report without frozen-summary comparison")
    parser.add_argument("--output", type=Path, help="explicit destination for regenerated certificate")
    args = parser.parse_args()
    certificate, result = make_certificate()
    if not args.derive:
        require(canonical_json(certificate) == canonical_json(json.loads((HERE / "certificate.json").read_text())),
                "regenerated certificate mismatch")
        require(canonical_json(result) == canonical_json(json.loads((HERE / "expected.json").read_text())["producer"]),
                "producer expected-summary mismatch")
    if args.output is not None:
        args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
