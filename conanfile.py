from conans import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout

class EpanetConan(ConanFile):
    name = "epanet"
    version = "2.2"
    description = "EPANET is an industry-standard program for modeling the hydraulic and water quality behavior of water distribution system pipe networks."
    homepage = "https://github.com/OpenWaterAnalytics/EPANET"
    url = "https://github.com/OpenWaterAnalytics/EPANET"
    license = "MIT"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    exports_sources = "CMakeLists.txt", "src/*", "include/*", "run/*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("lib/libepanet2.dylib", "lib", keep_path=False)
        self.copy("lib/libepanet-output.dylib", "lib", keep_path=False)
        self.copy("*.h", "include", "include", keep_path=False)
        self.copy("types.h", "include", "src", keep_path=False)
        self.copy("hash.h", "include", "src", keep_path=False)

    def package_info(self):
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.libs = ["epanet2", "epanet-output"]
        self.cpp_info.includedirs = ["include"]
