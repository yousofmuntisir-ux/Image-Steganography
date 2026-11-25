## 🚀 Live Demo

Try CyberHide Online:

[Open CyberHide Application](https://image-steganography-6jpu88w5ud3jwwnv3d2dxg.streamlit.app/)

**Status:** Successfully Deployed
# 🔐 CyberHide – Secure Image Steganography

## Project Overview
CyberHide is a Python-based application that protects secret messages by combining AES-256-GCM encryption with LSB (Least Significant Bit) image steganography.

## Technologies Used
- Python
- Streamlit
- AES-256-GCM
- LSB Steganography
- Pillow
- Cryptography

## Features
- Hide secret messages inside images.
- Encrypt messages using AES-256-GCM.
- Extract hidden messages from images.
- Decrypt messages using a password.
- Calculate image message capacity.
- Download encrypted images.

## Supported Media
Images (PNG and BMP).

## Installation

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Image-Steganography
pip install -r requirements.txt
```

## Run the Application

```bash
streamlit run app.py
```

## Project Structure

```text
Image-Steganography/
├── app.py
├── encryption.py
├── steganography.py
├── requirements.txt
└── README.md
```

## Security
The project uses AES-256-GCM for authenticated encryption and LSB for hiding encrypted messages inside images.

## Author
Muntisir Yousof Zakaria Mohamed

## Academic Project
Cryptography Course Project
