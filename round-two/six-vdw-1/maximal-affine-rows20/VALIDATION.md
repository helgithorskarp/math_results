# Standalone source validation

six-vdw-1, researcher,2026-10-02. Fresh self-contained source was copied
to an empty temporary directory and run under isolated Python3.12.14
on Linux. Every mathematical input was frozen before this replay. Only
standard-library code was used, with five serial children and thread
variables1. Each child retained the35-second guard.

Regeneration matched the entire22576-byte catalogue, SHA256
`5d7d345794d7b02dba66c6de65ce1b19e757e48335f350130785433a2512e18e`. Both independent checkers ran normally and
with optimized isolated Python; their full mathematical objects matched
EXPECTED.json. The catalogue covers1024 differences/64 cosets, all580
admissible antiperiodic rows and three proper extensions153,277,396.
The maximality mechanism verifies sixty actual bad-coset APs,24320
positive row/AP pairs,1024 membership inputs and1280 original point
identities. Nine catalogue damages and seven separate maximality damages
reject per mode. The ordinary affine argument is in PROOF.md.

Fresh replay took1.498221s with child peak19268KiB.
Core source/input manifest SHA256:
`96d5ec7a1aa9bc08142fa4dee6f21cf2cd28decd0d7bf042c20f9ccddf2483aa`. Full compact receipts are in verification.json.
Timing/resource fields are observations, not mathematical bounds.

This verifies the local construction, the complete containing-cube affine
classification and the row decoder. It checks no full31-field coloring,
actual pole extension,3704 witness or W bound. No native solver is a proof
input. Independent external review/formalization is not claimed.
