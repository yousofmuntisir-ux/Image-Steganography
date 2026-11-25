import streamlit as st
from PIL import Image
from io import BytesIO

from steganography import (
    encode_message,
    decode_message,
    calculate_capacity
)

from encryption import (
    encrypt_message,
    decrypt_message
)


# ===================================
# PAGE CONFIGURATION
# ===================================

st.set_page_config(
    page_title="CyberHide | Secure Steganography",
    page_icon="🔐",
    layout="wide"
)


# ===================================
# CUSTOM DESIGN
# ===================================

st.markdown("""
<style>

.stApp {
    background-color: #080F1E;
    color: #E2E8F0;
}

section[data-testid="stSidebar"] {
    background-color: #101B30;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #22D3EE;
}

.subtitle {
    color: #94A3B8;
    font-size: 16px;
}

.section-title {
    color: #22D3EE;
    font-size: 24px;
    font-weight: bold;
}

div.stButton > button {
    background: linear-gradient(90deg, #0891B2, #2563EB);
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: bold;
    width: 100%;
    padding: 10px;
}

div.stButton > button:hover {
    background: #0E7490;
    color: white;
}

div[data-testid="stMetric"] {
    background-color: #142238;
    border: 1px solid #263B57;
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# ===================================
# SIDEBAR
# ===================================

with st.sidebar:

    st.title("🔐 CyberHide")

    st.caption("Secure Information Protection")

    st.divider()

    st.markdown("### Project Information")

    st.write("**Technique:** LSB Steganography")

    st.write("**Encryption:** AES-256-GCM")

    st.write("**Language:** Python")

    st.write("**Framework:** Streamlit")

    st.divider()

    st.markdown("### How It Works")

    st.write("1. Enter your secret message.")

    st.write("2. Encrypt using AES.")

    st.write("3. Hide inside an image.")

    st.write("4. Extract and decrypt.")

    st.divider()

    st.caption("Cryptography Course Project")


# ===================================
# MAIN HEADER
# ===================================

st.markdown(
    '<div class="main-title">🔐 CyberHide</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Secure Image Steganography Using AES-256 & LSB'
    '</div>',
    unsafe_allow_html=True
)

st.write("")


# ===================================
# INFORMATION CARDS
# ===================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Encryption", "AES-256-GCM")

with col2:
    st.metric("Steganography", "LSB")

with col3:
    st.metric("Media Supported", "Images")

st.divider()


# ===================================
# APPLICATION TABS
# ===================================

tab1, tab2 = st.tabs([
    "🔒 Hide Secret Message",
    "🔓 Extract Secret Message"
])


# ===================================
# HIDE MESSAGE
# ===================================

with tab1:

    st.markdown(
        '<div class="section-title">Hide Your Secret Message</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Encrypt your message and hide it inside an image."
    )

    uploaded_image = st.file_uploader(
        "Upload Original Image",
        type=["png", "bmp", "jpg", "jpeg", "webp"],
        key="hide_image"
    )

    message = st.text_area(
        "Secret Message",
        placeholder="Write your secret message here..."
    )

    password = st.text_input(
        "Encryption Password",
        type="password",
        key="hide_password"
    )

    if uploaded_image:

        image = Image.open(uploaded_image).convert("RGB")

        col1, col2 = st.columns(2)

        with col1:

            st.image(
                image,
                caption="Original Image",
                use_container_width=True
            )

        with col2:

            st.markdown("### Image Information")

            st.metric(
                "Image Width",
                f"{image.width} px"
            )

            st.metric(
                "Image Height",
                f"{image.height} px"
            )

            st.metric(
                "Image Size",
                f"{len(uploaded_image.getvalue()) / 1024:.2f} KB"
            )

            capacity = calculate_capacity(image)

            st.metric(
                "Maximum Message Capacity",
                f"{capacity / 1024:.2f} KB"
            )

        # ENCRYPT AND HIDE BUTTON

        if st.button("🔐 Encrypt & Hide Message"):

            if not message or not password:

                st.warning(
                    "Please enter both message and password."
                )

            else:

                try:

                    # Step 1: Encrypt message

                    encrypted_message = encrypt_message(
                        message,
                        password
                    )

                    # Step 2: Check image capacity

                    encrypted_size = len(
                        encrypted_message.encode("ascii")
                    )

                    if encrypted_size > capacity:

                        st.error(
                            "Message is too large for this image!"
                        )

                    else:

                        # Step 3: Hide encrypted message

                        result = encode_message(
                            image,
                            encrypted_message
                        )

                        # Step 4: Save as PNG

                        output = BytesIO()

                        result.save(
                            output,
                            format="PNG"
                        )

                        output.seek(0)

                        # Step 5: Success message

                        st.success(
                            "Message encrypted and hidden successfully!"
                        )

                        # Step 6: Download image

                        st.download_button(
                            label="⬇ Download Secret Image",
                            data=output.getvalue(),
                            file_name="cyberhide_secret.png",
                            mime="image/png"
                        )

                except Exception as e:

                    st.error(
                        f"Encryption Error: {e}"
                    )


# ===================================
# EXTRACT MESSAGE
# ===================================

with tab2:

    st.markdown(
        '<div class="section-title">Extract Secret Message</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Upload the encrypted image and enter the correct password."
    )

    secret_image = st.file_uploader(
        "Upload Encrypted Image",
        type=["png", "bmp"],
        key="extract_image"
    )

    extract_password = st.text_input(
        "Decryption Password",
        type="password",
        key="extract_password"
    )

    if secret_image:

        try:

            image = Image.open(secret_image).convert("RGB")

            st.image(
                image,
                caption="Encrypted Image",
                width=400
            )

            if st.button("🔓 Extract & Decrypt Message"):

                if not extract_password:

                    st.warning(
                        "Please enter the decryption password."
                    )

                else:

                    # Step 1: Extract encrypted message

                    encrypted_message = decode_message(image)

                    if not encrypted_message:

                        st.warning(
                            "No hidden message found."
                        )

                    else:

                        # Step 2: Decrypt message

                        original_message = decrypt_message(
                            encrypted_message,
                            extract_password
                        )

                        # Step 3: Display result

                        st.success(
                            "Message extracted and decrypted successfully!"
                        )

                        st.text_area(
                            "Original Secret Message",
                            original_message,
                            height=150
                        )

        except Exception as e:

            st.error(
                "Extraction or decryption failed. "
                "Check the image and password."
            )

            st.caption(
                f"Technical details: {e}"
            )


# ===================================
# FOOTER
# ===================================

st.divider()

st.markdown(
    "<center>CyberHide | Cryptography Project | "
    "AES-256-GCM + LSB</center>",
    unsafe_allow_html=True
)