// Exploratory second symmetric opposed-pair generator. Every used premise
// must avoid the first proof's protected support. Positive records require
// an independent direct checker; zero records and time limits prove nothing.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
constexpr int P=617,N=3704,C=1852,H=565,LO=C-H,HI=C+H;
constexpr int U=2*P,W=(U+63)/64,E=N-2*H,EW=(E+63)/64;
using Mask=std::array<std::uint64_t,W>;
using Witness=std::array<std::uint16_t,3>;
int residue(int x) { x%=P; return x<0?x+P:x; }
void demand(bool b,const char* msg) { if (!b) throw std::runtime_error(msg); }
std::uint16_t get16(std::istream& in) {
    const int a=in.get(),b=in.get(); demand(a>=0&&b>=0,"truncated u16");
    return static_cast<std::uint16_t>(a|(b<<8));
}
std::uint32_t get32(std::istream& in) {
    std::uint32_t r=0;
    for(unsigned j=0;j<4;++j) { const int a=in.get(); demand(a>=0,"truncated u32"); r|=static_cast<std::uint32_t>(a)<<(8*j); }
    return r;
}
void put16(std::ostream& out,std::uint16_t x) { out.put(static_cast<char>(x&255));out.put(static_cast<char>(x>>8)); }
void put32(std::ostream& out,std::uint32_t x) { for(unsigned j=0;j<4;++j) out.put(static_cast<char>((x>>(8*j))&255)); }
std::size_t phase_index(int s,int t,int g) { return static_cast<std::size_t>(s)*U+g*P+t; }
int exterior_index(int x) { demand(0<=x&&x<N&&(x<LO||x>=HI),"erasure outside protected exterior"); return x<LO?x:x-2*H; }
}

