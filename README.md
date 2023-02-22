# Project Setup

## Repository and Dependencies

1. Clone repository
2. Create virtual environment
    ```
    python3 -m venv env
    ```
3. Start/stop virtual environment
    ```
    source env/bin/activate
    deactivate
    ```
4. Install dependencies (root folder)
    ```
    pip install -r requirements.txt
    ```

**NOTE:** Whenever you install a project, add it to the **requirements.txt** file using:
```
pip freeze > requirements.txt
```

## Kaggle

Kaggle should already be installed if you ran ```pip install -r requirements.txt```. You need to configure your credentials in order to be able to download the Airbus Dataset:

1. Get your credentials
    1. On Kaggle, go to your profile
    2. Click "Edit Public Profile"
    3. Under API, click on "Create New API Token": a **kaggle.json** file will be downloaded
    4. Copy and paste the contents of **kaggle.json** from your computer to another **kaggle.json** file in the root folder of the project

2. Move **kaggle.json** to the right place
    ```
    # move file
    mv kaggle.json ~/.kaggle/kaggle.json

    # change permissions
    chmod 600 ~/.kaggle/kaggle.json
    ```

## Download Datasets

### Airbus

1. In the root folder of the project run:
    ```
    kaggle competitions download -c airbus-ship-detection
    ```

2. Create the **airbus_dataset** folder:
    ```
    mkdir airbus_dataset
    mv airbus-ship-detection.zip airbus_dataset
    cd airbus_dataset
    ```

3. Unzip dataset:
    ```
    unzip airbus-ship-detection.zip
    ```

4. Create other folders (empty for now):
    ```
    mkdir train_v2_labels
    mkdir train_valid
    ```

5. Create **codes.txt** and put "background" and "ship" into it (each on a new line)


# Folder Structure

* **airbus_dataset:** dataset from the Airbus Ship Detection Challenge
    * **train_v2:** entire training dataset from the challenge (193k images with or without ships)
    * **test_v2:** test images from challenge (not really useful as we don't have ground truth)
    * **train_v2_labels:** png images representing the masks of the images (currently only for images that have at least one ship). Generated from run-length encoding. Values in the png are either 0 (background) or 1 (ship), because that's how fast.ai wants it
    * **train_valid:** training and validation data for the model. Contains 36k images with ships, the rest (6556) are for testing
    * **codes.txt:** mapping from integers to classes for the masks, needed by fast.ai. Only two values, background and ship
    * **results_unet:** raw outputs of Unet (trained only on 36k Airbus images with ships) saved as *.npy* files
    * **sample_submission_v2.csv:** from challenge, don't really need it
    * **train_ship_segmentation_v2.csv:** segmentation masks for the entire training dataset, in run-length encoding

* **satcen_dataset:** dataset from SatCen
    * **pictures:** all images from the dataset
    * **results_unet:** raw results of applying the trained Unet model on the Satcen images, in *.npy* format
    * **labels_images:** NOT USED - segmentations masks applied on images based on the provided JSON file, saved as png
    * **labels_images_binary:** BLACK and WHITE segmentations masks applied on images based on the provided JSON file, saved as png (black = no ship; white = ship)
    * **labels:** segmentations masks applied on images based on the provided JSON file, saved as png
    * **SatCen_skiffs256.json:** labels

* **image_analysis:** code to plot bounding boxes on SatCen images

* **ship_detection:**
    * **models:** saved models
        * **unet_googlenet.pth:** unet model with googlenet as encoder, trained for hardcoded epochs according to unet for ship detection papers

    * **unet.ipynb:** process data and train model