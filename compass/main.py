import subprocess
import sys

scripts = [
    "compass/gerar_bases_ruidosas.py",
    "compass/pre-processar-datasets.py",
    "compass/index_block.py",
    "compass/compare.py",
    "compass/classificador.py",
]

for script in scripts:
    subprocess.run([sys.executable, script])
