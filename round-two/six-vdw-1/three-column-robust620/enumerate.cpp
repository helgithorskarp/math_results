// Exact punctured-field enumeration and actual CRT obstructions outside holes.
#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>

struct Kernel {
    std::array<bool,128> forbidden{};
    std::array<unsigned,128> row_start{},row_step{};
    std::array<uint64_t,7> passed{};
    uint32_t holes=0;
    uint64_t word_sum=0,word_xor=0;
    std::ofstream output;
    void witness(uint32_t word,unsigned a,unsigned d,unsigned pattern) {
        unsigned start=row_start[pattern]+20*((a+31-row_start[pattern])*14%31);
        unsigned step=row_step[pattern]+20*((d+31-row_step[pattern])*14%31);
        if(step==0) throw std::runtime_error("constant CRT step");
        if(step>310) {start=(start+6*step)%620;step=620-step;}
        if(start+6*step>=2480) throw std::runtime_error("literal cutoff");
        for(unsigned j=0;j<7;j++) if((holes>>((start+j*step)%31))&1u)
            throw std::runtime_error("witness touches an exceptional column");
        uint64_t packed=word|(uint64_t(start)<<32)|(uint64_t(step)<<48);
        std::array<unsigned char,9> bytes{};
        for(unsigned i=0;i<8;i++) bytes[i]=static_cast<unsigned char>((packed>>(8*i))&255);
        output.write(reinterpret_cast<const char*>(bytes.data()),9);
    }
    void completed(uint32_t word) {
        passed[1]++;word_sum+=word;word_xor^=word;
        for(unsigned d=2;d<=6;d++) {
            for(unsigned a=0;a<31;a++) {
                unsigned pattern=0;bool outside=true;
                for(unsigned j=0;j<7;j++) {
                    unsigned r=(a+j*d)%31;
                    if((holes>>r)&1u) {outside=false;break;}
                    pattern|=((word>>r)&1u)<<j;
                }
                if(outside && forbidden[pattern]) {witness(word,a,d,pattern);return;}
            }
            passed[d]++;
        }
        throw std::runtime_error("regular-column survivor; no complete exclusion");
    }
    void visit(unsigned position,unsigned run,unsigned state,uint32_t word) {
        if(position==31) {completed(word);return;}
        if((holes>>position)&1u) {visit(position+1,0,0,word);return;}
        for(unsigned bit=0;bit<2;bit++) {
            if(run<6) visit(position+1,run+1,state|(bit<<run),word|(bit<<position));
            else {
                unsigned window=state|(bit<<6);
                if(!forbidden[window]) visit(position+1,6,window>>1,word|(bit<<position));
            }
        }
    }
};
int main(int argc,char** argv) {
    try {
        if(argc!=2) throw std::runtime_error("usage: enumerate DIRECTORY");
        std::filesystem::path directory(argv[1]);
        if(!std::filesystem::is_directory(directory)) throw std::runtime_error("missing output directory");
        for(unsigned third: {2u,3u,4u,5u,6u,12u}) for(unsigned mask: {8u,10u,12u,16u,20u,34u,72u}) {
            Kernel p;p.holes=3u|(1u<<third);
            std::string name="case"+std::to_string(third)+"-"+std::to_string(mask)+".bin";
            auto temporary=directory/(name+".tmp");
            p.output.open(temporary,std::ios::binary);
            if(!p.output) throw std::runtime_error("cannot open evidence");
            for(unsigned a=0;a<20;a++) for(unsigned d=0;d<20;d++) {
                unsigned pattern=0;
                for(unsigned j=0;j<7;j++) {
                    unsigned s=(a+j*d)%20;
                    pattern|=(((mask>>(s%10))&1u)^(s>=10))<<j;
                }
                p.forbidden[pattern]=true;p.row_start[pattern]=a;p.row_step[pattern]=d;
            }
            p.visit(0,0,0,0);p.output.close();
            if(!p.output) throw std::runtime_error("evidence write failed");
            std::filesystem::rename(temporary,directory/name);
            std::cout<<third<<' '<<mask<<' '<<p.word_sum<<' '<<p.word_xor;
            for(unsigned d=1;d<=6;d++) std::cout<<' '<<p.passed[d];
            std::cout<<'\n';
        }
    } catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 1;}
}
