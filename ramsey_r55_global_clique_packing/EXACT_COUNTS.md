# Exact physical-family count

An atom Rk is a red k-clique and Bk a blue k-clique. E3 has only red edge 01; P3 has red edges 01 and 02. Entries count labeled binary cross matrices whose two fixed atoms together contain no monochromatic five-set.

| Left / right | R4 | B4 | R3 | B3 | E3 | P3 |
|---|---:|---:|---:|---:|---:|---:|
| R4 | 37,823 | 35,714 | 3,125 | 3,375 | 3,315 | 3,259 |
| B4 | 35,714 | 37,823 | 3,375 | 3,125 | 3,259 | 3,315 |
| R3 | 3,125 | 3,375 | 478 | 512 | 504 | 497 |
| B3 | 3,375 | 3,125 | 512 | 478 | 497 | 504 |
| E3 | 3,315 | 3,259 | 504 | 497 | 512 | 512 |
| P3 | 3,259 | 3,315 | 497 | 504 | 512 | 512 |

The equality of transposed counts follows from a checked transpose bijection. It does not identify physical coordinates. The mixed/mixed entries are included for a complete six-type interface; only the final block can be mixed in this cover.

Set a=37823, b=35714, c=3125, d=3375, u=478 and v=512. For t=0,1,2,3, define the four vectors

    A = (3375,3315,3259,3125)
    B = (3125,3259,3315,3375)
    C = (512,504,497,478)
    D = (478,497,504,512).

Then the branch with r red four-cliques, s red forced triangles, and final shape t has exactly

    a^[C(r,2)+C(7-r,2)] * b^[r(7-r)]
    * c^[r*s+(7-r)*(4-s)] * d^[r*(4-s)+(7-r)*s]
    * u^[C(s,2)+C(4-s,2)] * v^[s*(4-s)]
    * A[t]^r * B[t]^(7-r) * C[t]^s * D[t]^(4-s)

physical pair-domain survivors. Sum this over r=5,6,7; s=0,...,4; t=0,...,3. The exact total is:

```text
52105359606181272362307579962621722114106272015578713235782438186788159504042493203566716228855321513659249093447235776110210523458564950887507716725468044940037791729321649029411002215759418052946948599069010299444926204159855842590332031250000000
```

Exact integer inequalities give N<2^823 and N<60·2^846/2^29. For orientation only, log2(N) is approximately 822.897671214. Floating-point arithmetic is not used to establish either count or inequality.

The final family also normalizes all eleven matrices incident to the first red 4-clique. Their root-orbit domain sizes are:

| Child | R4 | B4 | R3 | B3 | E3 | P3 |
|---|---:|---:|---:|---:|---:|---:|
| Canonical root matrices | 1,998 | 1,931 | 596 | 680 | 1,740 | 1,740 |
| Child automorphism order | 24 | 24 | 6 | 6 | 2 | 2 |
| Fixed-point sum | 47,952 | 46,344 | 3,576 | 4,080 | 3,480 | 3,480 |

With the same constants and vectors above, set F=(680,1740,1740,596). The final branch count is

    1998^(r-1) * 1931^(7-r) * 596^s * 680^(4-s) * F[t]
    * a^[C(r-1,2)+C(7-r,2)] * b^[(r-1)*(7-r)]
    * c^[(r-1)*s+(7-r)*(4-s)] * d^[(r-1)*(4-s)+(7-r)*s]
    * u^[C(s,2)+C(4-s,2)] * v^[s*(4-s)]
    * A[t]^(r-1) * B[t]^(7-r) * C[t]^s * D[t]^(4-s).

Summing the 60 branches gives M:

```text
660240714669680199118019058692577094194741553302998258599762144785709868285667050626208058793440228189482072376530575997205634640956641982551846046173436683889503838533385141976173038358410849468782544136047363281250000000000000000000000
```

Exact comparisons give M<2^787, 2^65·M<60·2^846, and 2^36·M<N. For orientation, log2(M) is approximately 786.698022501. The baseline 2^903/M exceeds 2^116. This is a search-space cardinality comparison after relabeling, not a count of target graphs or a measured speedup.

`COUNTS.json` contains all 60 final counts (`count`), pair-only counts (`unrooted_count`), and the exact final retained fraction of the packing baseline. Each full target formula uses 847 variables: 846 physical edges plus one true constant. Complete clause counts, including root ordering and the unit clause, range from 1,395,378 to 1,425,766.
