// GCParallel.cpp : Defines the entry point for the application.
//

#include<fstream>
#include<iostream>
#include<algorithm>
#include<iterator>
#include<vector>
#include<utility>
#include<chrono>
#include<omp.h>
#include "GCParallel.h"
#include<thread>

using namespace std;
using namespace std::chrono;

// Helper types
using uint = unsigned int;
using int64 = long long;
using intpair = pair<int, int>;

// Custom pair a<b
struct mpair
{
	int a, b;

	mpair() : a(0), b(0) {}
	mpair(int a0, int b0) : a(std::min(a0, b0)), b(std::max(a0, b0)) {}
};

fstream fin;
uint n;	// Number of Nodes
uint m;	// Number of Edges
uint dmax; // Maximum degree in Graph

vector<mpair> edges;
vector<uint> deg;

int **adj; // adj[x] - adjacency list of node x
intpair **inc; // inc[x] - incidence list of node x: (y, edge id)
bool adjacent_list(int x, int y) { return binary_search(adj[x], adj[x] + deg[x], y); }
int *adj_matrix; // compressed adjacency matrix
const int adj_chunk = 8 * sizeof(int);
bool adjacent_matrix(int x, int y) { return adj_matrix[(x*n + y) / adj_chunk] & (1 << ((x*n + y) % adj_chunk)); }
bool(*adjacent)(int, int);

int64 **orbit; // orbit[x][o] - how many times does node x participate in orbit o
vector<int> wflag;

int threads;

bool operator<(const mpair &x, const mpair &y)
{
	if (x.a == y.a) return x.b < y.b;
	else return x.a < y.a;
}
bool operator==(const mpair &x, const mpair &y)
{
	return x.a == y.a && x.b == y.b;
}

void printorbit3();
void rageTriangleCount();
void triGraphletCount();
void twoStarCount();
void triadcensus();

int main(int argc, char** argv)
{
	//if (argc < 2) 
	//{
	//	std::cerr << "Incorrect number of arguments.\n";
	//	std::cerr << "Usage: GCParallel [graph - input file] [(opt)threads - number of threads to use]\n";
	//	return 0;
	//}

	// dense
	//fin.open("frb100-40.mtx", fstream::in);

	// sparse
	//fin.open("dbpedia-country.edges", fstream::in);

	fin.open("5test.mtx", fstream::in);
	if (fin.fail())
	{
		cerr << "Failed to open file " << argv[2] << endl;
		return 0;
	}
	fin >> n >> m;
	edges.resize(m);
	deg.resize(n);
	wflag.resize(n);

	threads = 8;// atoi(argv[2]); // Thread count change here (testing)

	if (m < 100)
		threads = 1;	// force single thread for small graphs

	bool flag = true;
	for (uint i = 0; i < m; i++)
	{
		int a, b;
		fin >> a >> b;
		if (!(0 <= a && a < n) || !(0 <= b && b < n)) {
			cerr << "Node ids should be between 0 and n-1." << endl;
			return 0;
		}
		if (a == b) {
			if (flag)
			{
				cerr << "Data contains Self loops which are not allowed. Omitting self loops." << endl;
				flag = false;
			}
			continue;
		}
		deg[a]++; deg[b]++;
		edges[i] = mpair(a, b);
	}
	for (int i = 0; i < n; i++)
		dmax = max(dmax, deg[i]);

	printf("nodes: %d\n", n);
	printf("edges: %d\n", m);
	printf("max degree: %d\n", dmax);
	fin.close();

	// set up adjacency matrix if it's smaller than 100MB
	if ((int64)n*n < 100LL * 1024 * 1024 * 8)
	{
		adjacent = adjacent_matrix;
		adj_matrix = (int*)calloc((n*n) / adj_chunk + 1, sizeof(int));
		for (int i = 0; i < m; i++)
		{
			int a = edges[i].a, b = edges[i].b;
			adj_matrix[(a*n + b) / adj_chunk] |= (1 << ((a*n + b) % adj_chunk));
			adj_matrix[(b*n + a) / adj_chunk] |= (1 << ((b*n + a) % adj_chunk));
		}
	}
	else
		adjacent = adjacent_list;

	// set up adjacency, incidence lists
	adj = (int**)malloc(n * sizeof(int*));
	for (int i = 0; i < n; i++)
		adj[i] = (int*)malloc(deg[i] * sizeof(int));

	inc = (intpair **)malloc(n * sizeof(intpair*));
	for (int i = 0; i < n; i++)
		inc[i] = (intpair*)malloc(deg[i] * sizeof(intpair));

	int *d = (int*)calloc(n, sizeof(int));
	for (int i = 0; i < m; i++)
	{
		int a = edges[i].a, b = edges[i].b;
		adj[a][d[a]] = b; adj[b][d[b]] = a;
		inc[a][d[a]] = intpair(b, i); inc[b][d[b]] = intpair(a, i);
		d[a]++; d[b]++;
	}

	for (int i = 0; i < n; i++)
	{
		sort(adj[i], adj[i] + deg[i]);
		sort(inc[i], inc[i] + deg[i]);
	}

	// initialize orbit counts
	orbit = (int64**)malloc(n * sizeof(int64*));
	for (int i = 0; i < n; i++)
		orbit[i] = (int64*)calloc(73, sizeof(int64));

	cout << "Using " << threads << " threads\n";

	// Begin Algorithm

	//cout << "Rage\n";
	//rageTriangleCount();
	//cout << "two stars only\n";
	//twoStarCount();
	//cout << "three cycles only\n";
	//triGraphletCount();
	//cout << "two star + three cycle\n";
	//twoStarCount();
	//triGraphletCount();

	cout << "Triad census\n";
	triadcensus();

	printorbit3();

	system("pause");
	return 0;
}

