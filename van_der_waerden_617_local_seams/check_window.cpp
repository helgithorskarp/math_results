// Independent local-coordinate enumeration of the sharp seam window.
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <vector>

namespace {
constexpr int P = 617;
struct AP { std::array<int,7> y; };
int power(int x, int e) {
    int r=1;
    for (;e;e/=2,x=x*x%P) if (e%2) r=r*x%P;
    return r;
}
int positive_mod(int x) { return (x%P+P)%P; }

void check(int w, const std::array<int,P>& q) {
    std::vector<AP> aps;
    for (int d=1;6*d<2*w;++d)
        for (int a=0;a+6*d<2*w;++a) {
            if (!(a<w && a+6*d>=w)) continue;
            AP ap{};
            for (int j=0;j<7;++j) ap.y[j]=a+j*d;
            aps.push_back(ap);
        }
    const auto m=aps.size();
    std::vector<std::int8_t> l(P*m,-1),r(P*m,-1);
    for (int s=0;s<P;++s)
        for (std::size_t z=0;z<m;++z) {
            int masks[2]={0,0};
            bool hole[2]={false,false};
            for (const auto y:aps[z].y) {
                const int side=y>=w;
                const int color=q[positive_mod(y+s-w)];
                if (color<0) hole[side]=true;
                else masks[side]|=1<<color;
            }
            if (!hole[0] && masks[0]==1) l[s*m+z]=0;
            if (!hole[0] && masks[0]==2) l[s*m+z]=1;
            if (!hole[1] && masks[1]==1) r[s*m+z]=0;
            if (!hole[1] && masks[1]==2) r[s*m+z]=1;
        }
    std::uint64_t covered=0, diagonal=0;
    std::vector<std::array<int,3>> survivors;
    std::vector<std::array<int,5>> sharp_witnesses;
    for (int s=0;s<P;++s)
        for (int t=0;t<P;++t)
            for (int e=0;e<2;++e) {
                bool obstruction=false;
                for (std::size_t z=0;z<m;++z) {
                    if (l[s*m+z]<0 || r[t*m+z]<0 || l[s*m+z]!=(r[t*m+z]^e)) continue;
                    // Directly recheck all terms independently of half masks.
                    int common=-1;
                    for (int j=0;j<7;++j) {
                        const int y=aps[z].y[j];
                        const int phase=y<w ? s : t;
                        int color=q[positive_mod(y+phase-w)];
                        if (color<0) throw std::runtime_error("witness uses a pole");
                        if (y>=w) color^=e;
                        if (j==0) common=color;
                        else if (color!=common) throw std::runtime_error("invalid witness");
                    }
                    if ((s==154 && t==463 && e==1) || (s==155 && t==464 && e==1))
                        sharp_witnesses.push_back({s,t,e,aps[z].y[0]+P-w,aps[z].y[1]-aps[z].y[0]});
                    obstruction=true;break;
                }
                if (s==t && e==0) {
                    if (obstruction) throw std::runtime_error("compatible diagonal excluded");
                    ++diagonal;
                } else if (obstruction) ++covered;
                else survivors.push_back({s,t,e});
            }
    const std::vector<std::array<int,3>> expected = w==104 ?
        std::vector<std::array<int,3>>{{154,463,1},{155,464,1}} :
        std::vector<std::array<int,3>>{};
    if (survivors!=expected || covered+survivors.size()!=760761 || diagonal!=617)
        throw std::runtime_error("unexpected complete case classification");
    std::cout<<"{\"radius\":"<<w<<",\"crossing_aps\":"<<m
             <<",\"covered_incompatible_cases\":"<<covered<<",\"diagonal_survivors\":"<<diagonal
             <<",\"incompatible_survivors\":[";
    for (std::size_t i=0;i<survivors.size();++i) {
        if (i)std::cout<<',';
        const auto& v=survivors[i];std::cout<<'['<<v[0]<<','<<v[1]<<','<<v[2]<<']';
    }
    std::cout<<"],\"threshold_witnesses\":[";
    for (std::size_t i=0;i<sharp_witnesses.size();++i) {
        if(i)std::cout<<',';
        const auto& v=sharp_witnesses[i];
        std::cout<<'['<<v[0]<<','<<v[1]<<','<<v[2]<<','<<v[3]<<','<<v[4]<<']';
    }
    std::cout<<"]}";
}
}

int main() {
    try {
        const auto start=std::chrono::steady_clock::now();
        for (int d=2;d*d<=P;++d) if(P%d==0)throw std::runtime_error("nonprime modulus");
        std::array<int,P> q{};q[0]=-1;
        for (int x=1;x<P;++x) {
            const int symbol=power(x,308);
            if (symbol!=1 && symbol!=616)throw std::runtime_error("bad Euler symbol");
            q[x]=symbol==1 ? 0 : 1;
        }
        // Complete cyclic partial safety, including APs through a pole.
        std::uint64_t cyclic=0;
        for (int a=0;a<P;++a)for(int d=1;d<P;++d) {
            int mask=0;
            for(int j=0;j<7;++j) {
                const int color=q[(a+j*d)%P];
                if(color>=0)mask|=1<<color;
            }
            if(mask!=3)throw std::runtime_error("cyclic partial safety fails");
            ++cyclic;
        }
        // Recheck the elementary arbitrary-tail bridge from the earlier source.
        // Multiplicativity gives this from q(1-47j)=1; enumerate all multipliers.
        for (int multiplier=1;multiplier<P;++multiplier) {
            const int d=47*multiplier%P;
            for(int j=1;j<7;++j) {
                const int residue=positive_mod(multiplier-j*d);
                if(residue==0 || q[residue] != 1-q[multiplier])
                    throw std::runtime_error("saturation bridge fails");
            }
        }
        std::cout<<"{\"status\":\"VERIFIED\",\"windows\":[";
        check(104,q);std::cout<<',';check(105,q);
        std::cout<<"],\"cyclic_partial_cases\":"<<cyclic
                 <<",\"saturation_multiplier_cases\":616,\"seconds\":"
                 <<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"}\n";
    } catch(const std::exception& e) {
        std::cerr<<e.what()<<'\n';return EXIT_FAILURE;
    }
}
