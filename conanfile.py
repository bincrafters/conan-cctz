#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class CCTZConan(ConanFile):
    name = "cctz"
    version = "20180206"
    commit_id = "e19879df3a14791b7d483c359c4acd6b2a1cd96b"
    url = "https://github.com/bincrafters/conan-cctz"
    description = "C++ library for translating between absolute and civil times"
    license = "Apache 2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    source_subfolder = "source_subfolder"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False], 
        "build_testing" : [True, False], 
        "build_examples" : [True, False], 
        "fpic": [True, False]
    }
    
    default_options = (
        "shared=False", 
        "build_testing=False", 
        "fpic=False",
        "build_examples=False"
    )
    

    def requirements(self):
        if self.options.build_testing:
            self.requires("gtest/1.8.0@bincrafters/stable")

    def configure(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")
            
    def source(self):
        source_url = "https://github.com/google/cctz"
        tools.get("{0}/archive/{1}.zip".format(source_url, self.commit_id))
        extracted_dir = "cctz-" + self.commit_id
        os.rename(extracted_dir, self.source_subfolder)


    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_EXAMPLES"] = self.options.build_examples
        cmake.definitions["BUILD_TESTING"] = self.options.build_testing
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        cmake.configure()
        cmake.build()

    def package(self):
        include_folder = os.path.join(self.source_subfolder, "include")
        self.copy(pattern="LICENSE.txt", dst="license", src=self.source_subfolder)
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)


    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")