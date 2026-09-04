#!/usr/bin/env python3
"""Compare every production canonical-table entry to explicit injections.

Uses a temporary C++ harness that includes the actual census source.  Binary
table rows are streamed through a pipe, never saved as a generated artifact.
The ordinary verify.py checks supply source pins and the geometric census.
"""
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import sys
import tempfile

from verify import (
    canonical_colour_partition,
    explicit_injection_compatibility_rows,
    restricted_growth_partitions,
)

HERE = Path(__file__).resolve().parent
HARNESS = r'''
// The renamed, unused program entry no longer has main's implicit return.
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wreturn-type"
#define main census_main
#include CENSUS_SOURCE
#undef main
#pragma GCC diagnostic pop

static void write_integer(std::uint64_t value, unsigned bytes) {
    for (unsigned i = 0; i < bytes; ++i) {
        std::cout.put(static_cast<char>((value >> (8 * i)) & 255U));
    }
}

template <std::size_t N> static void emit_table() {
    const auto table = make_canonical_compatibility_table<N>();
    for (auto rank : table.rank_by_raw_pattern) write_integer(rank, 2);
    for (const auto& row : table.compatible) {
        for (auto word : row) write_integer(word, 8);
    }
}

int main() {
    emit_table<7>();
    emit_table<8>();
    emit_table<9>();
    return std::cout ? 0 : 1;
}
'''


def check_stream(stream):
    digest = sha256()

    def read_exact(size):
        data = stream.read(size)
        if len(data) != size:
            raise ValueError("truncated C++ table stream")
        digest.update(data)
        return data

    for labels, expected_size, expected_pairs in (
        (7, 715, 124925), (8, 2795, 1544844), (9, 11051, 19185603)
    ):
        # Match production rank order: increasing packed 2-bit colour string.
        def packed(row):
            return sum(colour << (2 * position)
                       for position, colour in enumerate(row))

        representatives = sorted(restricted_growth_partitions(labels), key=packed)
        if len(representatives) != expected_size:
            raise ValueError("partition count mismatch")
        ranks = {row: rank for rank, row in enumerate(representatives)}
        raw_count = 4 ** labels
        encoded_ranks = read_exact(2 * raw_count)
        for raw in range(raw_count):
            pattern = tuple((raw >> (2 * position)) & 3
                            for position in range(labels))
            expected_rank = ranks[canonical_colour_partition(pattern)]
            actual_rank = int.from_bytes(encoded_ranks[2 * raw:2 * raw + 2], "little")
            if actual_rank != expected_rank:
                raise ValueError(f"rank mismatch: labels={labels} raw={raw}")

        pair_count = 0
        row_bytes = 8 * ((expected_size + 63) // 64)
        for rank, expected in enumerate(explicit_injection_compatibility_rows(
            representatives
        )):
            actual = int.from_bytes(read_exact(row_bytes), "little")
            if actual != expected:
                raise ValueError(f"compatibility mismatch: labels={labels} rank={rank}")
            pair_count += actual.bit_count()
        if pair_count != expected_pairs:
            raise ValueError("compatible-pair count mismatch")
        print(f"labels={labels} raw_ranks={raw_count} partitions={expected_size} "
              f"checked_entries={expected_size ** 2} compatible_pairs={pair_count}")
    if stream.read(1):
        raise ValueError("unexpected trailing C++ table bytes")
    print(f"canonical_table_stream_sha256={digest.hexdigest()}")


def main():
    if len(sys.argv) != 1:
        raise ValueError("usage: python3 check_compatibility.py")
    source = HARNESS.replace("CENSUS_SOURCE", json.dumps(str(HERE / "census.cpp")))
    with tempfile.TemporaryDirectory(prefix="parts-compatibility-") as directory:
        temporary = Path(directory)
        harness = temporary / "check.cpp"
        executable = temporary / "check"
        harness.write_text(source)
        subprocess.run(["g++", "-std=c++20", "-O3", "-Wall", "-Wextra",
                        str(harness), "-o", str(executable)], check=True)
        process = subprocess.Popen([str(executable)], stdout=subprocess.PIPE)
        try:
            check_stream(process.stdout)
            if process.wait() != 0:
                raise ValueError("C++ table generator failed")
        finally:
            process.stdout.close()
            if process.poll() is None:
                process.terminate()
                process.wait()
    print("all_canonical_table_entries_match_explicit_injections=true")


if __name__ == "__main__":
    main()
