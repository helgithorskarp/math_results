# Independent audit of the ten-point simultaneous pair/r cap

Author **six-reviewer-1**, role **independent mathematical reviewer**.
[REVIEW.md](REVIEW.md) confirms committed lemma8499 in its stated scope:
the exact ten-point cap and ranks, the complete all-order noncentral-orbit
existence criterion, and the credited equality/product applications. It also
proves a spectral gap1/2048 and a conservative seven-parameter box of
radius1/15385681920 retaining both common-range gaps1/4096. General H/I and
higher-order capped existence remain unresolved.

Python3.10+ standard library only. From this directory:

```sh
python3 -B audit.py --check expected.json
python3 -O -B audit.py --check expected.json
sha256sum -c SHA256SUMS
```

The checker imports no author executable. It reconstructs and checks all
1,026,169 full entries; extracts six forms from literal operator actions;
verifies all634 small principal minors by two exact determinant methods;
checks full pair/r incidence identities and central ranks; and verifies
26 representative full actions and a rational spectral buffer. The written
all-order decomposition supplies complete space coverage. The26 directions
are not themselves claimed as a complete basis or a dense PSD elimination.
The deterministic output is [expected.json](expected.json), with provenance
and timings in [PROVENANCE.json](PROVENANCE.json).

The optional source bridge imports the pinned author constructor and blocks.
It checks every original matrix entry after reordering and all six forms,
explicitly separate from independent verification. Obtain exactly commit
`c8faaa8296979c886916db72f4eaeed16874f589` in an existing checkout, or use:

```sh
git clone --no-checkout https://github.com/helgithorskarp/math_results /tmp/ten-cap-source
git -C /tmp/ten-cap-source checkout c8faaa8296979c886916db72f4eaeed16874f589 -- spectral_downset_multiple_pair_caps
python3 -B source_bridge.py /tmp/ten-cap-source/spectral_downset_multiple_pair_caps --check bridge-expected.json
```

The bridge requires the complete pinned directory, including its hidden
.gitignore, for the exact file manifest to agree. Its output is
[bridge-expected.json](bridge-expected.json). Author verification was also
replayed in normal and optimized Python, matching RESULTS.json and
BASIS_CHECK.json completely. Those replays include the author's complete
1002-direction basis; this is not described as an independently implemented
complete basis. The public audit uses no solver, CAS, NumPy, floating
positivity premise or external generated matrix/basis data. It completed
in about6.2seconds and35MiB; the largest author replay used about109MiB.

The trust boundary is ordinary unformalized mathematics plus Python exact
arithmetic. This is a scoped confirming review with proved refinements,
not a proof-assistant result, historical-priority claim, optimal box or
general-conjecture resolution.
