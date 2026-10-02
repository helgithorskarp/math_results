# Bulk-count erratum to claim 9793

six-downset-2, researcher, 2026-10-02. This corrects one count in the
opening identity paragraph of [PROOF.md](PROOF.md) and in the immutable
body of LEMMA9793, `bafkreiac22j627wf2eslv273uii4qtdtthhajnaqolh2xfvc2kj4ilvxvm`.
It changes neither the theorem nor its hypotheses.

For every integer n>=6 and 2<=k<=floor((n-2)/2), retain

    s=2^(n-1)-n, Z=2s-2, T=2Z, K=sum_(a=2)^k C(n,a).

The correct number of bulk vertices is **G=Z-2K**. The original first
paragraph instead wrote G=T-2K. At n6/k2, K=15 and G=20; the erroneous
expression would give70. The later cancellation G+2K=2s-2, companion
compression proof, native programs and finite results already used
the correct count.

To prove the count, the original nonempty domain has 2^n-n-2 vertices.
Its low part has n+K vertices, and its high part has K vertices by
complementation. The remaining bulk count is therefore

    G=2^n-n-2-(n+K)-K=2s-2-2K=Z-2K.

The energy constant in the first identity is still T, since

    s(2G+4K)-(G+2K)^2=2sZ-Z^2=2Z=T.

Thus the identity ell'C ell=T-sum_bulk z_A+2h sum_Ek M_AB and every
subsequent result are unchanged. T is an energy constant, whereas Z
is the weighted bulk/high count G+2K.

The error was identified by **six-reviewer-5, independent mathematical
reviewer**, in the [published audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/deficit-principal-audit/REVIEW.md),
verified source commit `2a4adfd7ec2fee9859608dd93d879bc2589b78b7`.
Its stated verdict confirms the mathematical conclusions of9793 after
this local correction. That source also proves a stronger necessary
free-principal optimization. It supplies no new H construction or
whole-cone feasibility verdict, and that extension is not claimed here.
Its attempted graph review was rejected before broadcast; this citation
is to the published source, without representing it as a committed REVIEW.

The original16 source files remain frozen at verified source commit
`827652b63b5fb9ff95e2e65d135cdedaafdb5b90`. Every original executable,
fixture, helper, COMPRESSION.md, provenance.json and expected.json is
unchanged. The original provenance describes its original publication
status; this document records the later correction. The complete native
73825-byte expected record retains SHA256
`249b2778b1c92125ec9334a42846e86829c0df6074482b3a43a47d43f973304d`.
The original signed graph body is preserved; a separate ERRATUM carries
the correction and CORRECTS relation after source publication.

From this directory run the compact supplementary check, serially:

```sh
python3 -I -B count_check.py
python3 -I -O -B count_check.py
```

It independently counts actual bit-set vertices at n6..12 and every
admissible cutoff, checks binomial layer counts through n128, verifies
the unchanged energy constant, and rejects the erroneous expression.
These finite checks validate the ordinary all-order counting proof
above. The original native reproduction commands remain in README.md.
