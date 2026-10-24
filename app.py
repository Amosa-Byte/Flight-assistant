import streamlit as st
import requests
import json

st.set_page_config(page_title="乘机流程助手", page_icon="✈️", layout="centered")

texts = {
    "zh": {
        "nav_title": "乘机流程助手",
        "lang_btn": "EN",
        "tab_home": "首页",
        "tab_process": "流程",
        "tab_luggage": "行李",
        "tab_ai": "AI 安检",
        "tab_tips": "常识",
        "home_sub": "欢迎使用 AI 乘机助手",
        "process_title": "国内乘机完整步骤",
        "p1_t": "1. 值机办理", "p1_d": "提前 2 小时到机场；凭身份证换取登机牌，办理行李托运。",
        "p2_t": "2. 安全检查", "p2_d": "携带身份证、登机牌；电子设备、充电宝单独拿出来过机安检。",
        "p3_t": "3. 候机等待", "p3_d": "看登机牌找到对应登机口，在附近座位等候，留意登机广播。",
        "p4_t": "4. 登机上机", "p4_d": "广播通知登机后，出示登机牌，排队登机，对号入座。",
        "lug_title": "行李规定",
        "lug_carry_t": "✅ 随身带上飞机（登机箱）",
        "lug_carry_d": "1 件随身行李，尺寸 20×40×55cm 以内；重量一般 ≤5kg。<br><br>⚠️ 充电宝只能随身携带，严禁托运。",
        "lug_check_t": "📦 托运行李",
        "lug_check_d": "经济舱：免费托运额度 20kg；超重要额外付费。<br><br>⚠️ 锂电池、充电宝不可以放进托运行李。",
        "ai_title": "AI 安检大脑",
        "ai_desc": "输入任何物品，AI 为您判断能否带上飞机",
        "ai_ph": "例如：防狼喷雾、化妆品、钢丝球、打火机",
        "ai_btn": "立即查询",
        "ai_spin": "AI 安检专家正在思考中...",
        "ai_warn": "请输入物品名称！",
        "ai_err": "查询失败！错误: ",
        "ai_prompt": "你是一个专业的航空安检专家。请判断物品能否带上飞机。必须严格返回纯JSON格式：{\"type\": \"danger/warn/ok\", \"tip\": \"一句话结论\", \"desc\": \"详细解释\"}",
        "tips_title": "乘机小常识",
        "tips_q1": "Q: 什么时候到机场合适？", "tips_a1": "建议国内航班提前 2 小时，国际航班提前 3 小时。",
        "tips_q2": "Q: 身份证丢了怎么办？", "tips_a2": "可在机场公安窗口办理临时乘机证明。",
        "tips_q3": "Q: 液体能带多少？", "tips_a3": "随身携带单瓶≤100ml，总量≤1L，需装透明袋。"
    },
    "en": {
        "nav_title": "Flight Assistant",
        "lang_btn": "中",
        "tab_home": "Home",
        "tab_process": "Process",
        "tab_luggage": "Baggage",
        "tab_ai": "AI Check",
        "tab_tips": "Tips",
        "home_sub": "Welcome to AI Flight Assistant",
        "process_title": "Domestic Flight Steps",
        "p1_t": "1. Check-in", "p1_d": "Arrive 2 hours early; get your boarding pass with ID and check your bags.",
        "p2_t": "2. Security Check", "p2_d": "Show ID and boarding pass; take out electronics and power banks separately.",
        "p3_t": "3. Waiting at the Gate", "p3_d": "Find your gate, wait nearby, and listen for boarding announcements.",
        "p4_t": "4. Boarding", "p4_d": "Show your boarding pass, queue up and take your assigned seat.",
        "lug_title": "Baggage Rules",
        "lug_carry_t": "✅ Carry-on (Cabin Bag)",
        "lug_carry_d": "1 carry-on bag, size within 20×40×55cm; weight usually ≤5kg.<br><br>⚠️ Power banks must be carried on, never checked.",
        "lug_check_t": "📦 Checked Baggage",
        "lug_check_d": "Economy: 20kg free allowance; extra weight costs more.<br><br>⚠️ Lithium batteries and power banks are forbidden in checked baggage.",
        "ai_title": "AI Security Brain",
        "ai_desc": "Enter any item, AI will judge if it can be brought on the plane",
        "ai_ph": "e.g., pepper spray, cosmetics, steel wool, lighter",
        "ai_btn": "Search Now",
        "ai_spin": "AI is thinking...",
        "ai_warn": "Please enter an item name!",
        "ai_err": "Failed! Error: ",
        "ai_prompt": "You are a professional aviation security expert. Judge if the item can be brought on a plane. You MUST return strictly in JSON format: {\"type\": \"danger/warn/ok\", \"tip\": \"One sentence conclusion\", \"desc\": \"Detailed explanation\"}",
        "tips_title": "Travel Tips",
        "tips_q1": "Q: When should I arrive at the airport?", "tips_a1": "2 hours before domestic, 3 hours before international flights.",
        "tips_q2": "Q: What if I lose my ID?", "tips_a2": "Apply for a temporary boarding certificate at the airport police office.",
        "tips_q3": "Q: How much liquid can I bring?", "tips_a3": "Carry-on: ≤100ml per bottle, ≤1L total, in a clear bag."
    }
}

