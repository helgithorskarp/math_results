# Independent regular-nine Book Ramsey review

Actual reviewer six-reviewer-4, independent mathematical reviewer.
See [REVIEW.md](REVIEW.md) for the exact scope, complete coverage proof,
verdict, credited prior work and proved page-deficit matrix refinement.

From the repository root, with Python 3.11+ and g++ 12/C++17:

```sh
python3 round-two/six-reviewer-4/regular-nine-audit/reproduce.py --work scratch/regular-nine-review
python3 -O round-two/six-reviewer-4/regular-nine-audit/reproduce.py --work scratch/regular-nine-review-O --optimized
python3 round-two/six-reviewer-4/regular-nine-audit/validate.py --replay scratch/regular-nine-review --work scratch/regular-nine-damages
```

Use new scratch directories outside the source directory. The entry point
sets numerical threads to one, executes children serially and enforces
fixed 60-second guards. Standard libraries only; no network, solver,
private input or previous host catalogue is needed. Normal/O runs compare
the entire regenerated 10,827-byte mathematical record with [RESULTS.json](RESULTS.json).
Expected final status `REPRODUCTION_PASS`, SHA256
`2b49242ec77c6925d9c22b7b120891c7be38a595ef385d6658ac5de6c514a38f`.

The fresh search covers all 4,096 local words, 446,985 incidence multisets,
4,194,304 outside words and 583,416 retained completions. None is valid.
The ordinary symmetry/regularity reduction and exact code decoding are
unformalized trust bridges. This excludes only the stated nine-regular
automorphism cohort and does not determine R(B4,B7).

[structure.py](structure.py) checks the exact algebraic controls accompanying
the written weighted-cubic page-deficit, spectral and equitable-component
proofs. Controls are not existence witnesses. [INDEPENDENCE.json](INDEPENDENCE.json)
records the core source/result seal before author executable/fixture inspection.

The optional whole native sanitizer attempt reached the fixed 60-second
guard and is INCOMPLETE. It provides no exclusion evidence and was not
restarted with larger limits. The completed normal/O record supplies the
exhaustive computational evidence. See evidence.json for the exact receipts.

[compare.py](compare.py) is a later corroboration tool. To reproduce that
comparison, replay the separately published author's packet at commit
86ab673e6bda70f9bf7d84241c7459e7e6542898, then pass its scratch work and
EXPECTED.json paths along with the independent replay path. It is not
called by the independent cold verifier and is not an imported premise.
Both complete frame sets match after the explicitly recorded physical
transports; their complete outside-word lists also match.

All full streams, binaries, receipts and logs stay in scratch. No credentials,
private ledger or large proof corpus is part of this directory. Tool versions,
measured costs and later corroboration are recorded in [evidence.json](evidence.json).
