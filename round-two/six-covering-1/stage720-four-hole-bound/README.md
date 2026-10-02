# Conditional 99-hole bound for the owned period-720 stage

six-covering-1, researcher, 2026-10-02.

Every selection of the ORIGINAL divisor moduli of 720 at least 8,
containing `8:5` and `9:6` and covering everything outside `18:3` union
`4:0`, leaves at least **99 actual even target holes**. No stage witness
or arbitrary period-15120 exclusion is claimed. The application with
the existing 110-point seven-tail bound requires **99..110** even holes.

Read [proof.md](proof.md). [certificate.json](certificate.json) has all
block gain pairs and the complete exact convolution; it is compact data,
not a large phase corpus. The Python checker, separate literal C++ audit,
normal/optimized comparisons, semantic damages, and sanitizer controls
can be replayed with standard-library tools:

```sh
python3 verify.py --build-dir /tmp/six-covering-1-first99-build
```

Separate entry points:

```sh
python3 check.py
python3 -O check.py
python3 audit.py --build-dir /tmp/six-covering-1-first99-build
python3 -O audit.py --build-dir /tmp/six-covering-1-first99-build
python3 audit.py --build-dir /tmp/six-covering-1-first99-build --sanitized-controls
```

Author environment: CPython 3.11.2, g++ 12.2.0, C++17. Release flags:
`-O2 -std=c++17 -Wall -Wextra -Wpedantic`. Representative sanitizer flags:
`-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer` plus the same
standard and warning flags. Each child has a 20-second guard; all checks
run sequentially with numerical threads set to one. Generated binaries
belong in the supplied build directory and are excluded from publication.

Correctness still trusts the written finite reduction, these author
implementations, standard-library integer and bitset operations, and
the interpreter/compiler/runtime. No private input, solver, formal
kernel, external reviewer verdict, or incomplete enumeration is used.
The larger exploratory high-prefix probe was stopped at its internal
35-second guard and is not part of this proof or source bundle.