if "lang" not in st.session_state:
    st.session_state.lang = "zh"
t = texts[st.session_state.lang]

# ==========================================
# 🚨 核心安全配置：从云端读取 Key 🚨
# ==========================================
if "MY_API_KEY" in st.secrets:
    MY_API_KEY = st.secrets["MY_API_KEY"]
else:
    MY_API_KEY = "本地测试用的Key填这里"  # 如果在本地测试，可以填在这里

# ==========================================
# 🎨 CSS 样式
# ==========================================
st.markdown("""
<style>
    .stApp { background-color: #f5f7fa !important; }
    header {visibility: hidden;} footer {visibility: hidden;}
    .block-container { max-width: 450px !important; padding-top: 1rem !important; padding-bottom: 2rem !important; }
    .top-nav { background: linear-gradient(135deg, #1677ff 0%, #4d94ff 100%); padding: 16px 20px; border-radius: 12px; text-align: center; box-shadow: 0 4px 10px rgba(22, 119, 255, 0.2); margin-bottom: 10px; }
    .nav-title { font-size: 18px; font-weight: bold; letter-spacing: 1px; color: white !important; -webkit-text-fill-color: white !important; }
    button[kind="secondary"] { border-radius: 20px !important; border: 1px solid #1677ff !important; background: transparent !important; height: 35px !important; padding: 0 15px !important; font-size: 14px !important; font-weight: bold !important; }
    button[kind="secondary"] p { color: #1677ff !important; -webkit-text-fill-color: #1677ff !important; }
    div[data-baseweb="tab-list"] { gap: 15px; }
    button[data-baseweb="tab"] p { color: #666666 !important; -webkit-text-fill-color: #666666 !important; font-size: 15px !important; font-weight: 500 !important; }
    button[data-baseweb="tab"][aria-selected="true"] p { color: #1677ff !important; -webkit-text-fill-color: #1677ff !important; font-weight: bold !important; }
    div[data-baseweb="tab-highlight"] { background-color: #1677ff !important; }
    button[kind="primary"] { width: 100% !important; background: linear-gradient(135deg, #1677ff 0%, #4d94ff 100%) !important; border: none !important; border-radius: 12px !important; height: 50px !important; font-size: 16px !important; font-weight: bold !important; box-shadow: 0 6px 15px rgba(22, 119, 255, 0.3) !important; }
    button[kind="primary"] p { color: white !important; -webkit-text-fill-color: white !important; }
    div[data-testid="stTextInput"] input { border-radius: 12px !important; border: 2px solid #eef4ff !important; padding: 14px 20px !important; font-size: 16px !important; background-color: #ffffff !important; color: #333 !important; -webkit-text-fill-color: #333 !important; }
    .content-card { background: white !important; border-radius: 12px; padding: 20px; margin-bottom: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); font-size: 15px; line-height: 1.6; color: #333333 !important; -webkit-text-fill-color: #333333 !important; }
    .content-card b { color: #1677ff !important; font-size: 16px; -webkit-text-fill-color: #1677ff !important; display: block; margin-bottom: 8px; }
    .banner { background: linear-gradient(135deg, #87b8f7, #1677ff); padding: 40px 20px; border-radius: 12px; text-align: center; font-size: 20px; font-weight: bold; margin-bottom: 20px; box-shadow: 0 6px 15px rgba(22, 119, 255, 0.2); color: white !important; -webkit-text-fill-color: white !important; }
    .result-card { background: white !important; border-radius: 15px; padding: 20px; margin-top: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.06); animation: slideUp 0.4s ease-out; color: #333 !important; -webkit-text-fill-color: #333 !important; }
    @keyframes slideUp { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
    .res-tag { font-size: 20px; font-weight: bold; margin-bottom: 8px; }
    .res-desc { font-size: 15px; line-height: 1.6; color: #555 !important; -webkit-text-fill-color: #555 !important; }
    .danger { border-left: 8px solid #ff4d4f; } .danger .res-tag { color: #ff4d4f; -webkit-text-fill-color: #ff4d4f; }
    .warn { border-left: 8px solid #faad14; } .warn .res-tag { color: #faad14; -webkit-text-fill-color: #faad14; }
    .ok { border-left: 8px solid #52c41a; } .ok .res-tag { color: #52c41a; -webkit-text-fill-color: #52c41a; }
</style>
""", unsafe_allow_html=True)

