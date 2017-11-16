from imageio import get_writer, imread
from os import listdir

files = listdir('.')

with get_writer('images.gif', mode='I') as writer:
    for file in files[:]:
        if file.endswith(".png"):
            image = imread(file)
            writer.append_data(image)
            print("File {0:<8} processed...".format(file))
