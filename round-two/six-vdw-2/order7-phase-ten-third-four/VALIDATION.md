# Validation boundary

The public reconstruction regenerates all eight complete CNFs from the
published generator, compares every canonical hash and record to EXPECTED.csv,
reconstructs the full field clause multiset independently, checks both kinds of
exact-count gates, and runs both strict proof modes on untrusted candidates.
Every expected proof hash and count must reproduce in the recorded replay.

Normal and optimized controls reject missing branches, false counts or
premises, false next neighbors, damaged field constraints and counters,
removed/reversed prior rules for both backgrounds, modified helpers before
execution, and unsupported or missing live proof hints. Each proof mode also
accepts an explicit valid contradictory-unit RUP control. Repaired CNF hashes
and row counts make the semantic damages test more than hash comparison.

VERIFICATION.json gives exact results, runtime and memory measurements. These
checks establish the stated restricted computer-assisted lemma together with
the written mathematical cover. They do not claim an external review, a
formalization, the phase-endpoint exclusion, or a new numerical W bound.