void rageParallelBreak(int tnum)
{
	int u, w;
	for (int v = 0; v < n; v += threads + tnum)
	{
		for (int i = 0; i < deg[v]; i++)
		{
			u = adj[v][i];
			if (v < u)
			{
				for (int u_i = 0; u_i < deg[u]; u_i++)
				{
					w = adj[u][u_i];

					if (w <= v)
						continue;

					if (adjacent(v, w))		// constant time or log(n) depending on matrix or list
					{
						if (w <= u)
						{
							orbit[v][3]++;
							orbit[u][3]++;
							orbit[w][3]++;
						}
					}
					else
					{
						orbit[v][1]++;
						orbit[u][2]++;
						orbit[w][1]++;
					}
				}
			}
		}
	}
}

void rageTriangleCount()
{
	auto start = high_resolution_clock::now();


	//#pragma omp parallel for

	vector<thread> tvec;
	tvec.reserve(threads);

	for (int i = 0; i < threads; i++)
		tvec.push_back(thread(rageParallelBreak, i));
	for (int i = 0; i < threads; i++)
		tvec[i].join();

	auto stop = high_resolution_clock::now();

	duration<float> secs = stop - start;

	cout << "Time taken: " << secs.count() << "\n";
}

void triGraphletParallel(int tnum)
{
	for (int v = 0; v < n; v += threads + tnum)
	{
		for (int i = 0; i < (int(deg[v]) - 1); i++)
		{
			for (int j = i + 1; j < deg[v]; j++)
			{
				int u = adj[v][i];
				int w = adj[v][j];
				if (deg[u] > deg[v] && deg[w] > deg[v] && adjacent(u, w))
				{
					orbit[v][3]++;
					orbit[u][3]++;
					orbit[w][3]++;
				}
			}
		}
	}
}

void triGraphletCount()
{
	auto start = high_resolution_clock::now();

	vector<thread> tvec;
	tvec.reserve(threads);

	for (int i = 0; i < threads; i++)
		tvec.push_back(thread(triGraphletParallel, i));
	for (int i = 0; i < threads; i++)
		tvec[i].join();


	auto stop = high_resolution_clock::now();
	duration<float> secs = stop - start;
	cout << "Time taken: " << secs.count() << "\n";
}

void twoStarParallel(int tnum)
{
	for (int v = 0; v < n; v += threads + tnum)
	{
		for (int i = 0; i < deg[v]; i++)
		{
			int u = adj[v][i];

			if (v < u)
			{
				vector<int> uList(adj[u], adj[u] + deg[u]);
				vector<int> vList(adj[v], adj[v] + deg[v]);
				vector<int> difflist;
				//vector<int> intersectionlist(min(uList.size(), vList.size()));
				std::set_difference(uList.begin(), uList.end(), vList.begin(), vList.end(),
					std::inserter(difflist, difflist.begin()));
				difflist.erase(std::remove_if(difflist.begin(), difflist.end(), [v](int x) {return x <= v; }), difflist.end());

				//auto it = std::set_intersection(uList.begin(), uList.end(), vList.begin(), vList.end(), intersectionlist.begin());
				//intersectionlist.resize(it - intersectionlist.begin());

				for (auto w : difflist)
				{
					if (w > v)
					{
						orbit[v][1]++;
						orbit[u][2]++;
						orbit[w][1]++;
					}
				}
				//for (auto w : intersectionlist)
				//{
				//	if (w <= v || w <= u)
				//		continue;
				//	orbit[v][3]++;
				//	orbit[u][3]++;
				//	orbit[w][3]++;
				//}
			}
		}
	}
}

void twoStarCount()
{
	auto start = high_resolution_clock::now();

	vector<thread> tvec;
	tvec.reserve(threads);

	for (int i = 0; i < threads; i++)
		tvec.push_back(thread(twoStarParallel, i));
	for (int i = 0; i < threads; i++)
		tvec[i].join();


	auto stop = high_resolution_clock::now();
	duration<float> secs = stop - start;
	cout << "Time taken: " << secs.count() << "\n";
}


void triadparallel(int tnum)
{
	for (int i = 0; i < edges.size(); i += threads + tnum)
	{
		mpair e = edges[i];
		int u = e.a;
		int v = e.b;

		for (int u_i = 0; u_i < deg[u]; u_i++)
		{
			int w = adj[u][u_i];
			if (w == v)
				continue;
			wflag[w] = 1;
		}

		for (int v_i = 0; v_i < deg[v]; v_i++)
		{
			int w = adj[v][v_i];
			if (w == u)
				continue;
			if (wflag[w] == 1)
			{
				// value /3
				// u,v,w triangle
				orbit[u][3]++;
				orbit[v][3]++;
				orbit[w][3]++;
			}
			else
			{
				//TODO: Fix, incorrect values
				// u,v,w two star
				orbit[u][1]++;
				orbit[v][2]++;
				orbit[w][1]++;
			}
			wflag[w] = 0;
		}
	}
}

void triadcensus()
{
	auto start = high_resolution_clock::now();

	vector<thread> tvec;
	tvec.reserve(threads);

	for (int i = 0; i < threads; i++)
		tvec.push_back(thread(triadparallel, i));
	for (int i = 0; i < threads; i++)
		tvec[i].join();


	auto stop = high_resolution_clock::now();
	duration<float> secs = stop - start;
	cout << "Time taken: " << secs.count() << "\n";

}


void printorbit3()
{
	for (int i = 0; i < n; i++)
		cout << orbit[i][1] << " " << orbit[i][2] << " " << orbit[i][3] << "\n";
}
