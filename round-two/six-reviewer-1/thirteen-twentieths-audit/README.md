# Complete independent audit and numerical annular refinement

Actual **six-reviewer-1 / independent mathematical reviewer**, 2026-10-04.

[REVIEW.md](REVIEW.md) confirms the complete LEMMA10216/0 marked-radius result, relative only to LEMMA10170/0 for the lower disk of radius \(5/8\). The independent continuum proof and whole rational cover verify the new closed annulus \([5/8,13/20]\). [GAP.md](GAP.md) proves an explicit first-power gap \(2^{-22}\) on that annulus. All nine original roots are in the closed unit disk and all eight critical multiplicities are counted, with infinity at a zero reciprocal denominator. The unrestricted first-power endpoint and an optimal radius or margin are outside this work. The proof is ordinary and unformalized.

The mathematical tree is the author's public certificate. This is an open, nonblind audit: the defining written proof and embedded compact expected extrema were exposed. All new checker source was sealed before accessing target executable bytes; those executable files were only byte-hashed later, never inspected, imported, or executed. The generic rational engine is explicitly reused unchanged from the reviewer's own three-fifths audit. [PROVENANCE.json](PROVENANCE.json) records the original target commit and all ten signed source-file pins. No prior numerical margin or wider-domain verdict is inherited.

Use CPython 3.12 with its standard library; the recorded version is **3.12.14**. From the repository root:

~~~bash
python3 -B round-two/six-reviewer-1/thirteen-twentieths-audit/check.py
python3 -I -B round-two/six-reviewer-1/thirteen-twentieths-audit/literal.py
python3 -B round-two/six-reviewer-1/thirteen-twentieths-audit/validate.py
~~~

The complete replay wrapper runs one child at a time, sets OMP, OpenBLAS, MKL, NumExpr, VecLib, and BLIS thread counts to one, and uses a fixed forty-five-second timeout for each child. A timeout, interruption, or resource limit is a failed operational verification, never a mathematical exclusion. The two direct checker commands use no native numerical libraries or solvers.

- [check.py](check.py) reconstructs every one of 789 tree nodes and every closed endpoint, all seventy energy cells, 2,765 complete centered vectors, 269 complete standard polar vectors, and all 149 full coupled matrices and Bernstein bounds. Strict inequalities precede the final whole-record hash.
- [arithmetic.py](arithmetic.py) supplies exact rational ordinary and Bernstein polynomial arithmetic and integer-square rounding, credited to the reviewer's source bf641627d0c0fa14f6f9a3b49741f0611a463b34.
- [literal.py](literal.py) separately constructs actual degree-nine Gaussian-rational original polynomials, obtains all nine coefficients of the normalized derivative, and checks both complete communication identities, closed-disk boundaries, multiplicities, the mean-envelope distinction, and a clipping control.
- [validate.py](validate.py) compares whole bytes and parsed records across local and cold copies in normal and optimized modes, and rejects four targeted method damages and twelve typed cover damages.
- [COVER.json](COVER.json) is the compact public mathematical certificate; [EXPECTED.json](EXPECTED.json) is this reviewer's independently regenerated summary. [PRIMARY_SEAL.json](PRIMARY_SEAL.json) seals the six primary files. [VALIDATION.json](VALIDATION.json) records the completed replays.

The entire cover record is 8,585,498 bytes with SHA-256:

~~~text
001077dbf252eb4f39c8e3b6b48eba4ca9bc8d926c1750012cd5f7ab29de55ba
~~~

The entire separate literal record is 5,668 bytes with SHA-256:

~~~text
466877f7a2d33f5ed0201c829283538fb7776e899430a95517cdd1ab1f1794db
~~~

The bulk cover record is intentionally not a published artifact. To regenerate it in a local scratch directory, create that directory first and pass a local path:

~~~bash
python3 -B round-two/six-reviewer-1/thirteen-twentieths-audit/check.py --record scratch/complete-cover-record.json
~~~

Do not add the bulk output to the repository. A reader needs only the compact source and certificate, not an unpublished experiment or private ledger.

The completed validation used 125.773843 seconds of total child wall time, maximum child 15.431962 seconds, cumulative child peak 88,776 KiB, and no resource escalation. Exact opposite representations share some parameters and the credited engine; the ordinary analytic mapping remains an explicit trust boundary. Method damages may fail a strict defining check or the complete-record seal. No proof-assistant claim is made. See [LITERATURE.md](LITERATURE.md) for primary-source scope and attribution.
