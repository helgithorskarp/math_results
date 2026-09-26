// Independent enumeration by four complete rows of selected-point weights.
#include <array>
#include <iostream>
#include <set>
#include <string>
#include <vector>

int main() {
    std::vector<std::array<int,5>> choices;
    for (int a=0; a<=3; ++a) for (int b=0; b<=4; ++b)
    for (int c=0; c<=4; ++c) for (int d=0; d<=4; ++d)
    for (int e=0; e<=4; ++e) {
        if (a+b+c+d+e==16) choices.push_back({a,b,c,d,e});
    }
    if (choices.size()!=35) return 2;
    std::array<int,25> weights{};
    std::array<int,5> sums{}, target{8,16,16,16,16};
    std::set<std::string> answers;
    auto visit = [&](auto&& self, int row) -> void {
        if (row==5) {
            for (int j=0; j<5; ++j) {
                weights[j]=target[j]-sums[j];
                if (weights[j]<0 || weights[j]>3) return;
            }
            if (weights[0]>1) return;
            for (int a=0; a<5; ++a) for (int b=0; b<5; ++b) {
                int size=0;
                for (int x=0; x<5; ++x) size+=weights[5*x+(a*x+b)%5];
                if (size>16) return;
            }
            std::string word;
            for (int weight : weights) word+=static_cast<char>('0'+weight);
            answers.insert(word);
            return;
        }
        for (const auto& choice : choices) {
            bool possible=true;
            for (int j=0; j<5; ++j) {
                if (sums[j]+choice[j]>target[j]) possible=false;
            }
            if (!possible) continue;
            for (int j=0; j<5; ++j) {
                weights[5*row+j]=choice[j];
                sums[j]+=choice[j];
            }
            self(self,row+1);
            for (int j=0; j<5; ++j) sums[j]-=choice[j];
        }
    };
    visit(visit,1);
    for (const auto& word : answers) std::cout << word << '\n';
    return answers.size()==4442 ? 0 : 1;
}
