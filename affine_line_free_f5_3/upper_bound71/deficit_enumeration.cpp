// Complete normalized AA, AB, BB catalogues, enumerated by interior deficits.
#include <algorithm>
#include <array>
#include <iostream>
#include <set>
#include <string>

int main() {
    constexpr std::array<int,5> A{12,4,4,4,4}, B{11,5,4,4,4};
    for (int type = 0; type < 3; ++type) {
        const auto R = type < 2 ? A : B, C = type == 0 ? A : B;
        const int minimum_total = 28-R[0]-C[0]+(type == 2 ? 2 : 3);
        const int maximum_total = 28-R[0]-C[0]+4;
        std::array<int,25> deficit{};
        std::array<int,5> rows{}, columns{};
        std::set<std::string> words;
        auto enumerate = [&](auto&& self, int position, int total) -> void {
            if (position == 16) {
                if (total < minimum_total || total > maximum_total) return;
                for (int i = 1; i < 5; ++i) {
                    deficit[5*i] = R[i]-rows[i];
                    deficit[i] = C[i]-columns[i];
                    if (deficit[5*i] < 1 || deficit[5*i] > 4
                        || deficit[i] < 1 || deficit[i] > 4) return;
                }
                deficit[0] = R[0]+C[0]-28+total;
                for (int slope = 0; slope < 5; ++slope)
                for (int offset = 0; offset < 5; ++offset) {
                    int sum = 0;
                    for (int x = 0; x < 5; ++x)
                        sum += deficit[5*x+(slope*x+offset)%5];
                    if (sum < 4) return;
                }
                std::string word;
                for (int d : deficit) word += static_cast<char>('0'+4-d);
                words.insert(word);
                return;
            }
            const int x = position/4+1, y = position%4+1;
            const int maximum = std::min({4, R[x]-1-rows[x], C[y]-1-columns[y],
                                         maximum_total-total});
            for (int d = 0; d <= maximum; ++d) {
                deficit[5*x+y] = d;
                rows[x] += d;
                columns[y] += d;
                self(self, position+1, total+d);
                rows[x] -= d;
                columns[y] -= d;
            }
        };
        enumerate(enumerate, 0, 0);
        for (const auto& word : words) std::cout << type << ' ' << word << '\n';
    }
}
