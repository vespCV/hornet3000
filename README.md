# Vespa Computer Vision: Detect Asian Hornets on Rasberry Pi
This project aims to develop a computer vision model for detecting Asian hornets (Vespa velutina) using a Raspberry Pi. 
Citizen scientists can use this tool to capture clear images of hornets and report sightings on waarnemingen.nl (observation.org).
## Table of Contents
* [Project Summary](#project-summary)
* [Goal of the Project](#goal-of-the-project)
* [Content Description](#content-description)
* [Other Resources](#other-resources) 
    * Dataset on Kaggle 
    * Training with YOLOv10 on Colab
* [Background](#background)
* [Datasets](#datasets)
* [Model](#model)
* [Validate the Model](#validate-the-model)
    * [Confusion Matrix](#confusion-matrix)
    * [Example of Predicted Data](#example-of-predicted-data)
    * [Test the Model on a Slider with Images or Movie](#test-the-model-on-a-slider-with-images-or-movie)
* [Demo](#demo)
    * [Input from Slideshow](#input-from-slideshow)
    * [Input 16MP CSI Camera](#input-16mp-csi-camera)
* [To Do](#to-do)
* [Acknowledgements](#acknowledgements)

## Project Summary

- This project aims to develop a robust and efficient computer vision model capable of accurately detecting Asian hornets (Vespa velutina) in real-time. 
- The model is trained on a comprehensive dataset of hornet images and deployed on a Raspberry Pi4 B for practical field use.

## Goal of the project
**Aim:** Detection system using a Raspberry Pi 4 to capture images of Asian hornets with high accuracy (target: 95% accuracy, with a maximum of 5% false positives where other insects are misidentified as Asian hornets). These images will be used for reporting on waarnemingen.nl.

## Content Description
- **manuals:** 
    * [Instruction how to install this model on a Raspberry Pi](https://github.com/vespCV/hornet3000/blob/main/manuals/buildingAsianHornetDetector.md)
    * [Manual how to train your own model with Yolov10n](https://github.com/vespCV/hornet3000/blob/main/manuals/makingYolov10nModelWithHornet3000Dataset.md) on Colab.
- **colab:** code to make the model in Colab and the config file.
- **content_data3000_ _date_:** Results of the training with confusion matrix and best- and last weights file.
- **codeLocalComp:** Code on local computer to check images and test the model with a slideshow and with USB camera.
- **codeRasberryPi4:** Code to test the installation Torch and the CSI camera, test the model with a slideshow and use the model with the CSI camera.
- **test:** Images, slideshows and video's that can be used to test the model.

## Other resources
- [Hornet3000 dataset](https://www.kaggle.com/datasets/marcoryvandijk/vespa-velutina-v-crabro-vespulina-vulgaris) (located in Kaggle)
- [vespCV_YOLOv10n](https://colab.research.google.com/drive/1ZYySGP85AOX187GFbzVVCnE-DFEFDOyT) (located in Google Colab)

## Background
More information about the exotic invasive Asian hornet in the Netherlands can be found on 
- [NVWA](https://www.nvwa.nl/onderwerpen/aziatische-hoornaar)
- [EIS](https://www.eis-nederland.nl/DesktopModules/Bring2mind/DMX/API/Entries/Download?command=core%5Fdownload&entryid=1012&language=nl%2DNL&PortalId=4&TabId=563)

## Datasets
Images for the **training** and **validation** were collected mainly from waarnemingen.nl (observation.org) with the settings `alleen goedgekeurd` and `alle deelbare licenties`. 

The dataset is stored on [Kaggel](https://www.kaggle.com/datasets/marcoryvandijk/vespa-velutina-v-crabro-vespulina-vulgaris).

Images for testing are not approved (classification might be inaccurate) and stored in the folder [test](https://github.com/vespCV/hornet3000/tree/main/test)

## Model
The model was trained with yolov10 in google [colab](https://github.com/vespCV/hornet3000/tree/main/colab "colab"). Code based on https://github.com/computervisioneng/train-yolov10-custom-data-full-guide.

## Validate the model
### Confusion matrix
![confusionmatrix](https://github.com/vespCV/hornet3000/blob/main/content_data3000_24-09-20/content/runs/detect/train/confusion_matrix.png)
### Example of predicted data
![predicteddata](https://github.com/vespCV/hornet3000/blob/main/content_data3000_24-09-20/content/runs/detect/train/val_batch1_pred.jpg)
### Test the model on a slider with images or movie
Make a slideshow of test images (or download from the dataSlider folder hornet3000.m4v). 

Install repro yolov10, [click here for instruction](https://youtu.be/PfQwNe0P-G4?t=1886)

Use the test_slider.py on your local computer, [click here for more information](https://youtu.be/PfQwNe0P-G4?t=2640)

### Demo 
#### Input from slideshow
A bounding box, class and conficence is show. This can be used to finetune the confidence levels.

![Slideschow of the first model](https://github.com/vespCV/hornet3000/blob/main/test_hornet3000_24-09-21.gif)

#### Input 16MP CSI camera
The camera is taking images from the right side of the screen (showing hornets from waarnemingen.nl). On the left side the captured image of the camera and the inference. When a class 0 (Asian hornet) is detected the picture is saved under the name and timestamp in the folder imaged (bottom left).

![Test the detection with 5 sec interval](https://github.com/vespCV/hornet3000/blob/main/testIntervalCSIcamImagesRpi_24-09-23.gif)

## To do
- Optimize confidence threshold in the wild
- Add insects to the model if needed (false positive hornet detections by other species)
- Optional: connection with smartphone
- Optional: simplify installation process 

### Acknowledgements
Yolov10 training of the model is based on https://github.com/computervisioneng/train-yolov10-custom-data-full-guide
