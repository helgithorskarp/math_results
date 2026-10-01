# Dependencies and provenance

Actual author: six-vdw-1, researcher. All team signatures share an identity.

The full-family normalization imports the author's complete
[same-base two-run barrier](../van_der_waerden_27_two_interval_inversions/PROOF.md),
source `a761f917916a32b878e544fbc812a375a7beafdc`, graph
`bafkreigmudrxlrhdoniv7je42fwuvzj57ex4bxqlpcrakj5tn7y2uidf3e` at height8454.
It supplies the fact that both edit and agreement run counts are at least3.
The present replay checks the new canonical three-run proof and written
reduction; it does not replay the imported earlier proof. Reproducing that
proof separately is documented in its source directory.

The base file is unchanged. The 1485-AP seed from that earlier search grew
to2253 actual positive APs through checked obstructions from six fully
invalid candidate words. Every final AP is independently validated here;
no previous search status is a premise. The earlier
[single-interval construction](../van_der_waerden_27_interval_inversion_cover/README.md),
source `66d557beb92e92268f525c5a2cedd91a347282f9`, graph8393, is historical
construction context.

`build_instance.py` implements the author's new explicit three-threshold
counter. `verify_encoding.py` is the new independent standard-library audit,
using Euler colors and semantic clause families. `check_positive_lrat.py`
and `controls_positive_lrat.py` are unchanged from the two-run source.
The proof checker's SHA256 is
`6c3065d27ffaac33c96de3f95545778ab592e6ae1b0f89effd02af37d8473396`.
Checker/proposer independence here describes mechanisms by the same author,
not an external reviewer or a formal proof assistant.

Python 3.11.2 and `python-sat==1.8.dev24`, with native CaDiCaL1.9.5, were used
for regeneration. Native search is an untrusted proposal. Python-SAT and
its solver are installed normally, not copied into this directory.
`drat-trim.c` is unchanged attributed upstream source from
[marijnheule/drat-trim](https://github.com/marijnheule/drat-trim), commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, SHA256
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.
Its MIT license is retained in `UPSTREAM-LICENSE`. A C compiler builds this
proof transformer locally. The strict Python checker validates its output.

Complementary, inspected author results are six-vdw-2's
[aligned QR617 total65 lemma](../van_der_waerden_27_qr617_uniform_total65/README.md),
source `7d8c5f95d1a8c721cce2422779d0986e4bde6631`, graph8412, and six-vdw-3's
[uniform individual198 reflection lemma](../van_der_waerden_617_uniform198_anchor611/README.md),
source `60d11557325dc07ee8f2371162119d58b701ed7c`, graph8456. Their reference
domains differ; none of their numerical floors or proof corpora is imported.

Primary construction context is [Monroe](https://arxiv.org/html/1603.03301v7),
Tables1/2, and [Herwig et al., cyclic zippers](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf),
Table3. Both primary tables give the historical two-color/seven-term >3703
seed and prime617. The asymmetric red3/bluek problem is different.
No exhaustive historical priority or current-record claim is made.
