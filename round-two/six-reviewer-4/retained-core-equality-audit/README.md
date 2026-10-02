# Independent retained-core equality audit

six-reviewer-4, independent mathematical reviewer. [REVIEW.md](REVIEW.md) confirms Code LEMMA9251's labeled57-core rigidity and proves the sharp exact55/56-retention classification. The unrestricted A(18,6,5) problem remains open in the campaign interval69..71.

From this directory, with CPython3.11.2 and standard library only, run sequentially in initially empty work directories:

```sh
python3 -B reproduce.py --work /tmp/retained-core-audit-normal
python3 -O -B reproduce.py --work /tmp/retained-core-audit-optimized
python3 -B check_witnesses.py
```

The complete replay computes all1,596 pair and57 singleton punctures, all four pair restrictions, all84 full-core maxima, and the graph/control/provenance records. It compares every compact output byte and the entire private1,082,741-byte record hash. It uses no author program, solver or external executable input. `CORE.json` is its sole search input. `IDENTIFICATION.json` and `acl69.txt` establish credited seed provenance only.

Expected: every unrestricted pair has maximum14/count84 and every individual-forbidden pair maximum13. Exactly66 double-forbidden pairs attain13; the other1,530 attain12. Each singleton-forbidden domain has maximum12. There are5,148 exact56 size-68 codes and3,236 exact55 size-68 codes. `EXACT55_EXCEPTIONS.json` gives zero-based omitted core indices and counts for all66 size-68 pairs. `SHARP_TAILS.json` contains positive lower witnesses; `FULL_CORE_TAILS.json` enumerates the84 fixed-core maxima. `expected.json` and `controls.json` are complete compact readouts, not input assumptions used to calculate optima.

The independent normal/O entire record is SHA256283bc117e5f9a53bb28ec19294619025ab65fb8d6441f432fc854c23cfc6c6ee. Resource limits remain1CPU/2GiB, native threads1, serial mathematical children. Fixed independent180s child and45s/50-pair chunks; controls60s. Runtime failure or incomplete output is not an exclusion. Use workspace scratch for regenerated records; no large traces/tables are committed. `.gitignore` excludes local output/cache files only.

The credited original target source is1868799e4a622fd6442485335891adace47a5960, [core_retention_rigidity](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-code-2/core_retention_rigidity). Prior7540 source0d334e07cfd8161c4ebf0f89cc415143b9b38888 and the classical Aw–Chee–Ling69 code are prior art. Original program replays are later corroboration; details and timing receipts are in VALIDATION.json. The proof is exact computer-assisted and unformalized. No historical-priority or unrestricted bound improvement is claimed.
