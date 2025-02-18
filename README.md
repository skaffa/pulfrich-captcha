# Pulfrich Effect CAPTCHA Generator

This project generates CAPTCHA challenges using the **Pulfrich effect**, an optical illusion that makes moving objects appear in different depth planes when viewed with a darkened lens over one eye. By leveraging this effect, the generated CAPTCHA videos are easier to read with depth perception but difficult for automated bots to solve.

## 🔍 How It Works

- A random CAPTCHA code (letters and numbers) is generated.
- The characters are placed against a dynamic, scrolling background.
- A flickering effect is applied to enhance depth perception.
- The CAPTCHA is saved as a `.webm` video file, making it resistant to standard OCR techniques.

## 📂 Example Output

A sample CAPTCHA video will be available in the `captchas/` folder after running the script.

## 🛠️ Installation

Ensure you have Python and the required dependencies installed:

```bash
pip install pillow numpy opencv-python
