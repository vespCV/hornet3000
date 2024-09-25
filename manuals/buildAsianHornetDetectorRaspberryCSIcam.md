# Building an Asian Hornet Detector with a Raspberry Pi 4 and CSI Camera

## Requirements
- [Raspberry Pi4 B](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/?variant=raspberry-pi-4-model-b-8gb) (a 8gb version was used for this project, other nodels not tested)
- Powersupply for the raspberry
- Micro SD card (32GB card is used for the pilot)
- Micro SD card reader and computer to flash the OS on the micro SD card

- [Arducam IMX519 16MP Autofocus Camera Module for Raspberry Pi](https://www.antratek.nl/arducam-imx519) and cable (a lower quality or USB camera will to the job also)
- Camera mount and protector (optional)

- [Bait lure](https://www.rbka.org.uk/index.php/asian-hornet/traps-and-lures) to attract hornets.


## Prepare Raspberry Pi4

### 1. Connect camera to the Raspberry Pi and install it
For Arducam, you can find the manual [here](https://docs.arducam.com/Raspberry-Pi-Camera/Pivariety-Camera/Quick-Start-Guide/).


### 2. Install operating system on micro SD
Use Raspberry Pi Imager to install bookworm 64gb on your SD card
- Raspberry Pi Model: Raspberry Pi 4
- Operating System: Raspberry Pi OS (64-bit)
- Edit settings to preconfigure:
    hostname: vespcv

    username: detector

    password: `*****`

    and the other options according to your wifi and time zone

Detailed information can be found [here](https://www.raspberrypi.com/documentation/computers/getting-started.html)


### 3. Connect Raspberry Pi to your local computer

- Use [Raspberry Connect (beta)](https://connect.raspberrypi.com/sign-in) or connect via Secure Shell. Detailed information can be found [here](https://www.raspberrypi.com/documentation/computers/remote-access.html).

## Install vespCV

### 1. Create directory and virtual environment
- On the home directory on the Raspberry create a folder and cd to it.

```mkdir vespcv```

```cd vespcv```

- Make a virtual environment and source into it.

```python3 -m venv .vespCV```

```source vespCV-env/bin/activate```

### 2. Install dependencies
- update:
```sudo apt update```
- install openCV:
```sudo apt install python3-opencv```
- install ultralytics:
```pip install torch torchvision ultralytics```
- install libcamera-dev:
```sudo apt install libcamera-dev```
- Clone the yolov10 repository: 
```git clone https://github.com/THU-MIG/yolov10.git```
- Cd into the directory:
```cd yolov10```
- Install the packages:
```pip install .```

```pip install huggingface-hub```

Install pytorch on bookworm with one of the methodes described [here](https://qengineering.eu/install-pytorch-on-raspberry-pi-4.html)

### 3. Copy model weights and python code to Raspberry
- Copy last.pt to the directory vespcv:
```scp /path/to/local/last.pt username@raspberrypi_address:/path/to/remote/destination```
- Copy from codeRaspberryPi4 the testIntervalCSIcamImages.py to your Raspberry Pi:
```scp /path/to/local/testIntervalCSIcamImages.py username@raspberrypi_address:/path/to/remote/destination```
- Optional to test the camera:
`testCSIcamPi.py`
- Optional to test Torch installation:
`testTorchPi.py`
- Optional to test the installation of the model:
`testSlideshowVideoPi`
- Make all the downloaded python code executable with:
```chmod +x ./FILENAME.py```

## Run the model in the wild or at home
Make a setup so you camera captures images from the bait lure. For a pilot I used youtube video's of a bait lure with an [Asian hornet](https://www.youtube.com/watch?v=eXZwN4O0FdU) and pointed my camera to the screen.

Source into the environment on the Raspberry:
```source vespCV-env/bin/activate```

Run testIntervalCSIcamImages.py (or one of the optinal code to test parts of the detector):
```python3 testIntervalCSIcamImages.py```
![setup](https://github.com/vespCV/hornet3000/blob/main/manuals/setupAtHome.jpg)