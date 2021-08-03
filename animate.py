import rasterio
from PIL import Image
from fast_shadow import shadow_calc
import imageio
import numpy as np

azimuth = 70.54
altitude = 37.876
scale = 9.78


# when importing a DSM use something like this
# with rasterio.open('dsm.xxxx.tif') as dsmlayer:
#    dsmimg = dsmlayer.read(1)

#creating an example dsm
dsm = np.zeros((1000, 1000))
dsm[300:400, 600:800] = 20
dsm[700:750, 300:700] = 3
dsm[100:300, 400:500] = 9



with imageio.get_writer('animation/animation.gif', mode='I') as writer:
    for x in range(0, 50):
        sh = shadow_calc(dsm, azimuth + x/2, altitude - x/4, scale, resample="bilinear")
        sh = sh*255
        writer.append_data(sh.astype(np.uint8))

