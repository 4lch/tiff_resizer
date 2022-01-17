# What does this program do ?
This little script is mainly intended to help photographic labs and photo professionals to downsize their tiff files to deliver consistent file sizes to their clients. This makes it easier to have a standard size for film scans for example, eg "20MB scans", etc.

Tiff files are uncompressed so the only ways to reduce their file size is to resize them (here, that means reducing the amount of pixels in the image), or to convert them from 16 to 8 bits. 8-bit files are 2x lighter than equivalent pixel resolution 16-bit files so when reducing the size of a 16-bit original, a 8-bit target will give larger final pixel dimensions, as every pixel is lighter, so the image doesn't have to be downsized as much.

This program lets you choose your target file size in MB and the target bit depth (8-bit is recommended, especially if you need to reduce the size by a lot).
It works with files with extensions '.tif', '.tiff', '.TIF' and '.TIFF'.

If the size of the original images is too high vs the target, it will resize the image down while preserving aspect ratio until the new resolution matches the target size in MB. If the original image size is already under the target, it will not get downsized any further.

# Installation
## Python installation
If you do not currently have python > 3.6 installed, please install it from the official Python website. This program has been tested to work fine with [Python 3.8](https://www.python.org/downloads/release/python-3810/) but should also be alright with later versions. 

Make sure that Python is added to your PATH during installation. You might need to restart your computer after installation for it to find the Python executable.

## Program and dependencies installation
You can download the folder in this repo to your computer with the green "Code" button on this repo. Once this is done, open up a terminal in this folder and run

```
pip install -r requirements.txt
```

This should install the required dependencies on your computer. If the program does not run fine, it might be necessary to install some manually. I had to install opencv manually for example (pip install opencv-python)

# Using the script
## Configuration
The program is contained in the file **"50MB_8bits.py"**, in reference to its default parameters, a 50MB / 8-bits target. This means that images converted by this script will be at most 50MB and will be saved in 8-bit.

The top of the program has a place for you to edit these parameters, it is not recommended to modify the rest of the program unless you know what you are doing.

This place to edit looks like this : 

``` python
# --------------- Only change these parameters ---------------
# This is the target size of your images in MB. Should be lower than the original size, but will get ignored if not
targetSizeMB = 50 

# Target bit depth for the final image. Final 16-bit tiffs will be downsized a lot compared to 8-bit if the target file size in low (16-bit tiffs are twice as heavy as 8-bit tiffs of the same size)
# The program will not work correctly if choosing to output 16-bit files from 8-bit originals
targetDepth = 8
# ---------- Do not change anything under this line ----------
```

- **targetSizeMB** should ideally be less than the expected original size of the files you want to convert (eg 50MB for 65MB originals).
- **targetDepth** is the bit depth for the final images. It is **either 8 or 16**. 16 will only work if the original images are already 16-bit images.

## Making it happen
Once everything is installed and configured, I recommend placing the script somewhere accessible easily (eg on your Desktop). You can duplicate it and change parameters and script names between copies to have different output options (eg one 120MB 16-bit script for high-res scans, one 20MB 8-bit script for medium res scans...)

To use the script, simply drag and drop the ***folder*** where the images to convert are saved from your explorer to the script. There is no need to move the images or folders around at all, just drag the folder to the script.

The script will then create a subfolder in the original, named either "8_bits" or "16_bits" depending on the selected target bit depth. This is where the resized images will be saved with their original names, so that no file is ever automatically overwritten.

