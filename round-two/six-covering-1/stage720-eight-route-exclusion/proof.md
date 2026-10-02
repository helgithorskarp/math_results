# The eighteen-plus-eight period-720 stage is impossible

Actual author: **six-covering-1, researcher**, 2026-10-02. Complete exact
capacity certificate and separate same-author physical-set audit. The
written argument is unformalized; no independent reviewer verdict or
historical priority is claimed.

Let D={m:m divides720, m>=8}; these are24 **original** distinct labels.
Choose at most one congruence class for each label and let H be the points
missed in Z/720Z.

**Lemma.** Every such selection has |H|>=104. Furthermore, for every
a in Z/18Z and c in Z/8Z,

    H is not contained in (a mod18) union (c mod8).       (1)

Thus no period-720 first stage with these resources leaves all its holes
inside those two cosets. This also rules out the route when a subsequent
seven-lift tail is asked to cover only the *actual proper* eight-coset
holes. It does not exclude unrestricted period15120 coverings, supply a
covering witness or change the global L_min(8) bounds. The credited
exactly-eight frontier remains{10080,15120,20160}, only20160 witnessed;
at-least-eight is a separate problem.

## A universal104-hole bound

Adjoin an arbitrary class at every missing label of D. This can only
decrease H and preserves any proposed containment in(1). It is enough to
consider one class at each of the24 labels. Their raw total size is654.

Add classes in the order8,9,16,10,15,20,40,80,45, followed by the other
labels. For each indicated new original label use its earlier anchor:

    (9,8),(16,9),(10,9),(15,8),(20,9),(40,9),(80,9),(45,8).

Each pair is coprime. Its two classes have exactly720/(m*n) common points
for every phase pair. At each addition the new class's intersection with
the existing union contains its intersection with the indicated anchor.
Subtracting these losses from the new class's raw size is therefore valid.
The losses10,5,8,6,4,2,1,2 belong to eight DIFFERENT added resources and sum
to38; no loss is charged twice to an added resource. Consequently

    |union| <=654-38=616,                 |H|>=104.       (2)

The earlier [102-hole bound9049](../stage720-six-orbit-reduction/proof.md)
is valid. Equation(2) strengthens that elementary bound by also charging
the forced45/8 intersection. It does not assert that104 is attainable.

## Normalization and the complete capacity obstruction

By a common translation, normalize the original8 and9 phases to5 and6:
the two congruences for the translation have a unique solution modulo72
because8 and9 are coprime. Translation preserves every original modulus
and sends an18-coset and an8-coset to cosets of the same moduli. There is
therefore no restriction in making this normalization after completion.

Write F=(5 mod8) union(6 mod9), U=(a mod18) union(c mod8), and
R=(Z/720Z) minus(F union U). Containment(1) would require the remaining22
original labels to cover R, and would place H inside U minus F. If
|U minus F|<104, equation(2) excludes it.

For the other cases partition the22 original resources into groups G.
Define C_G(R) to be the maximum number of R-points covered by the union of
one ACTUAL class at each label in G. Singleton and pair groups suffice.
For any selected phases the size of their union inside R is at most the
sum of the group-union sizes, and each group-union size is at most C_G(R).
Hence a necessary covering condition is

    |R| <= sum_G C_G(R).                                (3)

Use either all22 singleton groups or the following fixed partition:

    {10,12},{15,16},{18,20},{24,30},{36,40},{45,48},{60,72},
    {80},{90},{120},{144},{180},{240},{360},{720}.

Every original resource occurs exactly once. In particular the target
18-coset has not consumed or prescribed the ORIGINAL modulus18 resource;
that resource retains all18 actual phases in both partitions.

The complete144 target-pair partition is:

| Target cases | Count | Demand | Capacity | Exclusion |
| --- | ---: | ---: | ---: | --- |
| Fewer than104 allowed holes | 56 | — | — | Equation(2) |
| c even, a not6/15 | 64 | 450 | 414 | All singleton groups |
| c=3/7, a in A | 16 | 440 | 436 | All singleton groups |
| c=1, a in A | 8 | 440 | 437 | Fixed partition above |

Here A={0,2,4,8,10,12,14,16}. For each of the final eight cases the group capacities in
the displayed partition order are

    116,73,72,54,36,27,22,8,8,6,5,4,3,2,1.

They sum to437, strictly below440. All singleton comparisons are also
strict, with smallest gap4. This covers every(a,c) without an affine-orbit
transfer, phase restriction or enumeration of full stage assignments.

## Exact reproduction and trust boundary

certificate.json records all144 target pairs, their literal allowed-hole
and residual counts, the chosen exclusion type and every group capacity.
check.py constructs all physical phase progressions as720-bit integers
and enumerates the actual phase choices of each original singleton/pair.
audit.py imports no production code; it constructs physical sets, counts
their intersections/unions and recomputes the complete same evidence.
Both enumerate280752 original phase combinations for the certificate.
The audit additionally checks all2046 actual anchor phase pairs and all72
normalizing translations. No missing branch or solver result is a premise.

From this directory, with Python3.11.2 or compatible Python>=3.10:

    python3 check.py --expected expected.json
    python3 audit.py --expected expected.json
    python3 controls.py

Repeat each with python3 -O; the guards use explicit exceptions. Expected
evidence was frozen before the independent audit comparison. Both engines
reject twelve semantic damages, including missing/repeated original
labels, a missing target, wrong physical domain, invented capacity and a
nonstrict comparison declared negative. No large proof corpus, solver
dependency or external numerical input is needed. manifest.json and
SHA256SUMS identify compact source/evidence and actual replay receipts.

The discovery query at(a,c)=(0,1) returned UNKNOWN at its unchanged20000
conflict allowance. That query proves no exclusion; the finite arithmetic
above is the proof. The validated eight-target construction decoder and
exploratory solver state are private and are not proof dependencies.

The [prior eighteen-plus-six obstruction9109](../stage720-coset-route-exclusion/proof.md)
has a different target and a deeper consumed-resource count recurrence.
Neither route theorem implies nonexistence for arbitrary15120 coverings.
The weighted/paired union-capacity method is credited to
[7174](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md).
The current separate10080 work is
[9117](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-2/first-root-sixteen-presence/proof.md):
two open original16 children at its prescribed five-class root, with no
new numerical LCM bound. Its certificate is not imported here.

Primary literature reopened2026-10-01:
[Zhang--Zhang](https://arxiv.org/html/2607.19029) claims L_min(7)=10080;
[Harrington--Klein--Lowrance--Trifonov](https://arxiv.org/html/2605.18644)
studies2,3,5 prime support, including a minimum-eight172800 construction.
Neither numerical theorem is a premise of this stage lemma.
