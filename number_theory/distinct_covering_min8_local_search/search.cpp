// Heuristic weighted local search. Failure establishes no exclusion.
// six-covering-1, researcher. One thread; all witnesses require literal audit.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

int main(int argc, char** argv) {
    if (argc != 6) throw std::runtime_error("period seconds seed input.tsv output.tsv");
    const int L = std::stoi(argv[1]);
    const double seconds = std::stod(argv[2]);
    if (L < 8 || L > 100000 || seconds <= 0 || seconds > 50)
        throw std::runtime_error("outside declared bounds");
    std::mt19937_64 rng(std::stoull(argv[3]));
    std::vector<int> moduli, phases;
    for (int m=8; m<=L; ++m) if (L%m==0) moduli.push_back(m);
    if (moduli.size() >= 60000) throw std::runtime_error("count overflow bound");
    phases.assign(moduli.size(), -1);
    std::ifstream input(argv[4]);
    if (!input) throw std::runtime_error("seed read failed");
    int a, m;
    while (input >> a >> m) {
        if (m < 8) continue;
        auto it = std::lower_bound(moduli.begin(), moduli.end(), m);
        if (a < 0 || a >= m) throw std::runtime_error("seed phase invalid");
        if (it == moduli.end() || *it != m) continue;
        phases[static_cast<std::size_t>(it-moduli.begin())] = a;
    }
    std::vector<std::uint16_t> covered(static_cast<std::size_t>(L), 0);
    std::vector<std::uint32_t> weight(static_cast<std::size_t>(L), 1);
    for (std::size_t i=0; i<moduli.size(); ++i) if (phases[i]>=0)
        for (int x=phases[i]; x<L; x+=moduli[i]) ++covered[static_cast<std::size_t>(x)];
    for (std::size_t i=0; i<moduli.size(); ++i) if (phases[i]<0) {
        std::vector<int> histogram(static_cast<std::size_t>(moduli[i]), 0);
        for (int x=0; x<L; ++x) if (!covered[static_cast<std::size_t>(x)])
            ++histogram[static_cast<std::size_t>(x%moduli[i])];
        int maximum=*std::max_element(histogram.begin(),histogram.end());
        std::vector<int> choices;
        for (int r=0;r<moduli[i];++r) if(histogram[static_cast<std::size_t>(r)]==maximum) choices.push_back(r);
        phases[i]=choices[rng()%choices.size()];
        for (int x=phases[i];x<L;x+=moduli[i]) ++covered[static_cast<std::size_t>(x)];
    }
    std::vector<int> holes, position(static_cast<std::size_t>(L),-1);
    for (int x=0;x<L;++x) if(!covered[static_cast<std::size_t>(x)]) {
        position[static_cast<std::size_t>(x)]=static_cast<int>(holes.size()); holes.push_back(x);
    }
    const auto start=std::chrono::steady_clock::now();
    const auto elapsed=[&](){return std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();};
    auto best_phases=phases;
    std::size_t best=holes.size();
    std::uint64_t iteration=0;
    std::cerr<<"initial holes="<<holes.size()<<" classes="<<moduli.size()<<"\n";
    auto remove=[&](int x){
        auto ix=static_cast<std::size_t>(x);
        if (!covered[ix]) throw std::runtime_error("invalid decrement");
        if (--covered[ix]==0) {position[ix]=static_cast<int>(holes.size()); holes.push_back(x);}
    };
    auto add=[&](int x){
        auto ix=static_cast<std::size_t>(x);
        if (covered[ix]++==0) {
            int pos=position[ix];
            if(pos<0 || static_cast<std::size_t>(pos)>=holes.size() || holes[static_cast<std::size_t>(pos)]!=x)
                throw std::runtime_error("bad hole index");
            int last=holes.back(); holes[static_cast<std::size_t>(pos)]=last;
            position[static_cast<std::size_t>(last)]=pos;
            holes.pop_back(); position[ix]=-1;
        }
    };
    // At most 200000 penalties: each weight<=200001 and each score has
    // magnitude<=L*200001<=20000100000, within signed 64-bit arithmetic.
    while(!holes.empty() && iteration<200000 && elapsed()<seconds) {
        ++iteration;
        int point=holes[rng()%holes.size()];
        std::int64_t top=INT64_MIN;
        std::vector<std::size_t> choices;
        for (std::size_t i=0;i<moduli.size();++i) {
            int next=point%moduli[i];
            if(next==phases[i]) throw std::runtime_error("a hole is covered");
            std::int64_t score=0;
            for(int x=next;x<L;x+=moduli[i]) if(!covered[static_cast<std::size_t>(x)]) score+=weight[static_cast<std::size_t>(x)];
            for(int x=phases[i];x<L;x+=moduli[i]) if(covered[static_cast<std::size_t>(x)]==1) score-=weight[static_cast<std::size_t>(x)];
            if(score>top) {top=score; choices.clear();}
            if(score==top) choices.push_back(i);
        }
        std::size_t chosen=choices[rng()%choices.size()];
        if(top<=0) for(int x:holes) ++weight[static_cast<std::size_t>(x)];
        if(rng()%100<8) chosen=rng()%moduli.size();
        int next=point%moduli[chosen];
        for(int x=phases[chosen];x<L;x+=moduli[chosen]) remove(x);
        phases[chosen]=next;
        for(int x=phases[chosen];x<L;x+=moduli[chosen]) add(x);
        if(holes.size()<best) {
            best=holes.size(); best_phases=phases;
            std::cerr<<"best="<<best<<" iterations="<<iteration<<" seconds="<<elapsed()<<"\n";
        }
    }
    if(best==0) {
        std::vector<unsigned int> literal(static_cast<std::size_t>(L),0);
        for(std::size_t i=0;i<moduli.size();++i)
            for(int x=best_phases[i];x<L;x+=moduli[i]) ++literal[static_cast<std::size_t>(x)];
        if(std::any_of(literal.begin(),literal.end(),[](unsigned int c){return c==0;}))
            throw std::runtime_error("invalid decoded witness");
    }
    std::ofstream output(argv[5]);
    if(!output) throw std::runtime_error("output write failed");
    for(std::size_t i=0;i<moduli.size();++i) output<<best_phases[i]<<'\t'<<moduli[i]<<'\n';
    std::cout<<"status="<<(best==0?"WITNESS":"INCONCLUSIVE")<<" best_holes="<<best
             <<" iterations="<<iteration<<" seconds="<<elapsed()<<"\n";
    return best==0 ? 0 : 2;
}
