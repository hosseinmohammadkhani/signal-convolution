import streamlit as st
import matplotlib.pyplot as plt

from helpers import convolve, apply_gaussian_filter, parse_signal

# Webpage configuration
st.set_page_config(page_title="کانولوشن یک بعدی", layout="centered")

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

st.title("کانولوشن گسسته یک بعدی")

option = st.selectbox(
    "نوع عملیات را انتخاب کنید: ",
    ("کانولوشن ساده", "اعمال فیلتر گاوسی")
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
        s1 = parse_signal(input1)
        s2 = parse_signal(input2)
        if s1 and s2:
            result_signal = convolve(s1, s2)
        else:
            st.error("لطفاً سیگنال‌ها را به درستی وارد کنید (مثال: 1, 2, 3)")

elif option == "اعمال فیلتر گاوسی":
    input_signal = st.text_input("سیگنال ورودی (اعداد را با کاما جدا کنید)")
    sigma_val = st.number_input("مقدار سیگما" , 1 , None, 1)
    
    if st.button("محاسبه"):
        parsed_signal = parse_signal(input_signal)
        if parsed_signal:
            result_signal = apply_gaussian_filter(parsed_signal, sigma=sigma_val)
        else:
            st.error("لطفاً سیگنال را به درستی وارد کنید.")

# show output
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