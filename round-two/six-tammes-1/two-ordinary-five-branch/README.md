# Two ordinary fives excluded from the nine-Q branch

**six-tammes-1, researcher.** Complete author-checked conditional proof;
independent mathematical review and formalization are pending.

For a complete connected15-point contact graph on1/2<c<3/5 with degrees
3..5 and a strictly convex hemispherical cellular T/Q sphere embedding,
if there are nine Qs and exactly two degree fives, **at least one five
has at most three Ts**. The [proof](PROOF.md) closes all four count rows.
The(a,b)=(2,2) row and the fourteen-position local core are credited
published mathematics; the other closures and the new adjacent
completion mechanism extend that prior work.

The geometric theorem has no beta premise. Its catalogue corollaries
retain every imported catalogue hypothesis: the ten r=2 profiles from
lemma8975's committed basis become seven; the later source-only seven
become five. These are necessary counts, not spherical realizations.
Global numerical Tammes15 bounds and unrestricted optimizer coverage
remain open.

Run from the repository root, using **CPython3.11 or later**, standard
library only. Each mathematical job is a single process; set all native
thread counts to one if your environment loads numerical libraries.

```sh
python3 -B round-two/six-tammes-1/two-ordinary-five-branch/check.py | cmp - round-two/six-tammes-1/two-ordinary-five-branch/EXPECTED.json
python3 -B -O round-two/six-tammes-1/two-ordinary-five-branch/check.py | cmp - round-two/six-tammes-1/two-ordinary-five-branch/EXPECTED.json
python3 -B round-two/six-tammes-1/two-ordinary-five-branch/audit.py | cmp - round-two/six-tammes-1/two-ordinary-five-branch/AUDIT_EXPECTED.json
python3 -B -O round-two/six-tammes-1/two-ordinary-five-branch/audit.py | cmp - round-two/six-tammes-1/two-ordinary-five-branch/AUDIT_EXPECTED.json
(cd round-two/six-tammes-1/two-ordinary-five-branch && sha256sum -c SHA256SUMS)
```

[check.py](check.py) reconstructs the old core over Q(c), verifies all91
point pairs including poles and strict injectivity, and covers all5460
necessary degree completions. Eight entries survive degree counting;
all fail the new geometric/link obstructions. The noncontact checks
retain225 original opposite pairs with nine admissible entries, all15
opposites in the credited b2 case, and all eight endpoint orientations.

[audit.py](audit.py) imports no primary modules. It enumerates the full
120 words per fan, all144 admissible word pairs, and65536 outside
neighbor bit masks, then uses Hamiltonian link edge subsets. It matches
the complete eight degree entries and all noncontact entry hashes.
The audit shares the proved continuous core classification as an explicit
input; it is a distinct finite representation by the same author, not
independent researcher review or a second continuous arithmetic proof.

[EXPECTED.json](EXPECTED.json) and [AUDIT_EXPECTED.json](AUDIT_EXPECTED.json)
are small output fixtures; neither checker reads them. Releasing the
eight adjacent terminal obstructions or allowing an eighth ordinary
four leaves nonempty incidence controls. Those controls are not packings.
[VALIDATION.json](VALIDATION.json) records output hashes, timings and
entry comparisons. [DEPENDENCIES.json](DEPENDENCIES.json) records exact
prior sources, file hashes, credit and the refreshed primary tables.
No solver, floating point, network input or private corpus is needed.
