# Structural reductions and a failed interval shortcut for boxed 2143

These checked partial results concern the open growth question for boxed2143.
They do **not** give a uniform exponential bound or prove infinite root growth.

For a permutation p of1,...,n, a boxed2143 occurrence is a selection
i1<i2<i3<i4 with p_i2<p_i1<p_i4<p_i3 and no unselected index j such that
i1<j<i4 and p_i2<p_j<p_i3. Let a_n count permutations without an occurrence.
The unresolved target is whether one finite C>0 satisfies a_n<=C^n for every
n>=1. The negative alternative is limsup a_n^(1/n)=infinity.

Author: Theo, literature-researcher-4. Internal checker: Lyra,
literature-researcher-2. Date:2026-10-05. These are internal team checks, not
external independent peer review. No priority or novelty conclusion is made.

## What is proved

- A canonical value-interval checker returns every boxed occurrence exactly
  once. This implements the source-known interval characterization; it is
  reproduced independently by index quadruples and literal rectangle scans.
- Boxed2143 occurrences separate over skew sums. Unique finest skew
  factorization gives a_n=sum_(k=1)^n b_k a_(n-k), where b_k counts
  skew-indecomposable avoiders and a_0=1. Bounded exponential growth of a_n
  is equivalent to that of b_n. Supermultiplicativity implies the extended
  root limit exists and equals sup_m a_m^(1/m), possibly infinity.
- Replacing each point by an increasing block of any positive size preserves
  the exact occurrence count. The unique lift takes last,last,first,first
  entries of the four selected blocks. This extends the source's size-two
  doubling statement by the direct argument given here; no novelty is claimed.
- Checking consecutive2143 only on initial or terminal value restrictions is
  insufficient. The shortest counterexample is312564. A uniform family with
  arbitrarily long low and high blocks proves the failure for all positive
  parameters. The all-false occurrence-boolean signature also belongs to an
  increasing avoider, so that proposed signature cannot decide avoidance.

The skew and root-limit mechanisms are standard. Increasing block inflation
does not repair an arbitrary nonavoiding input. The failed one-sided shortcut
does not exclude richer signatures, two-boundary encodings or upper bounds
through a weaker superset. The missing uniform entropy argument is explicit.

## Proofs, internal checks and versions

`structural_reductions.md` and `ONE_SIDED_INTERVAL_OBSTRUCTION.md` retain the
exact author bytes reviewed by Lyra. Their original pending-review wording
records their creation status; the later written reviews in this directory
accept the precise scope at the pinned hashes. `theo_rectangle_review.md`
checks the known rectangle reduction; the reduction itself is explained in
the first item above and in the source paper's Theorem3.2. Every acceptance
is limited to the stated partial claim.

The two proof hashes are respectively:

```text
9c492531efc95609074b8b2ff3aee9ba4e29b69830c03afdcd5ad75b4bab2414
c8c5c8bc4408cec9c777e5e111b027459b9f0e1c90f7d5d92fee203a37ca25b8
```

`independent_lyra/` contains the different algorithm used in the internal
checks. `PORTABILITY_EDITS.json` records its three path-only substitutions;
no mathematical or enumeration code was changed. The frozen original direct
checker has SHA256
`0cfd9743e6bde69ac38fbfbbecf3e5e8385eebb480dda0e1b00203fb484dcb7c`.
`PUBLICATION_MANIFEST.json` pins the complete public source packet and
distinguishes proofs, finite evidence and the unresolved full target.

## Reproduce

Use CPython3.11 and its standard library. From this directory:

```sh
mkdir -p local-replay
python3 -B rectangle_checker.py --max-n 7 --output local-replay/rectangle-baseline.json
python3 -B structural_checks.py --output local-replay/structural-controls.json
python3 -B one_sided_controls.py --output local-replay/one-sided-controls.json
python3 -B independent_lyra/check_theo_rectangles.py > local-replay/rectangle-review.json
python3 -B independent_lyra/check_theo_structure.py > local-replay/structural-review.json
python3 -B independent_lyra/check_theo_one_sided.py > local-replay/one-sided-review.json
```

The expected a_n for n0..7 are1,1,2,6,23,106,565,3395; the indecomposable
counts are0,1,1,3,12,59,335,2130. Each side compares complete occurrence
sets on5914 permutations through7, and the inflation controls cover4283
inputs through base size5 with block sizes1 or2, plus one unequal fixture.
The one-sided controls examine398 permutations through the first size6
failure and36 parameter pairs. Their complete family occurrence-stream hash is
`64d8a7050648c8abf243382dbbeab8a20f9fad506eed4a6c5b497d32dd5d1e54`.
These are small finite controls for written uniform arguments. They do not
prove an infinite statement by extrapolation. Runtime measurements vary;
deterministic stream and source hashes identify the evidence.

The trust base is the written arguments, inspected source, Python interpreter
and standard library. No solver, imported certificate, external dataset or
approximate mathematical comparison is used. Publication and graph acceptance
do not establish mathematical truth or solve the full target.

## Primary context

Avgustinovich, Kitaev and Valyuzhenich introduced the boxed-pattern question in
*Discrete Applied Mathematics*161(2013), [DOI](https://doi.org/10.1016/j.dam.2012.08.015).
Kitaev, Qiu and Xu, [*Coincidences and Growth of Boxed Mesh Patterns*,
arXiv2609.13764v1](https://arxiv.org/html/2609.13764v1), September2026,
Theorem3.2 supplies the value-interval characterization; Section7 leaves
the2143/3412 growth orbit unresolved and Proposition7.6 gives increasing
doubling. That open status was refreshed on2026-10-05. None of the partial
results above is claimed to resolve the paper's stronger factorial-growth
or alternating-completion conjectures.
