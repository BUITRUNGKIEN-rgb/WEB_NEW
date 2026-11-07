"""Modern Streamlit presentation for AI02 CNN V5; inference stays in cnn_utils.

Run: python -m streamlit run app_cnn.py
"""
from __future__ import annotations

import hashlib
import html
from io import BytesIO

import streamlit as st
from PIL import Image, ImageOps

from cnn_utils import LABELS, VI, available_models, predict_image

st.set_page_config(
    page_title='SMART CAMPUS AI | AI02 - Trường học xanh',
    page_icon='♻️', layout='wide', initial_sidebar_state='expanded'
)

st.markdown('''
<style>
:root {
  --bg:#ffffff; --blue:#0F6CBD; --blue-dark:#0B3768;
  --blue-soft:#EAF4FF; --orange:#F7931E; --orange-soft:#FFF3E6;
  --ink:#1F2D3D; --muted:#60758D; --line:#D9E6F2;
}
.stApp {background:linear-gradient(150deg,#FFFFFF 1%,#F3F9FF 67%,#FFFFFF 100%); color:var(--ink);}
[data-testid="stHeader"] {background:rgba(255,255,255,.88);}
.block-container {padding-top:1.4rem; max-width:1450px; padding-bottom:2.2rem;}
/* Thanh điều hướng xanh dương: chữ sáng, điểm nhấn cam */
[data-testid="stSidebar"] {background:linear-gradient(180deg,#0B3768 0%,#0F6CBD 100%); border-right:0;}
[data-testid="stSidebar"] h3, [data-testid="stSidebar"] label,
[data-testid="stSidebar"] p, [data-testid="stSidebar"] .stMarkdown {color:#F1F7FF;}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {color:#CDDEEF;}
[data-testid="stSidebar"] [data-testid="stAlert"] {background:#EDF6FF;}
[data-testid="stSidebar"] [data-testid="stAlert"] * {color:#1F2D3D !important;}
[data-testid="stSidebar"] [data-baseweb="select"] > div {background:#FFFFFF; border:1px solid #BBD5F0; border-radius:11px;}
[data-testid="stSidebar"] [data-baseweb="select"] span {color:#1F2D3D;}
/* Card, ảnh và vùng upload */
[data-testid="stVerticalBlockBorderWrapper"]:has(> div [data-testid="stFileUploader"]),
[data-testid="stVerticalBlockBorderWrapper"]:has(> div [data-testid="stProgress"]) {
  background:#FFFFFF; border:1px solid var(--line); border-radius:20px;
  box-shadow:0 10px 27px rgba(15,108,189,.055);
}
[data-testid="stFileUploader"] section {
 background:#F4F9FF; border:2px dashed #B5D5F3; border-radius:15px;
}
[data-testid="stFileUploader"] button {border-radius:10px; color:var(--blue-dark); border:1px solid var(--line);}
[data-testid="stFileUploader"] button:hover {border-color:var(--orange); color:var(--blue-dark);}
/* Nút chính xanh, hover cam */
.stButton>button[kind="primary"] {
 background:linear-gradient(96deg,#0F6CBD 0%,#2588DC 100%);border:0;
 color:#FFFFFF;font-weight:800;border-radius:13px;min-height:51px;
 box-shadow:0 8px 17px rgba(15,108,189,.16);
}
.stButton>button[kind="primary"]:hover {
 background:linear-gradient(95deg,#F7931E,#FFAA4D);color:#FFFFFF;
 box-shadow:0 8px 20px rgba(247,147,30,.2);
}
.stButton>button:not([kind="primary"]) {border-radius:12px;}
.stButton>button:focus-visible {outline:3px solid #F7931E;}
[data-testid="stMetricValue"] {color:var(--orange);font-weight:800;}
[data-testid="stProgress"] [role="progressbar"] {background-color:#EAF4FF;}
[data-testid="stProgress"] [role="progressbar"] > div {background:#F7931E !important;}
hr {border-color:var(--line) !important;}
/* Các phần nhận diện của giao diện */
.hero {
 position:relative;overflow:hidden;
 background:linear-gradient(110deg,#FFFFFF 0%,#F4F9FF 50%,#EAF4FF 100%);
 border:1px solid #CFE3F6;border-left:7px solid #F7931E;
 border-radius:21px;padding:29px 34px 30px;margin-bottom:21px;
 box-shadow:0 12px 30px rgba(15,108,189,.075);
}
.hero:after {content:"";position:absolute;width:220px;height:220px;border-radius:50%;
 right:-85px;top:-120px;background:rgba(15,108,189,.08);pointer-events:none;}
.hero .overline {color:#DF7C06;font-size:.83rem;letter-spacing:.12em;font-weight:800;}
.hero h1 {color:#0B3768;font-size:2.1rem;line-height:1.25;margin:9px 0 11px;font-weight:850;}
.hero h1 .accent {color:#F7931E;}
.hero .desc {color:#526B85;font-size:1rem;margin:0;line-height:1.55;}
.hero .tag-row {display:flex;gap:9px;flex-wrap:wrap;margin-top:16px;}
.hero .tag {font-size:.80rem;border-radius:99px;padding:6px 12px;
 background:#FFFFFF;color:#155F9C;border:1px solid #CFE3F6;font-weight:700;}
.hero .tag.orange {background:#FFF3E6;color:#B55F00;border-color:#FFD5A1;}
.page-title {color:#0B3768;font-weight:830;font-size:1.23rem;margin-bottom:2px;}
.page-desc {color:#60758D;font-size:.9rem;margin-bottom:14px;}
.result-pod {background:linear-gradient(110deg,#FFFFFF,#FFF3E6);
 border:1px solid #FFD5A1;border-left:5px solid #F7931E;
 padding:23px;border-radius:15px;margin:12px 0 18px;}
.result-pod .eyebrow {color:#C16D00;font-size:.82rem;font-weight:780;letter-spacing:.07em;}
.result-pod .name {font-size:2.0rem;font-weight:850;color:#0F6CBD;margin:8px 0;}
.result-pod .percent {font-size:1.2rem;color:#E27A00;font-weight:800;}
.note {background:#FFF3E6;color:#885012;border:1px solid #FFD29C;
 padding:13px 15px;border-radius:12px;margin:12px 0;line-height:1.5;}
.tip {background:#EAF4FF;border:1px solid #D0E5F8;
 color:#184E82;border-radius:13px;padding:16px;margin:11px 0;line-height:1.5;}
.smallprint {font-size:.82rem;color:#667B90;line-height:1.55;}
.sidebrand {color:#FFFFFF;font-size:1.25rem;font-weight:850;letter-spacing:.035em;}
.sidebrand em {font-style:normal;color:#FFB454;}
.sidecaption {color:#D6E7F7;font-size:.73rem;letter-spacing:.11em;font-weight:700;}
/* Tối ưu thiết bị nhỏ */
@media (max-width:700px) {
 .hero {padding:21px 21px 23px;}
 .hero h1 {font-size:1.5rem;}
 .result-pod .name {font-size:1.6rem;}
 .block-container {padding-top:1rem;}
}
</style>
''', unsafe_allow_html=True)

