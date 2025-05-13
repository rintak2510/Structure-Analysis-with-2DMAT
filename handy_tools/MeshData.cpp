#include <vector>
#include <fstream>
#include <iostream>
#include <iomanip>

// linspace関数は前述のものを使用

int main() {
    std::vector<std::vector<double>> axes = {
        linspace(-0.3, -0.2, 101),   // a1
        linspace(13.1, 13.5, 21),    // z1
        linspace(-0.31, -0.28, 31),  // a0
        linspace(10.4, 10.8, 9)      // z0
    };

    std::ofstream fout("MeshData.txt");
    if (!fout) {
        std::cerr << "ファイルを開けませんでした。" << std::endl;
        return 1;
    }

    std::vector<size_t> indices(axes.size(), 0);
    int idx = 0;

    while (true) {
        // パラメータ値を取り出し
        double a1 = axes[0][indices[0]];
        double z1 = axes[1][indices[1]];
        double a0 = axes[2][indices[2]];
        double z0 = axes[3][indices[3]];

        // 制約条件
        if (z1 > z0) {
            fout << idx << " "
                 << std::fixed << std::setprecision(8)
                 << a1 << " " << -a1 << " "
                 << z1 << " " << a0 << " " << -a0 << " " << z0 << "\n";
            ++idx;
        }

        // インデックスを進める（多軸カウンタ）
        bool carry = true;
        for (int d = axes.size() - 1; d >= 0 && carry; --d) {
            if (++indices[d] >= axes[d].size()) {
                indices[d] = 0;
            } else {
                carry = false;
            }
        }
        if (carry) break;  // 全組み合わせ終了
    }

    fout.close();
    std::cout << "MeshData.txt に " << idx << " 行を書き込みました。" << std::endl;
    return 0;
}
