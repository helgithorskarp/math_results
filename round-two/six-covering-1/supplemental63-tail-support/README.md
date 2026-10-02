# Supplemental63 tail support:99..116

six-covering-1, researcher. See [proof.md](proof.md) for the precise finite resource model and ordinary proof. The30-resource relaxation permits one repeated63 label; the accompanying49-distinct-class fixture covers only the99-point tail support. It is not a full minimum-eight covering.

Reproduce with Python3.11 and a C++17 compiler (tested with g++12.2). Only standard libraries are needed. Keep compilation and checks serial; one numerical thread suffices.

```sh
mkdir -p build
g++ -std=c++17 -O3 -march=native -Wall -Wextra producer.cpp -o build/producer
g++ -std=c++17 -O3 -march=native -Wall -Wextra audit.cpp -o build/audit
python3 verify.py
python3 -O verify.py
```

Expected: upper116 proved by598500 complete coarse cases and1200 equality profiles with at least20 finer9 overlap loss; positive support99 directly verified in both the supplemental63 and49-distinct TOP models; all semantic damages rejected. Output is a compact JSON summary. These are same-author different algorithms, with an unformalized ordinary bridge and no independent verdict.

No solver, private file, network, campaign state, key or ledger is required. Build products stay in ignored `build/`. [positive.json](positive.json) and [certificate.json](certificate.json) are compact fixtures; `SHA256SUMS` binds the public text inputs. The current exactly-eight problem remains open.
