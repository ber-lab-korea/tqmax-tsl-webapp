import streamlit as st

st.set_page_config(page_title="TQmax/TSL 계산기", layout="centered", page_icon="📈")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Medical_icon.svg/1200px-Medical_icon.svg.png", width=80)
st.title("📊 TQmax / TSL 계산기")

unit_factors = {
    "mg": 1000,
    "µg": 1,
    "ng": 0.001
}

st.markdown("---")

# 입력: TQ
col1, col2 = st.columns([2, 1])
with col1:
    tq_value = st.number_input("TQ 값", min_value=0.0, value=0.0, step=0.01)
with col2:
    tq_unit = st.selectbox("TQ 단위", ["mg", "µg", "ng"])

# 입력: MDb.c. 및 MDa.r.s
unit_options = ["cm²", "g", "ml", "Ea"]
col3, col4, col5 = st.columns(3)
with col3:
    mdbc = st.number_input("MDb.c.", min_value=0.0, value=0.0, step=0.01)
    mdbc_unit = st.selectbox("MDb.c. 단위", unit_options, key="mdbc")
with col4:
    mdars = st.number_input("MDa.r.s.", min_value=0.0, value=1.0, step=0.01)
    mdars_unit = st.selectbox("MDa.r.s. 단위", unit_options, key="mdars")
with col5:
    period = st.selectbox("Period of assumed exposure", ["≤1d", "≤30d", ">30d"])

# 계산 버튼
if st.button("🧮 계산하기"):
    if mdbc_unit != mdars_unit:
        st.error("❌ MDb.c.와 MDa.r.s.의 단위가 서로 다릅니다.")
    else:
        try:
            tq = tq_value * unit_factors[tq_unit]
            sf = mdbc / mdars
            tqmax = tq * sf
            tsl = 120 if period in ["≤1d", "≤30d"] else 600
            ratio = tqmax / tsl

            st.markdown("---")
            st.write(f"🔹 **TQ (µg):** `{tq:.2f}`")
            st.write(f"🔹 **SF:** `{sf:.3f}` = MDb.c. / MDa.r.s. = `{mdbc}` / `{mdars}`")
            st.write(f"🔹 **TQmax:** `{tqmax:.2f} µg` = TQ × SF")
            st.write(f"🔹 **TSL:** `{tsl} µg`")
            st.write(f"🔹 **TQmax / TSL:** `{ratio:.4f}`")

            if tqmax <= tsl:
                st.success("✅ 결과: Document Justification for SAFE")
            else:
                st.error("⚠️ 결과: TI or TTC and EEDmax 계산 필요")

        except Exception as e:
            st.error(f"에러 발생: {str(e)}")

# 개발자 정보 표시
st.markdown("회사: **BERLAB(밸랩)** | 개발자: **SANBAE LEE(이상배)** | 연락처: **010-9528-3091**")
