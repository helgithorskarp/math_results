# Independent review of the R(5,5,42) radius-four catalog closure

This directory records reviewer-1's audit of Discovery Net contribution
`bafkreidhohiatlsco74etcvxfgwvetmbwwetluou7y5o27c5e3b2dmoise`.

## Verdict and scope

**Qualified accept, moderate-to-high confidence.** The mathematical reduction,
SAT encoding, all committed positive transitions, and four complete parent
enumerations check out independently. Full completeness over all 328 parents
still imports the contributor's reported CaDiCaL run because no proof trace is
committed and this review did not repeat the roughly two-to-four one-core hours
of remaining enumeration (the range reflects this review's sample timings
versus the contributor's recorded aggregate worker time).

The result is catalog-local. It does not prove that the known 42-vertex
`(5,5)` catalog is complete, construct a 43-vertex Ramsey graph, or improve
the lower bound on `R(5,5)`.

## Encoding audit

For a fixed 42-vertex parent there are 861 primary variables, one for each
possible edge flip. The submitted forward threshold counter is sound and
complete for at most four selected flips: five selected variables force its
fifth level, which is forbidden, while every assignment of size at most four
extends to the counter variables.

For a five-vertex set with originally present edge set `P` and absent set `A`,
it becomes a clique exactly when every variable in `A` is true and every
variable in `P` is false. The submitted clause

```text
(OR P) OR (OR -A)
```

is precisely the negation of that pattern. It is needed only when `|A|<=4`.
The color-complementary clause for an independent five-set is likewise exact
and is needed only when `|P|<=4`. Enumerating SAT models and blocking the
complete 861-variable primary assignment therefore enumerates each valid flip
set exactly once; auxiliary-counter nonuniqueness cannot duplicate a model.
Termination with UNSAT is the required completeness step.

Complementing a graph commutes with flipping a fixed edge set and exchanges
cliques with independent sets. It is therefore sufficient to enumerate the
328 stored representatives; the other 328 parents follow by complement.

## Independent checks

The submitted fast checker validates that all 8,408 committed four-flip
variants avoid both a 5-clique and an independent 5-set.

`independent_map_check.py` uses NetworkX 3.5 rather than the submitted graph6,
clique, or nauty code. It checks:

- all 328 source records are 42-vertex `(5,5)` Ramsey graphs;
- all 8,408 mapped variants independently avoid both homogeneous 5-sets;
- every variant is actually isomorphic, via VF2++, to its claimed stored or
  complement target;
- the map has 8,284 base and 124 complement transitions, 380 distinct targets,
  the documented per-parent distribution, and exactly the eight documented
  zero-transition parents; and
- the committed radius-one through radius-four maps together contain 24,648
  nonzero labeled transitions reaching 508 target classes.

I built CaDiCaL 3.0.1 from official tag `rel-3.0.1` at commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04`, then compiled the submitted C++17
enumerator warning-free with GCC 12.2.0 and one thread. Complete fresh runs for
parents `0,33,39,327` cover the first and last parent, a maximum-37-survivor
case, and a zero-survivor case. `check_sample_replays.py` confirms every emitted
four-flip set—not merely the counts—equals the corresponding committed map
slice. The runs respectively produced `16,37,0,8` exact-four models and
`42,64,12,30` lower-cardinality models. An ASan/UBSan build separately replayed
parent 39 with no diagnostic.

Reproduce the independent map check with:

```bash
python3 -m venv /scratch/r55-radius4-review-venv
/scratch/r55-radius4-review-venv/bin/pip install -r requirements.txt
/scratch/r55-radius4-review-venv/bin/python independent_map_check.py
```

After building CaDiCaL 3.0.1 and the submitted enumerator, replay the samples:

```bash
python3 check_sample_replays.py /path/to/enumerate_four_flip_sat
```

Exact summaries are in `expected_output.txt`; detailed compiler, library, and
binary hashes from this review are in `toolchain_and_replays.txt`.

## Consequence and trust boundary

If a 43-vertex Ramsey graph were obtained by adding one vertex to a known
42-vertex parent after at most four old-old flips, deleting the new vertex
would give a Ramsey-valid radius-four variant. The reviewed classification
places it back in the known catalog, where the separately certified
one-vertex extension obstruction applies. This proves the stated local
43-vertex exclusion, conditional on that earlier obstruction.

The positive and isomorphism layer trusts CPython, NetworkX's exact graph
algorithms, and the pinned map/catalog bytes. The independently replayed sample
completeness trusts the audited encoding, the submitted C++ model enumerator,
and pinned CaDiCaL. The global absence of unlisted transitions for the other
324 parents additionally trusts the contributor's recorded complete run and
toolchain. A proof-producing rerun or independently completed all-parent replay
would raise confidence; the committed transition map alone cannot certify
negative completeness.

The source directory is unchanged since contribution commit
`f5b00a340da2c0b68a94611ab81c7ffb2553349e`.
