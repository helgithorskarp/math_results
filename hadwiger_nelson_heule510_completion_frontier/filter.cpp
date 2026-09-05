// Exhaustive modular superset of all unit-circumcircle triples.
// This filter makes no exact acceptance claim; audit.py supplies acceptance.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using U = std::uint64_t;
using Row = std::array<std::int64_t,16>;

struct Projection {
    U modulus;
    std::array<U,3> roots;
    std::vector<U> distances;
};

void project(Projection& f, const std::vector<Row>& points) {
    const U p=f.modulus;
    const std::array<U,3> primes={3,5,11};
    std::array<U,8> basis{};
    for (int bit=0;bit<3;++bit)
        if (f.roots[bit]*f.roots[bit]%p != primes[bit])
            throw std::runtime_error("invalid radical image");
    for (int mask=0;mask<8;++mask) {
        basis[mask]=1;
        for (int bit=0;bit<3;++bit)
            if (mask & (1<<bit)) basis[mask]=basis[mask]*f.roots[bit]%p;
    }
    std::vector<std::array<U,2>> xy(points.size());
    for (std::size_t v=0;v<points.size();++v)
        for (int axis=0;axis<2;++axis) {
            U total=0;
            for (int j=0;j<8;++j) {
                const auto value=points[v][8*axis+j];
                const U residue=static_cast<U>((value%static_cast<std::int64_t>(p)+static_cast<std::int64_t>(p))%static_cast<std::int64_t>(p));
                total=(total+residue*basis[j])%p;
            }
            xy[v][axis]=total;
        }
    const auto n=points.size();
    f.distances.assign(n*n,0);
    for (std::size_t i=0;i<n;++i)
        for (std::size_t j=i+1;j<n;++j) {
            U x=(xy[i][0]+p-xy[j][0])%p;
            U y=(xy[i][1]+p-xy[j][1])%p;
            f.distances[i*n+j]=f.distances[j*n+i]=(x*x+y*y)%p;
        }
}

bool survivor(U s,U t,U u,const Projection& f,U scale) {
    const U p=f.modulus;
    const U st=s*t%p, tu=t*u%p, us=u*s%p;
    const U squares=(s*s%p+t*t%p+u*u%p)%p;
    const U heron=(2*((st+tu+us)%p)+p-squares)%p;
    return st*u%p == (scale*scale%p)*heron%p;
}

int main(int argc,char** argv) {
    try {
        if (argc!=3) throw std::runtime_error("usage: filter points.txt survivors.tsv");
        std::ifstream in(argv[1]);
        std::size_t n=0; U scale=0;
        if (!(in>>n>>scale) || n<3 || n>510 || scale!=96)
            throw std::runtime_error("invalid point header");
        std::vector<Row> points(n);
        for (auto& row:points)
            for (auto& c:row)
                if (!(in>>c) || c < -144 || c > 144)
                    throw std::runtime_error("invalid coefficient");
        std::string trailing;
        if (in>>trailing) throw std::runtime_error("extra input data");
        Projection first{60289,{4799,25141,4267},{}};
        Projection second{1000081,{964569,816716,970601},{}};
        project(first,points); project(second,points);
        std::ofstream out(argv[2]);
        if (!out) throw std::runtime_error("cannot open output");
        U triples=0, stage1=0, stage2=0;
        for (std::size_t i=0;i<n;++i)
            for (std::size_t j=i+1;j<n;++j)
                for (std::size_t k=j+1;k<n;++k) {
                    ++triples;
                    if (!survivor(first.distances[i*n+j],first.distances[i*n+k],first.distances[j*n+k],first,scale)) continue;
                    ++stage1;
                    if (!survivor(second.distances[i*n+j],second.distances[i*n+k],second.distances[j*n+k],second,scale)) continue;
                    ++stage2;
                    out<<i<<' '<<j<<' '<<k<<'\n';
                }
        out.close();
        if (!out) throw std::runtime_error("output write failed");
        std::cout<<"{\"vertices\":"<<n<<",\"triples\":"<<triples
                 <<",\"first_survivors\":"<<stage1<<",\"second_survivors\":"<<stage2<<"}\n";
        return 0;
    } catch (const std::exception& e) {
        std::cerr<<e.what()<<'\n'; return 1;
    }
}
