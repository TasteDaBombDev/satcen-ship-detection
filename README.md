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

### Using Detectron2

When using the Detectron2 library, you need to use a different virtual environment, due to conflicting verions of PyTorch used by fast.ai and Detectron2. Create the virtual environment in the same way as above and install the dependencies from the **requirements_detectron2.txt** file. **IMPORTANT:** Do **NOT** include PyTorch and Detectron2 in the requirements file (these should be installed separately). 

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
    mkdir splits/train/images
    mkdir splits/test/images
    ```

5. Create **codes.txt** and put "background" and "ship" into it (each on a new line)


# Folder Structure

* **airbus_dataset:** dataset from the Airbus Ship Detection Challenge
    * **splits:** contains the 80-20 train-test split (only ship images) used to train the final U-Net model
    * **train_v2:** entire training dataset from the challenge (193k images with or without ships)
    * **test_v2:** test images from challenge (not really useful as we don't have ground truth)
    * **train_v2_labels:** png images representing the masks of the images (currently only for images that have at least one ship). Generated from run-length encoding. Values in the png are either 0 (background) or 1 (ship), because that's how fast.ai wants it
    * **train_valid:** training and validation data for the model. Contains 36k images with ships, the rest (6556) are for testing
    * **codes.txt:** mapping from integers to classes for the masks, needed by fast.ai. Only two values, background and ship
    * **results_unet:** raw outputs of Unet (trained only on 36k Airbus images with ships) saved as *.npy* files
    * **sample_submission_v2.csv:** from challenge, don't really need it
    * **train_ship_segmentation_v2.csv:** segmentation masks for the entire training dataset, in run-length encoding

* **satcen_dataset:** dataset from SatCen
    
    * **full:** contains both original images and the additional ones
        * **ground_truth_masks:** BLACK and WHITE segmentations masks applied on images based on the *labels.json* file, saved as png (black = no ship; white = ship)
        * **pictures:** RGB images
        * **unet_valid_outputs:** Decoded results of U-net on the validation set (format of files in this folder is *filename_unet_out.npy*)
        * **splits:** stratified 60-20-20 train-validation-test splits (used when training Unet)
            * **train/images:** training data
            * **validation/images:** validation data
            * **test/images:** test data
        * **splits_70_30:** stratified 70-30 train-test splits (used when training Unet)
            * **train/images:** training data
            * **test/images:** test data
        * **labels.json:** ground truth 
        * **codes.txt:** mapping from integers to classes for the masks, needed by fast.ai. Only two values, background and ship
    * **original:** original dataset received from Satcen
        * **pictures:** all images from the dataset
        * **results_unet:** raw results of applying the trained Unet model on the Satcen images, in *.npy* format
        * **labels_images:** NOT USED - segmentations masks applied on images based on the provided JSON file, saved as png
        * **labels_images_binary:** BLACK and WHITE segmentations masks applied on images based on the provided JSON file, saved as png (black = no ship; white = ship)
        * **labels:** segmentations masks applied on images based on the provided JSON file, saved as png
        * **SatCen_skiffs256.json:** labels
        * **codes.txt:** mapping from integers to classes for the masks, needed by fast.ai. Only two values, background and ship

* **image_analysis:** code to plot bounding boxes on SatCen images

* **misc:** miscellaneous files used for working with the datasets etc.
    * **satcen_handling.ipynb:** handles the addition of new images to the Satcen dataset

* **ship_detection:**
    * **models:** saved models
        * **faster_rcnn_rrpn:** 
            * **model_final.pth:** Faster R-CNN model trained only on Satcen images (60-20-20 split)
        * **unet_airbus_80_20.pth:** unet model trained on 80% of Airbus ship images
        * **unet_googlenet.pth:** unet model with googlenet as encoder, trained on ship images from Airbus for hardcoded epochs according to unet for ship detection papers
        * **unet_satcen_finetuned.pth:** *unet_googlenet.pth* fine-tuned on the satcen datsaet with 60-20-20 split
        * **unet_finetuned_satcen_70_30.pth:** *unet_airbus_80_20.pth* fine-tuned on the satcen dataset with 70-30 train-test split
    * **pipeline:** files related to the classification + detection pipeline
        * **unet_positive_predictions.npy:** list of filenames of images predicted as positive by U-net (at least one ship pixel in U-net output)
    * **unet_classifier.ipynb:** test unet trained only on (36k) ship images from Airbus as a classifier (ship/no ship)
    * **unet_finetune_satcen.ipynb:** fine tune U-Net using the initial Satcen dataset
    * **unet.ipynb:** train U-Net on ship images from Airbus (28.8k train, 7.2k validation)