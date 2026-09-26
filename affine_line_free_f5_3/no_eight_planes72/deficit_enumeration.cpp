// Complete mixed 8/9-plane projection enumeration using interior deficits.
#include <algorithm>
#include <array>
#include <iostream>
#include <set>
#include <string>

int main() {
    constexpr std::array<int,5> R{12,4,4,4,4}, C{11,5,4,4,4};
    std::array<int,25> deficit{};
    std::array<int,5> row_sum{}, col_sum{};
    std::set<std::string> words;
    auto enumerate = [&](auto&& self, int position, int total) -> void {
        if (position == 16) {
            if (total < 8 || total > 9) return;
            for (int i = 1; i < 5; ++i) {
                deficit[5*i] = R[i] - row_sum[i];
                deficit[i] = C[i] - col_sum[i];
                if (deficit[5*i] < 1 || deficit[5*i] > 4
                    || deficit[i] < 1 || deficit[i] > 4) return;
            }
            deficit[0] = total - 5;
            for (int slope = 0; slope < 5; ++slope)
            for (int offset = 0; offset < 5; ++offset) {
                int line_sum = 0;
                for (int x = 0; x < 5; ++x)
                    line_sum += deficit[5*x+(slope*x+offset)%5];
                if (line_sum < 4) return;
            }
            std::string word;
            for (int d : deficit) word += static_cast<char>('0'+4-d);
            words.insert(word);
            return;
        }
        const int x = position/4+1, y = position%4+1;
        const int maximum = std::min({4, R[x]-1-row_sum[x],
                                     C[y]-1-col_sum[y], 9-total});
        for (int d = 0; d <= maximum; ++d) {
            deficit[5*x+y] = d;
            row_sum[x] += d;
            col_sum[y] += d;
            self(self, position+1, total+d);
            row_sum[x] -= d;
            col_sum[y] -= d;
        }
    };
    enumerate(enumerate, 0, 0);
    for (const auto& word : words) std::cout << word << '\n';
}