st.sidebar.markdown(
    '<div class="sidebrand">✦ SMART CAMPUS <em>AI</em></div>'
    '<div class="sidecaption">TRƯỜNG HỌC XANH · UNETI 2026</div>',
    unsafe_allow_html=True
)
st.sidebar.write('')
st.sidebar.markdown('### Bảng điều khiển')

paths = available_models('model')
if not paths:
    choices = []
else:
    choices = []
    if len(paths) > 1:
        choices.append(('Kết hợp hai CNN · Ensemble', paths))
    for p in paths:
        name = 'MobileNetV3-Large' if 'mobilenet' in p.stem else 'EfficientNet-B0'
        choices.append((name, [p]))

if choices:
    choice_i = st.sidebar.selectbox('Chọn mô hình nhận diện',
                                   range(len(choices)),
                                   format_func=lambda i: choices[i][0])
else:
    st.sidebar.warning('Chưa tìm thấy checkpoint CNN `.pth`.')
    choice_i = 0

st.sidebar.markdown('---')
st.sidebar.markdown('**Phạm vi mô hình**')
st.sidebar.caption('6 lớp TrashNet · Ảnh một vật thể · Nền tương đối đơn giản')
st.sidebar.markdown('**Phương pháp**')
st.sidebar.caption('CNN pretrained ImageNet, fine-tune trên dữ liệu TrashNet. Không khẳng định độ chính xác tuyệt đối.')
st.sidebar.markdown('---')
st.sidebar.success('Ứng dụng Python · không dùng API AI trả phí')

st.markdown('''
<div class="hero">
  <div class="overline">OLYMPIC TRÍ TUỆ NHÂN TẠO UNETI 2026 · MÃ ĐỀ AI02</div>
  <h1>SMART CAMPUS <span class="accent">AI</span> · Phân loại rác thông minh</h1>
  <p class="desc">Ứng dụng trí tuệ nhân tạo hỗ trợ nhận diện vật liệu từ hình ảnh — hướng đến Trường học xanh.</p>
  <div class="tag-row"><span class="tag">6 nhóm rác TrashNet</span><span class="tag">Mô hình CNN</span><span class="tag orange">Trắng · Xanh · Cam</span></div>
</div>
''', unsafe_allow_html=True)

