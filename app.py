import streamlit as st
import pandas as pd
from datetime import datetime

# 頁面標題與設定
st.set_page_config(page_title="油價與加油紀錄助手", page_icon="⛽", layout="centered")
st.title("⛽ 油價與加油紀錄助手")

# 初始化 Session State 來儲存歷史紀錄
if "gas_logs" not in st.session_state:
    st.session_state.gas_logs = pd.DataFrame(
        columns=["加油時間日期", "每公升油價 (元)", "加油公升數 (L)", "總價 (元)"]
    )

st.subheader("📝 新增加油紀錄")

# 使用表單元件讓輸入流程更順暢
with st.form("gas_form", clear_on_submit=True):
    # 1. 自動取得當前日期與時間 (YYYY-MM-DD HH:MM)
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 顯示自動帶入的日期時間
    st.text_input("今日加油時間日期 (自動帶入)", value=current_time_str, disabled=True)
    
    col1, col2 = st.columns(2)
    with col1:
        # 2. 輸入油價價格
        price_per_liter = st.number_input("每公升油價 (元)", min_value=0.0, step=0.1, format="%.2f")
    with col2:
        # 3. 輸入公升數
        fuel_amount = st.number_input("加油公升數 (L)", min_value=0.0, step=0.1, format="%.2f")

    # 4. 自動計算總價 (即時顯示)
    total_price = round(price_per_liter * fuel_amount, 2)
    st.markdown(f"### 💰 **試算總價： `{total_price}` 元**")

    # 送出按鈕
    submitted = st.form_submit_button("新增並儲存紀錄", use_container_width=True)

    if submitted:
        if price_per_liter > 0 and fuel_amount > 0:
            # 建立新紀錄
            new_record = pd.DataFrame([{
                "加油時間日期": current_time_str,
                "每公升油價 (元)": price_per_liter,
                "加油公升數 (L)": fuel_amount,
                "總價 (元)": total_price
            }])
            
            # 儲存至 Session State
            st.session_state.gas_logs = pd.concat([st.session_state.gas_logs, new_record], ignore_index=True)
            st.success("✅ 紀錄已成功新增！")
            st.rerun()
        else:
            st.warning("⚠️ 請輸入大於 0 的油價與公升數！")


# 顯示歷史紀錄
st.subheader("📊 歷史加油紀錄")

if not st.session_state.gas_logs.empty:
    # 顯示表格數據
    st.dataframe(st.session_state.gas_logs, use_container_width=True)
    
    # 統計數據摘要
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("總加油次數", f"{len(st.session_state.gas_logs)} 次")
    col_b.metric("累積總花費", f"{st.session_state.gas_logs['總價 (元)'].sum():.1f} 元")
    col_c.metric("累積總公升數", f"{st.session_state.gas_logs['加油公升數 (L)'].sum():.1f} L")

    # 清空紀錄按鈕
    if st.button("🗑️ 清空所有紀錄"):
        st.session_state.gas_logs = pd.DataFrame(
            columns=["加油時間日期", "每公升油價 (元)", "加油公升數 (L)", "總價 (元)"]
        )
        st.rerun()
else:
    st.info("目前尚無加油紀錄，請在上方輸入資料並點擊新增。")
