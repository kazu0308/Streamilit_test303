import streamlit as st
import cv2
import numpy as np

# ESP32-CAMのストリームURL
ESP32_CAM_URL = "http://192.168.10.113:81/stream"

st.title("ESP32-CAM Live Stream")

# セッション状態の初期化
if "stream" not in st.session_state:
    st.session_state["stream"] = False

# コントロールを横に並べる
col1, col2 = st.columns(2)
with col1:
    if st.button("Start Stream"):
        st.session_state["stream"] = True
        st.rerun()
with col2:
    if st.button("Stop Stream"):
        st.session_state["stream"] = False
        st.rerun()

try:
    if st.session_state["stream"]:
        # ビデオキャプチャの設定
        stream = cv2.VideoCapture(ESP32_CAM_URL)
        
        if not stream.isOpened():
            st.error("Failed to open the stream. Check the URL or network connection.")
        else:
            # 外部ウィンドウを作成
            cv2.namedWindow("ESP32-CAM Stream", cv2.WINDOW_NORMAL)
            
            while st.session_state["stream"]:
                ret, frame = stream.read()
                if not ret:
                    st.warning("Failed to retrieve frame. Retrying...")
                    stream.release()
                    stream = cv2.VideoCapture(ESP32_CAM_URL)
                    continue
                
                # 外部ウィンドウに表示
                cv2.imshow("ESP32-CAM Stream", frame)
                
                # 'q'キーで終了
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    st.session_state["stream"] = False
                    break
            
            # ストリームとウィンドウの解放
            stream.release()
            cv2.destroyAllWindows()
    else:
        st.text("Stream stopped.")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    if 'stream' in locals():
        stream.release()
    cv2.destroyAllWindows()