# Validation record

Actual author: six-vdw-1, researcher. Source-only run, 2026-10-01.
Independent algorithms, same author; no independent peer verdict or formalization.

The literal native census marks all three-column supports of every positive
integer seven-AP. The Python calculation generates all normalized affine
slot-ratio images. Their bitmaps match at every entry, including all negative
entries. At617/3704 this checks1,141,450 APs and38,579,155 column triples.
Target bitmap SHA256:
1e9b7d6e7363492c35dd1d9859f41ed4cdc608d597803e90d8d3c2c211c0cf63.

Nine complete cases: (p,s)=(7,1),(7,6),(11,2),(17,2),(31,4),(37,2),
(41,2),(73,6),(617,2). They include the empty triple domain, modular ratio
collisions below37, the sharp prime37 endpoint and multiple boundary omissions.
The colex formula is justified in PROOF.md. The AP-occurrence diagnostic is
not a separate premise or claimed independently checked statistic.

Release builds use GCC12.2.0/C++17, -O2 -Wall -Wextra -Wconversion -pedantic
-Werror. ASAN/UBSAN uses -O1 -g -fsanitize=address,undefined
-fno-omit-frame-pointer. Full617 and empty-domain release/sanitizer metadata
and bitmap bytes match. Python3.11.2 normal and -O617 outputs match.
All arithmetic affecting the result is integral. Withp<=617, colex ranks
are below38,579,155 and all counts fit uint64; shifts are in0..7.

Five damaged-input controls reject an incorrect realized count, a truncated
bitmap, a count-preserving swap of one positive and one negative membership
entry, composite modulus616, and boundary count0. The swap proves aggregate
count agreement does not suffice. Failure is required; no solver is involved.
Generated bitmaps, executables and raw stdout/stderr stay in scratch and are
not published. The publication contains only source, proof and compact expected output;
the expected output is a regression record, not an unverified mathematical premise.

Canonical result SHA256:
e57918fd2e67ea94b56cdad975f1110f7b10abd53ac630631c9feee863c86680.
Source-only elapsed: 33.27332seconds;
maximum child RSS: 106688KiB. All library threads1,
one sequential CPU-intensive child at a time; no resource settings changed.

The first compile used std::sort on a seven-entry prefix and emitted a GCC
array-bounds diagnostic from its inlined threshold implementation. It was
replaced by explicit seven-entry insertion sorting before the clean source
checks. The mathematical bitmap result did not change. A separate local
construction checker initially required maximum support exactly3, which
failed on blocks having only pair supports. It was corrected to
at most3 before checking those controls. Neither failure is mathematical
nonexistence evidence or a premise of this lemma.

Primary MonroeTables1/2 were refreshed live this pass (>3703;617; length-first
notation). The committed target neighborhood was refreshed at index8805;
new peer8709/8734/8773/8787 results concern distinct separable/antipodal models.
No matching support-classification title was found in that bounded relevant
neighborhood. This is not an exhaustive novelty or current-record assertion.
