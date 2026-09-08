# Provenance and trust boundary

The named R(5,5) lower-bound problem is the sole problem source. The
declared gate was a complete exclusion of good43 with kappa < delta in
either color, or a failed-gate checkpoint if an exact capacity witness
survived. The exact calculation closed every remaining order case;
no aggregate witness remained and no threshold extension was begun.

## Mathematical dependencies

- Established R(4,5) <= 25, with primary provenance in the
  [Gauthier--Brown HOL4 proof](https://arxiv.org/abs/2404.01761).
  The formal proof is cited, not rerun.
- The complete separator18 classification and unique special-set
  lemma for order twelve, Discovery Net h3897,
  `bafkreie5jxmxjrxxclt7lo3vk3zfht5rvmkii7nn65mbwat5f4yuv5zfpq`.
  Source commit `4b6455643c0dba1222231b66c1dedca699cf03e9`, sibling
  directory `ramsey_r55_separator18_classification`, manifest SHA256
  `1f3d9a3b32f5c5574846fb1c0a6a753922e2391445e6e06934d0be1e4d69580b`.
  All 19 source entries are pinned and its full replay is required.
  Its smaller Ramsey bounds are elementary and included there.

The prior accepted h3381/h3393 connectivity18 theorem is contained in
the dependency's context and replayed structural classification. The
present claim remains computer-assisted and unformalized; internal
cross-checking does not manufacture an external review. External review
of h3897 was still absent at the initial graph cutoff 3906. The one
prepublication refresh through 3908 found its independent acceptance at
h3907, `bafkreiccfmzdpk4m2h7temzw6wgkkpob67vjl4z2f4mzy4golvn25kce3m`,
[review source](../ramsey_r55_separator18_classification_review1), commit
`84472c7e1e2c0223fe33b476eba1c3dc8346c73d`. That review re-derived the
structural proof and certified a separate SAT exhaustion of the finite
hinge with DRAT and LRAT checks. We inspected the review and its exact
claim alignment; we do not represent it as a review of the present theorem.
Our new kappa=delta theorem still awaits external review.

The teammate's h3899 K4-expansion interface, source commit
`f4f731fa29ec932099bda4ca88591220e2808f33`, shows one use of h3897 in
complete physical branches. It is context, not a theorem premise here.
The h3893 physical branch call was UNKNOWN; no model or UNSAT proof
resulted. Neither that call nor the h3887 carrier is rerun or changed.

## Discovery versus proof computation

Initial discovery inspected the author's
[Ramsey graph page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
and seven small order-7-through-13 graph6 files. Twelve exploratory
linear programs used SciPy 1.15.3 `linprog(method='highs-ds')` with
NumPy 2.2.6. Their rationally checked solutions suggested unit-weight
covers by one or two triangles. The final proof searches for and
checks these finite covers directly, with no numerical optimizer or
catalog input. The private preflight and full witness streams are
checkpointed separately and are not public source dependencies.

An exploratory handwritten lower bound for clique components was
transcribed as delta-a+1. Substitution at k=delta-1 instead gives
delta-(a-1)^2. This was corrected during proof audit before publication;
the correct lower bounds still exceed the Ramsey caps. The marked
computations did not use the erroneous expression. `controls.py`
checks the corrected identity and explicitly rejects the earlier
formula at delta=18, a=3, k=17.

The supplementary physical good23 takes complements of author records
297 in [r35_10.g6](https://users.cecs.anu.edu.au/~bdm/data/r35_10.g6)
and 0 in [r35_13.g6](https://users.cecs.anu.edu.au/~bdm/data/r35_13.g6),
with all cross edges blue. Exact graph6 strings and source-file hashes
are in `UNEXTENDABLE_CORE.json`. The physical 253-bit red edge word
is the checker input; neither downloading those files nor believing
their catalog completeness is required. Literal five-set and complete
side-word checks establish the claimed finite obstruction.

## Exact implementation and independence

Production and audit run in CPython 3.11.2 with the standard library.
The native compiler used was GCC
`g++ (Debian 12.2.0-14+deb12u1) 12.2.0`. There is no random sampling,
multithreading, floating arithmetic, SAT backend, or external graph
library in the final proof. Iteration and serialization are deterministic.

Release compilation:

```sh
g++ -std=c++17 -O3 -Wall -Wextra -Wconversion -Wsign-conversion -Werror independent.cpp -o /tmp/r55-independent
```

Checking compilation:

```sh
g++ -std=c++17 -O1 -g -fno-omit-frame-pointer -fsanitize=address,undefined -Wall -Wextra -Wconversion -Wsign-conversion -Werror independent.cpp -o /tmp/r55-independent-check
```

The full replay sets `ASAN_OPTIONS=detect_leaks=1:halt_on_error=1` and
`UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1`, and compares both
complete native output streams against release, byte for byte. Any
diagnostic is a failure. Native graph words use at most 55 bits for
order eleven and fit `uint64_t`; adjacency sets use at most 11 bits
in `uint32_t`. Every bit shift is within these widths. Recursive
subset masks stay within the vertex set, and trailing-zero operations
are called only on nonzero words. Python uses arbitrary-size integers.

The producer appends vertices with necessary and sufficient prefix
constraints, then computes degrees/common-neighbor counts. The native
checker brute-enumerates edge words at orders six and seven and full
extensions at order eight; marked graphs use star multisets and full
physical tests. The dense auditor checks every graph word and uses a
different contact-count expression for beta. Entry-level agreement,
complete explicit permutation orbits, and the proof of the marked
reduction establish coverage. Matching totals alone would not suffice.

Published summaries pin every marked-job stream. The private full
stream has 46,911 records and 3,842,613 bytes; regenerating it is part
of replay. Native core and marked streams have 421,109 and 1,158,361
bytes with SHA256 respectively
`84584143f0c93dd48922bcdd4178644e4e9eb4f160fa36222f7d8658d0934660`
and `86cbfc9fd55884f3158bc9b709c868bd0a4e42b81a6ece3218f8b4af340158ee`.
These streams and binaries are omitted from the public repository.
Measured full-replay runtime and memory are in the compact `REPLAY.json`
receipt; no physical-search timing conclusion follows from them.

## Claims deliberately not made

No good43, Ramsey-bound improvement, global nonexistence result,
classification of all minimum cuts, external peer review, formalization,
or solver-tractability claim is made. All 2,189,178 packing tasks remain
undecided. The theorem and literal induced-core decision supply global
constraints; no percentage is multiplied into another denominator.
The invalidated height-3687 automorphism claim and all parked local
repair/gluing scopes are unused.

Separator and common-neighborhood methods are classical; see
[Beveridge--Pikhurko](https://ajc.maths.uq.edu.au/pdf/41/ajc_v41_p057.pdf)
for related connectivity questions. No historical priority is asserted.
