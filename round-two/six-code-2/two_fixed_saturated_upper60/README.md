# Two saturated fixed points: sharp60

six-code-2, researcher, 2026-10-01. For an A(18,6,5) packing invariant
under an involution of cycle type2^8*1^2, if both fixed points occur in20
words then the packing has at most60 words. The new exact computation
proves the multiplicity4 case sharply; multiplicities0/2 use published
bounds56/60. Independent review is pending. The unrestricted69--71
campaign interval is unchanged.

Read [PROOF.md](PROOF.md) for the ordinary completeness bridges, precise
dependencies and scope. The main new reduction forces four fixed words
through each saturated fixed point. Three rooted interfaces,58 matching
configurations and39 complete36-word anchors replace an unrestricted
search. Two second-star decompositions agree entrywise; direct word
graphs and resource graphs agree on every vertex/edge; coloring and P/X
pivot search agree on every complete maximum family. [witness.json](witness.json)
is a compact directly checkable60-word construction.

From a repository checkout, use Python3.11 and GCC12 with C++20; there are
no third-party Python packages. The pinned prior directory
round-two/six-code-2/free_involution_upper68 must be present. Its17 files
are hash-checked before import. The default command cold-replays its
entire proof and three reviewed validators; missing reviewed runtime
files are downloaded by that source's existing SHA-pinned mechanism.

```sh
python3 round-two/six-code-2/two_fixed_saturated_upper60/reproduce.py \
  --work /tmp/six-code-2-two-fixed-normal
python3 -O round-two/six-code-2/two_fixed_saturated_upper60/reproduce.py \
  --work /tmp/six-code-2-two-fixed-optimized
python3 round-two/six-code-2/two_fixed_saturated_upper60/reproduce.py \
  --work /tmp/six-code-2-two-fixed-sanitized --sanitizers
```

Work directories must be new and outside the source bundle. All numerical
and OpenMP threads are set to1 and subprocesses run sequentially. Fixed
per-case guards are200000 nodes/10 seconds for second-star enumeration,
3000000 nodes/30 seconds for coloring, and30000000 nodes/30 seconds for
native pivot enumeration. Any guard failure terminates visibly without
an upper-bound claim. No solver status is used in this theorem.

The deterministic complete result must match [expected.json](expected.json)
byte for byte. Exact source input pins are in [DEPENDENCIES.json](DEPENDENCIES.json);
measured cold-run costs and result hashes are in [VALIDATION.json](VALIDATION.json).
For a repeated new-case check after separately replaying the imported
proof, --skip-dependency-replay still verifies all prior source hashes.
The transitive upper57 census is an imported mathematical premise even
in the default full dependency replay.

The full generated data and native executable remain in the chosen work
directory. They are reproducible outputs, not published proof corpora.
