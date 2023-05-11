# Tauri, a desktop bundler

We assume Rust is available on your system

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## Install tauri

```bash
cargo install tauri-cli
```

## Setup

Python setup for building sidecar as single file.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install trame pyinstaller

python -m PyInstaller \
    --clean --noconfirm \
    --distpath src-tauri \
    --name server \
    --hidden-import pkgutil \
    --collect-data trame_client \
    --collect-data trame_components \
    --collect-data trame_vuetify \
    --collect-data trame_vtk \
    server.py

cd src-tauri
cargo tauri icon
cargo tauri build

open target/release/bundle/macos/Cone.app
```
