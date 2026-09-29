// Independent meet-in-the-middle checker. It uses no CEGIS, shortest-path
// bounds, no-op pruning, or commutation reductions from rewrite.cpp.
#include <algorithm>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
using Bits=std::uint64_t;
struct Checker {
    int n=0,width=0,budget=0,lead=0;
    std::vector<std::pair<int,int>> network,alphabet;
    std::vector<std::vector<unsigned>> transforms,states;
    std::vector<unsigned> witness;
    std::vector<unsigned char> accept,empty;
    std::vector<Bits> good,possible;
    std::vector<int> prefix;
    std::size_t suffixes=0,words=0;
    std::uint64_t checked=0;
    static unsigned compare(unsigned x,std::pair<int,int> c) {
        const unsigned left=(x>>c.first)&1U,right=(x>>c.second)&1U;
        if(left>right) x^=(1U<<c.first)|(1U<<c.second);
        return x;
    }
    bool is_sorted(unsigned x) const {
        for(int i=0;i+1<n;++i) if(((x>>i)&1U)>((x>>(i+1))&1U)) return false;
        return true;
    }
    void prepare(int start) {
        const unsigned universe=1U<<n;
        accept.resize(universe);empty.assign(universe,1);
        for(unsigned x=0;x<universe;++x) {
            unsigned z=x;
            for(std::size_t k=static_cast<std::size_t>(start+width);k<network.size();++k) z=compare(z,network[k]);
            accept[x]=static_cast<unsigned char>(is_sorted(z));
        }
        suffixes=alphabet.size()*alphabet.size(); words=(suffixes+63)/64;
        good.assign(static_cast<std::size_t>(universe)*words,0);possible.resize(words);
        for(unsigned x=0;x<universe;++x) for(std::size_t a=0;a<alphabet.size();++a) {
            const unsigned y=transforms[a][x];
            for(std::size_t b=0;b<alphabet.size();++b) if(accept[transforms[b][y]]) {
                const std::size_t id=a*alphabet.size()+b;
                good[static_cast<std::size_t>(x)*words+id/64]|=Bits{1}<<(id%64);
                empty[x]=0;
            }
        }
        states.assign(static_cast<std::size_t>(lead+1),std::vector<unsigned>(witness.size()));
        bool zero_sorts=true;
        for(std::size_t k=0;k<witness.size();++k) {
            unsigned x=witness[k];
            for(int j=0;j<start;++j) x=compare(x,network[static_cast<std::size_t>(j)]);
            states[0][k]=x;
            if(!accept[x]) zero_sorts=false;
        }
        if(zero_sorts) throw std::runtime_error("certificate does not exclude the empty replacement");
        checked=0;prefix.clear();
    }
    bool test(int depth,int last) {
        ++checked;
        std::fill(possible.begin(),possible.end(),~Bits{0});
        if(suffixes%64) possible.back()=(Bits{1}<<(suffixes%64))-1;
        for(unsigned x:states[static_cast<std::size_t>(depth)]) {
            if(last>=0) x=transforms[static_cast<std::size_t>(last)][x];
            if(empty[x]) return false;
            const std::size_t offset=static_cast<std::size_t>(x)*words;
            Bits any=0;
            for(std::size_t t=0;t<words;++t) {possible[t]&=good[offset+t];any|=possible[t];}
            if(!any) return false;
        }
        for(std::size_t t=0;t<words;++t) if(possible[t]) {
            const std::size_t id=64*t+static_cast<std::size_t>(std::countr_zero(possible[t]));
            std::cerr<<"certificate insufficient: prefix";
            for(int c:prefix)std::cerr<<' '<<c;
            if(last>=0)std::cerr<<' '<<last;
            std::cerr<<", suffix "<<id/alphabet.size()<<' '<<id%alphabet.size()<<'\n';
            return true;
        }
        throw std::runtime_error("internal intersection inconsistency");
    }
    bool traverse(int depth) {
        if(lead==0) return test(depth,-1);
        if(depth==lead-1) {
            for(int c=0;c<static_cast<int>(alphabet.size());++c) if(test(depth,c)) return true;
            return false;
        }
        for(int c=0;c<static_cast<int>(alphabet.size());++c) {
            for(std::size_t k=0;k<witness.size();++k)
                states[static_cast<std::size_t>(depth+1)][k]=transforms[static_cast<std::size_t>(c)][states[static_cast<std::size_t>(depth)][k]];
            prefix.push_back(c);
            if(traverse(depth+1))return true;
            prefix.pop_back();
        }
        return false;
    }
};
int main(int argc,char** argv)try {
    if(argc!=7)throw std::runtime_error("usage: check_rewrite FIXTURE WITNESSES WIDTH BUDGET START END");
    Checker c;std::ifstream nf(argv[1]),wf(argv[2]);int m=0,wn=0,h=0;
    if(!(nf>>c.n>>m)||c.n<2||c.n>16||m<2||m>60)throw std::runtime_error("invalid fixture header");
    for(int k=0;k<m;++k) {int a=0,b=0;if(!(nf>>a>>b)||a<0||a>=b||b>=c.n)throw std::runtime_error("invalid gate");c.network.emplace_back(a,b);}
    std::string extra;if(nf>>extra)throw std::runtime_error("trailing fixture data");
    if(!(wf>>wn>>h)||wn!=c.n||h<1||h>(1<<c.n))throw std::runtime_error("invalid witness header");
    std::set<unsigned> unique;
    for(int k=0;k<h;++k) {unsigned x=0;if(!(wf>>x)||x>=(1U<<c.n)||!unique.insert(x).second)throw std::runtime_error("invalid witness");c.witness.push_back(x);}
    if(wf>>extra)throw std::runtime_error("trailing witness data");
    c.width=std::stoi(argv[3]);c.budget=std::stoi(argv[4]);c.lead=c.budget-2;
    const int begin=std::stoi(argv[5]),end=std::stoi(argv[6]);
    if(c.width<1||c.budget<2||c.budget>=c.width||c.budget>6||begin<0||end<begin||end+c.width>m)throw std::runtime_error("invalid search bounds");
    for(int a=0;a<c.n;++a)for(int b=a+1;b<c.n;++b)c.alphabet.emplace_back(a,b);
    for(auto gate:c.alphabet) {std::vector<unsigned> t(1U<<c.n);for(unsigned x=0;x<t.size();++x)t[x]=Checker::compare(x,gate);c.transforms.push_back(std::move(t));}
    std::uint64_t expected_prefix=1,strings=1;
    for(int k=0;k<c.lead;++k)expected_prefix*=c.alphabet.size();
    for(int k=0;k<c.budget;++k)strings*=c.alphabet.size();
    for(int s=begin;s<=end;++s) {
        c.prepare(s);
        if(c.traverse(0))return 4;
        if(c.checked!=expected_prefix)throw std::runtime_error("incomplete prefix enumeration");
        std::cout<<"certified_window="<<s<<" width="<<c.width<<" budget="<<c.budget<<" prefixes="<<c.checked<<" strings="<<strings<<std::endl;
    }
    std::cout<<"complete=1 windows="<<end-begin+1<<" strings="<<strings*static_cast<std::uint64_t>(end-begin+1)<<'\n';
    return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}
