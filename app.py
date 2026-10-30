import streamlit as st
import requests
import json

st.set_page_config(page_title="乘机流程助手", page_icon="✈️", layout="wide")

# ==========================================
# 🌐 文字字典 (精简防错)
# ==========================================
texts = {
    "zh": {
        "app_title": "AI 乘机流程助手",
        "lang_btn": "EN",
        "tab_home": "首页",
        "tab_process": "乘机流程",
        "tab_luggage": "行李规定",
        "tab_ai": "AI 安检",
        "tab_tips": "乘机常识",
        
        # 首页专用文案
        "welcome_title": "👋 欢迎使用乘机流程助手",
        "welcome_desc": "您的随身航空出行管家。查安检、看规定、排疑问，一键搞定。",
        "feat1_t": "🔍 AI 安检",
        "feat1_d": "输入任何物品，AI 秒判能否带上飞机。",
        "feat2_t": "🧳 行李规定",
        "feat2_d": "随身与托运行李的尺寸、重量及违禁品说明。",
        "feat3_t": "✈️ 乘机流程",
        "feat3_d": "从值机、安检到登机的完整乘机步骤指南。",
        
        "process_title": "国内乘机完整步骤",
        "p1": "**1. 值机办理**\n\n提前 2 小时到机场；凭身份证换取登机牌，办理行李托运。",
        "p2": "**2. 安全检查**\n\n携带身份证、登机牌；电子设备、充电宝单独拿出来过机安检。",
        "p3": "**3. 候机等待**\n\n看登机牌找到对应登机口，在附近座位等候，留意登机广播。",
        "p4": "**4. 登机上机**\n\n广播通知登机后，出示登机牌，排队登机，对号入座。",
        
        "lug_title": "行李规定",
        "lug_carry": "**随身带上飞机（登机箱）**\n\n1 件随身行李，尺寸 20x40x55cm 以内；重量一般 <=5kg。\n\n⚠️ 注意：充电宝只能随身携带，严禁托运。",
        "lug_check": "**托运行李**\n\n经济舱：免费托运额度 20kg；超重要额外付费。\n\n⚠️ 注意：锂电池、充电宝不可以放进托运行李。",
        
        "ai_title": "AI 安检大脑",
        "ai_desc": "输入任何物品，AI 为您判断能否带上飞机",
        "ai_ph": "例如：防狼喷雾、化妆品、钢丝球、打火机",
        "ai_btn": "立即查询",
        "ai_spin": "AI 安检专家正在思考中...",
        "ai_warn": "请输入物品名称！",
        "ai_err": "查询失败！错误: ",
        "ai_prompt": "你是一个专业的航空安检专家。请判断物品能否带上飞机。必须严格返回纯JSON格式，不要包含markdown代码块符号。JSON必须包含三个键：type（值为danger, warn, ok之一）, tip（一句话结论）, desc（详细解释）。",
        "res_empty": "请在左侧输入物品并点击查询",
        "res_basis": "依据民航局安检规定，具体以机场现场为准。",
        
        "tips_title": "乘机小常识",
        "tips_q1": "**Q: 什么时候到机场合适？**\n\n建议国内航班提前 2 小时，国际航班提前 3 小时。",
        "tips_q2": "**Q: 身份证丢了怎么办？**\n\n可在机场公安窗口办理临时乘机证明。",
        "tips_q3": "**Q: 液体能带多少？**\n\n随身携带单瓶<=100ml，总量<=1L，需装透明袋。"
    },
    "en": {
        "app_title": "AI Flight Assistant",
        "lang_btn": "中",
        "tab_home": "Home",
        "tab_process": "Process",
        "tab_luggage": "Baggage",
        "tab_ai": "AI Check",
        "tab_tips": "Tips",
        
        "welcome_title": "👋 Welcome to Flight Assistant",
        "welcome_desc": "Your personal travel steward. Check security, rules, and FAQs in one click.",
        "feat1_t": "🔍 AI Check",
        "feat1_d": "Enter any item, AI determines if it's allowed.",
        "feat2_t": "🧳 Baggage Rules",
        "feat2_d": "Dimensions, weight limits, and forbidden items.",
        "feat3_t": "✈️ Flight Process",
        "feat3_d": "Step-by-step guide from check-in to boarding.",
        
        "process_title": "Domestic Flight Steps",
        "p1": "**1. Check-in**\n\nArrive 2 hours early; get your boarding pass with ID and check your bags.",
        "p2": "**2. Security Check**\n\nShow ID and boarding pass; take out electronics and power banks separately.",
        "p3": "**3. Waiting at the Gate**\n\nFind your gate, wait nearby, and listen for boarding announcements.",
        "p4": "**4. Boarding**\n\nShow your boarding pass, queue up and take your assigned seat.",
        
        "lug_title": "Baggage Rules",
        "lug_carry": "**Carry-on (Cabin Bag)**\n\n1 carry-on bag, size within 20x40x55cm; weight usually <=5kg.\n\n⚠️ Note: Power banks must be carried on.",
        "lug_check": "**Checked Baggage**\n\nEconomy: 20kg free allowance; extra weight costs more.\n\n⚠️ Note: Lithium batteries forbidden in checked.",
        
        "ai_title": "AI Security Brain",
        "ai_desc": "Enter any item, AI will judge if it can be brought on the plane",
        "ai_ph": "e.g., pepper spray, cosmetics, steel wool, lighter",
        "ai_btn": "Search Now",
        "ai_spin": "AI is thinking...",
        "ai_warn": "Please enter an item name!",
        "ai_err": "Failed! Error: ",
        "ai_prompt": "You are a professional aviation security expert. Judge if the item can be brought on a plane. You MUST return strictly in raw JSON format without markdown blocks. The JSON must contain exactly three keys: type (must be danger, warn, or ok), tip (one sentence conclusion), and desc (detailed explanation).",
        "res_empty": "Enter an item on the left and click Search",
        "res_basis": "Based on civil aviation security regulations.",
        
        "tips_title": "Travel Tips",
        "tips_q1": "**Q: When should I arrive at the airport?**\n\n2 hours before domestic, 3 hours before international flights.",
        "tips_q2": "**Q: What if I lose my ID?**\n\nApply for a temporary boarding certificate at the airport police office.",
        "tips_q3": "**Q: How much liquid can I bring?**\n\nCarry-on: <=100ml per bottle, <=1L total, in a clear bag."
    }
}

