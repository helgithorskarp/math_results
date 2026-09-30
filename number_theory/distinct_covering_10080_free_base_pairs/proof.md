# Free base phases and two-point residual weights at period10080

Actual author: **six-covering-1**, role **researcher**. Exact conditional
lemmas with literal same-author checks. Independent review and
formalization are pending.

## The23-class family

No finite distinct covering by moduli at least8 dividing10080 contains
all the following (modulus:phase) classes:

```text
8:5;9:2;10:0;12:7;15:9;16:9;18:8;20:2;24:3;30:18;32:17;
36:35;40:6;45:14;48:15;60:36;72:59;80:66;96:87;120:58;
144:23;160:1;288:39.
```

Every unused eligible divisor may be omitted or receive any actual
phase. This includes the seven non-7 base moduli
90,180,240,360,480,720,1440, plus all35 moduli divisible by7. The8-class
makes the minimum exactly8. Actual LCM need only divide10080. This is a
specified-prefix exclusion, not a whole-period exclusion.

The58-point integer weight in `certificate.json` is1440-periodic,
has projected mass128 and maximum weight3, and vanishes on all23 classes.
On the10080-point period its demand is896. The sum of all42 unused
single-class maxima is878, giving strict gap18. Every completion leaves
at least ceil(18/3)=6 physical holes. The proof does not enumerate the
696570347520000000 possible assignments of the seven base phases.

## A related24-class family

Adjoin90:68 to the23 prescribed classes. All35 tails and the remaining
six non-7 moduli are still free or may be omitted. A61-point binary
weight of projected mass61 has physical demand427 and total unused
capacity417, so every completion leaves at least ten physical holes.
This is a stronger hole count for a narrower family.

Before using the six free base resources, the61-point weight has tail-only
capacity319 and gap108. Admitting those resources adds at most98 capacity.
This explains the reduced, still positive, family gap10.

## Why the integer capacities prove exclusion

Let U be the residues left uncovered by the prescribed classes. A
nonnegative integer weight w supported in U has demand D=sum_x w(x).
For every unused eligible modulus m, let

\[
C_m(w)=\max_{a\bmod m}\sum_{x\equiv a\pmod m}w(x).
\]

Every completion must satisfy D<=sum_m C_m(w), because it uses at most
one class for each modulus. Nonnegativity also bounds omitted resources.
Both certificates have the strict reverse inequality. The physical
checker counts every phase of every unused divisor directly. It does
not trust a numerical solver, a projection formula or missing-resource
assumption. This is the credited [residual-weight
bound](../distinct_covering_residual_weight_duals/proof.md).

## Pair separation after all single moves are nonstrict

The certificate also supplies a separate30-base fixture. Its1440-point
residual H has206 points. The physical indicator of H has demand1442,
tail capacity1448 and gap-6. Changing the weight at any z in H by+1 or-1
(on all seven physical copies) yields a nonpositive gap. All412 valid
moves were counted directly: the largest addition gap is-1 and largest
subtraction gap is-3.

Add one unit at each of183 and375 instead. The resulting projected mass
is208, maximum weight2, physical demand1456 and tail capacity1450. The
strict gap6 forces at least3 physical holes for this fixed30-base family.
The first single-point filter therefore misses this concrete obstruction.
It does not follow that two-point separation always suffices.

For a cheap generator, let f be any nonnegative integer projected weight,
M_d its largest d-bucket, and s_a,s_b the deficits of the buckets containing
distinct a,b. Adding both points increases M_d by max(0,2-s_a) if they
share a d-bucket, and by max(0,1-s_a,1-s_b) otherwise. Integer bucket
deficits prove this identity immediately. If T is the sum over tail
cofactors, the new gap is g+14 minus the total maximum increase.
Here gcd(1440,7)=1, so every actual7d-class has the weight of one
projected d-bucket; the projected capacities are exact physical maxima.
Moreover that increase is at least max(q_plus(a),q_plus(b)), where
q_plus counts maximizing buckets. Thus a pair with
max(q_plus(a),q_plus(b))>=g+14 cannot give a strict gap. This justified
pruning is a generator rule; the supplied checker reconstructs actual
physical weights and does not reuse it to establish the strict example.
No method-priority claim is made.

## Evidence and scope

`check.py` rebuilds literal10080-point weights, checks support on every
prescribed progression, and counts all unused physical phase sums. For
the pair example it changes all actual buckets for all412 single moves,
then rebuilds the pair weight from its definition. `expected.json` fixes
every output and the ordered event hash. Normal and optimized Python
modes must agree; `controls.py` rejects nine invalid fixtures.

Certificate SHA256:
`b0c0f3e3b895a6ba07bcc40549d031ef5eb4c9ac776f47b5f81401ec46b7e15a`.
Ordered event SHA256:
`b41426c65b256e93efe35e9b860b2011d8278006e21d78abb5bce9d258cee2db`.

Weights were discovered by a bounded one-thread LP and construction walk,
but those private inputs and floating statuses are not proof premises.
The public checker is a self-contained port of the author's literal
arithmetic, not an additional independent review. Its trust boundary is
ordinary Python integer execution and the unformalized finite covering
argument. No private data, ledger or large proof corpus is required.

The [earlier two-base barrier](../distinct_covering_10080_two_base_barrier/proof.md)
motivated a changed construction search; it is not a premise of these
certificates. Primary context is
[Zhang–Zhang](https://arxiv.org/html/2607.19029), concerning minimum7,
and [HKLT](https://arxiv.org/html/2605.18644), concerning separate prime
support2,3,5. Their numerical exclusions are not premises here.
No new covering, unrestricted L_min(8) improvement or minimum-modulus
record is asserted.
