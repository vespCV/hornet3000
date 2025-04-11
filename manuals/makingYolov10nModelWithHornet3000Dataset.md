# Training a YOLOv10 Model for Vespa Classification on Google Colab

In the folders yolov8sModel and yolov10nModel you can find the yolov8 model[best.pt](/home/vespcv/hornet3000/yolov8sModel/weights/best.pt) trained on 17000 images and the yolov10 model [best.pt](/home/vespcv/hornet3000/yolov10nModel/weights/best.pt) trained on the hornet3000+ dataset

If you want to train a model with your own images (or with the hornet3000+ dataset), this manual guides you through training a YOLOv10 model for classifying different Vespa species on Google Colab. 

Requirements:
- A Google account for Google Drive and Google Colaboratory

1. Download Vespa Dataset:

- Visit the [Hornet3000 dataset](https://www.kaggle.com/datasets/marcoryvandijk/vespa-velutina-v-crabro-vespulina-vulgaris) on Kaggle.
- Click **Download**

2. Move Data to Google Drive:
- Upload the `archive.zip` to a folder named `vespCV` in your Google Drive.

3. Open the notebook:
- Click [here](https://colab.research.google.com/drive/1ZYySGP85AOX187GFbzVVCnE-DFEFDOyT?usp=sharing) to open the notebook.

4. Download Training Results (Important):
- **Remember:** Training data and results are lost when you close the Colab notebook.