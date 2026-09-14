# Point606 conditional criticality: a 530-point core misses the cap

An unrestricted colouring query resolves a gap left by the old fixed
colouring library: **H606 minus vertex122 is five-chromatic**, not merely a
graph on which the old words fail to extend. One deterministic deletion
sweep extracts a **530-point, 2648-edge, vertex-critical five-chromatic
strict plane unit-distance graph**. Exact geometry, a proper five-colouring,
and proper four-colourings of all 530 single-vertex deletions are supplied.
The non-four-colouring proofs were checked locally; regeneration and checking
are provided below. The generated proofs are not included in this compact
source package.

**This is a failed construction gate for the at-most-508 objective.** The
core exceeds the cap by 22, and every proper induced subgraph of this core
is four-colourable. It is not a record graph, an improvement to the published
509-point record, or a closure of all at-most-508 subgraphs of H606.
Different deletion choices in the full host remain undecided.

## Frozen geometry and target

Use the original Parts labels V={0,...,508}, and the published 76 completion
points P={509,...,584} with at least seven original unit neighbours. Put

    q606 = (-(1+sqrt(33))/6, (sqrt(3)+sqrt(11))/6),
    H606 = UD(V union P union {q606}).

The full envelope has 586 distinct points and 3090 strict unit edges. The
new point has exactly the neighbours {37,51,69,142,180,198,530}.
Coordinates use Q(sqrt(3),sqrt(5),sqrt(11)), with coefficients in the mask
basis (1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165))
and denominator 288. The verifier parses pinned original coordinates and
completion coordinates, checks collision freedom, and checks all 171405
unordered pairs. It includes every exact unit contact.

The starting finite target was a non-four-colourable induced subgraph of
H606 on at most 508 points. The published
[partial-forcing reduction](../hadwiger_nelson_parts509_partial_forcing_family/README.md)
leaves 450 forced original points, q606, and at most 57 of 135 optional points.
Its original selector is already certified SAT; it was not rerun in an
attempt to prove that unchanged formula UNSAT. The present new graph query
instead tests the missing original 122 with all four-colourings allowed.
The positive geometric input was an actual five-chromatic parent and a
documented failure of old full-graph deletion words to extend, not a newly
screened pair relation. Omitting122 also separates the extracted branch
from a fixed-L374 transfer cohort, which retains 122.

After deleting 122, the 585-point graph has 3079 edges. Kissat 4.0.4 returned
UNSAT in 1.590 seconds, and drat-trim accepted its complete proof. This
establishes a genuine larger obstruction, not a record-scale signal.

## Exact extraction boundary

Starting with H606-122, try deleting the 58 original optional labels in
increasing order, then the 76 pool labels in increasing order. Each query
has a 15-second native limit. Keep a deletion on UNSAT; retain the vertex
on SAT or UNKNOWN. The one sweep made 134 queries, completed in 128.137
seconds, and had no UNKNOWN query. It removed 55 additional vertices and
recorded 79 checked proper four-colourings for failed deletions. No seed,
order, host, or pool variation followed this sweep.

The final deleted set is in [certificate.json](certificate.json). A new
ordinary four-colour query on its 530-point remainder produced a complete
proof in 1.713 seconds. drat-trim accepted that proof. Intermediate UNSAT
answers are discovery information; the final independently checked proof
is sufficient to certify the frozen remainder.

For every remaining optional vertex, restrict its recorded SAT word to
the final core with that vertex omitted. For the 450 remaining forced
originals, restrict an indexed word from the published lifting library.
For q606, restrict the original A7-122 colouring. Every restriction is
checked against the complete physical graph, giving all 530 deletion words
and 1398144 retained-edge checks. Thus every proper induced subgraph of
this particular 530-point core is four-colourable. Together with the
negative proof and proper five-colouring, this proves vertex criticality.

The certificate reuses 451 indexed old words and supplies 79 new literal
words. These positive checks do not import an old nonexistence theorem.
The original partial-forcing reduction explains the target selection only;
it is not required to prove this core's chromaticity or criticality.

## Reproduce

From this directory in a full checkout, with Python 3.11 or later:

```sh
python3 -B verify.py
sha256sum -c SHA256SUMS
```

This checks exact geometry, the proper five-colouring, all deletion
colourings, three invalid-word controls, and the exact negative CNF hash.
It explicitly reports that the non-four proof has **not** been checked.
The CNF has 2120 variables and 11125 clauses, SHA256
`a4d45411df483f11b0b1cbc5e16d0af2ecf2e3221d4924112d71a85031b54f3e`.

To regenerate and independently check the negative proof, use a fresh
directory outside the checkout, Kissat 4.0.4 and drat-trim:

```sh
python3 -B run_native.py --work /scratch/fresh-point606-proof \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

The native script allows one bounded query, at most 120 seconds, with a 4 GiB
address-space limit. It does not restart an existing directory. A timeout
is UNKNOWN. A checked proof gives:
`530-POINT FIVE-CHROMATIC VERTEX-CRITICAL CORE VERIFIED; CAP MISSED`.
Alternatively, check an existing proof without running a solver:

```sh
python3 -B verify.py --proof /path/to/core.drat \
  --drat-trim /path/to/drat-trim
```

Each vertex has four Boolean colour variables, an at-least-one clause,
and one same-colour exclusion for each unit edge and colour. At-most-one
clauses are unnecessary: choosing any true colour gives a proper word.
The unit triangle {0,149,152} is pinned to colours 0,1,2; every proper
four-colouring admits that global colour permutation. No other symmetry,
interface hypothesis, or restriction on the other colourings is imposed.

## Evidence limits and disposition

[manifest.json](manifest.json) pins exact inputs, point/edge/CNF identities,
and the two locally checked proof hashes. The proofs occupy 1869344 and
2058905 bytes and remain outside the repository. A reader must regenerate
a proof or supply one to verify non-four-colourability; the default
positive checker alone does not establish it. [validation.json](validation.json)
records the author-run proof check. This is not independent external review
or proof-assistant formalization. Trust includes the ordinary encoding
argument, pinned data, Python integer arithmetic, SHA256, drat-trim and
runtime/hardware. Native solver verdicts alone are not trusted as proofs.

The capped construction gate failed on this extracted core. Bank its exact
criticality evidence, preserve the full-host question as open, and do not
use the larger obstruction to justify more random deletion orders, nearby
points, host growth, or a return to standalone pair-source screening.
The companion operational report records any bounded conditional-selector
probe separately; no selector probe is needed for the claims above.
