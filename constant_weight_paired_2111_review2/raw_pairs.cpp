#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

// Independent reviewer2: all nine-point permutations filtered by the three
// shared triples, followed by ALL seven-point permutations. No automorphisms,
// double cosets, forbidden-triple table or partial-assignment pruning.
using Word = std::uint32_t;
using Clock = std::chrono::steady_clock;
using Star = std::array<Word,20>;
using Quad = std::array<int,4>;
void need(bool ok, const char* message) { if (!ok) throw std::runtime_error(message); }
int integer(const std::string& s) {
    std::size_t used=0; int x=std::stoi(s,&used);
    need(used==s.size(),"malformed integer argument"); return x;
}
double real(const std::string& s) {
    std::size_t used=0; double x=std::stod(s,&used);
    need(used==s.size(),"malformed real argument"); return x;
}
std::vector<int> vertices(Word w) {
    std::vector<int> a;
    for (int z=0;z<17;++z) if (w & (Word{1}<<z)) a.push_back(z);
    return a;
}
std::vector<Word> tails(const Star& star) {
    std::vector<Word> a;
    for (Word w:star) if (w&1U) a.push_back(w^1U);
    return a;
}
std::vector<int> support(const std::vector<Word>& a) {
    Word w=0; for (Word q:a) w|=q; return vertices(w);
}
std::vector<int> complement(const std::vector<int>& a) {
    std::vector<int> b;
    for(int z=1;z<=16;++z) if (std::find(a.begin(),a.end(),z)==a.end()) b.push_back(z);
    return b;
}
void validate(const Star& star) {
    std::set<Word> words(star.begin(),star.end());
    need(words.size()==20,"duplicate template word");
    std::array<int,17> r{};
    for (Word w:star) {
        need(w<(Word{1}<<17) && __builtin_popcount(w)==4,"bad template mask");
        for(int z:vertices(w)) ++r[z];
    }
    for(int z=0;z<17;++z) need(r[z]==(z==0?3:(z<4?4:5)),"bad template replication");
    for(int a=0;a<20;++a) for(int b=0;b<a;++b)
        need(__builtin_popcount(star[a]&star[b])<=1,"template pair conflict");
}
int main(int argc,char** argv) {
  try {
    need(argc==5,"usage: raw_pairs begin end fiber_cap fiber_seconds");
    int begin=integer(argv[1]),end=integer(argv[2]),cap=integer(argv[3]);
    double seconds=real(argv[4]);
    need(0<=begin && begin<end && end<=64 && 0<=cap && cap<=200000 && 0<seconds && seconds<=10,"invalid guard/domain");
    std::array<Star,8> stars{};
    for(Star& star:stars) { for(Word& w:star) need(bool(std::cin>>w),"truncated templates"); validate(star); }
    std::string extra; need(!(std::cin>>extra),"trailing input");
    for(int index=begin;index<end;++index) {
        const int i=index/8,j=index%8;
        auto at=tails(stars[i]),bt=tails(stars[j]);
        auto ad=support(at),bd=support(bt),af=complement(ad),bf=complement(bd);
        need(ad.size()==9 && bd.size()==9 && af.size()==7 && bf.size()==7,"tail dimensions");
        std::set<Word> targets(at.begin(),at.end());
        std::vector<Word> left;
        std::vector<Quad> right;
        for(Word w:stars[i]) if(!(w&1U)) left.push_back(w);
        for(Word w:stars[j]) if(!(w&1U)) {
            auto v=vertices(w); Quad q{}; std::copy(v.begin(),v.end(),q.begin()); right.push_back(q);
        }
        need(left.size()==17 && right.size()==17,"residual dimensions");
        std::array<int,17> image{}; image.fill(-1); image[0]=17;
        auto nine=ad;
        std::uint64_t nine_count=0,tail_count=0,assignments=0,accepted=0,positive=0;
        do {
            ++nine_count;
            for(std::size_t k=0;k<9;++k) image[bd[k]]=nine[k];
            bool aligned=true;
            for(Word w:bt) {
                Word out=0; for(int z:vertices(w)) out|=Word{1}<<image[z];
                if(!targets.count(out)) {aligned=false;break;}
            }
            if(!aligned) continue;
            ++tail_count;
            auto seven=af;
            auto started=Clock::now();
            int nodes=0,found=0;
            do {
                ++nodes; ++assignments;
                need(nodes<=cap,"INCOMPLETE raw fiber node guard");
                if(nodes%128==0) need(std::chrono::duration<double>(Clock::now()-started).count()<=seconds,"INCOMPLETE raw fiber time guard");
                for(std::size_t k=0;k<7;++k) image[bf[k]]=seven[k];
                bool compatible=true;
                for(const Quad& q:right) {
                    Word w=(Word{1}<<image[q[0]])|(Word{1}<<image[q[1]])|(Word{1}<<image[q[2]])|(Word{1}<<image[q[3]]);
                    for(Word a:left) if(__builtin_popcount(a&w)>2) {compatible=false;break;}
                    if(!compatible) break;
                }
                if(compatible) {
                    ++accepted; ++found;
                    std::cout<<"MAP "<<i<<' '<<j;
                    for(int z:image) std::cout<<' '<<z;
                    std::cout<<'\n';
                }
            } while(std::next_permutation(seven.begin(),seven.end()));
            need(nodes==5040 && std::chrono::duration<double>(Clock::now()-started).count()<=seconds,"INCOMPLETE final raw fiber guard");
            if(found) ++positive;
        } while(std::next_permutation(nine.begin(),nine.end()));
        need(nine_count==362880 && tail_count==1296 && assignments==6531840,"INCOMPLETE raw domain coverage");
        std::cout<<"PAIR "<<i<<' '<<j<<' '<<nine_count<<' '<<tail_count<<' '<<assignments<<' '<<accepted<<' '<<positive<<" COMPLETE\n"<<std::flush;
    }
  } catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 2;}
}
