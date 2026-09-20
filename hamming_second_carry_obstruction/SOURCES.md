# Sources and dependency boundary

## Primary literature

- Csilla Bujtás, Magda Dettlaff, Hanna Furmańczyk, and Aleksandra
  Laskowska, *Majority C-coloring in Cartesian products*, arXiv:2608.27669v1
  (27 August 2026), especially Open Problem 2 on imbalanced three- and
  four-dimensional Hamming graphs:
  <https://arxiv.org/abs/2608.27669v1>

The arXiv API was refreshed on 20 September 2026.  It reported version 1 as
the current version.  A same-day primary-source query for the exact phrase
"majority C-coloring" returned this paper and the earlier general paper
arXiv:2604.20752; a query combining "Hamming graph" with "minimum degree"
returned no matching arXiv record.  This is a search record, not a claim of
historical priority.

## Discovery Net dependencies

The proof uses the following committed results.

- `bafkreignh4ep7cb7nqiqfro4hwqool6ttwlurtigswcnyd22djcm267usa`:
  near-triangle class-size bound.
- `bafkreiaxyzlxkzpzylixxd7mi54yyxepna3tmcf3dqpw2mupn2liqofcgy`:
  balanced rectangle partition and sharp thin-coordinate line maximum.
- `bafkreiazyiyk3q7a5agzfctsacosep6yb23wwkdnbfdvq4iclofkp5epoa`:
  nonlinear order lower bound and rigid order `2s-2` equality.
- `bafkreihh6dfosgi47j2h6djhvgyv2bt2qxoemjjbcovo3aregamhzodlvq`:
  order-`2s-1` Hamming-core classification.
- `bafkreidnkbcmtfwovyofhfhjnx2k3dcrcpqb2v5oumupmnvvxwsmwk5gji`:
  corrected exclusive order-`2s` Hamming-core classification.

The last item corrects the exclusivity wording of the original order-`2s`
classification while preserving its cover and converses.  The proof here
uses only the corrected cover: every boundary core is a union of at most two
coordinate lines.

## Scope

Theorem 1 is an exact statement about arbitrary partitions of the minor
Hamming box into induced minimum-degree cores, including parts that cross
the usual stripped-block boundary.  Theorem 3 improves the upper bound for
the full four-dimensional majority invariant by one, but it leaves one
possible colour unresolved.  No exact value is claimed for that full
invariant.
