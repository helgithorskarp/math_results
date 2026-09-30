// Independent complete permutation scan: no partial-word or recursive pruning.
#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
using Mask=unsigned int;
using Clock=std::chrono::steady_clock;

std::vector<int> positions(Mask w) {
    std::vector<int> p;
    for(int z=0;z<18;++z) if((w>>z)&1U) p.push_back(z);
    return p;
}

int main(int argc,char** argv) {
    try {
        if(argc!=3)throw std::runtime_error("usage: brute INPUT OUTPUT");
        std::ifstream input(argv[1]);std::ofstream output(argv[2]);
        if(!input||!output)throw std::runtime_error("input/output unavailable");
        int count;if(!(input>>count)||count!=3)throw std::runtime_error("expected three templates");
        std::vector<std::vector<Mask>> templates(3,std::vector<Mask>(20));
        for(auto& star:templates)for(auto& word:star) {
            if(!(input>>word)||word>=(1U<<17)||__builtin_popcount(word)!=4)
                throw std::runtime_error("invalid word");
        }
        std::string extra;if(input>>extra)throw std::runtime_error("trailing input");
        for(int f=0;f<3;++f)for(int s=0;s<3;++s) {
            std::vector<Mask> fixed;for(Mask w:templates[f])fixed.push_back(w|(1U<<17));
            std::vector<std::vector<int>> target_triples,source_triples;
            Mask target_union=0,source_union=0;
            for(Mask w:templates[f])if(w&1U) {target_triples.push_back(positions(w^1U));target_union|=w^1U;}
            for(Mask w:templates[s])if(w&1U) {source_triples.push_back(positions(w^1U));source_union|=w^1U;}
            std::sort(target_triples.begin(),target_triples.end());std::sort(source_triples.begin(),source_triples.end());
            if(source_triples.size()!=3||target_triples.size()!=3||
               __builtin_popcount(source_union)!=9||__builtin_popcount(target_union)!=9)
                throw std::runtime_error("invalid common triple partition");
            std::vector<int> source_free,target_free;
            for(int z=1;z<17;++z) {
                if(!((source_union>>z)&1U))source_free.push_back(z);
                if(!((target_union>>z)&1U))target_free.push_back(z);
            }
            if(source_free.size()!=7||target_free.size()!=7)throw std::runtime_error("invalid free domain");
            std::vector<std::array<int,4>> constraints;
            for(Mask w:templates[s])if(!(w&1U)) {
                auto p=positions(w);constraints.push_back({p[0],p[1],p[2],p[3]});
            }
            if(constraints.size()!=17)throw std::runtime_error("wrong constraint count");
            std::set<std::vector<Mask>> stars;
            std::array<int,17> labels{};labels[0]=17;
            std::array<int,3> order{0,1,2};
            unsigned long long anchors=0,scanned=0,accepted=0;
            do {
                auto a=target_triples[order[0]];
                do {
                    auto b=target_triples[order[1]];
                    do {
                        auto c=target_triples[order[2]];
                        do {
                            ++anchors;
                            for(int j=0;j<3;++j) {
                                labels[source_triples[0][j]]=a[j];labels[source_triples[1][j]]=b[j];
                                labels[source_triples[2][j]]=c[j];
                            }
                            auto free_order=target_free;
                            unsigned long long anchor_scanned=0;auto started=Clock::now();
                            do {
                                ++scanned;++anchor_scanned;
                                if(anchor_scanned>200000ULL||((anchor_scanned&255ULL)==0&&
                                    std::chrono::duration<double>(Clock::now()-started).count()>10.0))
                                    throw std::runtime_error("INCOMPLETE brute transport node/time guard");
                                for(int j=0;j<7;++j)labels[source_free[j]]=free_order[j];
                                bool valid=true;
                                for(const auto& p:constraints) {
                                    Mask image=1U|(1U<<labels[p[0]])|(1U<<labels[p[1]])|
                                        (1U<<labels[p[2]])|(1U<<labels[p[3]]);
                                    for(Mask w:fixed)if(__builtin_popcount(w&image)>2) {valid=false;break;}
                                    if(!valid)break;
                                }
                                if(!valid)continue;
                                ++accepted;std::vector<Mask> star;
                                for(Mask w:templates[s]) {
                                    Mask image=1U;
                                    for(int z:positions(w))image|=1U<<labels[z];
                                    star.push_back(image);
                                }
                                std::sort(star.begin(),star.end());stars.insert(star);
                                if(stars.size()>100000U)throw std::runtime_error("INCOMPLETE brute output guard");
                            } while(std::next_permutation(free_order.begin(),free_order.end()));
                            if(anchor_scanned!=5040ULL)throw std::runtime_error("missing free permutation");
                        } while(std::next_permutation(c.begin(),c.end()));
                    } while(std::next_permutation(b.begin(),b.end()));
                } while(std::next_permutation(a.begin(),a.end()));
            } while(std::next_permutation(order.begin(),order.end()));
            if(anchors!=1296ULL||scanned!=6531840ULL)throw std::runtime_error("incomplete full transport scan");
            output<<"{\"first\":"<<f<<",\"second\":"<<s<<",\"anchors\":"<<anchors
                  <<",\"scanned\":"<<scanned<<",\"maps\":"<<accepted<<",\"stars\":[";
            bool initial=true;
            for(const auto& star:stars) {
                if(!initial)output<<',';
                initial=false;output<<'[';
                for(std::size_t j=0;j<star.size();++j) {if(j)output<<',';output<<star[j];}
                output<<']';
            }
            output<<"]}\n";output.flush();if(!output)throw std::runtime_error("write failure");
            std::cout<<"case "<<f<<','<<s<<" COMPLETE scanned="<<scanned<<" maps="<<accepted<<" stars="<<stars.size()<<'\n'<<std::flush;
        }
        return 0;
    } catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 2;}
}
