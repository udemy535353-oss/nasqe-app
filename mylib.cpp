#include <iostream>
#include <cmath>

// Basit print
extern "C" void cpp_print(const char* text) {
    std::cout << text << std::endl;
}

// Toplama
extern "C" int add(int a, int b) {
    return a + b;
}

// Çarpma
extern "C" int multiply(int a, int b) {
    return a * b;
}

// Karekok
extern "C" double square_root(double x) {
    return std::sqrt(x);
}
