// Independent direct-weight enumeration: choose four rows, infer the zero row.
#include <array>
#include <iostream>
#include <set>
#include <string>
#include <vector>

int main() {
    std::array<std::vector<std::array<int,5>>,17> rows;
    for (int a = 0; a <= 3; ++a)
    for (int b = 0; b <= 4; ++b)
    for (int c = 0; c <= 4; ++c)
    for (int d = 0; d <= 4; ++d)
    for (int e = 0; e <= 4; ++e) {
        const int sum = a+b+c+d+e;
        if (sum == 15 || sum == 16) rows[sum].push_back({a,b,c,d,e});
    }
    constexpr std::array<int,5> A{8,16,16,16,16}, B{9,15,16,16,16};
    for (int type = 0; type < 3; ++type) {
        const auto R = type < 2 ? A : B, C = type == 0 ? A : B;
        std::array<int,25> weight{};
        std::array<int,5> sums{};
        std::set<std::string> words;
        auto enumerate = [&](auto&& self, int r) -> void {
            if (r == 5) {
                int total = 0;
                for (int j = 0; j < 5; ++j) {
                    weight[j] = C[j]-sums[j];
                    if (weight[j] < 0 || weight[j] > 3) return;
                    total += weight[j];
                }
                if (total != R[0] || weight[0] > (type == 2 ? 2 : 1)) return;
                for (int slope = 0; slope < 5; ++slope)
                for (int offset = 0; offset < 5; ++offset) {
                    int sum = 0;
                    for (int x = 0; x < 5; ++x)
                        sum += weight[5*x+(slope*x+offset)%5];
                    if (sum > 16) return;
                }
                std::string word;
                for (int w : weight) word += static_cast<char>('0'+w);
                words.insert(word);
                return;
            }
            for (const auto& row : rows[R[r]]) {
                bool possible = true;
                for (int j = 0; j < 5; ++j)
                    if (sums[j]+row[j] > C[j]) possible = false;
                if (!possible) continue;
                for (int j = 0; j < 5; ++j) {
                    weight[5*r+j] = row[j];
                    sums[j] += row[j];
                }
                self(self, r+1);
                for (int j = 0; j < 5; ++j) sums[j] -= row[j];
            }
        };
        enumerate(enumerate, 1);
        for (const auto& word : words) std::cout << type << ' ' << word << '\n';
    }
}
