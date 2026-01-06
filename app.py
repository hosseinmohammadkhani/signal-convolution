import io
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image

import helpers as hp

# Webpage configuration
st.set_page_config(page_title="کانولوشن دو بعدی", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn&display=swap');
    html, body, title [data-testid="stAppViewContainer"], .main {
        direction: RTL;
        text-align: center;
        font-family: 'Vazirmatn', sans-serif;
    }
    div[data-testid="stSelectbox"] > label, div[data-testid="stTextInput"] > label {
        text-align: right;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("کانولوشن گسسته")

option = st.selectbox(
    "نوع عملیات را انتخاب کنید: ",
    ("کانولوشن ساده", "اعمال فیلتر گاوسی", "اعمال فیلتر گاوسی روی تصویر")
)

# initialize result signal
result_signal = None

if option == "کانولوشن ساده":
    col1, col2 = st.columns(2)
    with col1:
        input1 = st.text_input("سیگنال اول (اعداد را با کاما جدا کنید)")
    with col2:
        input2 = st.text_input("سیگنال دوم (اعداد را با کاما جدا کنید)")
    
    if st.button("محاسبه"):
        s1 = hp.parse_signal(input1)
        s2 = hp.parse_signal(input2)
        if s1 and s2:
            result_signal = hp.convolve(s1, s2)
        else:
            st.error("لطفاً سیگنال‌ها را به درستی وارد کنید (مثال: 1, 2, 3)")

elif option == "اعمال فیلتر گاوسی":
    input_signal = st.text_input("سیگنال ورودی (اعداد را با کاما جدا کنید)")
    sigma_val = st.number_input("مقدار سیگما" , 1 , None, 1)
    
    if st.button("محاسبه"):
        parsed_signal = hp.parse_signal(input_signal)
        if parsed_signal:
            result_signal = hp.apply_1d_gaussian_filter(parsed_signal, sigma=sigma_val)
        else:
            st.error("لطفاً سیگنال را به درستی وارد کنید.")

elif option == "اعمال فیلتر گاوسی روی تصویر":
    st.write("لطفاً یک تصویر آپلود کنید. تصویر به صورت خاکستری شده و به اندازه 512×512 تغییر اندازه می‌یابد.")
    input_image = st.file_uploader("انتخاب تصویر (jpg/png)", type=["jpg", "jpeg", "png"])
    sigma_img = st.number_input("مقدار سیگما برای فیلتر گاوسی تصویر", min_value=0.1, value=1.0, step=0.1, format="%.2f")
    
    if input_image is not None:
        st.image(input_image, caption="تصویر آپلود شده (ورودی)")
        if st.button("تبدیل"):
            try:

                # convert input image to 2D matrix
                img_matrix = hp.convert_image_to_matrix(input_image)
                
                # apply 2D gaussian filter (returns blurred matrix)
                blurred_matrix = hp.apply_gaussian_filter_on_image(img_matrix, sigma=sigma_img)
                
                buf = io.BytesIO()
                hp.matrix_to_image(blurred_matrix , buf)
                buf.seek(0)
                
                st.image(buf, caption="تصویر تار شده")
                
                # provide download button
                st.download_button(
                    label="دانلود تصویر تار شده",
                    data=buf.getvalue(),
                    file_name="blurred_image.png",
                    mime="image/png"
                )
                
            except Exception as e:
                st.error(f"خطا هنگام پردازش تصویر: {e}")    

# show output(for 1D convolution)
if result_signal:
    st.subheader("خروجی نهایی")
    
    # show signal as a list
    formatted_output = [round(i, 3) for i in result_signal]
    st.code(f"Output Signal: {formatted_output}")
    
    # create chart
    fig, ax = plt.subplots(figsize=(7,4))
    ax.stem(result_signal)
    ax.set_title("Output signal" ,  fontsize=12)
    ax.grid()
    st.pyplot(fig)