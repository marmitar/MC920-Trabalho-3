import sys, cv2
import numpy as np
from matplotlib import pyplot as plt

import seaborn as sns
sns.set_theme(context='paper', style='darkgrid', palette='muted')

try:
    [_, filename, output] = sys.argv
except ValueError:
    [_, filename] = sys.argv
    output = None

img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

sns.histplot(x=img.flat, bins=np.arange(256), fill=False, color='k')
plt.xlabel('Intensidade')
plt.ylabel('Número de Pixels')

if output is None:
    plt.show()
else:
    plt.savefig(output)