if not choices:
    st.error('Chưa có mô hình CNN trong thư mục `model`. Hãy chạy `02_HUAN_LUYEN_CNN.bat` trước. '
             'Mô hình `.joblib` V4 không thể thay cho checkpoint `.pth` V5.')
    st.stop()

left, right = st.columns([1.05, 1.0], gap='large')
with left:
    with st.container(border=True):
        st.markdown('<div class="page-title">01 · Hình ảnh đầu vào</div>'
                    '<div class="page-desc">Chọn ảnh có một vật thể, tương đồng với dữ liệu TrashNet</div>',
                    unsafe_allow_html=True)
        upload = st.file_uploader('Chọn JPG, PNG, WEBP hoặc BMP',
                                  type=['jpg', 'jpeg', 'png', 'webp', 'bmp'],
                                  label_visibility='collapsed')
        image = None
        if upload is not None:
            try:
                image = ImageOps.exif_transpose(Image.open(BytesIO(upload.getvalue()))).convert('RGB')
                st.image(image, use_container_width=True)
                st.caption(f'Ảnh: {upload.name} · {image.width} × {image.height} px')
            except Exception as exc:
                st.error('Không thể mở ảnh: ' + str(exc))
                image = None
        else:
            st.markdown('<div class="tip">📷 Ảnh sẽ hiển thị ở đây sau khi bạn chọn tệp.</div>',
                        unsafe_allow_html=True)
        go = st.button('✦ PHÂN TÍCH HÌNH ẢNH', type='primary', use_container_width=True,
                       disabled=image is None)
        st.markdown('<div class="smallprint">Ảnh được xử lý trong phiên ứng dụng này. '
                    'Không sử dụng ảnh này để tự động huấn luyện lại mô hình.</div>',
                    unsafe_allow_html=True)

selection_name, selected_paths = choices[choice_i]
current_token = None
if upload is not None:
    current_token = hashlib.sha256(upload.getvalue()).hexdigest() + ':' + selection_name

if go and image is not None:
    try:
        with st.spinner('CNN đang phân tích ảnh...'):
            result = predict_image(image, selected_paths)
        st.session_state.ai02_result = result
        st.session_state.ai02_token = current_token
    except Exception as exc:
        st.session_state.pop('ai02_result', None)
        st.session_state.pop('ai02_token', None)
        st.error('Không thể dự đoán: ' + str(exc))

shown = (st.session_state.get('ai02_result')
         if st.session_state.get('ai02_token') == current_token and current_token
         else None)

with right:
    with st.container(border=True):
        st.markdown('<div class="page-title">02 · Kết quả nhận diện</div>'
                    '<div class="page-desc">Dự đoán, độ tin cậy tham khảo và gợi ý phân loại</div>',
                    unsafe_allow_html=True)
        if shown is None:
            st.markdown('<div class="result-pod">'
                        '<div class="eyebrow">KẾT QUẢ AI</div>'
                        '<div class="name">Sẵn sàng phân tích</div>'
                        '<div class="smallprint">Tải một ảnh và nhấn “Phân tích hình ảnh”.</div>'
                        '</div>', unsafe_allow_html=True)
            st.info('Ứng dụng chỉ nhận diện sáu nhóm rác thuộc TrashNet.')
        else:
            name = html.escape(shown['label_vi'])
            percent = shown['confidence'] * 100
            st.markdown(
                f'<div class="result-pod"><div class="eyebrow">DỰ ĐOÁN CỦA HỆ THỐNG</div>'
                f'<div class="name">{name}</div>'
                f'<div class="percent">Xác suất tham khảo: {percent:.1f}%</div></div>',
                unsafe_allow_html=True
            )
            if shown['uncertain']:
                st.markdown('<div class="note">⚠️ ' + html.escape(shown['warning']) + '</div>',
                            unsafe_allow_html=True)
            else:
                st.success('Kết quả có mức độ tin cậy tương đối cao theo ngưỡng hiện tại.')
            st.markdown('**Xác suất của sáu nhóm rác**')
            ranked = sorted(shown['probabilities'].items(), key=lambda kv: -kv[1])
            for category, probability in ranked:
                st.progress(float(probability), text=f'{VI[category]} · {probability * 100:.1f}%')
            st.markdown('**Gợi ý phân loại**')
            st.markdown('<div class="tip">' + html.escape(shown['recommendation']) + '</div>',
                        unsafe_allow_html=True)
            st.caption('Mô hình: ' + ', '.join(shown['architectures']))
            st.caption(shown['note'])

st.divider()
st.caption('AI02 – Trường học xanh | Nguyên mẫu học thuật, không tự động quyết định khả năng tái chế. '
           'Cần so sánh Macro-F1 với baseline trên cùng tập validation theo yêu cầu cuộc thi.')
