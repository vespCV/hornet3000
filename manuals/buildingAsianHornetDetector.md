# Building an Asian Hornet Detector with a Raspberry Pi 4 and CSI Camera

## Requirements
- [Raspberry Pi4 B](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/?variant=raspberry-pi-4-model-b-8gb) (An 8GB version was used for this project; other models have not been tested.)
- Powersupply for the Raspberry Pi
- Micro SD card (32GB card was used for this project.)
- Micro SD card reader and computer to flash the OS onto the micro SD card

- [Arducam IMX519 16MP Autofocus Camera Module for Raspberry Pi](https://www.antratek.nl/arducam-imx519) and cable (A lower quality or USB camera will also work.)
- Camera mount and protector (optional)

- [Bait lure](https://www.rbka.org.uk/index.php/asian-hornet/traps-and-lures) to attract hornets.


## Prepare Raspberry Pi4

### 1. Connect camera to the Raspberry Pi and install it
For Arducam, refer to the manual [here](https://docs.arducam.com/Raspberry-Pi-Camera/Pivariety-Camera/Quick-Start-Guide/).


### 2. Install operating system on micro SD
Use Raspberry Pi Imager to install bookworm (64-bit) on your SD card:
- Raspberry Pi Model: Raspberry Pi 4
- Operating System: Raspberry Pi OS (64-bit)
- Edit settings to preconfigure:
    hostname: pi

    username: vespcv

    password: `*****`

    Configure other options according to your Wi-Fi and time zone settings.

Detailed information can be found [here](https://www.raspberrypi.com/documentation/computers/getting-started.html)


### 3. Connect Raspberry Pi to your local computer

- Use [Raspberry Connect (beta)](https://connect.raspberrypi.com/sign-in) or connect via Secure Shell. Detailed information can be found [here](https://www.raspberrypi.com/documentation/computers/remote-access.html).

## Install vespCV

### 1. Create directory and virtual environment
- In the home directory on the Raspberry create a folder and change to it.

```
mkdir vespcv
cd vespcv
```

- Make a virtual environment and source into it.

```
python3 -m venv .vespcv
source .vespcv/bin/activate
```

### 2. Install dependencies
- Update package list:
```sudo apt update```
- Install openCV:
```sudo apt install python3-opencv```
- Install ultralytics:
```pip install torch torchvision ultralytics```
- Install libcamera-dev:
```sudo apt install libcamera-dev```
- Clone the yolov10 repository: 
```git clone https://github.com/THU-MIG/yolov10.git```
- Change to the cloned directory:
```cd yolov10```
- Install the required packages:
```
pip install .
pip install huggingface-hub
```

Install Pytorch on Bookworm described [here](https://qengineering.eu/install-pytorch-on-raspberry-pi-4.html) with a few modifications:

Deactivate the venv with `deactivate`.
1. Install the dependencies:
```sh
sudo apt-get install python3-pip libjpeg-dev libopenblas-dev libopenmpi-dev libomp-dev
```
2. Activate the virtual environment now:
```sh
source .vespcv/bin/activate
```
3. See this page on how to set up an virtual environment:
```sh
pip3 install setuptools numpy Cython
pip3 install requests
```
4. Install PyTorch and Torchvision and (optional) Torchaudio:
```sh
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip3 install torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 3. Copy model weights and python code to Raspberry
1. Enable SSH with `raspi-config`, select option 3 and enable SSH.
2. Check your RASPBERRYIP
Get your RASBERRYIP with `ifconfig`.
3. Copy last.pt (or best.pt) to the vespcv directory on your Raspberry Pi:
```scp /path/to/local/last.pt vespcv@RASPBERRYIP:/home/vespcv/vespcv```
If you have not trained your own model you can use: [last.pt](https://github.com/vespCV/hornet3000/blob/main/content_data3000_24-09-20/content/runs/detect/train/weights/last.pt)
4. Copy testIntervalCSIcamImages.py to your Raspberry Pi:
```scp /path/to/local/testIntervalCSIcamImages.py username@raspberrypi_address:/path/to/remote/destination```
5.  Optionally, test the camera with:
`testCSIcamPi.py`
6.  Optionally, to test Torch installation:
`testTorchPi.py`
7. Optionally, test the installation of the model with:
`testSlideshowVideoPi.py`
8. Optionally, to test the home setup with all three classes
`detectAllConf.py'
9. Make all downloaded Python scripts executable:
```chmod +x ./*.py```

## Test the model in the wild or at home
- Setup your camera to capture images from the bait lure. For this pilot, I used a home-based setup with a camera pointed at a bait lure attached to a window, a simple yet effective way to conduct a pilot for wildlife monitoring.
- Activate the virtual environment on the Raspberry:
```source vespcv/bin/activate```
- Run testIntervalCSIcamImages.py (or one of the optional scripts to test parts of the detector):
```python3 testIntervalCSIcamImages.py```
- Optimize the delay between the images taken and the confidence tresholds in the python code if needed.

![setup](https://github.com/vespCV/hornet3000/blob/main/manuals/setupAtHome.jpg)

![Test the detection with 5 sec interval](https://github.com/vespCV/hornet3000/blob/main/manuals/VVU_2024-10-03s.gif)

# Make autostart on Raspberry Pi boot

- In terminal from the Raspberry Pi open crontab:
```sudo crontab -e```
- Select option 1 (or the option corresponding to your preferred editor) if prompted.
- Add the autostart line: 
```@reboot /home/detector/vespCV/.venv/bin/python3 /home/detector/vespCV/testIntervalCSIcamImages.py```
- Optional to detect and save all classes and save a logfile in cronlog.txt. (I used it to for my test setupAtHome with only limonade wasps on the bait).
```@reboot /home/detector/vespCV/.venv/bin/python3 /home/detector/vespCV/detectAllConf.py >> /home/detector/vespCV/cronlog.txt 2>&1```
- Save and exit, press `ctrl+X`, `y` and enter to save the changes. This will schedule the script to run automatically whenever the Raspberry Pi boots.



