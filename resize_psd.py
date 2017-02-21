#
# Resize PSD to jpg
# 
# Usage :  
# convert psd to jpg, with resizing function
#
# Author: Naoko Nishimura
#
# Date: 17/2/20
#


import os,shutil
from PIL import Image
from psd_tools import PSDImage

extension = "jpg"
resizeWidth = 1398
resizeHeight = 928
scaler = 'BICUBIC'
resample = {
    'ANTIALIAS': Image.ANTIALIAS,
    'BILINEAR': Image.BILINEAR,
    'BICUBIC': Image.BICUBIC
}


def outputfile(s):
    return "./jpg/" + s+ "." + extension

def inputfile(s):
    return "./psd/" + s 

print('-----------------------------------\n')
for folderName,subfolders,filenames in os.walk('./psd'):
        for myfilename in filenames:
                if(myfilename == ".DS_Store"):
                    continue
                print('input' + ':' + myfilename)
                fname,fext = os.path.splitext(myfilename)
                if(fext == ".psd"):
                    psd = PSDImage.load(inputfile(myfilename))
                    merged_image = psd.as_PIL()
                    merged_image = merged_image.resize((resizeWidth, resizeHeight),resample[scaler])
                    # print(merged_image)
                    merged_image.format = extension
                    merged_image.save(outputfile(fname),quality=100, optimize=True)
                    print('output' + ':' + outputfile(fname) + '\n-----------------------------------')
