"""Fast CPU HOG + RGB histograms; improvement target is replacing/optimizing this baseline."""
from pathlib import Path
import numpy as np
from PIL import Image
from skimage.feature import hog

EXTS={'.jpg','.jpeg','.png','.bmp','.webp'}

def image_features(path):
    with Image.open(path) as im:
        rgb=np.asarray(im.convert('RGB').resize((64,64)),dtype=np.float32)/255
        gray=np.asarray(im.convert('L').resize((64,64)),dtype=np.float32)/255
    h=hog(gray,orientations=9,pixels_per_cell=(8,8),cells_per_block=(2,2),feature_vector=True)
    color=np.hstack([np.histogram(rgb[:,:,c],bins=8,range=(0,1),density=True)[0] for c in range(3)])
    return np.hstack([h,color]).astype('float32')

def collect(folder):
    folder=Path(folder)
    labels=['cardboard','glass','metal','paper','plastic','trash']
    paths=[]; y=[]
    for label in labels:
        root=folder/label
        if not root.exists(): raise FileNotFoundError(f'Khong thay thu muc {root}')
        for f in sorted(root.rglob('*')):
            if f.suffix.lower() in EXTS: paths.append(f);y.append(label)
    if not paths:raise RuntimeError('Khong tim thay anh hop le.')
    return paths,np.asarray(y)
