# Verification, discovery and trust boundary

The public verifier uses Python's standard library and a C++20 modular
filter. Tested versions were Python 3.11.2 and g++ 12.2.0. It invokes no
SAT solver. Its 411 new colouring words, together with 664 inherited words,
give 2,717,716 direct base-edge checks and 599,850 extension tests.

The exact coverage histogram, as `covered deletions: exterior points`, is:

    508:33, 509:14, 510:17, 511:20, 512:30,
    513:39, 514:80, 515:115, 516:210.

Normal and optimized Python verification produce byte-identical results.
Four malformed certificate controls reject: an improper colouring word,
a changed target order, a missing exterior point, and removal of all new
colourings, leaving insufficient deletion coverage.

## Native and geometric controls

The native filter is adapted from the previously audited H510 filter only
by increasing its maximum input order from 510 to 516. The scale remains
96 and every coefficient is checked to lie between -144 and 144. All
residue products are at most `(1000080)^2`; intermediate sums are below
2.1 trillion, safely within unsigned 64-bit arithmetic. Subtractions are
offset by the modulus before reduction. The count 22,765,060 also fits.

The producer uses exact rational field inversion. The auditor uses a
separate monomial-exponent representation and does not invert or reconstruct
centres. Every centre and all its neighbours are checked entrywise. The
native loop and the polynomial homomorphism argument supply exhaustive
coverage; agreement of aggregate counts alone would not suffice.

`controls.py` compares all 2,526 triples of three small fixtures with direct
exact arithmetic, finding 48 unit-circle triples. It also rejects an order
517 header, a wrong scale, and an out-of-range coefficient. Release and
AddressSanitizer/UndefinedBehaviorSanitizer runs agree on those fixtures.
The sanitized executable also reproduces the entire 105,755-row survivor
stream byte for byte.

```sh
g++ -std=c++20 -O1 -g -fsanitize=address,undefined \
  -fno-omit-frame-pointer -Wall -Wextra -Wconversion -Wshadow -pedantic \
  hadwiger_nelson_heule516_all_plane_onepoint_closure/filter.cpp \
  -o /tmp/hn516-filter-sanitized
python3 -B hadwiger_nelson_heule516_all_plane_onepoint_closure/controls.py \
  --filter /tmp/hn516-filter-sanitized --work /tmp/hn516-filter-controls
```

The `--reuse-census` path recompiles the filter and enumerates all triples
again, then compares the exact stream before auditing the centres. A cached
stream with one omitted survivor was rejected at this comparison. It cannot
be certified solely by keeping a matching count in a metadata file.

## Colour discovery and compact certificate

The 516-vertex source already has exact physical non-four-colourability
evidence. No new source query was used. Transporting the 664 existing words
first closed 316 of the 558 exterior points and left 242 unresolved.

One incremental Glucose42 encoding then searched for colourings of B-v+q
only for exterior q. Base-vertex activation literals disable exactly v;
point-selection literals activate q's exact unit-neighbour constraints.
Three mutually adjacent base vertices have fixed distinct colours, a valid
global colour-permutation normalization even if one of them is omitted.
Each vertex has an at-least-one-colour clause; adjacency forbids sharing
any chosen colour, so selecting one colour from a satisfying colour set is
sound. Every resulting word is checked directly and transported to every
exterior centre for which it extends.

There were 441 queries, all SAT, with a limit of 200,000 conflicts per query;
the whole run took about 113 seconds. No UNKNOWN or UNSAT result was used.
One reverse-order pass removed 30 redundant new words while retaining
coverage at least 508. The public compaction script regenerated the
82,664-byte certificate byte for byte. No optimality is claimed for its size.

Optional discovery reproduction requires `python-sat==1.9.dev15`:

```sh
# First create a fresh census with verify.py as documented in README.md.
python3 hadwiger_nelson_heule516_all_plane_onepoint_closure/discover_colourings.py \
  --work /tmp/hn516-plane-onepoint
python3 -B hadwiger_nelson_heule516_all_plane_onepoint_closure/compact.py \
  --work /tmp/hn516-plane-onepoint
```

Discovery refuses to overwrite an existing query result. The theorem does
not depend on reproducing solver choices: the published words are sufficient
witnesses. Bulky centre tables, survivor streams, query logs and binaries
are regenerated in the external work directory and are not committed.

## Provenance and scope

`INPUTS.json` pins the source geometry, inherited colouring words, input
tables and reused exact arithmetic modules. The geometry modules come from
the earlier H510 census and use different representations for production
and audit. This is algorithmic independence within the author's check;
no independent-author review of the new closure is claimed.

The new theorem concerns q outside H632. Its whole-plane corollary imports
h3991 for the 116 points of H632 outside B; that closed family was not
queried again. The source's positive chromatic evidence supplies motivation,
while the negative theorem depends only on checked colourings and the exact
geometric census. Trust remains in the stated Euclidean and pigeonhole
arguments, pinned inputs, exact integer/Fraction arithmetic, the native
enumeration and direct verification code. No floating-point decision,
solver refutation, LRAT proof or heuristic search boundary is trusted.

No graph of order at most 508 with chromatic number five is established.
This complete one-point family is closed; further construction is a separate
phase involving a different base or more than one added point.