if "lang" not in st.session_state:
    st.session_state.lang = "zh"
if "ai_result" not in st.session_state:
    st.session_state.ai_result = None
if "ai_item" not in st.session_state:
    st.session_state.ai_item = ""

t = texts[st.session_state.lang]

if "MY_API_KEY" in st.secrets:
    MY_API_KEY = st.secrets["MY_API_KEY"]
else:
    MY_API_KEY = "本地测试Key"

# 顶部标题与语言切换
col_title, col_lang = st.columns([8, 2])
with col_title:
    st.title(t["app_title"])
with col_lang:
    st.write("")
    if st.button(t["lang_btn"], use_container_width=True):
        st.session_state.lang = "en" if st.session_state.lang == "zh" else "zh"
        st.rerun()

# 选项卡
tab1, tab2, tab3, tab4, tab5 = st.tabs([t["tab_home"], t["tab_process"], t["tab_luggage"], t["tab_ai"], t["tab_tips"]])

# ================= 首页 =================
with tab1:
    st.write("")
    st.header(t["welcome_title"])
    st.write(t["welcome_desc"])
    st.divider()
    
    # 使用原生三列布局 + 边框卡片
    c1, c2, c3 = st.columns(3, gap="medium")
    
    with c1:
        with st.container(border=True):
            st.subheader(t["feat1_t"])
            st.caption(t["feat1_d"])
            st.write("---")
            st.write("👉 请点击上方 **AI 安检** 标签页")
            
    with c2:
        with st.container(border=True):
            st.subheader(t["feat2_t"])
            st.caption(t["feat2_d"])
            st.write("---")
            st.write("👉 请点击上方 **行李规定** 标签页")
            
    with c3:
        with st.container(border=True):
            st.subheader(t["feat3_t"])
            st.caption(t["feat3_d"])
            st.write("---")
            st.write("👉 请点击上方 **乘机流程** 标签页")

# ================= 流程 =================
with tab2:
    st.header(t["process_title"])
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.info(t["p1"])
        with st.container(border=True):
            st.info(t["p3"])
    with col2:
        with st.container(border=True):
            st.info(t["p2"])
        with st.container(border=True):
            st.info(t["p4"])

# ================= 行李 =================
with tab3:
    st.header(t["lug_title"])
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.info(t["lug_carry"])
    with col2:
        with st.container(border=True):
            st.info(t["lug_check"])

# ================= AI 安检 =================
with tab4:
    st.header(t["ai_title"])
    st.write(t["ai_desc"])
    
    col_in, col_out = st.columns([1, 1.2], gap="large")
    with col_in:
        with st.container(border=True):
            st.write(t["ai_ph"])
            item = st.text_input("item_input", label_visibility="collapsed")
            if st.button(t["ai_btn"], type="primary", use_container_width=True):
                if not item:
                    st.warning(t["ai_warn"])
                else:
                    with st.spinner(t["ai_spin"]):
                        url = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
                        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + MY_API_KEY}
                        data = {
                            "model": "glm-4-flash",
                            "messages": [{"role": "system", "content": t["ai_prompt"]}, {"role": "user", "content": "请判断：" + item}],
                            "temperature": 0.1,
                            "top_p": 0.7
                        }
                        try:
                            response = requests.post(url, headers=headers, json=data, timeout=10)
                            response.raise_for_status()
                            ai_text = response.json()['choices'][0]['message']['content']
                            ai_text = ai_text.replace('```json', '').replace('```', '').strip()
                            st.session_state.ai_result = json.loads(ai_text)
                            st.session_state.ai_item = item
                        except Exception as e:
                            st.error(t['ai_err'] + str(e))
                            st.session_state.ai_result = None
    
    with col_out:
        if st.session_state.ai_result is None:
            st.info(t["res_empty"])
        else:
            res = st.session_state.ai_result
            # 用 Streamlit 原生组件展示结果卡片（绝对稳定）
            if res['type'] == 'danger':
                st.error(f"❌ **{res['tip']}**\n\n**{st.session_state.ai_item}**\n\n{res['desc']}")
            elif res['type'] == 'warn':
                st.warning(f"⚠️ **{res['tip']}**\n\n**{st.session_state.ai_item}**\n\n{res['desc']}")
            else:
                st.success(f"✅ **{res['tip']}**\n\n**{st.session_state.ai_item}**\n\n{res['desc']}")
            
            st.caption(t["res_basis"])

# ================= 常识 =================
with tab5:
    st.header(t["tips_title"])
    with st.container(border=True):
        st.info(t["tips_q1"])
    with st.container(border=True):
        st.info(t["tips_q2"])
    with st.container(border=True):
        st.info(t["tips_q3"])
