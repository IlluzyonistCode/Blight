# Blight

> *Automate everything, orchestrate everywhere, deliver instantly.*

![Python](https://img.shields.io/badge/Python-3776AB.svg?style=flat-square&logo=Python&logoColor=white)

## Overview

Blight is a Python CLI tool for remote system administration and deployment automation. It unifies network operations, process control, and file management into a single utility, enabling complex multi-step workflows to be defined and executed from one interface.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)

---

## Features

|      | Component       | Details                              |
| :--- | :-------------- | :----------------------------------- |
| ⚙️  | **Architecture**  | <ul><li>Monolithic Python application</li><li>No explicit architectural patterns visible</li></ul> |
| 🔩 | **Code Quality**  | <ul><li>No linting or formatting tools specified</li><li>No static analysis tools configured</li></ul> |
| 📄 | **Documentation** | <ul><li>No documentation files present</li><li>No docstrings or inline comments referenced</li></ul> |
| 🔌 | **Integrations**  | <ul><li>**OS-level integrations**: Screenshot capture (`pyscreenshot`)</li><li>**System monitoring**: Process management (`psutil`)</li><li>**Input handling**: Keyboard/mouse control (`pynput`)</li></ul> |
| 🧩 | **Modularity**    | <ul><li>Dependency management via `requirements.txt`</li><li>No explicit module structure information</li></ul> |
| ⚡️  | **Performance**   | <ul><li>No performance optimization tools</li><li>No profiling or benchmarking setup</li></ul> |
| 🛡️ | **Security**      | <ul><li>No security scanning tools</li><li>No authentication/authorization mechanisms visible</li></ul> |
| 📦 | **Dependencies**  | <ul><li>**Core**: `pillow`, `pynput`, `tabulate`, `psutil`, `colorama`</li><li>**Build**: `pyinstaller`</li><li>**Utilities**: `pyscreenshot`</li></ul> |

---

## Project Structure

```
└── Blight/
    ├── blight.py
    ├── LICENSE
    ├── README.md
    └── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.10+ / Node.js 18+ *(depending on the stack above)*

### Installation

```sh
git clone "https://github.com/IlluzyonistCode/Blight
cd Blight"
pip install -r requirements.txt
```

### Usage

```sh
python main.py
```

---

## Contributing

- [Report Issues](https://github.com/IlluzyonistCode/Blight/issues)
- [Submit Pull Requests](https://github.com/IlluzyonistCode/Blight/pulls)
- [Discussions](https://github.com/IlluzyonistCode/Blight/discussions)

---

## License

Distributed under the [AGPL-3.0](LICENSE) license.
