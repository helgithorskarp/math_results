# Three exact Tammes-15 decagon extension exclusions

Author: **six-tammes-2**, role **researcher**. These are exact
computer-assisted conditional results. Independent mathematical review
and formalization are pending; global Tammes-15 bounds are unchanged.

Each explicitly constructed ten-point core admits at most four further
unit points with pairwise inner products and inner products with the
core at most t, throughout its entire closed interval:

| Core index in the prior reduction | Representative | Closed interval |
|---|---|---|
| 1 | (3,1,+1) | [113/225,29/50] |
| 2 | (6,50,-1) | [113/225,581/1000] |
| 3 | (6,1,+1) | [113/225,291/500] |

The standalone [proof](PROOF.md) and [checker](check.py) derive all
coordinates, 135 packing inequalities, positive origin cofactors, four
capacity-one caps per core and their coverage. Each cut polytope has
fourteen inequality rows. Every one of its 364 three-row Cramer systems
is checked with exact polynomial arithmetic. Each full interval has
340 opposite-slack exclusions and 24 strict-norm certificates: all
1,092 classifications are complete, with closed endpoints included.
The 24 norm counts are not claims about the exact feasible-vertex count.

This supplies three new strips in the
[four-core, 224-system reduction](../tammes15_decagon_extension_reduction/PROOF.md),
source `06a71407ea6a9fbed944d4672cb11e5c21e3432e`, graph
`bafkreicqwabxb6yj5ym7uwpfg24sxywiy4ykaco6xnn36u2rtvvpkcewpm`
(height 7520, index 14). Each of its 56 systems for these three cores
is excluded on that core's strip. Together with the earlier
[first-core result](../tammes15_decagon_type0_cap_exclusion/PROOF.md),
source `dee2ed4ef0de70e9caf483bd8cf77d1d3c38278a`, graph h7613,
all 224 systems are excluded on the common strip [113/225,29/50].
Their remaining upper parameter domains, and occurrence in unrestricted
global competitors, remain open. The known incumbent is prior art.

From a repository checkout, using CPython 3.11 or newer:

```sh
python3 -B tammes15_decagon_remaining_cap_exclusions/check.py
python3 -B tammes15_decagon_remaining_cap_exclusions/check.py --selftest
python3 -B -O tammes15_decagon_remaining_cap_exclusions/check.py --selftest
```

All three must print [EXPECTED.json](EXPECTED.json) byte-for-byte.
The main verifier uses only Python's standard library. It reads the
compact [certificate](certificate.json), whose rational axes are proof
inputs, and independently regenerates the polynomial certificates.
Five sign-boundary and eleven false-certificate controls remain active
under optimized Python, including missing/duplicate cores, parameter
gaps, malformed rational denominators and axes that fail coverage.

The optional separate arithmetic audit uses SymPy 1.14.0, pinned in
[requirements.txt](requirements.txt):

```sh
python3 -B tammes15_decagon_remaining_cap_exclusions/audit_sympy.py --compare-parent
(cd tammes15_decagon_remaining_cap_exclusions && sha256sum -c SHA256SUMS)
```

The audit uses explicit coordinate tables, QQ[t], permutation Cramer
determinants and native affine composition. It compares every polynomial
for all 1,092 triples, checks all 1,092 signed witnesses and verifies
all 90 coordinate identities with the earlier reduction. The certificate
and geometric proof are shared; this is separate arithmetic validation,
not an independent mathematical review. Only the optional parent
comparison requires the earlier public source directory.

Optional --trace output is generated locally and need not be published.
The audit's --limit option labels a truncated run as partial. The
[manifest](SHA256SUMS) covers the compact source; no search dump or
external proof corpus is required.

Bounded Powell/Nelder--Mead searches supplied axis proposals, with
NumPy 2.4.6 and SciPy 1.16.2. Floating tolerances, search convergence,
failed wider proposals and incomplete interval tests are not proof
premises. Exact rational checks and interval polynomial signs establish
the stated results. All mathematical processes ran sequentially with
native threads one; no resource limit was increased.
