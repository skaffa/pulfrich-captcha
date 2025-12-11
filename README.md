This script generates CAPTCHAs using the pulfrich effect, making it visually impossible to detect using traditional OCR algorithms.

For best effect, cover your right eye with a sunglass or some other translucent object.  

[https://skaffa.github.io/pulfrich-captcha/](https://skaffa.github.io/pulfrich-captcha/)

I consider this a Proof of Concept

In the 'captchas' folder are some examples

Note: This project is mostly made by AI. ChatGPT and Deepseek were used for this.
If for some reason anyone decides to contribute to this repo, I recommend using AI generated code, to not waste your time. Otherwise, fork or clone this repo and do whatever with it.

> [!IMPORTANT]  
> Unfortunately, the current implementation still leaks enough signal for the correct CAPTCHA code to be programmatically recovered. Using an optical-flow–based analysis, attackers can extract motion differences that reveal the underlying characters.
