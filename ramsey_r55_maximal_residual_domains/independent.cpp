// Independent census: literal triangle list, direct incidence enumeration
// of triangle-free subsets in every superset, then inclusion-exclusion.
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
void need(bool ok,const char* why){if(!ok)throw std::runtime_error(why);}
// Each parity sum is at most 2^(5n)<=2^75. Two unsigned limbs suffice.
struct Wide {std::uint64_t low=0,high=0;void add(std::uint64_t x){auto old=low;low+=x;if(low<old)++high;}};
int main(int argc,char** argv){try{
    need(argc==4,"usage: independent order counts.tsv profiles.bin");unsigned n=std::stoul(argv[1]);need(n>0&&n<=15,"order");
    unsigned size=1u<<n,full=size-1;std::ifstream rows(argv[2]),profiles(argv[3],std::ios::binary);need(bool(rows)&&bool(profiles),"files");
    std::uint64_t records=0,profile_count=0,incidences=0;std::string line;auto start=std::chrono::steady_clock::now();
    while(std::getline(rows,line)){
        std::istringstream row(line);unsigned index;std::string g;std::uint64_t expected_free,expected_cover;
        need(bool(row>>index>>g>>expected_free>>expected_cover),"count row");std::string extra;need(!(row>>extra),"extra field");
        need(g.size()==1+(n*(n-1)/2+5)/6&&unsigned(g[0])==63+n,"graph6 order/length");
        bool edge[15][15]{};unsigned position=0;
        for(unsigned v=1;v<n;++v)for(unsigned u=0;u<v;++u){unsigned symbol=unsigned(g[1+position/6]);need(symbol>=63&&symbol<=126,"graph6 alphabet");
            edge[u][v]=edge[v][u]=((symbol-63)&(32u>>(position%6)))!=0;++position;}
        for(unsigned p=position;p%6;++p)need(((unsigned(g[1+p/6])-63)&(32u>>(p%6)))==0,"padding");
        std::vector<unsigned> triangles;
        for(unsigned i=0;i<n;++i)for(unsigned j=i+1;j<n;++j)for(unsigned k=j+1;k<n;++k)
            if(edge[i][j]&&edge[i][k]&&edge[j][k])triangles.push_back((1u<<i)|(1u<<j)|(1u<<k));
        std::vector<std::uint32_t> subcounts(size);
        for(unsigned subset=0;subset<size;++subset){bool valid=true;
            for(unsigned triangle:triangles)if((subset&triangle)==triangle){valid=false;break;}
            if(!valid)continue;
            unsigned rest=full^subset,added=rest;
            while(true){++subcounts[subset|added];++incidences;if(!added)break;added=(added-1)&rest;}
        }
        Wide positive,negative;
        for(unsigned subset=0;subset<size;++subset){int lo=profiles.get(),hi=profiles.get();need(lo>=0&&hi>=0,"missing profile");
            need(subcounts[subset]==unsigned(lo+256*hi),"entrywise subset profile differs");++profile_count;
            std::uint64_t t=subcounts[subset];need(t<=32768,"profile overflow bound");auto fourth=t*t*t*t;
            if((n-std::popcount(subset))%2)negative.add(fourth);else positive.add(fourth);
        }
        need(positive.high>negative.high||(positive.high==negative.high&&positive.low>=negative.low),"negative inclusion-exclusion");
        auto carry=std::uint64_t(positive.low<negative.low);auto high=positive.high-negative.high-carry;auto count=positive.low-negative.low;
        need(high==0&&count<=std::uint64_t(1)<<(4*n),"four-row result bound");
        need(count==expected_cover&&subcounts.back()==expected_free,"cover count differs");++records;
    }
    need(profiles.get()==std::char_traits<char>::eof(),"trailing profile");
    std::cout<<"{\"status\":\"INDEPENDENT_INCLUSION_EXCLUSION_CENSUS_VERIFIED\",\"records\":"<<records<<",\"profiles\":"<<profile_count<<",\"direct_incidences\":"<<incidences
             <<",\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"}\n";return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}}
