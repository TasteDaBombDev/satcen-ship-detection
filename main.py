import ijson
from PIL import Image, ImageDraw as Drawer


def main():
    for prefix, the_type, value in ijson.parse(open('dataset/SatCen_skiffs256.json')):
        print(prefix, the_type, value)


def add_rectangular_on_image(points_list, image):
    i = Image.open(image)
    draw = Drawer.Draw(i)
    draw.rectangle(points_list, outline="red")
    i.show()


main()
# add_rectangular_on_image([(100, 100), (250, 250)], 'dataset/pictures/0-0-0.png')
