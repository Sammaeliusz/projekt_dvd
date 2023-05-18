from PIL import Image
import os

directory = os.getcwd()
c=1
for filename in os.listdir(directory):
    if filename.endswith(".jpeg"):
        im = Image.open(filename)
        name=filename[:-5]+'.png'
        rgb_im = im.convert('RGB')
        rgb_im.save(name)
        c+=1
        print(os.path.join(directory, filename))
        continue
    else:
        continue
