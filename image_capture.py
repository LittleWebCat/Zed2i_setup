########################################################################
#
# Copyright (c) 2022, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################
import pyzed.sl as sl
import cv2
import numpy as np


def main():
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.AUTO # Use HD720 opr HD1200 video mode, depending on camera type.
    init_params.camera_fps = 30  # Set fps at 30

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Camera Open : "+repr(err)+". Exit program.")
        exit()


    # Capture 50 frames and stop
    i = 0
    image_lft = sl.Mat()
    image_rgt = sl.Mat()
    runtime_parameters = sl.RuntimeParameters()
    while i < 50:
        # Grab an image, a RuntimeParameters object must be given to grab()
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # A new image is available if grab() returns SUCCESS
            zed.retrieve_image(image_lft, sl.VIEW.LEFT)
            zed.retrieve_image(image_rgt, sl.VIEW.RIGHT)
            img_cv_lft = image_lft.get_data()
            img_cv_rgt = image_rgt.get_data()
            img_cv_lft = cv2.cvtColor(img_cv_lft, cv2.COLOR_RGBA2RGB)
            img_cv_rgt = cv2.cvtColor(img_cv_rgt, cv2.COLOR_RGBA2RGB)

            combined_img = np.hstack((img_cv_lft, img_cv_rgt))

            cv2.imwrite(f"/home/adas/zed2i_img/img_comb/frame_{i:03d}_comb.png", combined_img)
            cv2.imwrite(f"/home/adas/zed2i_img/img_lft/rame_{i:03d}_lft.png", img_cv_lft)
            cv2.imwrite(f"/home/adas/zed2i_img/img_rgt/frame_{i:03d}_rgt.png", img_cv_rgt)

            # timestamp = zed.get_timestamp(sl.TIME_REFERENCE.CURRENT)  # Get the timestamp at the time the image was captured
            # print("Image resolution: {0} x {1} || Image timestamp: {2}\n".format(image_lft.get_width(), image_lft.get_height(),
                #   timestamp.get_milliseconds()))
            i = i + 1

    # Close the camera
    zed.close()

if __name__ == "__main__":
    main()
