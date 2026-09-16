# Provenance and source integrity

Reviewed target: sibling directory
hadwiger_nelson_ud93_equilateral_closure_stop, mathematical commit
9ac74f0c9858aa04d84a72e13f1b903f2dacb978.

Pinned target bytes:

    EXPECTED.json        b437ecd7250c0c26ac818fd5f58217361046feacf137552e57d4dda9f0df34f3
    PROOF.md             c1db54f95a93d80ba2be798c28a7500f39d66acb77e5fc18c6746de01e89ad83
    README.md            503e72d164ff67492d83b50da3280cca2caf07e6cf9c58a8c5c12075a212e9d1
    build_certificate.py 37d245ecccf2afa044ff9096c0bb4efcf0c057f2961d168b22e8d6cf8f31a98e
    certificate.json     cb6e06023fb334cf60d556df153dfd07c6b239a59214b2d1e6e27559eefec549
    controls.py          9f037721a7d6e0bfeb535e9a2ec135b5d8df712878ce72aff6a7c04bcaf17cee
    verify.py            e22d7cfbada440e5135b1412abe701c57744907c36311d1d6e402fbd826bf522

The target checksum manifest passed. Its normal and optimized verifier outputs
were byte-identical and matched its EXPECTED.json. Its three certificate
corruptions were rejected and its valid certificate replayed.

Upstream source:

- repository: https://github.com/Parcly-Taxel/Shibuya
- commit: 218097c9971db2b60ab94a0b8dae20d76741cc43
- file: shibuya/graphs/pegg.py
- raw-file SHA-256:
  2ba335b24fd02294030595d9b0ae055b30b10b4dfc886f183eb27321c0de75c1

At 100 decimal digits, the pinned upstream construction and the review's
ordered affine source differ by at most 1.05780565562e-90. The upstream
closure residual is below 2.86e-101, and the independently enumerated unit
edge list is exactly the target's 15-edge source list. This numerical check
is reproducible with source_check.py and corroborates provenance only; the
reviewed theorem is exact and self-contained.

Producer regeneration used CPython 3.11.2, mpmath 1.3.0, and
python-sat 1.9.dev15 with CaDiCaL 1.5.3. The regenerated certificate is
byte-identical with SHA-256
cb6e06023fb334cf60d556df153dfd07c6b239a59214b2d1e6e27559eefec549.

Independent proof checking uses CPython 3.11 standard-library exact
arithmetic. Mathematical review commit:
da76985cabd273c524ec2825ae44241ff94b0bef.
