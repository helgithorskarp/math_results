# Tuza's conjecture for every two-neighborhood split graph

**Claim:** if a finite simple graph has a specified split partition whose
triangle-active independent vertices have at most two distinct clique
neighborhoods, then `tau(G) <= 2 nu(G)`. All clique orders and all
multiplicities are covered. Neighborhoods need not be nested.

**Status:** complete computer-assisted author proof; independent peer review
and formal verification pending. This does not settle unrestricted split
graphs or the general Tuza conjecture.

[PROOF.md](PROOF.md) supplies the finite reduction, packing and cover bounds,
coverage proof, arithmetic bounds and trust boundary. The new finite closure
joins the existing large-order theorem, restated and attributed in
[LARGE_ORDER.md](LARGE_ORDER.md). [SOURCES.md](SOURCES.md) records provenance.

From this directory, using a C++20 compiler and Python 3.11+:

```sh
mkdir -p build
g++ -std=c++20 -O3 -Wall -Wextra -Wconversion -Wshadow -pedantic verify_rectangles.cpp -o build/rectangles
g++ -std=c++20 -O3 -Wall -Wextra -Wconversion -Wshadow -pedantic verify_literal.cpp -o build/literal
./build/rectangles > actual.txt
./build/literal > actual_literal.txt
diff -u EXPECTED.txt actual.txt
diff -u EXPECTED_LITERAL.txt actual_literal.txt
python3 audit.py ./build/rectangles actual.txt actual_literal.txt > actual_audit.txt
diff -u AUDIT.json actual_audit.txt
sha256sum -c SHA256SUMS
```

Both full runs cover **3,642,650 shapes and 7,636,614,579 parameter tuples**,
with zero failures. They use different enumerations and cut calculations.
The first certifies 11,301,625 monotonicity rectangles; the second certifies
12,157,453. The reports contain a separate completeness count for every
clique order from 3 through 112. Clique orders at least 113 are covered by
the analytic bridge, and orders at most two are immediate.

`audit.py` independently checks the domain counts and compares all 3,402
small tuples entry by entry against rational arithmetic and literal cuts.
It checks actual matching choices on 876 tuples, constructs and validates
triangle packings on 384 complete small graphs, and includes invalid-input
and boundary controls. Expected status: `VERIFIED`. Both C++ programs and
the audit use standard libraries only. No solver or external data is needed.

Tested with GCC 12.2.0 (Debian 12.2.0-14+deb12u1), C++20, and CPython 3.11.2
on Linux x86-64. The full optimized first run took approximately 1.5 seconds;
the literal run took approximately 57.2 seconds, each single-threaded. The
Python runner reported process-family peak RSS below 11 MiB. Performance is
host-dependent. Both C++ programs also passed address/undefined-behavior
sanitizer builds through order 16:

```sh
g++ -std=c++20 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer verify_rectangles.cpp -o build/rectangles_san
./build/rectangles_san 16
g++ -std=c++20 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer verify_literal.cpp -o build/literal_san
./build/literal_san 16
```

Optional `./build/rectangles --dump 8` emits the 3,402 scalar cases used by
the Python audit. Its SHA-256 is
`fd78f7ea2ebd7bbf355fc251f24586e1674ded1d11bfcea46f1e9a380fc4c1d4`.
No dump, binary, cache, or large certificate is part of the publication.
The independent checker is a second implementation by the same author,
not a claim of independent peer review.
