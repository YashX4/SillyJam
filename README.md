# readme:

A small [raylib](https://www.raylib.com/) game written in Python, managed with [uv](https://docs.astral.sh/uv/).

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) (handles Python and dependencies)
- Python 3.12+ (uv will install it automatically if missing)

## Setup

Install dependencies into a local virtual environment:

```bash
uv sync
```

This reads [pyproject.toml](pyproject.toml) and pins exact versions from [uv.lock](uv.lock).

## Run

```bash
uv run python main.py
```

`uv run` activates the project environment automatically — no need to manually create or activate a venv. A window titled "Hello raylib from Python" should open.



## building for web:
To build for web we use pygbag. It builds a WASM vesion of the game which can be accessed over a small hosted server.
To build and launch a webserver with the WASM version use command: 
```bash
uv run pygbag main.py
``` 

## building binaries for windows, mac, linux:
(oto TODO:)