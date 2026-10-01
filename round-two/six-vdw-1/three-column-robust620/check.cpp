// Independent segment-path cardinality + membership/uniqueness/literal cover.
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
Table patterns(unsigned mask) {
    Table p{};
    for(unsigned first=0;first<20;first++) for(unsigned second=0;second<20;second++) {
        unsigned code=0;
        for(unsigned j=0;j<7;j++) {
            unsigned s=(first+j*(second+20-first))%20;
            code=(code<<1)|(((mask>>(s%10))&1u)^(s>=10));
        }
        p[code]=true;
    }
    return p;
}
uint64_t linear_count(const Table& p,unsigned length) {
    if(length<6) return uint64_t(1)<<length;
    std::array<uint64_t,64> current{};current.fill(1);
    for(unsigned i=6;i<length;i++) {
        std::array<uint64_t,64> next{};
        for(unsigned state=0;state<64;state++) for(unsigned bit=0;bit<2;bit++) {
            unsigned window=(state<<1)|bit;
            if(!p[window]) next[window&63]+=current[state];
        }
        current=next;
    }
    uint64_t total=0;for(auto value:current) total+=value;return total;
}
uint64_t domain_count(const Table& p,uint32_t holes,unsigned q) {
    require((holes&1u)!=0,"zero must be an exceptional coordinate");
    uint64_t product=1;unsigned run=0;
    for(unsigned x=0;x<q;x++) {
        if((holes>>x)&1u) {product*=linear_count(p,run);run=0;}
        else run++;
    }
    return product*linear_count(p,run);
}
std::vector<std::array<unsigned,7>> supports(uint32_t holes,unsigned q) {
    std::vector<std::array<unsigned,7>> result;
    for(unsigned a=0;a<q;a++) {
        std::array<unsigned,7> points{};bool outside=true;
        for(unsigned j=0;j<7;j++) {points[j]=(a+j)%q;outside&=((holes>>points[j])&1u)==0;}
        if(outside) result.push_back(points);
    }
    return result;
}
bool eligible(uint32_t word,const Table& p,const std::vector<std::array<unsigned,7>>& aps) {
    for(const auto& points:aps) {
        unsigned code=0;for(unsigned x:points) code=(code<<1)|((word>>x)&1u);
        if(p[code]) return false;
    }
    return true;
}
unsigned row_bit(unsigned mask,unsigned position) {
    unsigned s=position%20;return ((mask>>(s%10))&1u)^(s>=10);
}
int main(int argc,char** argv) {
    try {
        if(argc==2 && std::string(argv[1])=="--controls") {
            uint64_t linear_inputs=0,partial_inputs=0,positive=0;
            for(unsigned mask: {8u,10u,12u,16u,20u,34u,72u}) {
                Table p=patterns(mask);
                for(unsigned n=0;n<=12;n++) {
                    uint64_t direct=0;
                    for(uint32_t word=0;word<(1u<<n);word++) {
                        bool good=true;
                        for(unsigned a=0;a+7<=n;a++) {
                            unsigned code=0;
                            for(unsigned j=0;j<7;j++) code=(code<<1)|((word>>(a+j))&1u);
                            if(p[code]) {good=false;break;}
                        }
                        direct+=good;linear_inputs++;
                    }
                    require(direct==linear_count(p,n),"small linear count mismatch");positive+=direct;
                }
                for(unsigned q=7;q<=12;q++) for(unsigned third=2;third<q;third++) {
                    uint32_t h=3u|(1u<<third);auto aps=supports(h,q);
                    std::vector<unsigned> free;for(unsigned x=0;x<q;x++) if(((h>>x)&1u)==0) free.push_back(x);
                    uint64_t direct=0;
                    for(uint32_t packed=0;packed<(1u<<free.size());packed++) {
                        uint32_t word=0;
                        for(unsigned j=0;j<free.size();j++) word|=((packed>>j)&1u)<<free[j];
                        direct+=eligible(word,p,aps);partial_inputs++;
                    }
                    require(direct==domain_count(p,h,q),"small punctured count mismatch");positive+=direct;
                }
            }
            Table empty{};require(domain_count(empty,3u|(1u<<12),31)==uint64_t(1)<<28,"all-allowed control");
            Table full{};full.fill(true);require(domain_count(full,3u|(1u<<12),31)==0,"all-forbidden control");
            require(positive>0,"vacuous controls");
            std::cout<<"CONTROLS "<<linear_inputs<<' '<<partial_inputs<<' '<<positive<<'\n';return 0;
        }
        require(argc==4,"usage: check DIRECTORY THIRD ROW_MASK");
        unsigned third=unsigned(std::stoul(argv[2])),mask=unsigned(std::stoul(argv[3]));
        require(std::string(argv[2])==std::to_string(third) && std::string(argv[3])==std::to_string(mask),"noncanonical integer case arguments");
        std::array<unsigned,6> thirds={2,3,4,5,6,12};std::array<unsigned,7> masks={8,10,12,16,20,34,72};
        require(std::find(thirds.begin(),thirds.end(),third)!=thirds.end() &&
                std::find(masks.begin(),masks.end(),mask)!=masks.end(),"unknown normalized case");
        uint32_t holes=3u|(1u<<third);Table p=patterns(mask);auto aps=supports(holes,31);
        uint64_t expected=domain_count(p,holes,31),sum=0,xor_words=0;
        std::filesystem::path directory(argv[1]);
        std::ifstream input(directory/("case"+std::to_string(third)+"-"+std::to_string(mask)+".bin"),std::ios::binary);
        require(bool(input),"missing normalized case");
        std::vector<uint32_t> words;words.reserve(size_t(expected));
        std::array<unsigned char,9> bytes{};unsigned largest_end=0,largest_field_step=0;
        while(input.read(reinterpret_cast<char*>(bytes.data()),9)) {
            uint64_t record=0;for(unsigned i=0;i<8;i++) record|=uint64_t(bytes[i])<<(8*i);
            uint32_t word=uint32_t(record);
            unsigned start=unsigned((record>>32)&65535),step=unsigned(record>>48),color=bytes[8];
            require(word<(1u<<31) && (word&holes)==0,"regular input outside domain/undefined bits nonzero");
            require(eligible(word,p,aps),"input violates step-one domain");
            require(start<620 && step>0 && step<=310 && color<2 && start+6*step<2480,"invalid integer AP bounds");
            unsigned dr=step%31,absolute=std::min(dr,31-dr);
            require(absolute>=2 && absolute<=6,"field witness step outside the proved cover");
            for(unsigned j=0;j<7;j++) {
                unsigned x=start+j*step,r=x%31;
                require(((holes>>r)&1u)==0,"literal witness touches an exceptional column");
                require((((word>>r)&1u)^row_bit(mask,x))==color,"literal product AP is not monochromatic");
            }
            largest_end=std::max(largest_end,start+6*step);largest_field_step=std::max(largest_field_step,absolute);
            words.push_back(word);sum+=word;xor_words^=word;
            require(words.size()<=expected,"too many coverage records");
        }
        require(input.eof() && input.gcount()==0,"truncated/unreadable record");
        require(words.size()==expected,"incomplete exact regular-input domain");
        std::sort(words.begin(),words.end());
        require(std::adjacent_find(words.begin(),words.end())==words.end(),"duplicate regular input");
        std::cout<<third<<' '<<mask<<' '<<expected<<' '<<sum<<' '<<xor_words<<' '<<largest_end<<' '<<largest_field_step<<'\n';
    } catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 1;}
}
