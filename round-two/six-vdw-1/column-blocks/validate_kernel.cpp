#include "block12.hpp"
#include <iostream>
#include <random>

int main() {
    const auto reject=[](auto action) {
        try { action(); } catch(const std::invalid_argument&) { return; }
        throw std::runtime_error("invalid kernel input accepted");
    };
    for(const auto rs:std::array<std::array<int,2>,4>{{{{0,2}},{{1,2}},{{2,617}},{{2,2}}}})
        reject([&](){vdw::Block12 invalid(rs[0],rs[1]);});
    vdw::Block12 valid(2,3);
    reject([&](){valid.evaluate(4096);});
    std::array<int,12> edited{};
    reject([&](){valid.minimum({2,0},{30,35},edited);});
    reject([&](){valid.minimum({0,1},{-1,35},edited);});
    reject([&](){valid.minimum({0,1},{30,35},edited,4096);});
    edited[0]=2;
    reject([&](){valid.minimum({0,1},{30,35},edited);});
    std::mt19937 rng(20261001U);
    std::cout<<'[';
    for(int trial=0;trial<120;++trial) {
        vdw::Block12 model(2,3);
        for(auto& a:model.linear) a={static_cast<int>(rng()%41)-20,static_cast<int>(rng()%101)-50};
        for(auto& row:model.cross) for(auto& a:row)
            a={static_cast<int>(rng()%11)-5,static_cast<int>(rng()%31)-15};
        const std::array<int,2> classes{(trial/2)%2,trial%2};
        const std::array<int,2> outside{25+static_cast<int>(rng()%16),25+static_cast<int>(rng()%16)};
        std::array<int,12> edited{}; for(auto& e:edited) e=static_cast<int>(rng()%2);
        const unsigned allowed=trial%3==0?4095U:(trial%3==1?0U:rng()%4096);
        const auto result=model.minimum(classes,outside,edited,allowed);
        unsigned seen=0;
        model.all([&](unsigned mask,vdw::Cost cost) {
            const auto direct=model.evaluate(mask);
            if(direct.raw!=cost.raw || direct.weighted!=cost.weighted)
                throw std::runtime_error("Gray-code mismatch");
            ++seen;
        });
        if(seen!=4096) throw std::runtime_error("Gray-code coverage");
        if(trial) std::cout<<',';
        std::cout<<"{\"classes\":["<<classes[0]<<','<<classes[1]<<"],\"outside\":["
                 <<outside[0]<<','<<outside[1]<<"],\"edited\":[";
        for(int i=0;i<12;++i) { if(i) std::cout<<','; std::cout<<edited[i]; }
        std::cout<<"],\"allowed\":"<<allowed<<",\"linear\":[";
        for(int i=0;i<12;++i) { if(i) std::cout<<','; std::cout<<'['<<model.linear[i].raw<<','<<model.linear[i].weighted<<']'; }
        std::cout<<"],\"cross\":[";
        for(int i=0;i<6;++i) {
            if(i) std::cout<<',';
            std::cout<<'[';
            for(int j=0;j<6;++j) { if(j) std::cout<<','; std::cout<<'['<<model.cross[i][j].raw<<','<<model.cross[i][j].weighted<<']'; }
            std::cout<<']';
        }
        std::cout<<"],\"feasible\":"<<(result.feasible?"true":"false")
                 <<",\"mask\":"<<result.mask<<",\"minimum\":["<<result.value.raw<<','<<result.value.weighted<<"]}";
    }
    std::cout<<"]\n";
}
