// Independent coverage: transfer-matrix trace + unique literal AP records.
// Shares no code or enumeration with the producer.
#include <algorithm>
#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Table=std::array<bool,128>;
void require(bool b,const std::string& m) {if(!b) throw std::runtime_error(m);}
Table forbidden(unsigned mask) {
    Table p{};
    for(unsigned a=0;a<20;a++) for(unsigned b=0;b<20;b++) {
        unsigned code=0;
        for(unsigned j=0;j<7;j++) {
            unsigned x=(a+j*b)%20;
            code=(code<<1)|(((mask>>(x%10))&1u)^(x>=10));
        }
        p[code]=true;
    }
    return p;
}
uint64_t trace(const Table& p,unsigned n) {
    uint64_t result=0;
    // MSB-first states; exact nonnegative integer paths, each <=2^n.
    for(unsigned first=0;first<64;first++) {
        std::array<uint64_t,64> current{};current[first]=1;
        for(unsigned length=0;length<n;length++) {
            std::array<uint64_t,64> next{};
            for(unsigned state=0;state<64;state++) for(unsigned bit=0;bit<2;bit++) {
                unsigned window=(state<<1)|bit;
                if(!p[window]) next[window&63]+=current[state];
            }
            current=next;
        }
        result+=current[first];
    }
    return result;
}
bool eligible(uint32_t word,unsigned n,const Table& p) {
    for(unsigned a=0;a<n;a++) {
        unsigned code=0;
        for(unsigned j=0;j<7;j++) code=(code<<1)|((word>>((a+j)%n))&1u);
        if(p[code]) return false;
    }
    return true;
}
unsigned row_bit(unsigned mask,unsigned position) {
    return ((mask>>(position%10))&1u)^(position%20>=10);
}
int main(int argc,char** argv) {
    try {
    require(argc==2,"usage: check_walks DIRECTORY or --controls");
    if(std::string(argv[1])=="--controls") {
        uint64_t comparisons=0,positive_words=0;
        for(unsigned mask: {8u,10u,12u,16u,20u,34u,72u}) {
            Table p=forbidden(mask);
            for(unsigned n=1;n<=10;n++) {
                uint64_t direct=0;
                for(uint32_t word=0;word<(1u<<n);word++) {
                    direct+=eligible(word,n,p);comparisons++;
                }
                require(direct==trace(p,n),"small exhaustive trace mismatch");
                positive_words+=direct;
            }
        }
        Table empty{}; require(trace(empty,31)==uint64_t(1)<<31,"all-allowed control");
        Table full{};full.fill(true);require(trace(full,31)==0,"all-forbidden control");
        require(positive_words>0,"vacuous small controls");
        std::cout<<"CONTROLS "<<comparisons<<' '<<positive_words<<'\n';return 0;
    }
    std::filesystem::path directory(argv[1]);
    for(unsigned mask: {8u,10u,12u,16u,20u,34u,72u}) {
        Table p=forbidden(mask);
        uint64_t expected=trace(p,31),sum=0,xor_words=0,after_two=0;
        std::ifstream input(directory/("case"+std::to_string(mask)+".bin"),std::ios::binary);
        require(bool(input),"missing row case");
        std::vector<uint32_t> words; words.reserve(size_t(expected));
        std::array<unsigned char,9> bytes{};
        while(input.read(reinterpret_cast<char*>(bytes.data()),9)) {
            uint64_t record=0;
            for(unsigned i=0;i<8;i++) record|=uint64_t(bytes[i])<<(8*i);
            uint32_t word=uint32_t(record);
            unsigned start=unsigned((record>>32)&65535),step=unsigned(record>>48),color=bytes[8];
            require(word<(1u<<31),"field word outside domain");
            require(eligible(word,31,p),"record violates step-one domain");
            require(start<620 && step>0 && step<=310 && color<2 && start+6*step<2480,"invalid literal AP bounds");
            unsigned dr=step%31;
            require(dr==2 || dr==3 || dr==28 || dr==29,"witness outside the proved field-step2/3 cover");
            for(unsigned j=0;j<7;j++) {
                unsigned x=start+j*step;
                unsigned actual=((word>>(x%31))&1u)^row_bit(mask,x);
                require(actual==color,"literal product AP is not monochromatic");
            }
            if(dr==3 || dr==28) {
                for(unsigned a=0;a<31;a++) {
                    unsigned code=0;
                    for(unsigned j=0;j<7;j++) code=(code<<1)|((word>>((a+2*j)%31))&1u);
                    require(!p[code],"incorrect step-two survivor record");
                }
                after_two++;
            }
            words.push_back(word);sum+=word;xor_words^=word;
            require(words.size()<=expected,"excess coverage records");
        }
        require(input.eof() && input.gcount()==0,"truncated or unreadable record");
        require(words.size()==expected,"incomplete exact domain coverage");
        std::sort(words.begin(),words.end());
        require(std::adjacent_find(words.begin(),words.end())==words.end(),"duplicate field record");
        std::cout<<mask<<' '<<expected<<' '<<sum<<' '<<xor_words<<' '<<after_two<<'\n';
    }
    } catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 1;}
}
