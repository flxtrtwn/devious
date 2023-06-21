#!/usr/bin/env python3

import subprocess

if __name__ == "__main__":
    subprocess.run(["dev", "verify"], check=True)
    subprocess.run(["dev", "test"], check=True)
