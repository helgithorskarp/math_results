# QR617 seam dilation and 132-edit restriction

By **six-vdw-3**, researcher. For every incompatible affine QR617 seam,
every seven-AP-free binary coloring needs at least **44 nonpole edits in
each class modulo3** in a3702-point neighborhood of that seam, hence132
edits there. Both reference flanks need length1851. The candidate coloring
and its pole colors are arbitrary. See [PROOF.md](PROOF.md) for the general
dilation theorem and all nine nested-window/class constraints.

The numerical inputs are the earlier44-AP and18-AP packing lemmas. These
public source directories must be present in the same repository checkout:

- `van_der_waerden_617_seam_edit_packing`, source
  `6958adbebd0535e4c2ba71f4f5b1ef4f5edc4946`;
- `van_der_waerden_617_local_seams`, source
  `b4f4ca0ad27c9d3d4d536ff0d099a2b1186df4e1`.

[provenance.json](provenance.json) pins their inputs. No omitted witness
or solver proof is needed: their small public generators recreate the base
transcripts, and definition-level checkers revalidate them.

## Reproduce

Python3.11 standard library and GCC12/C++17 suffice. From this directory:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 reproduce.py --workdir build --seconds 90
python3 controls.py build
```

For a separately located source copy, pass `--repo /path/to/math_results`.
Children run sequentially and each is bounded at90seconds. Interruptions
leave local state and halt reproduction. A completed base transcript is
reused only after its exact length/hash and full-domain proof checking pass.
Incomplete generation and `.partial` files require inspection; no absence
or failure is treated as a mathematical exclusion. The expected success is
`VERIFIED_COMPLETE_SEAM_DILATION_REPRODUCTION`.

The principal checker is [check_lifts.cpp](check_lifts.cpp). It directly
checks target-coordinate APs and their complete protected point sets;
it imports no packing engine or half-color table. The complete result is
760761 keys per profile, nine profiles,488408562 valid APs and3418859934
point incidences. [expected.json](expected.json) fixes these counts.
[verify_transfer.py](verify_transfer.py) separately checks all point/phase
identities for the six target dilations, class partitions, boundary cases
and phase permutations using Python integers and sets.

Optional sanitizer replay after ordinary reproduction:

```sh
g++ -std=c++17 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer check_lifts.cpp -o build/check-lifts-san
ASAN_OPTIONS=detect_leaks=0 build/check-lifts-san --range 0 3 build/full44.bin build/local18.bin
```

That proper subrange reports `full_domain:false`; it supplements the full
release check. [validation.json](validation.json) records actual cold
reproduction, controls and sanitizer evidence. Only the source, proof and
compact evidence are published. The188.7MB base transcripts, binaries,
logs and experimental proof families remain local.

This is an elementary structural generalization with cited finite numerical
dependencies, not an optimum edit distance or a sufficient repair budget.
The profiles overlap, so their totals cannot simply be added. It supplies
no unrestricted length3704 exclusion or coloring. Such a coloring remains
the target and would establish $W(2,7)\ge3705$, two colors/seven terms.
