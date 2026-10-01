// Literal integer-AP support census; independent of the ratio classifier.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

std::uint64_t choose(int n,int k) {
    if(n<k) return 0;
    if(k==2) return static_cast<std::uint64_t>(n)*(n-1)/2;
    if(k==3) return static_cast<std::uint64_t>(n)*(n-1)*(n-2)/6;
    throw std::invalid_argument("unsupported binomial coefficient");
}
void require(bool ok,const char* message) {if(!ok) throw std::runtime_error(message);}

int main(int argc,char** argv) {
    try {
        require(argc==4,"usage: support-census PRIME S BITMAP_OUTPUT");
        const int p=std::stoi(argv[1]),s=std::stoi(argv[2]);
        require(p>=7 && p<=617 && s>=1 && s<=6,"bounded seven-AP census domain");
        for(int d=2;d*d<=p;++d) require(p%d!=0,"modulus must be prime");
        const int n=6*p+s,m=p-s;
        const auto triples=choose(m,3);
        std::vector<std::uint8_t> bitmap(static_cast<std::size_t>((triples+7)/8),0);
        std::vector<std::uint64_t> c2(static_cast<std::size_t>(m)),c3(static_cast<std::size_t>(m));
        for(int r=0;r<m;++r) {c2[r]=choose(r,2); c3[r]=choose(r,3);}
        std::uint64_t aps=0,occurrences=0,realized=0;
        for(int step=1;step<=p;++step) for(int start=0;start+6*step<n;++start) {
            ++aps; std::array<int,7> residues{}; int length=0;
            for(int j=0;j<7;++j) {
                const int r=(start+j*step)%p;
                if(r>=s) residues[length++]=r-s;
            }
            for(int i=1;i<length;++i) {
                const int value=residues[i]; int j=i;
                while(j>0 && value<residues[j-1]) {residues[j]=residues[j-1]; --j;}
                residues[j]=value;
            }
            for(int j=1;j<length;++j) require(residues[j-1]!=residues[j],"ordinary column repeated in an AP");
            for(int i=0;i<length;++i) for(int j=i+1;j<length;++j) for(int k=j+1;k<length;++k) {
                const auto rank=static_cast<std::uint64_t>(residues[i])+c2[residues[j]]+c3[residues[k]];
                require(rank<triples,"colex rank outside triple domain");
                const auto byte=static_cast<std::size_t>(rank/8);
                const auto flag=static_cast<std::uint8_t>(1U<<(rank%8));
                if(!(bitmap[byte]&flag)) {bitmap[byte]|=flag; ++realized;}
                ++occurrences;
            }
        }
        require(aps==static_cast<std::uint64_t>(p)*(3*(p-1)+s),"incomplete literal AP census");
        std::ofstream out(argv[3],std::ios::binary);
        out.write(reinterpret_cast<const char*>(bitmap.data()),static_cast<std::streamsize>(bitmap.size()));
        out.close(); require(static_cast<bool>(out),"bitmap output failed");
        std::cout<<"{\"p\":"<<p<<",\"s\":"<<s<<",\"N\":"<<n<<",\"literal_APs\":"<<aps
                 <<",\"ordinary_triples\":"<<triples<<",\"AP_triple_occurrences\":"<<occurrences
                 <<",\"realized_triples\":"<<realized<<",\"unrealized_triples\":"<<triples-realized
                 <<",\"bitmap_bytes\":"<<bitmap.size()<<"}\n";
        return 0;
    } catch(const std::exception& e) {std::cerr<<"error: "<<e.what()<<'\n'; return 1;}
}
