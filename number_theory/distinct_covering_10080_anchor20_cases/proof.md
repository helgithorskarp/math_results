# Two nine-class period10080 exclusions

Actual author: **six-covering-2**, role **researcher**. Exact computer-assisted
conditional lemma with same-author literal checks; independent review and
formalization are pending.

No finite covering of the integers by congruences with pairwise distinct
moduli, each at least8 and dividing10080, contains either list

```text
8:0, 9:0, 10:1, 14:1, 12:6, 16:4, 15:2, 18:3, 20:0;
8:0, 9:0, 10:1, 14:1, 12:6, 16:4, 15:2, 18:3, 20:2.
```

All unused eligible moduli may be omitted or have arbitrary phases. The
actual LCM need only divide10080. The prescribed8-class makes the minimum
exactly8. These are two specified-prefix exclusions, not a whole-period
exclusion or an improvement of the unrestricted L_min(8) bounds.

Consequently **any distinct covering retaining either list has actual LCM
at least15120**. Each list has LCM5040, so the only positive possible actual
LCMs below15120 are5040 and10080. Both divide the excluded period. This
implication uses no external minimum-six/seven theorem.

## Proof mechanism

Coverage is equivalent to coverage of all10080 physical residues. At a prefix
A let U be the uncovered set. A nonnegative integer weight w supported on U
has demand D=sum_x w(x). For each unused eligible modulus m, the largest
weight of one of its actual classes is C_m. A completion must satisfy
D<=sum_m C_m. Uniform certificates use w=1_U.

For disjoint pairs of unused moduli replace C_m+C_n by the maximum weight
of the union of one actual m-class and one actual n-class. Every other
unused modulus remains a singleton. Nonnegativity also bounds completions
omitting either paired class. A strict reverse inequality excludes the
prefix. This is the existing [grouped resource bound](../distinct_covering_joint_capacity/proof.md),
extending the [weighted residual bound](../distinct_covering_residual_weight_duals/proof.md).
The union-bound principle is standard; no method-priority claim is made.

To split an unplaced eligible modulus d, retain its class if present or
adjoin any d-class if missing. A class covering no residual point is already
contained in A's union; remove it and substitute a positive-residual class.
All expanded prefixes have nonempty U.

Every positive actual phase is retained or transported to a retained phase.
The checker constructs permutations on the CRT axes32,9,5,7. It checks
bijectivity and every prime-power congruence partition, fixes every
prescribed coordinate class, and verifies the proposed phase's image.
Their Cartesian product therefore fixes each placed class and preserves
every eligible divisor partition. A transported hypothetical completion
would be a child completion. Gcd signatures only propose a target; the
explicit full permutations establish completeness.

At both roots, all32 raw phases of the missing modulus32 are checked before
retaining1,2,12. Each of these branches splits modulus21 with representatives
0,1,2,4,8,15; all21 raw phases are checked. One further modulus24 split in
each tree completes the proof. Terminal cuts are all strict, so induction
up each finite tree excludes its root.

## Exact evidence and reproduction

The [certificate](certificate.json) contains two30-record trees:10 expansions,
24 uniform cuts and26 weighted cuts, of which21 are singleton bounds and5
use disjoint pairs. It has1667 positive Cartesian weight boxes. A box
`[mask32,mask9,mask5,mask7,t]` assigns weight t to the residues whose remainder
on each axis has its mask bit set. Boxes are disjoint and supported in U.
The checker decodes them by physical remainder predicates, counts singleton
progressions and enumerates all actual paired progressions by Python set
unions. It checks238 raw branch phases, including216 positive transports.

Phase0 event SHA256:
`b76e2559f984013168e3a9961867b7f259916f0bdf4e860200891f8e049bf459`.
Phase2 event SHA256:
`b0b2e349bb470d17b5e59994e038af245885440caf410d2f9a6a917281dc36f6`.
Certificate SHA256:
`90b02f0b1ebdb29fe8ed2b0ddbc4fc82c43b9e2e3f96c3784f0fa207965eda7c`.

Run `python3 number_theory/distinct_covering_10080_anchor20_cases/check.py`
from the repository root. The same exact fields and events match with `-O`.
`controls.py` rejects nine malformed/invalid fixtures, including missing
siblings, pending leaves, bad integer totals, negative weights, a consumed
paired resource and a transport moving a fixed anchor.

The exported tree's every event matches the author's separate literal
replay of the new search extension. Public arithmetic and transport code
are ported from that literal checker, not an additional independent peer
check. Integer vectors were discovered with one-thread bounded LPs, but no
solver, floating status, private forest or external corpus is required to
check this certificate. The trust boundary is ordinary Python integer
execution and the stated unformalized finite-covering argument.

Primary context: [Zhang–Zhang](https://arxiv.org/html/2607.19029) concerns
minimum7; [HKLT](https://arxiv.org/html/2605.18644) concerns separate prime
support2,3,5. Their numerical exclusions are not premises here.
