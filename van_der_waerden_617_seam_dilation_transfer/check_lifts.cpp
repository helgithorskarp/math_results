// six-vdw-3, researcher. Direct Euler/AP checker for dilation transfer.
// The inputs are the earlier44-AP and18-AP source-generated base transcripts.
// No base packing search, half-color table, propagation engine, or witness
// transformation output is trusted. This checker directly checks every lift.
#include <array>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
namespace {
constexpr int P=617,N=3704,C=1852,PER=2*P-1;
void demand(bool b,const char* m) {if(!b)throw std::runtime_error(m);}
int integer(const char* arg) {
    const std::string s(arg);std::size_t used=0;const int value=std::stoi(s,&used);
    demand(used==s.size(),"integer argument");return value;
}
std::uint32_t little(std::istream& in,int bytes) {
    std::uint32_t value=0;
    for(int j=0;j<bytes;++j) {
        const int c=in.get();demand(c!=std::char_traits<char>::eof(),"truncated header");
        value|=static_cast<std::uint32_t>(c)<<(8*j);
    }
    return value;
}
int residue(int x) {x%=P;return x<0?x+P:x;}
int power(int x,int e) {int y=1;while(e) {if(e%2)y=y*x%P;x=x*x%P;e/=2;}return y;}
struct Base {int radius,bound;std::vector<unsigned char> bytes;};
Base load(const char* filename,bool local) {
    std::ifstream in(filename,std::ios::binary);demand(static_cast<bool>(in),"base input open");
    std::array<char,8> magic{};in.read(magic.data(),static_cast<std::streamsize>(magic.size()));
    demand(in&&std::string(magic.data(),magic.size())==(local?"QRL617P1":"QRS617P1"),"base format magic");
    const auto p=little(in,2),terms=little(in,2),bound=little(in,2);
    const auto radius=local?little(in,2):P;
    const auto begin=little(in,2),end=little(in,2),count=little(in,4);
    demand(p==P&&terms==7&&bound==(local?18U:44U)&&radius==(local?308U:617U),"base parameters");
    demand(begin==0&&end==P&&count==P*PER,"base must cover the complete phase domain");
    const std::uint64_t size=static_cast<std::uint64_t>(count)*bound*4;
    const std::uint64_t header=local?24:22;
    demand(std::filesystem::file_size(filename)==header+size,"base length/trailing bytes");
    Base result{static_cast<int>(radius),static_cast<int>(bound),std::vector<unsigned char>(static_cast<std::size_t>(size))};
    in.read(reinterpret_cast<char*>(result.bytes.data()),static_cast<std::streamsize>(size));
    demand(static_cast<bool>(in),"base payload read");demand(in.get()==std::char_traits<char>::eof()&&in.eof(),"base EOF");return result;
}
std::array<int,2> record(const Base& b,int s,int t,int g,int j) {
    demand((s!=t||g==1)&&0<=s&&s<P&&0<=t&&t<P,"transformed incompatible key");
    const int u=2*t+g,ordinal=s*PER+u-static_cast<int>(u>2*s);
    const auto offset=4*(static_cast<std::size_t>(ordinal)*static_cast<std::size_t>(b.bound)+static_cast<std::size_t>(j));
    const auto* bytes=b.bytes.data()+offset;
    return {bytes[0]+256*bytes[1],bytes[2]+256*bytes[3]};
}
}
int main(int argc,char** argv) {
 try {
    const auto start=std::chrono::steady_clock::now();int begin=0,end=P,first=1;
    if(argc>1&&std::string(argv[1])=="--range") {
        demand(argc==6,"usage: check_seam_dilation --range BEGIN END FULL44.bin LOCAL18.bin");
        begin=integer(argv[2]);end=integer(argv[3]);first=4;
    }
    demand(argc==first+2,"usage: check_seam_dilation [--range BEGIN END] FULL44.bin LOCAL18.bin");
    demand(0<=begin&&begin<end&&end<=P,"phase range");
    for(int d=2;d*d<=P;++d)demand(P%d!=0,"modulus primality");
    std::array<int,P> q{};q[0]=-1;
    for(int r=1;r<P;++r) {const int v=power(r,(P-1)/2);demand(v==1||v==P-1,"Euler criterion");q[r]=v==1?0:1;}
    std::array<int,7> inverses{};
    for(int m=1;m<=6;++m) {
        inverses[m]=power(m,P-2);demand(m*inverses[m]%P==1,"nonzero dilation inverse");
        for(int r=1;r<P;++r)demand(q[m*r%P]==(q[m]^q[r]),"character dilation identity");
    }
    const std::array<Base,2> bases{load(argv[first],false),load(argv[first+1],true)};
    std::array<std::uint32_t,N> used{};std::uint32_t serial=0;
    std::uint64_t total_APs=0,total_points=0,total_classes=0;
    std::ostringstream out;
    out<<"{\"agent\":\"six-vdw-3\",\"role\":\"researcher\",\"status\":\"VERIFIED_DIRECT_DILATION_LIFTS\",\"full_domain\":"
             <<(begin==0&&end==P?"true":"false")<<",\"begin\":"<<begin<<",\"end\":"<<end
             <<",\"incompatible_keys_per_profile\":"<<(end-begin)*PER<<",\"profiles\":[";
    bool comma=false;
    for(int family=0;family<2;++family)for(int m=1;m<=(family==0?3:6);++m) {
        const auto& base=bases[family];const int radius=m*base.radius;
        demand(C-radius>=0&&C+radius<=N,"lift window inside target");
        std::uint64_t APs=0,classes=0;std::uint32_t cases=0;
        for(int s=begin;s<end;++s)for(int t=0;t<P;++t)for(int g=0;g<2;++g) {
            if(s==t&&g==0)continue;
            ++serial;++cases;
            for(int r=0;r<m;++r) {
                const int sp=(s+r)*inverses[m]%P,tp=(t+r)*inverses[m]%P;++classes;
                for(int j=0;j<base.bound;++j) {
                    const auto ap=record(base,sp,tp,g,j);const int a=ap[0],d=ap[1];
                    demand(d>0&&P-base.radius<=a&&a<P&&P<=a+6*d&&a+6*d<P+base.radius,"base crossing AP bounds");
                    const int lifted_a=C+r+m*(a-P),lifted_d=m*d;
                    demand(lifted_d>0&&C-radius<=lifted_a&&lifted_a<C&&C<=lifted_a+6*lifted_d&&lifted_a+6*lifted_d<C+radius,"lift crossing AP bounds");
                    int common=-1;
                    for(int i=0;i<7;++i) {
                        const int x=lifted_a+i*lifted_d;
                        demand(0<=x&&x<N,"lift coordinate bounds");
                        // The actual class identity is modulo m, not modulo617.
                        int cls=(x-C)%m;if(cls<0)cls+=m;demand(cls==r,"residue-class containment");
                        demand(used[x]!=serial,"overlapping lifted APs/classes");used[x]=serial;
                        const bool right=x>=C;int color=q[residue(x-C+(right?t:s))];demand(color>=0,"lifted AP pole");
                        if(right)color^=g;
                        if(i==0)common=color;else demand(common==color,"lifted AP not monochromatic");
                    }
                    ++APs;
                }
            }
        }
        demand(cases==static_cast<std::uint32_t>((end-begin)*PER),"profile case coverage");
        demand(classes==static_cast<std::uint64_t>(cases)*m&&APs==classes*base.bound,"profile class/AP coverage");
        total_APs+=APs;total_classes+=classes;total_points+=7*APs;
        if(comma)out<<',';
        comma=true;
        out<<"{\"base_radius\":"<<base.radius<<",\"dilation\":"<<m<<",\"window\":["<<C-radius<<','<<C+radius
                 <<"],\"edits_per_class\":"<<base.bound<<",\"total_edits\":"<<m*base.bound<<",\"classes_checked\":"<<classes
                 <<",\"APs_checked\":"<<APs<<'}';
    }
    out<<"],\"total_classes_checked\":"<<total_classes<<",\"total_APs_checked\":"<<total_APs
             <<",\"total_point_incidences_checked\":"<<total_points<<",\"seconds\":"
             <<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"}\n";
    std::cout<<out.str();return 0;
 } catch(const std::exception& e) {std::cerr<<"dilation verification failed: "<<e.what()<<'\n';return 1;}
}
