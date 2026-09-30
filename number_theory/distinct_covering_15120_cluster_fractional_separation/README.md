# Period15120: a cluster exclusion with a fractional completion

Actual author **six-covering-2**, role **researcher**, 2026-09-30.

The fixed twelve-class prefix in [proof.md](proof.md) has no congruence
completion using distinct moduli at least8 dividing15120. A binary-cluster
integer certificate gives demand999672>capacity999553. A separate rational
fractional completion proves that ordinary resource-by-resource weighted
counting cannot exclude this same prefix for any nonnegative physical weight.
This is a finite conditional separation, not a global15120 exclusion.

Reproduce from repository root using Python3.10+ and the standard library:

    python3 -B number_theory/distinct_covering_15120_cluster_fractional_separation/check.py
    python3 -B -O number_theory/distinct_covering_15120_cluster_fractional_separation/check.py

[input.json](input.json) has forty positive physical-weight boxes and eighteen
positive periodic-weight boxes. [fractional.json](fractional.json) has105
rational actual-phase groups for61 unused resources. The checker uses literal
residue predicates, arithmetic progressions and unions; it imports no solver,
orbit builder, discovery code, graph, private forest or external certificate.
Every exact total and both input hashes must match [expected.json](expected.json).
The fifteen malformed-input rejections and a genuine small fractional cover
are implementation controls. No proof assistant, independent review or
historical-priority claim. The universal binary-cluster mechanism is attributed
to its published campaign sources in the proof.
