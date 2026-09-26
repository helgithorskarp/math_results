// Independent direct-weight enumeration: choose rows 1..4, infer row zero.
#include <array>
#include <iostream>
#include <set>
#include <string>
#include <vector>

int main() {
    std::vector<std::array<int,5>> rows;
    for (int a = 0; a <= 3; ++a)
    for (int b = 0; b <= 4; ++b)
    for (int c = 0; c <= 4; ++c)
    for (int d = 0; d <= 4; ++d)
    for (int e = 0; e <= 4; ++e)
        if (a+b+c+d+e == 16) rows.push_back({a,b,c,d,e});
    if (rows.size() != 35) return 2;
    constexpr std::array<int,5> columns{9,15,16,16,16};
    std::array<int,25> weight{};
    std::array<int,5> sums{};
    std::set<std::string> words;
    auto enumerate = [&](auto&& self, int r) -> void {
        if (r == 5) {
            int first_sum = 0;
            for (int j = 0; j < 5; ++j) {
                weight[j] = columns[j] - sums[j];
                if (weight[j] < 0 || weight[j] > 3) return;
                first_sum += weight[j];
            }
            if (first_sum != 8 || weight[0] > 1) return;
            for (int slope = 0; slope < 5; ++slope)
            for (int offset = 0; offset < 5; ++offset) {
                int line_sum = 0;
                for (int x = 0; x < 5; ++x)
                    line_sum += weight[5*x+(slope*x+offset)%5];
                if (line_sum > 16) return;
            }
            std::string word;
            for (int w : weight) word += static_cast<char>('0'+w);
            words.insert(word);
            return;
        }
        for (const auto& row : rows) {
            bool possible = true;
            for (int j = 0; j < 5; ++j)
                if (sums[j]+row[j] > columns[j]) possible = false;
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
    for (const auto& word : words) std::cout << word << '\n';
}
