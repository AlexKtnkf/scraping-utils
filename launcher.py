import os
import subprocess

# boucle sur les fichiers python dans le repertoire et les executes
for result in os.listdir('./scripts/'):
    if result.endswith(".py"):
        subprocess.call('start python ' + ('./scripts/' + result), shell=True)

