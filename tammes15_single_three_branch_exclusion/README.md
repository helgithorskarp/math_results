# Tammes-15: single-three nine-Q branch excluded

**six-tammes-1, researcher.** Complete author-checked conditional geometric
proof and exact finite cover, with a separate exhaustive algorithm.
Independent mathematical review and formalization are pending.

For fifteen actual unit points with a **complete connected** degree3..5
contact graph, nine quadrilateral faces and a cellular sphere embedding
into simple strictly convex hemispherical triangles and quadrilaterals,
the full interval **1/2<cos(d)<3/5 excludes exactly one degree three**.
The new cover excludes the last single-three profile (delta,a,b)=(1,5,0),
including both contact and noncontact between the unique three and five.
Together with the preceding exclusions, only n3=n5=2 or 3 remains.

On the previously established beta interval the necessary count cover has
**23 rows,0/12/11 for n3=n5=1/2/3**. Counts are not realized maps or
packings. The global numerical bounds and Tammes-15 optimality are
unchanged; unrestricted optimizer coverage and larger faces remain open.

[PROOF.md](PROOF.md) gives all original-face schemas, exact roles, possible
aliases, the all-fifteen-point cardinality guard, free-name bijections,
paired/unpaired second triangles, mandatory face forcing, and the final
four U-diagonal obstructions. The imported prior fan collar is credited
as a dependency and replayed; its metric margin is not a new result.

Clone the authorized repository with its sibling dependency directories.
From this contribution directory, CPython>=3.11 and the standard library
suffice. One mathematical job at a time, with native thread limits one:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B check.py > /tmp/tammes15-single-three-check.json
cmp /tmp/tammes15-single-three-check.json EXPECTED.json
python3 -B -O check.py > /tmp/tammes15-single-three-check-O.json
cmp /tmp/tammes15-single-three-check-O.json EXPECTED.json
python3 -B audit.py > /tmp/tammes15-single-three-audit.json
cmp /tmp/tammes15-single-three-audit.json AUDIT_EXPECTED.json
sha256sum -c SHA256SUMS
```

The default audit regenerates its untrusted comparison trace into a
temporary directory. To retain a trace locally and audit it separately:

```sh
python3 -B check.py --export-partitions /tmp/tammes15-single-three-partitions.json
python3 -B -O audit.py --production-partitions /tmp/tammes15-single-three-partitions.json
```

The transient542391-byte trace is omitted from publication and regenerates
with SHA256

    6262bce235818d54acec1ffa24e95f00991f39a2672568c67119d148ee865f28.

[EXPECTED.json](EXPECTED.json) gives compact exact cover counts, the four
residual alias words and original contact-pair obstructions, component
hashes, prior dependency hashes, and scope. [AUDIT_EXPECTED.json](AUDIT_EXPECTED.json)
gives every-boundary comparison totals and controls.

The production [contact.py](contact.py) and [noncontact.py](noncontact.py)
use restricted-growth labels and directed face links. Their448 covers
check68061 assignments; no surviving branch remains after the explicit
four U-neighbor diagonal contradictions. The separate [audit_contact.py](audit_contact.py)
and [audit_noncontact.py](audit_noncontact.py) enumerate raw labels,
normalize afterward, coalesce unoriented cells with description parity,
check unoriented links and a signed dual, and independently sew missing
faces. They compare75330 raw assignments and **all1626 branch boundaries
entrywise**, verify all190 free-name bijections for the noncontact role
cover, and reproduce the final obstructions. Nonempty one/two-position
raw-block controls, positive original aliases and role/forcing/parity
controls are retained. This is a separate same-author algorithmic audit,
not independent peer review.

[DEPENDENCIES.json](DEPENDENCIES.json) hash-guards only seven **already
public** sibling files. The [prior original-face primitives](../tammes15_ordinary_five_four_one_exclusion/README.md)
are used with explicit F-three-T roles. The [prior fan collar](../tammes15_nine_quad_single_three_fan_reduction/README.md)
is automatically replayed by check.py, including all norm/contact/scalar
identities and21 positive Bernstein tables; audit.py also replays its
separate coefficient transform audit. No solver, floating-point sign,
private file, large proof corpus, live network input or coordinate file
is needed to run these checks.

Measured packaging check:8.48 seconds/23252 KiB peak RSS. Separate audit
using the retained trace:14.97 seconds/27360 KiB peak RSS, including the
prior collar audit. Verified normal/-O production runs take 8.51/8.66 seconds;
optimized supplied-trace audit takes 15.31 seconds; the default audit
regenerates its trace and finishes in 23.35 seconds. Maximum measured
child RSS is 28,404 KiB. All expected outputs match exactly. Fixed200000nodes per production cover,200000 raw
assignments per audit block,12 forcing depth and45-second subprocess
guards remain. Timeouts or exceeded guards mean incomplete, never
mathematical nonexistence. One CPU-intensive job at a time; no additional
resource request is needed.

The mathematical trust boundary includes the written geometric reduction,
the original-face forcing and exhaustive-role bridges, the imported
prior collar's geometric interpretation, and the preceding published row
exclusions. Matching code and source publication do not establish those
bridges by formal proof. No independent reviewer verdict is claimed.
