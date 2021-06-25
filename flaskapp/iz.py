if __name__=="__main__":
 print("Hello World!")
 
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np

def distr(img, fig, ax, name, f):
    res = np.array(img.histogram()).reshape(3,256)
    zer = np.arange(256)
    ax.fill_between(zer, res[0], alpha=0.4, color='red')
    ax.fill_between(zer, res[1], alpha=0.4, color='green')
    ax.fill_between(zer, res[2], alpha=0.4, color='blue')
    ax.set_xlabel('Color Intensity')
    ax.set_ylabel('Frequency')
    ax.set_title(name)
    fig.savefig(f)
    plt.cla()
    return res


def crops(img, vals):
    size = img.size
    resim = Image.new(img.mode, size)
    width = size[0] // 2
    height = size[1] // 2
    im_crop = [img.crop((0, 0, width, height)), img.crop((width, 0, size[0], height)),
               img.crop((0, height, width, size[1])), img.crop((width, height, size[0], size[1]))]

    for i in range(4):
        im_crop[i] = ImageEnhance.Contrast(im_crop[i]).enhance(vals[i])

    resim.paste(im_crop[0], (0, 0))
    resim.paste(im_crop[1], (width, 0))
    resim.paste(im_crop[2], (0, height))
    resim.paste(im_crop[3], (width, height))
    return resim


def subtracts(img):
    a = np.zeros((img.size[1]+1,img.size[0]+1,3),np.int16)
    b = a.copy()
    a[:-1,:-1,:] = np.array(img)
    b[1:,1:,:] = a[:-1,:-1,:]
    a -= b
    resim1 = Image.fromarray(np.uint8(a))
    a[a<0] = 0
    resim2 = Image.fromarray(np.uint8(a))
    return [resim1,resim2]    


def makegraphs(img, cval):
    file = img.filename
    res = [file, #0
    '.'.join(file.split('.')[:-1])+'graph.png', #1
    '.'.join(file.split('.')[:-1])+'new.'+file.split('.')[-1], #2
    '.'.join(file.split('.')[:-1])+'newgraph.png', #3
    '.'.join(file.split('.')[:-1])+'sub.'+file.split('.')[-1], #4
    '.'.join(file.split('.')[:-1])+'subgraph.png', #5
    '.'.join(file.split('.')[:-1])+'zerocapsub.'+file.split('.')[-1], #6
    '.'.join(file.split('.')[:-1])+'zerocapsubgraph.png'] #7
    print(res)
    fig, ax = plt.subplots(figsize=(10, 10))
    
    subs = subtracts(img)
    subs[0].save(res[4])
    distr(subs[0], fig, ax, res[4], res[5])
    subs[1].save(res[6])
    distr(subs[1], fig, ax, res[6], res[7])
    subs[0].close()
    subs[1].close()
    
    distr(img, fig, ax, name=res[0], f=res[1])

    img = crops(img,cval)
    img.save(res[2])
    img.close()
    img = Image.open(res[2])

    distr(img, fig, ax, res[2], res[3])
    img.close()
    
    
    print('savepaths: {}'.format(res))
    res = {res[0]:'Original Image', 
    res[1]:'Original Image color distribution graph', 
    res[2]:'Image with contrast modifiers {}, {}, {}, {}'.format(float(cval[0]), float(cval[1]), float(cval[2]), float(cval[3])), 
    res[3]:'New Image color distribution graph', 
    res[4]:'Image shifted by 1px subtracted from itself', 
    res[5]:'Subtracted image color distribution', 
    res[6]:'Image shifted by 1px subtracted from itself, min at zero', 
    res[7]: 'Subtracted image color distribution'}
    
    return res
