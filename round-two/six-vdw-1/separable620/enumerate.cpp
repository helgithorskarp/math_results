// Exact de Bruijn walk enumeration, followed by literal F31 AP checking.
#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>

struct Census {
    std::array<bool,128> forbidden{};
    std::array<unsigned,128> row_start{},row_step{};
    std::array<uint64_t,4> passed{};
    uint64_t word_sum=0,word_xor=0;
    unsigned root=0;
    std::ofstream output;
    void witness(uint32_t word,unsigned a,unsigned d,unsigned pattern) {
        unsigned start=row_start[pattern]+20*((a+31-row_start[pattern]%31)*14%31);
        unsigned step=row_step[pattern]+20*((d+31-row_step[pattern]%31)*14%31);
        if(step==0) throw std::runtime_error("constant CRT step");
        if(step>310) {start=(start+6*step)%620;step=620-step;}
        if(start+6*step>=2480) throw std::runtime_error("literal cutoff");
        uint64_t record=word|(uint64_t(start)<<32)|(uint64_t(step)<<48);
        std::array<unsigned char,9> bytes{};
        for(unsigned i=0;i<8;i++) bytes[i]=static_cast<unsigned char>((record>>(8*i))&255);
        // Byte eight is zero: matching field/row patterns give product color zero.
        output.write(reinterpret_cast<const char*>(bytes.data()),9);
    }
    void completed(uint32_t word) {
        passed[1]++; word_sum+=word; word_xor^=word;
        for(unsigned d=2;d<=3;d++) {
            for(unsigned a=0;a<31;a++) {
                unsigned p=0;
                for(unsigned j=0;j<7;j++) p|=((word>>((a+j*d)%31))&1u)<<j;
                if(forbidden[p]) {witness(word,a,d,p);return;}
            }
            passed[d]++;
        }
        throw std::runtime_error("construction candidate needs an independent interval check");
    }
    void visit(unsigned position,unsigned state,uint32_t word) {
        if(position==31) {
            for(unsigned j=0;j<6;j++) {
                unsigned b=(root>>j)&1u,p=state|(b<<6);
                if(forbidden[p]) return;
                state=p>>1;
            }
            if(state!=root) throw std::runtime_error("invalid closed walk");
            completed(word); return;
        }
        for(unsigned b=0;b<2;b++) {
            unsigned p=state|(b<<6);
            if(!forbidden[p]) visit(position+1,p>>1,word|(b<<position));
        }
    }
};

int main(int argc,char** argv) {
    try {
    if(argc!=2) throw std::runtime_error("usage: enumerate DIRECTORY");
    std::filesystem::path directory(argv[1]);
    if(!std::filesystem::is_directory(directory)) throw std::runtime_error("missing output directory");
    for(unsigned mask: {8u,10u,12u,16u,20u,34u,72u}) {
        Census c;
        c.output.open(directory/("case"+std::to_string(mask)+".bin"),std::ios::binary);
        if(!c.output) throw std::runtime_error("cannot open evidence");
        std::array<unsigned,20> g{};
        for(unsigned i=0;i<20;i++) g[i]=((mask>>(i%10))&1u)^(i>=10);
        for(unsigned d=0;d<20;d++) for(unsigned a=0;a<20;a++) {
            unsigned p=0;
            for(unsigned j=0;j<7;j++) p|=g[(a+j*d)%20]<<j;
            c.forbidden[p]=true;
            c.row_start[p]=a; c.row_step[p]=d;
        }
        for(c.root=0;c.root<64;c.root++) c.visit(6,c.root,c.root);
        std::cout<<mask<<' '<<c.word_sum<<' '<<c.word_xor;
        for(unsigned d=1;d<=3;d++) std::cout<<' '<<c.passed[d];
        std::cout<<'\n';
        c.output.close();
        if(!c.output) throw std::runtime_error("evidence write failed");
    }
    } catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 1;}
}
