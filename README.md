# Pulfrich Effect CAPTCHA Generator

## Overview
This project generates CAPTCHA videos using the Pulfrich effect, making it difficult for bots to interpret while remaining readable to humans using a simple monocular depth illusion.

The CAPTCHA consists of characters embedded in a moving background. The movement, combined with random flickering and transformations, makes it hard to extract characters using standard OCR techniques.

## Features
- Randomized CAPTCHA codes with configurable length
- Scrolling background to leverage the Pulfrich effect
- Random character positioning and transformations (rotation, tilt)
- Background and character variations to enhance obfuscation
- Outputs WebM videos with adjustable quality settings

## How It Works
1. A random alphanumeric code is generated.
2. Characters are placed in distinct regions with random transformations.
3. A grayscale background is generated and set to scroll at an angle.
4. Visual variations are applied to further obscure detection.
5. The video is saved as a WebM file for easy embedding and viewing.

## Requirements
Ensure you have the following installed:
- Python 3
- OpenCV (`cv2`)
- PIL (`Pillow`)
- NumPy

Install dependencies using:
```sh
pip install opencv-python numpy pillow
```

## Usage
Run the script to generate a new CAPTCHA video:
```sh
python captcha_generator.py
```
The generated video will be saved in the `captchas/` directory.

## Example Output
A sample CAPTCHA video will be generated in `.webm` format and can be viewed in any modern browser.   
[Example](skaffa.github.io/pulfrich-captcha/)

## Configuration
Modify the `CONFIG` dictionary in the script to adjust settings like image size, font size, character length, and scrolling speed.

## License
This project is open-source under the MIT License.

