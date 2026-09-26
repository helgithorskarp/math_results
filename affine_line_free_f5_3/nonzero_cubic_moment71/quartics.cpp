// Complete information-word enumeration over F_5, with coordinate-dependent
// allowed triples. Partial integer sums are <= 8*4*4=128 before reduction;
// stored residues are <=4 and their sums are <=8. No orbit quotient is used.
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>

int main() {
    std::array<std::array<int,15>,31> generator{};
    std::array<std::array<int,5>,31> allowed{};
    std::array<std::array<int,3>,15> bases{};
    for (auto& row : generator) for (int& v : row)
        if (!(std::cin >> v) || v<0 || v>4) return 2;
    for (auto& row : allowed) {
        int count = 0;
        for (int& v : row) {
            if (!(std::cin >> v) || (v!=0 && v!=1)) return 3;
            count += v;
        }
        if (count!=3) return 4;
    }
    for (auto& row : bases) {
        for (int& v : row) if (!(std::cin >> v) || v<0 || v>4) return 5;
        if (!(row[0]<row[1] && row[1]<row[2])) return 6;
    }
    int extra;
    if (std::cin >> extra) return 7;
    if (!std::cin.eof()) return 8;
    auto partial = [&](int start, int length) {
        int size = 1;
        for (int i=0; i<length; ++i) size *= 3;
        std::vector<std::array<uint8_t,31>> values(size);
        for (int code=0; code<size; ++code) {
            int remaining = code;
            std::array<int,15> word{};
            for (int i=0; i<length; ++i) {
                word[start+i] = bases[start+i][remaining%3];
                remaining /= 3;
            }
            for (int p=0; p<31; ++p) {
                int sum = 0;
                for (int i=start; i<start+length; ++i)
                    sum += generator[p][i]*word[i];
                values[code][p] = static_cast<uint8_t>(sum%5);
            }
        }
        return values;
    };
    const auto left = partial(0,7), right = partial(7,8);
    uint64_t tested = 0, retained = 0;
    for (const auto& a : left) for (const auto& b : right) {
        ++tested;
        bool valid = true;
        for (int p=0; p<31; ++p)
            if (!allowed[p][(a[p]+b[p])%5]) { valid = false; break; }
        if (!valid) continue;
        ++retained;
        for (int p=0; p<31; ++p)
            std::cout << static_cast<char>('0'+(a[p]+b[p])%5);
        std::cout << '\n';
    }
    if (tested!=14348907) return 9;
    std::cout << "COMPLETE " << tested << ' ' << retained << '\n';
}
