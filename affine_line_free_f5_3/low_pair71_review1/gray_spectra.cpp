// Independent planar-spectrum census for the 71-point low-plane review.
//
// The reviewed enumerator recomputes intersections of each subset with all
// line masks.  Here consecutive subsets follow Gray-code order and the six
// line occupancies through the toggled point are updated incrementally.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <set>
#include <vector>

namespace {

[[noreturn]] void fail(const char* message) {
    std::cerr << message << '\n';
    std::exit(1);
}

}  // namespace

int main() {
    std::vector<std::array<int, 5>> lines;
    // Five vertical lines and 25 lines y=a*x+b give AG(2,5) directly.
    for (int c = 0; c < 5; ++c) {
        std::array<int, 5> line{};
        for (int y = 0; y < 5; ++y) line[y] = 5*c+y;
        lines.push_back(line);
    }
    for (int a = 0; a < 5; ++a)
    for (int b = 0; b < 5; ++b) {
        std::array<int, 5> line{};
        for (int x = 0; x < 5; ++x) line[x] = 5*x+(a*x+b)%5;
        lines.push_back(line);
    }
    if (lines.size() != 30) fail("incorrect line count");
    std::set<std::array<int, 5>> distinct;
    for (auto line : lines) {
        std::sort(line.begin(), line.end());
        distinct.insert(line);
    }
    if (distinct.size() != 30) fail("duplicate planar lines");

    std::array<std::vector<int>, 25> incident{};
    for (int line = 0; line < 30; ++line)
        for (int point : lines[line]) incident[point].push_back(line);
    for (const auto& through_point : incident)
        if (through_point.size() != 6) fail("incorrect point-line degree");

    std::array<int, 30> occupancy{};
    std::array<std::uint64_t, 26> visited{};
    std::map<std::array<int, 6>, std::uint64_t> spectra;
    std::uint64_t valid17 = 0;
    std::uint32_t previous = 0;
    int size = 0;
    constexpr std::uint32_t limit = std::uint32_t{1} << 25;
    for (std::uint32_t index = 0; index < limit; ++index) {
        const std::uint32_t gray = index ^ (index >> 1);
        if (index != 0) {
            const std::uint32_t changed = gray ^ previous;
            if (std::popcount(changed) != 1) fail("Gray-code transition failure");
            const int point = std::countr_zero(changed);
            const int delta = (gray & changed) ? 1 : -1;
            size += delta;
            for (int line : incident[point]) occupancy[line] += delta;
        }
        previous = gray;
        ++visited[size];
        if (size < 7 || size > 17) continue;
        const int maximum = size <= 10 ? 3 : 4;
        std::array<int, 6> spectrum{};
        spectrum[0] = size;
        bool valid = true;
        for (int count : occupancy) {
            if (count < 0 || count > 5) fail("invalid line occupancy");
            if (count > maximum) {
                valid = false;
                break;
            }
            ++spectrum[count+1];
        }
        if (!valid) continue;
        if (size == 17) ++valid17;
        else ++spectra[spectrum];
    }

    std::uint64_t binomial = 1;
    for (int size_check = 0; size_check <= 25; ++size_check) {
        if (visited[size_check] != binomial) fail("subset-size coverage failure");
        if (size_check < 25)
            binomial = binomial*std::uint64_t(25-size_check)/std::uint64_t(size_check+1);
    }
    if (valid17 != 0) fail("unexpected line-free 17-subset");
    for (const auto& [spectrum, multiplicity] : spectra) {
        for (int value : spectrum) std::cout << value << ' ';
        std::cout << multiplicity << '\n';
    }
}
