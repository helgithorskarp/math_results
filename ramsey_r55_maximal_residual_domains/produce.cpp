// Complete census: triangle-free subset indicators, subset zeta, fourth
// power, then Mobius inversion. All intermediate cover counts are nonnegative.
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
void need(bool ok,const char* why){if(!ok)throw std::runtime_error(why);}
int main(int argc,char** argv){try{
    need(argc==7,"usage: produce order graph6 start end counts.tsv profiles.bin");
    unsigned n=std::stoul(argv[1]),lo=std::stoul(argv[3]),hi=std::stoul(argv[4]);
    need(n>=1 && n<=15 && lo<hi,"range");unsigned size=1u<<n;
    std::ifstream input(argv[2]);std::ofstream output(argv[5]),profiles(argv[6],std::ios::binary);
    need(bool(input)&&bool(output)&&bool(profiles),"files");std::string line;
    std::uint64_t records=0,subsets=0;auto started=std::chrono::steady_clock::now();
    for(unsigned index=0;std::getline(input,line);++index){
        if(index<lo)continue;
        if(index>=hi)break;
        need(line.size()==1+(n*(n-1)/2+5)/6 && unsigned(line[0])==n+63,"graph6 framing");
        for(char c:line)need(c>=63&&c<=126,"graph6 character");
        std::vector<unsigned> adjacency(n);unsigned pos=0;
        for(unsigned v=1;v<n;++v)for(unsigned u=0;u<v;++u,++pos)
            if((unsigned(line[1+pos/6])-63)>>(5-pos%6)&1u){adjacency[u]|=1u<<v;adjacency[v]|=1u<<u;}
        for(unsigned k=pos;k%6;++k)need(!((unsigned(line[1+k/6])-63)>>(5-k%6)&1u),"graph6 padding");
        std::vector<unsigned char> free(size,1);
        for(unsigned s=1;s<size;++s){unsigned v=std::countr_zero(s),rest=s&(s-1);
            if(!free[rest]){free[s]=0;continue;}
            unsigned neighbors=rest&adjacency[v];
            while(neighbors){unsigned u=std::countr_zero(neighbors);neighbors&=neighbors-1;
                if(adjacency[u]&neighbors){free[s]=0;break;}}
        }
        std::vector<std::uint64_t> table(free.begin(),free.end());
        for(unsigned bit=0;bit<n;++bit)for(unsigned base=0;base<size;base+=2u<<bit)
            for(unsigned k=0;k<(1u<<bit);++k)table[base+(1u<<bit)+k]+=table[base+k];
        for(auto t:table){need(t<=32768,"profile range");profiles.put(char(t&255));profiles.put(char(t>>8));}
        auto free_count=table.back();
        for(auto& t:table){t*=t;t*=t;}
        for(unsigned bit=0;bit<n;++bit)for(unsigned base=0;base<size;base+=2u<<bit)
            for(unsigned k=0;k<(1u<<bit);++k){auto& a=table[base+(1u<<bit)+k];auto b=table[base+k];need(a>=b,"nonnegative partial cover");a-=b;}
        output<<index<<'\t'<<line<<'\t'<<free_count<<'\t'<<table.back()<<'\n';
        ++records;subsets+=size;
    }
    need(records==hi-lo,"incomplete range");need(bool(output)&&bool(profiles),"output failure");
    std::cout<<"{\"status\":\"COMPLETE_MOBIUS_COVER_CENSUS\",\"records\":"<<records<<",\"profiles\":"<<subsets
             <<",\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count()<<"}\n";
    return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}}
