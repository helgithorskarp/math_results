// Independent conditioning: enumerate the closing physical matrix and one
// left column-type profile, then count permitted right-column type choices.
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
void require(bool ok,const char* why){if(!ok)throw std::runtime_error(why);}
struct Domain {std::vector<unsigned> matrices;std::array<std::uint64_t,625> histogram{};};
std::array<std::array<unsigned,8>,8> pair_index{};
std::vector<unsigned> five_masks;
void initialize(){
    unsigned k=0;
    for(unsigned u=0;u<8;++u)for(unsigned v=u+1;v<8;++v)pair_index[u][v]=pair_index[v][u]=k++;
    for(unsigned s=0;s<256;++s)if(std::popcount(s)==5){unsigned mask=0;for(unsigned u=0;u<8;++u)for(unsigned v=u+1;v<8;++v)if((s&(1u<<u)) && (s&(1u<<v)))mask|=1u<<pair_index[u][v];five_masks.push_back(mask);}
    require(five_masks.size()==56,"five-set count");
}
unsigned literal_type(unsigned matrix,unsigned col){
    unsigned type=0,found=0;
    for(unsigned omitted=0;omitted<4;++omitted){
        bool all=true;
        for(unsigned row=0;row<4;++row)if(row!=omitted && ((matrix>>(4*row+col))&1u)==0)all=false;
        if(all){type=omitted+1;++found;}
    }
    require(found<=1,"two-block domain allows four neighbours");return type;
}
Domain enumerate(unsigned left_color,unsigned right_color){
    Domain d;unsigned fixed=0;
    for(unsigned block=0;block<2;++block)for(unsigned u=0;u<4;++u)for(unsigned v=u+1;v<4;++v)
        if(block==0?left_color:right_color)fixed|=1u<<pair_index[4*block+u][4*block+v];
    for(unsigned x=0;x<65536;++x){
        unsigned red=fixed;
        for(unsigned u=0;u<4;++u)for(unsigned v=0;v<4;++v)if((x>>(4*u+v))&1u)red|=1u<<pair_index[u][4+v];
        bool valid=true;
        for(unsigned mask:five_masks){unsigned intersection=red&mask;if(intersection==0 || intersection==mask){valid=false;break;}}
        if(!valid)continue;
        d.matrices.push_back(x);
        if(left_color==1){unsigned code=0,power=1;for(unsigned v=0;v<4;++v){code+=power*literal_type(x,v);power*=5;}++d.histogram[code];}
    }
    return d;
}
std::array<unsigned,4> decode(unsigned code){std::array<unsigned,4> t{};for(unsigned i=0;i<4;++i){t[i]=code%5;code/=5;}require(code==0,"type code");return t;}
std::vector<std::uint64_t> permissions(const Domain& d){
    std::vector<std::uint64_t> table(65536);
    for(unsigned code=0;code<625;++code){auto t=decode(code);unsigned mask=0;for(unsigned j=0;j<4;++j)if(t[j])mask|=1u<<(4*j+t[j]-1);table[mask]+=d.histogram[code];}
    // Subsets here are permissions for right-column types, not physical edges.
    for(unsigned bit=0;bit<16;++bit)for(unsigned mask=0;mask<65536;++mask)if(mask&(1u<<bit))table[mask]+=table[mask^(1u<<bit)];
    require(table.back()==d.matrices.size(),"permission total");return table;
}
std::uint64_t calculate(const std::string& name,const Domain& left,const Domain& right,const Domain& closing,std::ostream& out,std::uint64_t& visits){
    auto table=permissions(right);std::uint64_t sum=0;
    std::vector<std::array<unsigned,4>> columns;
    for(unsigned c:closing.matrices){std::array<unsigned,4> cs{};for(unsigned j=0;j<4;++j)for(unsigned i=0;i<4;++i)cs[j]|=((c>>(4*i+j))&1u)<<i;columns.push_back(cs);}
    for(unsigned code=0;code<625;++code)if(left.histogram[code]){
        auto types=decode(code);std::array<unsigned,16> unions{};
        for(unsigned subset=0;subset<16;++subset)for(unsigned j=0;j<4;++j)if((subset&(1u<<j)) && types[j])unions[subset]|=1u<<(types[j]-1);
        std::uint64_t subtotal=0;
        for(auto c:columns){unsigned permitted=0;for(unsigned j=0;j<4;++j)permitted|=(15u^unions[c[j]])<<(4*j);subtotal+=table[permitted];++visits;}
        out<<name<<'\t'<<code<<'\t'<<left.histogram[code]<<'\t'<<subtotal<<'\n';
        sum+=left.histogram[code]*subtotal;
    }
    return sum;
}
void write_domain(const Domain& d,const std::string& path){std::ofstream out(path,std::ios::binary);require(static_cast<bool>(out),"domain output");for(unsigned x:d.matrices){out.put(static_cast<char>(x&255));out.put(static_cast<char>((x>>8)&255));}require(static_cast<bool>(out),"domain write");}
int main(int argc,char** argv){try{
    require(argc==2,"usage: independent_count output-directory");std::string out=argv[1];initialize();auto start=std::chrono::steady_clock::now();
    Domain rr=enumerate(1,1),rb=enumerate(1,0),bb=enumerate(0,0);
    require(rr.matrices.size()==37823 && rb.matrices.size()==35714 && bb.matrices.size()==37823,"literal pair-domain counts");
    std::ofstream hist(out+"/HISTOGRAM.tsv");require(static_cast<bool>(hist),"histogram output");
    for(unsigned mode=0;mode<2;++mode){const auto& d=mode==0?rr:rb;for(unsigned code=0;code<625;++code)if(d.histogram[code])hist<<(mode==0?"RR":"RB")<<'\t'<<code<<'\t'<<d.histogram[code]<<'\n';}
    require(static_cast<bool>(hist),"histogram write");
    std::ofstream profile(out+"/PROFILE.tsv");require(static_cast<bool>(profile),"profile output");std::uint64_t visits=0;
    auto same=calculate("same",rr,rr,rr,profile,visits),majority=calculate("majority",rr,rb,rb,profile,visits),minority=calculate("minority",rb,rb,bb,profile,visits);
    require(static_cast<bool>(profile),"profile write");write_domain(rr,out+"/RR.bin");write_domain(rb,out+"/RB.bin");write_domain(bb,out+"/BB.bin");
    std::ofstream summary(out+"/TOTALS.tsv");require(static_cast<bool>(summary),"totals output");
    summary<<"same\t"<<same<<'\n'<<"majority\t"<<majority<<'\n'<<"minority\t"<<minority<<'\n';require(static_cast<bool>(summary),"totals write");
    std::cout<<"{\"status\":\"COMPLETE_INDEPENDENT_CENTRED_CENSUS\",\"conditioned_cases\":"<<visits<<",\"literal_pair_assignments\":196608,\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"}\n";return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}}
