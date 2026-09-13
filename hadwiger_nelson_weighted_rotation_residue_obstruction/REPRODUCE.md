# Reproduction

Run from this directory in a checkout of the repository. The only imported
research input is the existing `../hadwiger_nelson_parts509_completion_census_degree9/points.tsv`;
its exact SHA256 is checked in `exact.py`. Python source requires only the
standard library (tested with CPython 3.11.2). Full verification takes about
7 seconds and 40 MiB of resident memory on the recorded host.

```sh
python3 verify.py
python3 controls.py
```

The deterministic result is [EXPECTED.json](EXPECTED.json). This check
establishes the residue colouring, the complete physical contact census,
the positive auxiliary witnesses, and the explicit mixed contact. The
auxiliary UNSAT assertion requires the separate proof check below.

To compare the square-root contact generator against a direct polynomial
scan of all 135,745,801 difference pairs:

```sh
hn_out=/tmp/hn-weighted-replay
python3 verify.py --emit "$hn_out"
g++ -std=c++17 -O3 -Wall -Wextra -Wconversion -pedantic direct_contacts.cpp -o "$hn_out/direct_contacts"
"$hn_out/direct_contacts" < "$hn_out/differences.txt" > "$hn_out/direct_contacts.txt"
python3 verify.py --audit "$hn_out/direct_contacts.txt"
```

GCC 12.2.0 was used. The direct audit takes about 0.5 seconds and returns
78 oriented directions; comparison is entrywise. A checking build was also
run on the entire input:

```sh
g++ -std=c++17 -O1 -g -fsanitize=undefined -fno-sanitize-recover=all -Wall -Wextra -Wconversion -pedantic direct_contacts.cpp -o "$hn_out/direct_contacts_ubsan"
"$hn_out/direct_contacts_ubsan" < "$hn_out/differences.txt" > "$hn_out/direct_contacts_ubsan.txt"
cmp "$hn_out/direct_contacts.txt" "$hn_out/direct_contacts_ubsan.txt"
```

To regenerate the auxiliary two-distance graph's binary DRAT proof, install
Kissat 4.0.4 and drat-trim, then run:

```sh
python3 certify_aux.py "$hn_out/aux-proof" --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

The wrapper requires solver exit 20, checker exit 0, and `s VERIFIED`.
It imposes 60-second subprocess timeouts; both tasks completed below one
second in the recorded run. Kissat source version was
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`. The installed drat-trim build
is identified by its executable SHA256 in VALIDATION.json. The generated
26,431-byte CNF has SHA256
`4f308ac0cc7ba3aecb51ae36464ec79eabf7af1f77f703ce925157bc4cb7e8f7`.
The recorded binary DRAT is 469,791 bytes, SHA256
`38b01d6feb39043deef0b3414294e8cfaf4cdf86e57f33bbcaebfdeee358fc17`.
Another solver may produce a different valid proof; the CNF and verification
status are the mathematical obligations, not a prescribed solver trajectory.

The source indices and positive colour words are compact committed
certificates. SAT discovery used python-sat 1.8.dev24 / CaDiCaL 1.9.5;
that package is not needed to verify the committed positive witnesses.
The original large physical graph and its SAT logs are omitted. The residue
colouring supersedes them as a substantially smaller proof.
