# J74 local mirror rigidity: independent audit

Actual reviewer **six-reviewer-4**, independent mathematical reviewer.
See [REVIEW.md](REVIEW.md) for the complete proof, verdict, trust boundary,
literature and improvement opportunities.

Confirmed local theorem 8839 and new shadow prerequisite 8775. All-source
receiving collars are positive but unquantified. This audit supplies an
explicit joint box: receiver tangent norm and relative Cayley norm at most
`1/3939996766880`. It also enlarges the closed shadow-reduction chord radius
from `1/15` to `2/29`. These are distinct scopes; neither is a numerical
all-source exclusion radius. Global J74 remains open.

Tested with CPython 3.11.2; standard library only. From this directory:

```sh
python3 -B audit.py
python3 -B -O audit.py
python3 -B symbolic.py
python3 -B -O symbolic.py
sha256sum -c SHA256SUMS
```

Each Python command prints `PASS`. `audit.py --emit` reproduces every value
of the compact `expected.json`; `symbolic.py --emit` reproduces the separate
coefficient-identity record. Normal and optimized runs agree. Finite evidence
includes 132,480 original support comparisons, 184 acute corners, 46 complete
closed cones, 4,320 boundary supports, 2,304 interior distances, 168 prototype
reflection images, 616 marked boundary matches, five rejected geometric
controls and 28 polynomial identities with two consequential damage controls.

The optional attribution comparison needs the producer's small public
`round-two/six-rupert-2/local_mirror_rigidity/expected.json` at commit
`370d5cf35fd56ee1e345348b96f0359e8aae4870`. Its SHA256 is recorded in
`PROVENANCE.json`. Save that file outside this directory, then run:

```sh
python3 -B compare.py /path/to/producer-expected.json
python3 -B -O compare.py /path/to/producer-expected.json
```

Both print `PASS 398 exact scalar comparisons`. This is optional comparison
evidence; the physical proof checks do not import or execute producer code.

`geometry.py` reconstructs the original body independently.
`inputs.json` contains untrusted, reindexed literal rays, weights, edges,
boundary inventories and matrices, whose assertions `audit.py` checks against
that body. `symbolic.py` uses an independent sparse integer-polynomial ring.
The continuum estimates and compactness argument remain ordinary proofs.
Named-body identification and complete global minimum catalogue 8551 are
credited to sufficient independent review 8635, not re-enumerated here.

`VALIDATION.json` provides compact run evidence. Source publication does not
formalize the theorem. No raw support corpus, ledger, private log or large
certificate is included.
