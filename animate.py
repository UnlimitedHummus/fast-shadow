import rasterio
from PIL import Image
from fast_shadow import shadow_calc
import imageio
import numpy as np


azimuth = 70.54
altitude = 37.876
scale = 6.78


with rasterio.open('dsm.xxxx.tif') as dsmlayer:
    dsmimg = dsmlayer.read(1)


with imageio.get_writer('animation/animation.gif', mode='I') as writer:
    for x in range(0, 36):
        sh = shadow_calc(dsmimg, azimuth + x, altitude - x/2, scale, resample="nearest")
        sh = sh*255
        writer.append_data(sh.astype(np.uint8))

