# Vespa Computer Vision trained with hornet3000 dataset
A model to detect three different classes of insects (hymenoptera): 
1. Asian hornets (Vespa velutina)
2. European hornets (Vespa crabro)
3. Ordinary wasp (Vespula vulgaris)

## Goal of the project
Aim is to end up with a detector on a Raspberry pi4 to make clear and sharp images to report it on waarnemingen.nl

## Background
More information about the exotic invasive Asian hornet can be found on 
- [NVWA](https://www.nvwa.nl/onderwerpen/aziatische-hoornaar)
- [EIS](https://www.eis-nederland.nl/DesktopModules/Bring2mind/DMX/API/Entries/Download?command=core%5Fdownload&entryid=1012&language=nl%2DNL&PortalId=4&TabId=563)

## Datasets
Images for the **training** and **validation** were collected mainly from waarnemingen.nl (observation.org) with the settings `alleen goedgekeurd` and `alle deelbare licenties`. 

The dataset is stored on [Kaggel](https://www.kaggle.com/datasets/marcoryvandijk/vespa-velutina-v-crabro-vespulina-vulgaris) (private).

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

![Slider of the first model](https://github.com/vespCV/hornet3000/blob/main/test_hornet3000_24-09-21.gif)



Project is based on https://github.com/computervisioneng/train-yolov10-custom-data-full-guide
