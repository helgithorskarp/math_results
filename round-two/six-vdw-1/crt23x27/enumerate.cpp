// Complete finite enumeration. Integer shifts use unsigned 32-bit words.
#include <array>
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>

std::uint32_t rotate23(std::uint32_t word,unsigned shift) {
    constexpr std::uint32_t mask=(1U<<23)-1;
    shift%=23;
    return shift==0?word:((word>>shift)|(word<<(23-shift)))&mask;
}
template<class Container> void array(const Container& values) {
    std::cout<<'['; bool first=true;
    for(auto x:values) { if(!first) std::cout<<','; first=false; std::cout<<x; }
    std::cout<<']';
}
int main() {
    constexpr std::uint32_t mask=(1U<<23)-1;
    std::vector<std::uint32_t> u;
    std::array<std::uint64_t,11> u_rejected{};
    for(std::uint32_t index=0;index<(1U<<22);++index) {
        const std::uint32_t word=index<<1;
        bool failed=false;
        for(unsigned r=1;r<=11;++r) {
            const auto derivative=word^rotate23(word,3*r);
            const auto bad=mask^(derivative|rotate23(derivative,r)|
                                 rotate23(derivative,2*r)|rotate23(derivative,3*r));
            if(bad) { ++u_rejected[r-1]; failed=true; break; }
        }
        if(!failed) u.push_back(word);
    }
    std::array<int,23> qr{}; qr.fill(1); qr[0]=0;
    for(int x=1;x<23;++x) qr[x*x%23]=0;
    std::array<bool,128> forbidden{};
    for(int a=0;a<23;++a) for(int r=0;r<23;++r) {
        unsigned pattern=0;
        for(unsigned j=0;j<7;++j) pattern|=static_cast<unsigned>(qr[(a+static_cast<int>(j)*r)%23])<<j;
        forbidden[pattern]=forbidden[pattern^127U]=true;
    }
    std::vector<int> forbidden_words;
    for(int p=0;p<128;++p) if(forbidden[p]) forbidden_words.push_back(p);
    std::array<std::uint64_t,3> v9_rejected{};
    std::vector<std::uint32_t> v9, v9_after_two;
    for(std::uint32_t word=0;word<512;word+=2) {
        bool failed=false;
        for(int step=1;step<=3 && !failed;++step) {
            for(int a=0;a<9;++a) {
                unsigned pattern=0;
                for(unsigned j=0;j<7;++j)
                    pattern|=((word>>((a+static_cast<int>(j)*step)%9))&1U)<<j;
                if(forbidden[pattern]) { ++v9_rejected[step-1]; failed=true; break; }
            }
            if(step==2 && !failed) v9_after_two.push_back(word);
        }
        if(!failed) v9.push_back(word);
    }
    std::array<std::array<std::uint32_t,6>,9> column{};
    for(int x=0;x<9;++x) for(int s=0;s<6;++s) for(int y=0;y<3;++y) {
        const int bit=(s/3)^static_cast<int>(s%3==y);
        column[x][s]|=static_cast<std::uint32_t>(bit)<<(x+9*y);
    }
    constexpr std::uint32_t coverage=5038848; // 3*6^8, v(0)=0
    std::array<std::uint64_t,3> v_rejected{};
    std::vector<std::uint32_t> v, after_two;
    for(std::uint32_t index=0;index<coverage;++index) {
        std::uint32_t digits=index;
        std::uint32_t word=column[0][1+digits%3]; digits/=3;
        for(int x=1;x<9;++x) { word|=column[x][digits%6]; digits/=6; }
        bool failed=false;
        for(int step=1;step<=3 && !failed;++step) {
            for(int a=0;a<27;++a) {
                unsigned pattern=0;
                for(unsigned j=0;j<7;++j)
                    pattern|=((word>>((a+static_cast<int>(j)*step)%27))&1U)<<j;
                if(forbidden[pattern]) { ++v_rejected[step-1]; failed=true; break; }
            }
            if(step==2 && !failed) after_two.push_back(word);
        }
        if(!failed) v.push_back(word);
    }
    std::cout<<"{\"u_coverage\":"<<(1U<<22)<<",\"u_survivors\":"; array(u);
    std::cout<<",\"u_first_rejection\":"; array(u_rejected);
    std::cout<<",\"forbidden_words\":"; array(forbidden_words);
    std::cout<<",\"v9_coverage\":256,\"v9_survivors\":"; array(v9);
    std::cout<<",\"v9_first_rejection\":"; array(v9_rejected);
    std::cout<<",\"v9_after_step2\":"; array(v9_after_two);
    std::cout<<",\"v_coverage\":"<<coverage<<",\"v_survivors\":"; array(v);
    std::cout<<",\"v_first_rejection\":"; array(v_rejected);
    std::sort(after_two.begin(),after_two.end());
    std::cout<<",\"v_after_step2\":"; array(after_two);
    std::cout<<"}\n";
}