st.markdown(f'<div class="top-nav"><div class="nav-title">✈️ {t["nav_title"]}</div></div>', unsafe_allow_html=True)

col1, col2 = st.columns([7, 3])
with col2:
    if st.button(t["lang_btn"], type="secondary"):
        st.session_state.lang = "en" if st.session_state.lang == "zh" else "zh"
        st.rerun()

tab1, tab2, tab3, tab4, tab5 = st.tabs([t["tab_home"], t["tab_process"], t["tab_luggage"], t["tab_ai"], t["tab_tips"]])

with tab1:
    st.markdown(f'<div class="banner">{t["home_sub"]}</div>', unsafe_allow_html=True)
    st.info("👆 请点击上方选项卡，切换不同功能模块！")

with tab2:
    st.markdown(f'<div style="color:#1677ff !important; font-weight:bold; margin-bottom:15px; font-size:20px;">{t["process_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-card"><b>{t["p1_t"]}</b>{t["p1_d"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-card"><b>{t["p2_t"]}</b>{t["p2_d"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-card"><b>{t["p3_t"]}</b>{t["p3_d"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-card"><b>{t["p4_t"]}</b>{t["p4_d"]}</div>', unsafe_allow_html=True)

with tab3:
    st.markdown(f'<div style="color:#1677ff !important; font-weight:bold; margin-bottom:15px; font-size:20px;">{t["lug_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-card" style="border-left: 8px solid #1677ff;"><b>{t["lug_carry_t"]}</b>{t["lug_carry_d"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-card" style="border-left: 8px solid #1677ff;"><b>{t["lug_check_t"]}</b>{t["lug_check_d"]}</div>', unsafe_allow_html=True)

with tab4:
    st.markdown(f'<div style="color:#1677ff !important; font-weight:bold; font-size:20px;">{t["ai_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:#888 !important; font-size:14px; margin-bottom:20px;">{t["ai_desc"]}</div>', unsafe_allow_html=True)
    
    item = st.text_input("item", placeholder=t["ai_ph"], label_visibility="collapsed")
    
    if st.button(t["ai_btn"], type="primary", use_container_width=True):
        if not item:
            st.warning(t["ai_warn"])
        else:
            with st.spinner(t["ai_spin"]):
                url = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
                headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {MY_API_KEY}'}
                data = {
                    "model": "glm-4-flash",
                    "messages": [
                        {"role": "system", "content": t["ai_prompt"]},
                        {"role": "user", "content": item}
                    ],
                    "temperature": 0.1
                }
                try:
                    response = requests.post(url, headers=headers, json=data, timeout=10)
                    response.raise_for_status()
                    ai_text = response.json()['choices'][0]['message']['content']
                    ai_text = ai_text.replace('```json', '').replace('```', '').strip()
                    result = json.loads(ai_text)
                    
                    if result['type'] == 'danger': card_class = "danger"
                    elif result['type'] == 'warn': card_class = "warn"
                    else: card_class = "ok"
                        
                    html_card = f"""
                    <div class="result-card {card_class}">
                        <div class="res-tag">{result['tip']}</div>
                        <div class="res-desc">{result['desc']}</div>
                    </div>
                    """
                    st.markdown(html_card, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"{t['ai_err']} {e}")

with tab5:
    st.markdown(f'<div style="color:#1677ff !important; font-weight:bold; margin-bottom:15px; font-size:20px;">{t["tips_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-card"><b>{t["tips_q1"]}</b>{t["tips_a1"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-card"><b>{t["tips_q2"]}</b>{t["tips_a2"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-card"><b>{t["tips_q3"]}</b>{t["tips_a3"]}</div>', unsafe_allow_html=True)
