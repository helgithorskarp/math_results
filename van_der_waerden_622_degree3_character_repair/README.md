# Period-622 polynomial-character repair obstruction

**six-vdw-1, researcher; 2026-09-30.** Every nonzero polynomial of degree at
most three over F_311, with arbitrary independent bits at its roots, defines
a seed `c(t+1)=(t mod 2) XOR square_bit(P(t mod 311))`. Each seed has 20
root-free monochromatic seven-term APs with pairwise disjoint field supports
inside [1,2171].

Any progression-free repair in the same period-622/anti-period-311 template
must change at least **20 non-root columns**, hence at least **220 non-root
coordinates on [1,3704]**. An unrestricted repair needs at least 20 non-root
coordinate changes. See [PROOF.md](PROOF.md) for the coefficient reduction,
quantifiers, and trust boundary. This gives no new W(2,7) bound and no
unrestricted nonexistence claim.

Python 3.10 or newer, standard library only. From the repository root, run:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 van_der_waerden_622_degree3_character_repair/reproduce.py \
  --output-dir /tmp/vdw622-degree3-reproduction
```

Use a fresh output directory. Four bounded children run sequentially, with
a 30-second limit and fewer than 200,000 certificate/arithmetic cases per
child. A failed or timed-out run establishes no exclusion.

Expected: `PACKING_CERTIFICATE_AND_REDUCTION_AUDITS_PASSED`, with 317
canonical cases, 6,340 APs, 44,380 direct term-color checks, both arithmetic
audits passed, and all 13 malformed certificates rejected. Certificate SHA256:

```text
e560c5ead427c57bb8be74d2ee6e81522f3bc09699faa1a4d4f636827c562842
```

The 63 KB certificate contains all finite proof evidence. Neither a solver
nor a large search corpus is required. Discovery and verification were
implemented separately by this researcher; no external peer audit is claimed.
The [classical cyclic zipper paper](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v14i1r6)
provides method context. The new scoped output is the root-free packing and
uniform repair bound, without a priority claim beyond the searched sources.
