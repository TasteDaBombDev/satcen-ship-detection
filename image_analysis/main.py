import ijson
from PIL import Image, ImageDraw as Drawer

from action_enum import Action
from image_names import FILES_NAME

# CONSTANTS TO MODIFY:
# FILE_NAME - holds the name of the files in the dataset
# ACTION - is the action to be performed after the data collection is complete.
# It can have 2 values:
#   - VISUALISE (to see the actual image with all the bounding boxes of skiffs identified)
#   - PRINT (to print the pairs of coordinates, sorted per skiff


ACTION = Action.EXPORT


def main():
    """
    The main function of the program. Processes all the image data and prints the skiff coordinates or adds bounding boxes
    """
    json = ijson.items(open('../satcen_dataset/full/labels.json'), 'item')
    file_name = []
    for object_property in json:
        file_name.append(object_property['name'])
    
    print(file_name)
    


def process_image_data(file_name, json):
    """
    The function that processes the image data getting json file and directly selecting the list of annotations.
    The operation above builds a json that contains a list of all the annotations for all the skiffs in the dataset that
    looks like this:
    {[data], [data2], [data3], ...}
    Then, the json is filtered with a lambda function to contain only the object for the specified image
    Then, for each point of each bounding box of the skiffs form that image, it is build a pair if (x,y)
    The final array looks like this:
                       --- SKIFF 1 ---                                --- SKIFF 2 ---
    [ [(x11,y11), (x12, y12), (x13, y13), (x14, y14)], [(x21,y21), (x22, y22), (x23, y23), (x24, y24)], ... ]

    :return: matrix of pairs of coordinates
    """
    picture_object_metadata = filter(
        lambda annotation: annotation['name'] == file_name, json)

    for object_property in picture_object_metadata:
        all_points_list = [
            [
                (coordinate_pair['x'], coordinate_pair['y'])
                for coordinate_pair in identified_object['data']
            ]
            for identified_object in object_property['objects']
        ]
        return all_points_list


def add_rectangular_on_image(points_coordinates, image):
    """
    This function uses Drawer to add for each skiff a bounding box
    """
    initial_image = Imopen('../satcen_dataset/pictures/' + image)
    i = Image.new('RGB', (initial_image.width, initial_image.height))

    draw = Drawer.Draw(i)
    for points_list in points_coordinates:
        draw.polygon(points_list, outline="red")

    i.save('../satcen_dataset/labeled_images_binary/' + image, 'PNG')


# main call
main()
