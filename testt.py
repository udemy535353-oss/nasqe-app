import ctypes
import os

# Define the library path using a raw string to handle backslashes correctly.
library_path = r"C:/Users/halim/OneDrive/Ekler/Masaüstü/MySQL/Machine Learning"

# --- Olası Hata Giderme ---
# Check if the mylib.dll file exists at the specified path.
if not os.path.exists(library_path):
    print(f"HATA: '{library_path}' dosya yolu mevcut değil.")
    print("Lütfen dosya yolunun doğru olduğundan ve dosyanın gerçekten bu konumda bulunduğundan emin olun.")
    exit()

# If the file exists but the error persists, it's likely due to missing dependencies.
# You need to copy the required DLLs from your MinGW-w64 bin directory.
# For example, from C:\msys64\mingw64\bin, copy the following files:
# libgcc_s_seh-1.dll, libstdc++-6.dll, and libwinpthread-1.dll
# Paste these files into the same directory as your mylib.dll file.
# ---

try:
    # Load the library.
    lib = ctypes.CDLL(library_path)
    print(f"'{library_path}' kütüphanesi başarıyla yüklendi.")

    # 1. Define the 'add' function.
    # Specify the argument and return types for Python.
    lib.add.argtypes = [ctypes.c_int, ctypes.c_int]  # Takes two integers.
    lib.add.restype = ctypes.c_int                   # Returns an integer.
    
    # 2. Define the 'multiply' function.
    lib.multiply.argtypes = [ctypes.c_int, ctypes.c_int] # Takes two integers.
    lib.multiply.restype = ctypes.c_int                  # Returns an integer.
    
    # 3. Define the 'square_root' function.
    # Use 'c_double' for the floating-point number.
    lib.square_root.argtypes = [ctypes.c_double]  # Takes a double.
    lib.square_root.restype = ctypes.c_double       # Returns a double.

    print("Fonksiyon tipleri tanımlandı.")

    # Use the functions.
    result_add = lib.add(5, 7)
    print(f"5 + 7 = {result_add}")

    result_multiply = lib.multiply(6, 5)
    print(f"6 * 5 = {result_multiply}")
    
    result_sqrt = lib.square_root(16.0)
    print(f"16'nın karekökü = {result_sqrt}")

except OSError as e:
    print(f"Hata: Kütüphane yüklenemedi. '{library_path}' dosyasının varlığından emin ol.")
    print(f"Hata detayı: {e}")
except AttributeError as e:
    print(f"Hata: Fonksiyonlar bulunamadı veya tipleri yanlış tanımlandı. Hata detayı: {e}")
