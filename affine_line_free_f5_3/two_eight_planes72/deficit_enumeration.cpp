// Complete AA quotient enumeration by the 16 interior deficits.
#include <algorithm>
#include <array>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>

int main() {
    std::array<int,25> deficit{};
    std::array<int,4> row{}, col{};
    std::set<std::string> answers;
    auto visit = [&](auto&& self, int cell, int total) -> void {
        if (cell == 16) {
            if (total < 7 || total > 8) return;
            for (int i=0; i<4; ++i) {
                deficit[5*(i+1)] = 4-row[i];
                deficit[i+1] = 4-col[i];
            }
            deficit[0] = total-4;
            for (int a=0; a<5; ++a) for (int b=0; b<5; ++b) {
                int sum=0;
                for (int x=0; x<5; ++x) sum += deficit[5*x+(a*x+b)%5];
                if (sum < 4) return;
            }
            std::string word;
            for (int d : deficit) {
                if (d<0 || d>4) throw std::logic_error("invalid deficit");
                word += static_cast<char>('0'+4-d);
            }
            answers.insert(word);
            return;
        }
        const int i=cell/4, j=cell%4;
        const int upper=std::min({3-row[i],3-col[j],8-total});
        for (int d=0; d<=upper; ++d) {
            deficit[5*(i+1)+j+1]=d;
            row[i]+=d; col[j]+=d;
            self(self,cell+1,total+d);
            row[i]-=d; col[j]-=d;
        }
    };
    visit(visit,0,0);
    for (const auto& word : answers) std::cout << word << '\n';
    return answers.size()==4442 ? 0 : 1;
}
