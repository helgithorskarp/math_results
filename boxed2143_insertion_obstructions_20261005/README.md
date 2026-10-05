# Boxed2143: an exact insertion kernel and a failed pointwise growth route

Author: Quinn (literature-researcher-3). Internal checker: Theo
(literature-researcher-4). Date: 2026-10-05. **The full growth problem is
unsolved.** This directory publishes two checked partial results, not a solution
or an external peer-review claim. No priority claim is made for the kernel.

## The literature target

In a permutation p of [n], a boxed2143 occurrence consists of indices
i1<i2<i3<i4 with p[i2]<p[i1]<p[i4]<p[i3] and no unselected index j between i1
and i4 whose value lies strictly between p[i2] and p[i3]. Let a_n count avoiders.
The target is to decide whether a finite C>0 satisfies a_n<=C^n for every n>=1,
or instead limsup a_n^(1/n)=infinity. Collecting examples or narrowing the
class is insufficient.

The question originated in Avgustinovich, Kitaev and Valyuzhenich,
[*Avoidance of boxed mesh patterns on permutations*](https://doi.org/10.1016/j.dam.2012.08.015),
Discrete Applied Mathematics161 (2013),43–51, Section5. Kitaev, Qiu and Xu,
[*Coincidences and Growth of Boxed Mesh Patterns*](https://arxiv.org/html/2609.13764v1),
12 September2026, Theorem4.4 and Section7, explicitly leave the2143/3412 orbit
unresolved and conjecture factorial growth. That manuscript supplies the
current orbit correction and interval-consecutive formulation. Its stronger
strict odd/even completion conjecture is one sufficient route, not the target
being silently substituted here. Primary-source status was refreshed on
2026-10-05.

## Checked partial results

1. **Exact maximum insertion.** For an old index j let l(j),r(j) be the nearest
   greater entries on its left and right. Call j eligible if both exist and
   p[l(j)]<p[r(j)]. In zero-based indexing, insertion of n+1 at gap g creates
   exactly the occurrences (l(j),j,g,r(j)+1) for eligible j with j+1<=g<=r(j).
   All old occurrences persist. Therefore an avoiding parent has an avoiding
   child exactly outside the union of these closed gap intervals. Restricting
   to values<=M, deleting M and applying the rule enumerates every occurrence
   according to its unique selected maximum M. The legal-gap set alone fails
   as a deterministic next-state description:12 and21 collide, but appending3
   gives different legal sets for the next insertion.
2. **A uniform constant-site obstruction.** For every n>=4,
   p_n=(1,n-1,n-2,...,2,n) avoids even classical2143. Its exact legal maximum
   gaps are{0,1,2,n}, and its exact legal minimum gaps are{0,n-2,n-1,n}.
   Thus its total extremal-site count is8. This refutes every pointwise
   positive linear lower bound on that total for all avoiders. It leaves
   population averages, weighted arguments and the full growth question open.

The complete arbitrary-size proofs are in `PROOF_DRAFT.md`,
`STATE_OBSTRUCTION.md` and `EXTREMAL_SITE_OBSTRUCTION.md`. The files are the
exact bytes transferred before review; their initial awaiting-review headers
are historical. The current verdicts are the separate
`QUINN_KERNEL_REVIEW.md` and `QUINN_EXTREMAL_SITE_REVIEW.md`. Each review checks
the written argument as well as independently replays its finite certificate.
The first review does not automatically cover the later family.

## Reproduction

Requires CPython3.11 or later and only its standard library. Entry indices are
zero-based; gap g follows g old entries. A minimum insertion increases all old
values by one before inserting1. Use one process and one native thread.

From this directory:

```sh
python3 -B check_quinn_kernel.py --max-n 7 --output kernel-portable-replay.json
python3 -B check_quinn_extremal_sites.py --output family-portable-replay.json
python3 -B verify_kernel.py --max-parent 7
python3 -B extremal_site_probe.py --max-n 8
python3 -B kernel.py --pi 2,1,3
```

The independently designed rectangle checker is Theo's exact reviewed source.
His two replay scripts are adapted only to resolve this public directory and
its selected author-file manifest; their mathematical tests are unchanged.
`PUBLICATION_PROVENANCE.json` records the original and adapted hashes. All
selected author source and original review/evidence files are copied verbatim.
`SOURCE_MANIFEST.json` pins that selected author source.

Expected independent kernel replay:5914 parents,46233 maximum insertions,
9 rejected malformed inputs; child-occurrence stream SHA256
`896b9bf0d7ae78603ac8cdd500df0b3b232d1dad94cf4cd55bc379beedff185a`.
The complete literal-definition author replay independently reports stream
SHA256 `1cc6f0ce06411a95eb4b05cf1b1bb68c0755b0bb10e3150173383be341f8f247`.
The full-class finite counts at n=0..8 are
1,1,2,6,23,106,565,3395,22593. They are finite observations, not a fitted
recurrence or asymptotic estimate.

Expected independent family replay: all16 n=7 certificate children,
286 extremal insertions for4<=n<=16, and all704 avoiders through n=6.
It verifies that the n+2 pointwise proposal first fails in length7 at1654327.
The author's probe with upper limit8 stops at the first size7 failure and does
not exhaust sizes7 or8. Lexicographic minimality within size7 is outside the
independent review; the uniform family requires no finite minimality claim.

The original replay JSON files contain original workspace locations and run
timings as historical provenance. Public portable replay outputs can differ
in paths, manifest subset and timings, while the deterministic mathematical
stream, counts, witnesses and source hashes match. Generated fresh outputs
are ignored. No solver, floating point, downloaded dataset or proof assistant
is used. No source-paper PDFs or bulky operational artifacts are included.

## Remaining obligation

The kernel gives the exact object-level recurrence
a_(n+1)=sum_(p avoiding,|p|=n) |G_max(p)|. It does not close the total counts.
The constant-site family defeats a particular sufficient pointwise lower bound;
it does not prove an exponential upper bound or refute factorial growth.
A full answer still needs a uniform entropy/counting proof or a persistent
construction with rigorously unbounded roots, checked by a different researcher.
Public source and graph publication preserve these partial claims; they do not
establish completion of the agreed target.
