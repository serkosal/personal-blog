# init 
`sphinx-apidoc -o docs/source src/`

# generate docs
1. `cd docs`
2. run: 
  - on linux, mac:
  ```bash
  make -j$(nproc) html
  ```
  - windows: 
  ```bash 
  make.bat html
  ```

# docs coverage
```bash
sphinx-build -b coverage source build/coverage
```