```bash
pip install git+https://github.com/nlhepler/pydot.git

pip install git+https://github.com/NVIDIA/keras.git
pip install mxnet-cu80mkl

conda install graphviz pillow scikit-image matplotlib
```

# >= vtk 7.0
```bash
conda install -c menpo vtk
```

# >= opencv 3.3
```bash
conda install -c conda-forge opencv 
```

# OpenGV
```bash
cmake .
make
sudo make install
```

# ceres-solver
```bash
git clone https://ceres-solver.googlesource.com/ceres-solver
mkdir ceres-solver/build
cd ceres-solver/build
cmake \
    -D CMAKE_C_FLAGS="-fPIC" \
    -D CMAKE_CXX_FLAGS="-fPIC" \
    -D BUILD_EXAMPLES=OFF \
    -D BUILD_SHARED_LIBS=ON \
..
make -j $(($(nproc)+1))
sudo make install
```