int main(int argc,char**argv) {
 try {
    demand(argc==5,"usage: second_pair_generate FIRST.bin STAR_SUPPORTS.txt OUTPUT.bin SECONDS");
    const std::filesystem::path output(argv[3]),partial(output.string()+".partial");
    demand(!std::filesystem::exists(output)&&!std::filesystem::exists(partial),"refusing to overwrite output");
    std::size_t used=0; const double limit=std::stod(argv[4],&used);
    demand(used==std::string(argv[4]).size()&&limit>0&&limit<=90,"pilot budget must be in (0,90]");
    const auto start=std::chrono::steady_clock::now();
    const auto seconds=[&] {return std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();};
    std::array<int,P> q; q.fill(1);q[0]=-1;
    for(int z=1;z<P;++z)q[z*z%P]=0;
    std::vector<std::uint64_t> erased(static_cast<std::size_t>(P)*U*EW,0);
    std::vector<Witness> first(static_cast<std::size_t>(P)*U,Witness{}),second(first.size(),Witness{});
    const auto erase=[&](std::size_t index,int x,int s,int t,int g) {
        const int y=exterior_index(x),phase=x<LO?s:t;
        demand(q[residue(x-C+phase)]>=0,"first support includes a pole");
        (void)g;
        erased[index*EW+y/64]|=std::uint64_t{1}<<(y%64);
    };
    std::ifstream input(argv[1],std::ios::binary); demand(static_cast<bool>(input),"first input open");
    std::array<char,8> magic{};input.read(magic.data(),8);
    demand(std::string(magic.data(),8)=="QRD617P1","first magic");
    for(int x:{P,7,N,H,0,P}) demand(get16(input)==x,"first dimensions");
    const std::uint32_t target=P*(U-1); demand(get32(input)==target,"first record count");
    std::uint32_t holes=0;
    for(int s=0;s<P;++s)for(int t=0;t<P;++t)for(int g=0;g<2;++g) {
        if(s==t&&g==0)continue;
        const auto index=phase_index(s,t,g);auto& r=first[index];
        for(auto& x:r)x=get16(input);
        if(r==Witness{}) {++holes;continue;}
        const int v=r[0];demand(LO<=v&&v<HI,"first free center");
        for(int b=0;b<2;++b) {
            const int d=r[1+b];demand(d>0&&v-3*d>=0&&v+3*d<N,"first AP bounds");
            for(int j:{-3,-2,-1,1,2,3}) {
                const int x=v+j*d;const int y=exterior_index(x);(void)y;
                const int value=q[residue(x-C+(x<LO?s:t))];
                demand(value>=0&&(value^(x<LO?0:g))==b,"first AP color");
                erase(index,x,s,t,g);
            }
        }
    }
    demand(input.get()==std::char_traits<char>::eof(),"first trailing data");
    std::ifstream stars(argv[2]);demand(static_cast<bool>(stars),"star support file open");
    std::vector<bool> star_seen(first.size(),false);std::uint32_t star_count=0;
    int s0,t0,g0,count;
    while(stars>>s0>>t0>>g0>>count) {
        demand(0<=s0&&s0<P&&0<=t0&&t0<P&&(g0==0||g0==1)&&(s0!=t0||g0),"star key");
        demand(count>0&&count<=22,"star support size");
        const auto index=phase_index(s0,t0,g0);
        demand(first[index]==Witness{}&&!star_seen[index],"star must cover distinct first hole");
        for(int j=0;j<count;++j) {int x;demand(static_cast<bool>(stars>>x),"truncated star support");erase(index,x,s0,t0,g0);}
        star_seen[index]=true;++star_count;
    }
    demand(stars.eof()&&star_count==holes,"missing or malformed star support");
    std::vector<Mask> covered(P,Mask{});
    for(int s=0;s<P;++s)covered[s][s/64]|=std::uint64_t{1}<<(s%64);
    std::vector<int> centers;
    for(int v=std::max(LO,(3*HI+3)/4);v<=std::min(HI-1,(N-1+3*(LO-1))/4);++v)centers.push_back(v);
    std::sort(centers.begin(),centers.end(),[](int a,int b) {
        const int da=std::abs(2*a-(N-1)),db=std::abs(2*b-(N-1));return da!=db?da<db:a<b;
    });
    std::uint32_t total=0,frames=0;std::uint64_t candidates=0,rejected=0;
    int processed=0;bool complete=true;
    std::vector<std::array<std::uint32_t,3>> counts;
    for(int v:centers) {
        if(seconds()>=limit) {complete=false;break;}
        std::array<std::vector<Mask>,2> known{std::vector<Mask>(P,Mask{}),std::vector<Mask>(P,Mask{})};
        std::array<std::vector<std::uint16_t>,2> source{std::vector<std::uint16_t>(first.size(),0),std::vector<std::uint16_t>(first.size(),0)};
        const auto before=total;
        for(int d=std::max({1,v-LO+1,HI-v});d<=std::min(v/3,(N-1-v)/3);++d) {
            ++frames;std::array<std::vector<int>,2> left;std::array<Mask,2> right{};
            std::array<int,6> premise{};int jx=0;
            for(int j:{-3,-2,-1,1,2,3})premise[jx++]=exterior_index(v+j*d);
            for(int s=0;s<P;++s) {
                const int b=q[residue(v-d-C+s)];
                if(b>=0&&q[residue(v-2*d-C+s)]==b&&q[residue(v-3*d-C+s)]==b)left[b].push_back(s);
            }
            for(int t=0;t<P;++t) {
                const int b=q[residue(v+d-C+t)];
                if(b>=0&&q[residue(v+2*d-C+t)]==b&&q[residue(v+3*d-C+t)]==b) {
                    right[b][t/64]|=std::uint64_t{1}<<(t%64);
                    const int u=P+t;right[1-b][u/64]|=std::uint64_t{1}<<(u%64);
                }
            }
            for(int b=0;b<2;++b)for(int s:left[b])for(int w=0;w<W;++w) {
                auto fresh=right[b][w]&~covered[s][w]&~known[b][s][w];
                while(fresh) {
                    const unsigned bit=static_cast<unsigned>(__builtin_ctzll(fresh));fresh&=fresh-1;
                    const int u=64*w+static_cast<int>(bit);demand(u<U,"phase padding bit");
                    const std::uint64_t one=std::uint64_t{1}<<bit;const auto index=static_cast<std::size_t>(s)*U+u;
                    ++candidates;bool blocked=false;
                    for(int y:premise)if(erased[index*EW+y/64]&(std::uint64_t{1}<<(y%64))) {blocked=true;break;}
                    if(blocked) {++rejected;continue;}
                    source[b][index]=static_cast<std::uint16_t>(d);known[b][s][w]|=one;
                    if(known[1-b][s][w]&one) {
                        demand(second[index]==Witness{}&&source[1-b][index]>0,"duplicate second proof");
                        second[index][0]=static_cast<std::uint16_t>(v);second[index][1+b]=static_cast<std::uint16_t>(d);
                        second[index][2-b]=source[1-b][index];covered[s][w]|=one;++total;
                    }
                }
            }
        }
        ++processed;counts.push_back({static_cast<std::uint32_t>(v),total-before,total});
        if(total==target)break;
    }
    std::ofstream out(partial,std::ios::binary);demand(static_cast<bool>(out),"output open");
    out.write("QRD617P2",8);for(int x:{P,7,N,H,0,P})put16(out,static_cast<std::uint16_t>(x));put32(out,target);
    for(int s=0;s<P;++s)for(int t=0;t<P;++t)for(int g=0;g<2;++g) {
        if(s==t&&g==0)continue;
        for(auto x:second[phase_index(s,t,g)])put16(out,x);
    }
    out.close();demand(static_cast<bool>(out),"incomplete output write");std::filesystem::rename(partial,output);
    std::cout<<"{\"status\":\"GENERATED_REQUIRES_INDEPENDENT_CHECK\",\"half_width\":"<<H<<",\"phase_count\":"<<target
             <<",\"second_opposed_pairs\":"<<total<<",\"supplement_required\":"<<target-total<<",\"motif_search_complete\":"<<(complete?"true":"false")
             <<",\"centers_processed\":"<<processed<<",\"frames_processed\":"<<frames<<",\"candidates\":"<<candidates<<",\"rejected_overlap\":"<<rejected
             <<",\"erasure_matrix_bytes\":"<<erased.size()*sizeof(std::uint64_t)<<",\"seconds\":"<<seconds()<<",\"per_center\":[";
    for(std::size_t j=0;j<counts.size();++j) {if(j)std::cout<<',';const auto& r=counts[j];std::cout<<'['<<r[0]<<','<<r[1]<<','<<r[2]<<']';}
    std::cout<<"],\"uncovered_keys\":[";bool comma=false;
    for(int s=0;s<P;++s)for(int t=0;t<P;++t)for(int g=0;g<2;++g) {
        if(s==t&&g==0)continue;
        if(second[phase_index(s,t,g)]!=Witness{})continue;
        if(comma)std::cout<<',';
        comma=true;std::cout<<'['<<s<<','<<t<<','<<g<<']';
    }
    std::cout<<"]}\n";return 0;
 } catch(const std::exception& e) {std::cerr<<"generation failed: "<<e.what()<<'\n';return 1;}
}
