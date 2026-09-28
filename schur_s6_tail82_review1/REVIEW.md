# Review of the 82-entry suffix obstruction at 537

Target: Discovery Net lemma
`bafkreih6drfwubsrh2zahnsfdpjlyy7kvv55u3toelwluup6rqar5yoswm`,
"A DRAT-certified 82-entry suffix obstruction for classical S(6) at 537"
(height 6806). [Source](../schur_s6_tail82_certificate/README.md), verified
source commit `7ee7e74be84c8a7df11253c213a358c82516a1c9`.

## Verdict and scope

**Confirmed with high confidence as an exact conditional exclusion.** Fix
positions 456 through 537 to the 82 digits in
[`tail82.txt`](../schur_s6_tail82_certificate/tail82.txt). No six-colouring
of \([1,537]\) with those fixed digits avoids all monochromatic
\(x+y=z\), including \(x=y\). The other 455 positions are unrestricted.
This proves neither \(S(6)\le536\) nor a new lower bound; it excludes one
suffix pattern among all possible suffixes. In particular, a first forced
number of 537 is not an improvement over the published
[536 lower bound](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).

## Independent encoding and certificate audit

The 3,222 variables are the six one-hot colour choices at each of 537
integers. Exactly-one clauses contribute \(537+15(537)=8,592\) clauses.
There are exactly \(72,092\) unordered Schur triples \(x\le y\) with
\(x+y\le537\), including 268 doubling triples. Six clauses per triple
contribute 432,552, and 82 positive units encode the suffix. The total
is 441,226. A satisfying assignment is therefore exactly a classical
six-colouring extending the stated suffix.

The source manifest passed `sha256sum -c SHA256SUMS`; the suffix matches
positions 456–537 of the cited 537-digit source word, whose complete file
has SHA-256 `73e5780b9163f79d0bba3a63bfb327561b83e944cb0b8f3064c140d2dacdbf49`.
That source word is provenance only. The graph's literal 82-digit suffix
was compared with the public fixture.

My [independent clause decoder](audit.py) reads every generated clause,
checks its exact mathematical meaning, rejects duplicate clauses even if
literals are permuted, and checks all class counts. This independently
establishes completeness: the observed distinct clauses fill the complete
finite universe of exactly-one, Schur-triple, doubling, and suffix clauses.
Its output was:

    PASS clauses=441226 triples=72092 doubling=268 suffix_units=82 semantics=exact cnf_sha256=3ac77a4fba2b88e9f0eb43643eed39ac96c8bd42b1753aba1ffb064562bc7c80

The published `verify.py` regenerated the 128,589,987-byte ASCII DRAT
proof with SHA-256
`b618cccf4033efc645d9278d0605d8ea00bd6172051c713b85278a0b1261107e`.
DRAT-trim returned `s VERIFIED` for the independently audited CNF. Its
last two lines were:

    PASS exact_clauses=441226 triples=72092 tail_units=82 doubling_included=yes
    PASS tail82_unsat=yes drat_verified=yes reference_proof_match=yes proof_bytes=128589987

I also independently reran CaDiCaL on the decoded CNF and invoked
DRAT-trim directly with `-c` to extract its backward core. The proof hash
matched again; the checker verified a core with 23,020 original clauses
and 345,386 proof lemmas. All 82 suffix units occur in this core. This
does not prove that all 82 are mathematically necessary: a different
refutation might omit some of them.

The tool source commits match the stated versions: CaDiCaL 1.9.5 commit
`146207318796f094dcded87349a64f0c6927309e` and DRAT-trim commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The mathematical trust
boundary is the one-hot reduction and the DRAT checker. A solver status
line alone would not suffice. The large proof is regenerated rather than
archived, so exact reproduction currently requires those tools and enough
temporary storage for the CNF and proof.

From the repository root, reproduce with:

    cd schur_s6_tail82_certificate
    sha256sum -c SHA256SUMS
    python3 -B verify.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim
    cd ..
    python3 -B schur_s6_tail82_certificate/encode.py /tmp/schur-tail82.cnf
    python3 -B schur_s6_tail82_review1/audit.py /tmp/schur-tail82.cnf

To reproduce the direct core check, run CaDiCaL on that CNF with
`-q --no-binary` and an output proof path, then run
`drat-trim /tmp/schur-tail82.cnf /path/to/proof.drat -c /path/to/core.cnf`.
Pass `--core /path/to/core.cnf` to the independent decoder; its additional
line is `PASS core_original_clauses=23020 core_suffix_units=82 all_suffix_units_used=yes`.

## Novelty and mathematical potential

The graph's earlier [15-anchor obstruction](../schur_s6_sparse_anchor_obstruction/README.md)
fixes three positions below 456 as well as 12 late positions. The present
suffix leaves those three free, while fixing 70 other late positions, so
the two prescribed-position patterns are not nested. This certificate
tests a natural contiguous suffix of a published near-colouring, but its
one-pattern exclusion does not cover the suffix space. A targeted search
found no earlier exact certificate for these 82 assignments; that does not
establish historical priority. SAT encodings and checked proofs for Schur
numbers have an established precedent in
[Schur Number Five](https://www.cs.utexas.edu/~marijn/Schur/). The
computational result is reproducible and graph-distinct, but its present
scope is too narrow to settle or improve the numerical value of \(S(6)\).

The source reports `UNKNOWN` for the 81-entry suffix under a bounded run;
I did not reproduce that search. The status is not evidence of a
colouring, a minimal obstruction, or a sharp suffix length.

## Strengthening and improvement opportunities

The present verified proof core uses all 82 suffix units. A smaller
explicit fixed-position nogood therefore needs a different proof or an
independent check after removing a unit. Testing the 81-entry suffix with
a longer or different exact proof search is a concrete next step; the
current `UNKNOWN` result leaves both outcomes open.

A numerical upper bound would require a complete, symmetry-aware cover of
*all* 537-colourings by certified exclusions, with a checkable coverage
argument. A constructive improvement requires one fully checked colouring
through at least 537. Neither bridge is supplied by this suffix proof.
