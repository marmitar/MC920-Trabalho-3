import cv2, sys
import numpy as np


_, input = sys.argv

img = cv2.imread(input, cv2.IMREAD_GRAYSCALE)
if img is None:
    raise ValueError(f"imagem não encontrada: {input}")


branco = np.count_nonzero(img)
p_branco = branco / img.size
p_preto = 1 - p_branco
print(100 * p_preto)
