import numpy as np
from PIL import Image
import PIL
import matplotlib.pyplot as plt

# MIT Licensed (see License text at the bottom


def rotate_image(a, angle, resample="nearest"):
    if resample == "bilinear":
        resampling_method = PIL.Image.BILINEAR
    elif resample == "nearest":
        resampling_method = PIL.Image.NEAREST
    else:
        raise ValueError(f'option "{resample}" not recognised')
    img = Image.fromarray(a)
    img_rotated = img.rotate(angle=angle, expand=True, resample=resampling_method)  # TODO: decide on resampling method
    return np.array(img_rotated)


def shadow_calc(a, azimuth, altitude, scale, resample="bilinear"):
    """a: DSM , azimuth: 0-360 degrees, altitude:0-90, scale: how high are the features on the dsm
    resample [bilinear or nearest]"""
    if altitude == 90:  # everything gets hit if the sun is shining straight down
        return np.ones(a.shape, dtype=np.double)

    azimuth = azimuth - 90  # turning for calculations
    altitude = altitude*np.pi/180
    tan_altitude = np.tan(altitude)
    min_a = np.min(a)
    a = a - min_a  # make the lowest point even with surroundings when turning
    a = a * scale
    original_shape = a.shape
    # calculate the maximum number of places to check later
    max_a = np.max(a)
    max_hops = round(max_a // tan_altitude + 1)

    rotated = rotate_image(a, azimuth, resample)

    # tilt image by altitude degrees
    n, m = rotated.shape

    tilt_vector = - np.arange(n)*tan_altitude  # create a vector with the same shape as the rotated image
    tilted = rotated + tilt_vector

    highest_exponent = np.ceil(np.log2(max_hops))
    shifts = [2**x for x in range(highest_exponent.astype(np.int32)+1)]
    filled = tilted.copy()
    cumulative_shift = 0
    for shift in shifts:  # shift one plane across the other and fill all concave parts that way
        cumulative_shift += shift
        filled[:, :-cumulative_shift] = np.fmax(filled[:, :-cumulative_shift], filled[:, cumulative_shift:])

    shadows = np.greater(filled, tilted)
    shadows = np.logical_not(shadows)
    shadows = np.double(shadows)

    # rotate back
    shadows = rotate_image(shadows, -azimuth, resample)
    new_shape = shadows.shape
    x_offset = (new_shape[0] - original_shape[0])//2
    y_offset = (new_shape[1] - original_shape[1])//2
    x_remainder = (new_shape[0] - original_shape[0]) % 2
    y_remainder = (new_shape[1] - original_shape[1]) % 2
    if x_offset != 0 and y_offset != 0:
        shadows = shadows[x_offset + x_remainder:-x_offset, y_offset + y_remainder:-y_offset]

    plt.imshow(shadows)
    plt.show()
    plt.imshow(a[360:480, 200:500])
    plt.show()
    return shadows


# Copyright © 2021 Magnus Balzer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


