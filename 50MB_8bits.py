import tifffile as tiff
import sys
import os
import glob
import numpy as np
import cv2





# --------------- Only change these parameters ---------------
# This is the target size of your images in MB. Should be lower than the original size, but will get ignored if not
targetSizeMB = 50 

# Target bit depth for the final image. Final 16-bit tiffs will be downsized a lot compared to 8-bit if the target file size in low (16-bit tiffs are twice as heavy as 8-bit tiffs of the same size)
# The program will not work correctly if choosing to output 16-bit files from 8-bit originals
targetDepth = 8
# ---------- Do not change anything under this line ----------





# Get the folder that the user has dropped on the script
droppedFolder = sys.argv[1]
print(droppedFolder)

# Convert target size to bits
targetSizeBits = targetSizeMB * 8388608

# Create target directory if it does not exist yet, according to the target bit depth
if targetDepth == 8:
    if not os.path.exists(f'{droppedFolder}/8_bits'):
        print('Creating folder for converted images')
        os.mkdir(f'{droppedFolder}/8_bits')
    else:
        print('Result folder already exists')
elif targetDepth == 16:
    if not os.path.exists(f'{droppedFolder}/16_bits'):
        print('Creating folder for converted images')
        os.mkdir(f'{droppedFolder}/16_bits')
    else:
        print('Result folder already exists')

# Iterate over all images with tiff-like extension in the folder
grabbed_files = glob.glob(f'{droppedFolder}/*.tif')
grabbed_files += glob.glob(f'{droppedFolder}/*.tiff')
grabbed_files += glob.glob(f'{droppedFolder}/*.TIF')
grabbed_files += glob.glob(f'{droppedFolder}/*.TIFF')

for f in grabbed_files:
    name = os.path.basename(f)
    location = os.path.dirname(f)
    print(name)

    img = None
    # Load images with the correct bit depth, mandatory to get correct values
    if targetDepth == 8:
        img = tiff.imread(f).astype(np.uint8)
    elif targetDepth == 16:
        img = tiff.imread(f).astype(np.uint16)

    # Get original dimensions of the image
    height, width, channels = img.shape

    # Capture original image aspect ratio to preserve it when resizing it down
    aspect = width/height
    print(f'\tAspect ratio : {aspect}')

    # Capture original image size in bits
    originalSize = channels * targetDepth * width * height
    print(f'\tSize (bits) : {originalSize}, {originalSize/8388608}MB')
    print(f'\tTarget size (bits) : {targetSizeBits}')

    # No need to resize the image if it is already less heavy than the target size
    if originalSize < targetSizeBits:
        print('\tOriginal file is already under the target size, not resizing')
    # Resize images that are heavier than the target size
    else:
        print('\tOriginal file is larger than target size, resizing')
        print(f'\tOriginal dimensions : {width}x{height}px')

        # Reduce the width pixel by pixel, and calculate the new image size, preserving aspect ratio, until the size is less than the target size
        for w in range(width, 0, -1):
            h = int(w/aspect)
            totalSize = channels * targetDepth * w * h
            # print(totalSize)
            
            # Break out of the loop once the new dimensions have been found 
            if totalSize <= targetSizeBits:
                break
        
        # Resize the image with the new dimensions, using cubic interpolation
        newWidth = w+1
        newHeight = int(newWidth/aspect)
        print(f'\tNew dimensions : {newWidth}x{newHeight}px')

        img = cv2.resize(img, (newWidth, newHeight), interpolation=cv2.INTER_CUBIC)

    # Save resized image under the correct folder
    if targetDepth == 16:
        tiff.imwrite(f'{location}/16_bits/{name}', img)
    elif targetDepth == 8:
        tiff.imwrite(f'{location}/8_bits/{name}', img.astype(np.uint8))
    else:
        print(f'\t\'{targetDepth}\' bit depth is incorrect, can\'t save')

# input('press Enter to escape')
