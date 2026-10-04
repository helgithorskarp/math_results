# Same-sign two-double angular audit

six-reviewer-1 / independent mathematical reviewer. Independently audits LEMMA10235/0, six-sendov-2's complete real same-sign two-double claim, source39ccb1eef4b190986e60a79154cbd07cef0ed671.

[REVIEW.md](REVIEW.md) contains the full physical classification, all-seven-slot compression bridge, universal exact proof, sharp limit, actual endpoint counterexample and trust boundaries. It confirms \(C<16\) and proves:

- \(C<16-10d^2\) on the entire stated real stratum;
- \(p^2<6\) gives \(C<16-32(u-1)<16-16d^2\);
- \(p^2\ge6\) gives \(C<10\).

Here \(d\) is distance from the normalized vector to its collapsed sign profile. These are sufficient constants, without optimality, historical priority or a full complex first-power verdict.

CPython3.12.14 and SymPy1.14.0 reproduce the fresh CAS route. The complete portable proof check and actual seven-slot checks require only Python's standard library:

~~~sh
python3 -B round-two/six-reviewer-1/two-double-audit/check.py --record scratch/two-double-whole-check.json
python3 -I -B round-two/six-reviewer-1/two-double-audit/literal.py --record scratch/two-double-actual-check.json
python3 -B round-two/six-reviewer-1/two-double-audit/certificate.py
python3 -B round-two/six-reviewer-1/two-double-audit/validate_certificate.py
~~~

Create the scratch output directory first. Set OMP_NUM_THREADS, OPENBLAS_NUM_THREADS, MKL_NUM_THREADS, NUMEXPR_NUM_THREADS, BLIS_NUM_THREADS and VECLIB_MAXIMUM_THREADS to1. Run one child at a time.

For full twelve-mode verification, install SymPy1.14.0 in the selected interpreter, then:

~~~sh
python3 -B round-two/six-reviewer-1/two-double-audit/derive.py
python3 -B round-two/six-reviewer-1/two-double-audit/validate.py --scratch scratch
~~~

If SymPy is in a separate existing library directory, pass that directory to validate.py with --cas-lib. Its isolated children add only that library for derive.py; portable and literal children use no CAS. All child limits remain45seconds. A timeout or resource interruption is a failed verification, never nonexistence.

POLYNOMIALS.json is this reviewer's fresh complete CAS coefficient output. check.py regenerates the whole Fraction companion/cofactor mathematics and verifies every cleared coefficient before any sign inference. It computes all270 denominator,260 divided-gap and270 strengthened-gap tensor controls and reconstructs every polynomial. EXPECTED.json records compact checksums/minima, not proof premises. Complete records112479B/180120B are reproducible outputs and intentionally omitted.

PRIMARY_SEAL.json records five source/input files sealed before any author mathematical fixture exposure. AUTHOR_CERTIFICATE.json is the credited published eight-field mathematical input from the target, copied unchanged after that seal. certificate.py checks every field and inverse position against the independent mathematics, plus sixteen semantic/schema defects. CERTIFICATE_SEAL.json records those three subsequent files. Author native programs were never inspected/imported/run; their bytes and native summary were only pinned for provenance.

VALIDATION.json and CERTIFICATE_VALIDATION.json give whole local/cold normal/optimized comparison results and resource measurements. PROVENANCE.json binds all seven original files and the exact signed original claim. The Fraction matrix/Sturm helpers are credited reuse from own REVIEW10234; its three-double theorem and coefficient17 are not transferred.

The proof's classification, compression, interlacing, domain coverage and interpretation are ordinary and unformalized. Finite actual cases test implementation and pay the counterexample; they do not prove the universal parameter assertion. No large corpus, private checkpoint or runtime environment is included.
