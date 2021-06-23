if __name__=="__main__"
 print("Hello World!")
 
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np

def distr(img):
    img = np.array(img)
    (Image_Height, Image_Width, Image_Channels) = img.shape

    res = np.zeros([256, Image_Channels], np.int32)

    for y in range(Image_Height):
        for x in range(Image_Width):
            for c in range(Image_Channels):
                res[img[y, x, c], c] += 1
    return res


def makegraphs(img, cval):
    file = img.filename
    res = [img.filename, '.'.join(poo.split('.')[:-1]) + 'graph.png', 'new' + file, 'new' + '.'.join(poo.split('.')[:-1]) + 'graph.png']
    img.save(res[0])

    fig, ax = plt.subplots(figsize=(10, 10))
    zer = np.arange(256)

    origgraph = distr(img)
    ax.fill_between(zer, origgraph[:, 0], alpha=0.4, color='red')
    ax.fill_between(zer, origgraph[:, 1], alpha=0.4, color='green')
    ax.fill_between(zer, origgraph[:, 2], alpha=0.4, color='blue')
    ax.set_xlabel('Color Intensity')
    ax.set_ylabel('Frequency')
    ax.set_title(res[0])
    fig.savefig(res[1])
    plt.cla()

    newimg = ImageEnhance.Contrast(img)
    img = newimg.enhance(cval)
    img.save(res[2])
    img = Image.open(res[2])

    newgraph = distr(img)
    ax.fill_between(zer, newgraph[:, 0], alpha=0.4, color='red')
    ax.fill_between(zer, newgraph[:, 1], alpha=0.4, color='green')
    ax.fill_between(zer, newgraph[:, 2], alpha=0.4, color='blue')
    ax.set_xlabel('Color Intensity')
    ax.set_ylabel('Frequency')
    ax.set_title(res[2])
    fig.savefig(res[3])

    return res
