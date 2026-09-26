// Exhaust all 3^15 residue-valued information words for ternary quartics.
// Input: a 31-by-15 F_5 evaluation map with a verified identity minor.
// Output: every retained 31-symbol word, followed by complete counters.
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>

int main() {
    std::array<std::array<int,15>,31> generator{};
    for (auto& row : generator)
        for (int& value : row)
            if (!(std::cin >> value) || value < 0 || value > 4) return 2;
    int extra;
    if (std::cin >> extra) return 3;
    if (!std::cin.eof()) return 4;

    auto partial_values = [&](int start, int length) {
        int size = 1;
        for (int i=0; i<length; ++i) size *= 3;
        std::vector<std::array<uint8_t,31>> result(size);
        constexpr std::array<int,3> values{0,1,4};
        for (int code=0; code<size; ++code) {
            int remaining = code;
            std::array<int,15> word{};
            for (int i=0; i<length; ++i) {
                word[start+i] = values[remaining%3];
                remaining /= 3;
            }
            for (int p=0; p<31; ++p) {
                int sum = 0;
                for (int i=0; i<length; ++i)
                    sum += generator[p][start+i]*word[start+i];
                result[code][p] = static_cast<uint8_t>(sum%5);
            }
        }
        return result;
    };

    const auto left = partial_values(0,7), right = partial_values(7,8);
    uint64_t visited = 0, retained = 0;
    for (const auto& first : left) for (const auto& second : right) {
        ++visited;
        bool allowed = true;
        for (int p=0; p<31; ++p) {
            const int value = (first[p]+second[p])%5;
            if (value == 2 || value == 3) { allowed = false; break; }
        }
        if (!allowed) continue;
        ++retained;
        for (int p=0; p<31; ++p)
            std::cout << static_cast<char>('0'+(first[p]+second[p])%5);
        std::cout << '\n';
    }
    if (visited != 14348907) return 5;
    std::cout << "COMPLETE " << visited << ' ' << retained << '\n';
}
