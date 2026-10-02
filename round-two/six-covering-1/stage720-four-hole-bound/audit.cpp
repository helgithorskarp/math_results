#include <algorithm>
#include <array>
#include <bitset>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Mask = std::bitset<720>;
using Gain = std::pair<int, int>;
const std::vector<std::vector<int>> groups = {
    {10,12,15,16,18,20}, {24,30}, {36,40}, {45,48}, {60,72},
    {80,90}, {120,144}, {180,240}, {360,720}
};

void need(bool ok, const std::string& message) {
    if (!ok) throw std::runtime_error(message);
}

struct Data {
    Mask compulsory, even;
    std::array<std::vector<Mask>,721> phase;
    std::vector<int> labels;
    Data() {
        for (int x=0; x<720; ++x) {
            if (x%8!=5 && x%9!=6 && x%18!=3 && x%4!=0) compulsory.set(x);
            if (x%4==0 && x%9!=6) even.set(x);
        }
        need(compulsory.count()==370 && even.count()==160 && (compulsory&even).none(),
             "literal physical compulsory/even domain");
        int total_incidence=0;
        for (int m=8; m<=720; ++m) {
            if (720%m!=0 || m==8 || m==9) continue;
            labels.push_back(m);
            total_incidence+=720/m;
            phase[m].resize(m);
            for (int a=0; a<m; ++a)
                for (int x=a; x<720; x+=m) phase[m][a].set(x);
        }
        need(labels.size()==22 && total_incidence<=720, "DP integer bound");
        std::vector<int> inventory;
        for (const auto& group: groups)
            inventory.insert(inventory.end(),group.begin(),group.end());
        std::sort(inventory.begin(),inventory.end());
        need(inventory==labels,"ORIGINAL disjoint resource partition");
    }
};

void visit(const Data& d, const std::vector<int>& group, std::size_t position, const Mask& union_mask,
           std::array<std::array<bool,161>,371>& present, std::uint64_t& visits) {
    if (position==group.size()) {
        const auto f=(union_mask&d.compulsory).count();
        const auto s=(union_mask&d.even).count();
        need(f<=370 && s<=160,"physical gain bounds");
        present[f][s]=true;
        ++visits;
        return;
    }
    for (const auto& phase: d.phase[group[position]])
        visit(d,group,position+1,union_mask|phase,present,visits);
}

void controls(const Data& d) {
    std::uint64_t phase_points=0, pair_points=0;
    for (int m: d.labels)
        for (int a=0; a<m; ++a)
            for (int x=0; x<720; ++x) {
                need(d.phase[m][a].test(x)==(x%m==a), "literal phase predicate control");
                ++phase_points;
            }
    for (int a=0; a<24; ++a)
        for (int b=0; b<30; ++b) {
            const auto mask=d.phase[24][a]|d.phase[30][b];
            int f=0,s=0;
            for (int x=0; x<720; ++x) {
                const bool hit=x%24==a || x%30==b;
                f+=static_cast<int>(hit && x%8!=5 && x%9!=6 && x%18!=3 && x%4!=0);
                s+=static_cast<int>(hit && x%4==0 && x%9!=6);
                ++pair_points;
            }
            need(static_cast<int>((mask&d.compulsory).count())==f &&
                 static_cast<int>((mask&d.even).count())==s,"per-point ORIGINAL pair gain control");
        }
    std::cout << "CONTROLS " << phase_points << ' ' << pair_points << '\n';
}

int main(int argc, char** argv) {
    try {
        const Data d;
        if (argc==2 && std::string(argv[1])=="controls") {
            controls(d);
            return 0;
        }
        need(argc==1,"unexpected arguments");
        std::vector<std::vector<Gain>> tables;
        std::cout << "SPLIT 370 160\n";
        for (const auto& group: groups) {
            std::array<std::array<bool,161>,371> present{};
            std::uint64_t visits=0, expected=1;
            for (int m: group) expected*=static_cast<std::uint64_t>(m);
            visit(d,group,0,Mask{},present,visits);
            need(visits==expected,"incomplete all-ORIGINAL-phase product");
            std::vector<Gain> gains;
            for (int f=0; f<=370; ++f)
                for (int s=0; s<=160; ++s)
                    if (present[f][s]) gains.emplace_back(f,s);
            tables.push_back(gains);
            std::cout << "GROUP " << group.size();
            for (int m: group) std::cout << ' ' << m;
            std::cout << ' ' << visits << ' ' << gains.size() << '\n';
            for (const auto& p: gains) std::cout << p.first << ' ' << p.second << '\n';
        }
        // No Pareto deletion, no phase-mask deduplication. Full gain table
        // convolution, exact integer arithmetic, including all f>=370.
        std::array<int,721> dp;
        dp.fill(-1);
        dp[0]=0;
        for (const auto& gains: tables) {
            std::array<int,721> next;
            next.fill(-1);
            for (int f=0; f<=720; ++f) {
                if (dp[f]<0) continue;
                for (const auto& p: gains) {
                    need(f+p.first<=720 && dp[f]+p.second<=720,"bounded DP sum");
                    next[f+p.first]=std::max(next[f+p.first],dp[f]+p.second);
                }
            }
            dp=next;
        }
        int count=0, maximum=-1;
        for (int f=0; f<=720; ++f) {
            if (dp[f]>=0) ++count;
            if (f>=370) maximum=std::max(maximum,dp[f]);
        }
        need(maximum==61,"conditional gain bound differs");
        std::cout << "DP " << count << '\n';
        for (int f=0; f<=720; ++f)
            if (dp[f]>=0) std::cout << f << ' ' << dp[f] << '\n';
        std::cout << "BOUND " << maximum << ' ' << 160-maximum << '\n';
        return 0;
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
}
