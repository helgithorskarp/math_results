# Conditional distinct-covering exclusion: 100/108 completion tree

Actual author **six-covering-3**, role **researcher**, 2026-10-01.
Author-checked written proof and exact certificate; independent review and
formalization are pending.

No distinct covering with moduli at least 8 dividing 43200 contains this
entire twenty-class prefix (moduli and phases paired in the two rows):

    8,9,10,12,15,16,18,20,24,25,30,36,40,45,48,50,75,54,60,72
    0,0, 5,10, 1, 4, 3,17, 2, 3,11,30,27,19,14,33,13,33,29, 6

Every remaining eligible divisor may be omitted or used at any phase,
at most once. Its actual LCM may divide the ambient period. The fixed 8
class makes the minimum exactly 8. This conditional exclusion does not
exclude the unrestricted period or change a global bound on L_min(8).

The [proof](proof.md) gives a complete 32-orbit missing-100 split, then
complete 28-orbit missing-108 splits at 100 phases 43 and 93. There are
86 representative leaves and 49 stored integer weights, shared only
where their literal zero support is checked. Missing 100 and 108 divide
the prescribed LCM 10800, so adjoining them preserves the actual LCM.

## Reproduce all four required parts

Use Python 3.11 or later, standard library only; Python 3.11 was tested.
From this directory, run these sequentially:

```bash
python3 -B check.py --part orbits100
python3 -B check.py --part orbits108
python3 -B check.py --part capacity100 --controls
python3 -B check.py --part capacity108
```

**All four must pass.** A single part deliberately reports
`part_alone_excludes_parent: false`. Each part checks exact equality
with [expected.json](expected.json), and each has a 20-second loop cap.
Normal Python and `python3 -B -O` passed all four parts; malformed-fixture
controls passed in both modes. Computation uses one process and no solver,
BLAS or OpenMP workers. A slower machine's timeout gives no exclusion;
no saved partial part is accepted as a complete result.

| Part | Complete finite check | Smallest physical gap |
|---|---|---:|
| orbits100 | 32 orbits; 1,771,200 ambient generator points | structural |
| orbits108 | 28 orbits; 1,252,800 ambient generator points | structural |
| capacity100 | 17 vectors exclude 30 representative leaves | 634 |
| capacity108 | 32 vectors exclude all 56 refined leaves | 34 |

The numeric parts evaluate 2,761 actual resource instances, 7,674,452
physical phase buckets and 188,160 binary union cases. Both check the
support of every assignment in the 86-leaf tree. The structural parts
check full classes and divisor partitions, not only phase labels.
There are 16 malformed-fixture controls and 11 structural controls.

[input.json](input.json) is a compact mathematical fixture: 410 literal
basis boxes and 4,878 sparse positive integer terms. Each individual
vector uses disjoint boxes; the basis may overlap across different
vectors. Fixture SHA256:

    87ecb07649aad87ccb60a2eac1979aecd2cad846f4ee49088a2f0ac15f6a523d

Expected-output SHA256:

    67ea6f8a1e1a4ec7032ced8ce5fbfe9e3eaa704aaaf3c7b9cd375e59d631800a

[MANIFEST.md](MANIFEST.md) records the source and fixture hashes. The
trust boundary is exact Python integers, the fixture and the unformalized
written CRT/completion/binary argument. No private forest, numerical
solver, graph, ledger or omitted large proof corpus is a reader input.

## Attribution and primary context

The proof credits [six-covering-2's fixed binary cluster bound](../distinct_covering_fixed_binary_clusters/proof.md),
[six-covering-3's stabilizer lemma](../distinct_covering_43200_stabilizer_orbits/proof.md)
and earlier related conditional certificates. These general methods are
not claimed as new. The complete twenty-class exclusion is the present
explicit application.

Current primary context, refreshed 2026-10-01:
[Zhang--Zhang](https://arxiv.org/html/2607.19029) and
[Harrington--Klein--Lowrance--Trifonov, Problem 3](https://arxiv.org/html/2605.18644).
Their computational exclusion tables are not inputs to this certificate.
