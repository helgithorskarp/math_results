# A constant-site family excludes every pointwise linear extremal-site bound

Author derivation by Quinn, responding to Lyra's chat hypothesis 438. Different-researcher review is requested. This refutes a proposed sufficient route, not the agreed growth target. It does not exclude an aggregate or weighted site lower bound over the avoidance class.

For n>=4 let

    p_n = 1, n-1, n-2, ..., 2, n.

Then p_n avoids boxed 2143 and has exactly four legal maximum-insertion gaps and four legal minimum-insertion gaps. Gap g follows g old entries. The respective gap sets are

    G_max(p_n) = {0,1,2,n},
    G_min(p_n) = {0,n-2,n-1,n}.

Hence the total site count is always 8, independently of n. In particular, no positive constant c can give L_max(p)+L_min(p)>=c*n for every avoiding parent p and all sufficiently large sizes.

## Direct proof

The parent avoids even classical 2143. Its initial 1 cannot be the first entry of a decreasing first pair. If the first entry is in the decreasing middle block, any later middle entry is smaller and therefore cannot be the largest (third) selected entry of a 2143 occurrence. The final n cannot be that third entry because no entry follows it. These cases exclude every classical 2143 occurrence, and therefore every boxed occurrence.

Insert a new maximum n+1. Old occurrences cannot be created among old entries, since the inserted value is above every old rectangle. Thus any occurrence must use n+1 as its third selected entry. Gaps 0 and 1 leave fewer than two entries before it. At gap 2 the only possible first pair is 1,n-1, which is increasing. At gap n there is no entry after it. All four stated gaps are legal.

For each 3<=g<=n-1, the child indices

    (2,3,g+1,n+1)

in one-based notation select values

    n-1, n-2, n+1, n.

They form 2143. Every other entry strictly between the first and last selected positions has value below n-2, so it is outside the open vertical rectangle. This is an explicit boxed occurrence for every other gap. The maximum gap set is exact.

Reverse-complement preserves the pattern 2143 and its rectangle condition. The permutation p_n is fixed by reverse-complement. Under this operation insertion of a new minimum at gap g becomes insertion of a new maximum at gap n-g, including the old-value shift by one. Therefore its minimum gap set is the reflection of its maximum gap set. This proves the second formula and the constant total 8.

## Finite certificate and scope

The first failure of the particular proposed bound L_max+L_min>=n+2 is p_7=1654327, with maximum gaps {0,1,2,7} and minimum gaps {0,5,6,7}; 8<9. extremal_site_probe_n8.json preserves exhaustive smaller-size minima and the first lexicographic failure. Although the command's upper limit was 8, it stopped at that size-7 failure and did not exhaust size 7 or 8. This minimality evidence is finite and depends on the checked occurrence implementation.

extremal_site_definition_certificate.json independently checks the parent and every extremal child of this explicit size-7 example with Lyra's literal definition checker, recording complete occurrence witnesses and source hash. The uniform family and exact site sets follow from the written proof above, not extrapolation from this example.

The total-site hypothesis would have been a sufficient bridge to factorial growth after summing and using symmetry, but these rare low-site parents do not decide the average site count of all avoiders. Their presence cannot justify either an exponential upper bound or a refutation of factorial growth. A possible aggregate mechanism must account for such parents rather than assert a pointwise linear bound.
