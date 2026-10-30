import streamlit as st
import requests
import json

st.set_page_config(page_title="乘机流程助手", page_icon="✈️", layout="wide")

# ==========================================

# 🌐 文字字典

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
        
    "hero_title": "让安检不再是盲盒，出行更从容。",
    "hero_desc": "基于大模型实时推理，精准解答随身携带与托运规则。",
    "hero_tag1": "航空级标准",
    "hero_tag2": "极速 AI 响应",
    "hero_tag3": "安心伴飞",
    
    # 首页美化文案
    "welcome_title": "👋 欢迎使用乘机流程助手",
    "welcome_subtitle": "您的随身航空出行管家，一站式解答所有乘机疑问。",
    "feat1_t": "🔍 AI 安检查询",
    "feat1_d": "输入任何物品，秒出能否携带结果。",
    "feat2_t": "🧳 行李规定",
    "feat2_d": "随身与托运的尺寸、重量及违禁品说明。",
    "feat3_t": "✈️ 乘机流程",
    "feat3_d": "从值机、安检到登机的完整步骤指南。",
    "welcome_action": "👆 请点击上方选项卡，开启您的智能出行体验！",
    
    "process_title": "国内乘机完整步骤",
    "p1_t": "1. 值机办理", "p1_d": "提前 2 小时到机场；凭身份证换取登机牌，办理行李托运。",
    "p2_t": "2. 安全检查", "p2_d": "携带身份证、登机牌；电子设备、充电宝单独拿出来过机安检。",
    "p3_t": "3. 候机等待", "p3_d": "看登机牌找到对应登机口，在附近座位等候，留意登机广播。",
    "p4_t": "4. 登机上机", "p4_d": "广播通知登机后，出示登机牌，排队登机，对号入座。",
    
    "lug_title": "行李规定",
    "lug_carry_t": "随身带上飞机（登机箱）",
    "lug_carry_d": "1 件随身行李，尺寸 20x40x55cm 以内；重量一般 <=5kg。注意：充电宝只能随身携带，严禁托运。",
    "lug_check_t": "托运行李",
    "lug_check_d": "经济舱：免费托运额度 20kg；超重要额外付费。注意：锂电池、充电宝不可以放进托运行李。",
    
    "ai_title": "AI 安检大脑",
    "ai_desc": "输入任何物品，AI 为您判断能否带上飞机",
    "ai_ph": "例如：防狼喷雾、化妆品、钢丝球、打火机",
    "ai_btn": "立即查询",
    "ai_spin": "AI 安检专家正在思考中...",
    "ai_warn": "请输入物品名称！",
    "ai_err": "查询失败！错误: ",
    "ai_prompt": "你是一个专业的航空安检专家。请判断物品能否带上飞机。必须严格返回纯JSON格式：{\"type\": \"danger/warn/ok\", \"tip\": \"一句话结论\", \"desc\": \"详细解释\"}",
    "res_empty": "请在左侧输入物品并点击查询",
    "res_basis": "判断依据",
    
    "tips_title": "乘机小常识",
    "tips_q1": "Q: 什么时候到机场合适？", "tips_a1": "建议国内航班提前 2 小时，国际航班提前 3 小时。",
    "tips_q2": "Q: 身份证丢了怎么办？", "tips_a2": "可在机场公安窗口办理临时乘机证明。",
    "tips_q3": "Q: 液体能带多少？", "tips_a3": "随身携带单瓶<=100ml，总量<=1L，需装透明袋。"
},
"en": {
    "app_title": "AI Flight Assistant",
    "lang_btn": "中",
    "tab_home": "Home",
    "tab_process": "Process",
    "tab_luggage": "Baggage",
    "tab_ai": "AI Check",
    "tab_tips": "Tips",
    
    "hero_title": "No More Guessing. Travel with Confidence.",
    "hero_desc": "Powered by LLM to provide instant and accurate carry-on & checked baggage rules.",
    "hero_tag1": "Airline Standards",
    "hero_tag2": "Instant AI",
    "hero_tag3": "Travel Securely",
    
    "welcome_title": "👋 Welcome to Flight Assistant",
    "welcome_subtitle": "Your personal travel steward, solving all your flight queries in one place.",
    "feat1_t": "🔍 AI Security Check",
    "feat1_d": "Enter any item, AI determines if it's allowed.",
    "feat2_t": "🧳 Baggage Rules",
    "feat2_d": "Dimensions, weight limits, and forbidden items.",
    "feat3_t": "✈️ Flight Process",
    "feat3_d": "Step-by-step guide from check-in to boarding.",
    "welcome_action": "👆 Click the tabs above to start your smart travel experience!",
    
    "process_title": "Domestic Flight Steps",
    "p1_t": "1. Check-in", "p1_d": "Arrive 2 hours early; get your boarding pass with ID and check your bags.",
    "p2_t": "2. Security Check", "p2_d": "Show ID and boarding pass; take out electronics and power banks separately.",
    "p3_t": "3. Waiting at the Gate", "p3_d": "Find your gate, wait nearby, and listen for boarding announcements.",
    "p4_t": "4. Boarding", "p4_d": "Show your boarding pass, queue up and take your assigned seat.",
    
    "lug_title": "Baggage Rules",
    "lug_carry_t": "Carry-on (Cabin Bag)",
    "lug_carry_d": "1 carry-on bag, size within 20x40x55cm; weight usually <=5kg. Note: Power banks must be carried on, never checked.",
    "lug_check_t": "Checked Baggage",
    "lug_check_d": "Economy: 20kg free allowance; extra weight costs more. Note: Lithium batteries and power banks are forbidden in checked baggage.",
    
    "ai_title": "AI Security Brain",
    "ai_desc": "Enter any item, AI will judge if it can be brought on the plane",
    "ai_ph": "e.g., pepper spray, cosmetics, steel wool, lighter",
    "ai_btn": "Search Now",
    "ai_spin": "AI is thinking...",
    "ai_warn": "Please enter an item name!",
    "ai_err": "Failed! Error: ",
    "ai_prompt": "You are a professional aviation security expert. Judge if the item can be brought on a plane. You MUST return strictly in JSON format: {\"type\": \"danger/warn/ok\", \"tip\": \"One sentence conclusion\", \"desc\": \"Detailed explanation\"}",
    "res_empty": "Enter an item on the left and click Search",
    "res_basis": "Basis",
    
    "tips_title": "Travel Tips",
    "tips_q1": "Q: When should I arrive at the airport?", "tips_a1": "2 hours before domestic, 3 hours before international flights.",
    "tips_q2": "Q: What if I lose my ID?", "tips_a2": "Apply for a temporary boarding certificate at the airport police office.",
    "tips_q3": "Q: How much liquid can I bring?", "tips_a3": "Carry-on: <=100ml per bottle, <=1L total, in a clear bag."
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

# ==========================================

# 🎨 CSS 样式

# ==========================================

st.markdown("""

""", unsafe_allow_html=True)

# ==========================================

# 🚀 页面渲染

# ==========================================

col_space, col_lang = st.columns([9, 1])
with col_lang:
    if st.button(t["lang_btn"], type="secondary"):
        st.session_state.lang = "en" if st.session_state.lang == "zh" else "zh"
        st.rerun()

st.markdown(f'{t["hero_title"]}{t["hero_desc"]}{t["hero_tag1"]}{t["hero_tag2"]}{t["hero_tag3"]}',
            unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([t["tab_home"], t["tab_process"], t["tab_luggage"], t["tab_ai"], t["tab_tips"]])

# ================= 👇 首页改造 =================

with tab1:
    st.write("")
    st.write("")

```
# 使用容器构建欢迎面板
with st.container(border=True):
    # 居中大标题
    st.markdown(f"<h1 style='text-align: center; color: #1677ff !important; font-size: 36px !important; margin-bottom: 0;'>{t['welcome_title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #64748b !important; font-size: 16px !important; margin-top: 8px; margin-bottom: 30px;'>{t['welcome_subtitle']}</p>", unsafe_allow_html=True)
    
    # 三列功能简介卡片
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.info(f"**{t['feat1_t']}**\n\n{t['feat1_d']}")
    with c2:
        st.success(f"**{t['feat2_t']}**\n\n{t['feat2_d']}")
    with c3:
        st.warning(f"**{t['feat3_t']}**\n\n{t['feat3_d']}")
        
    st.write("")
    st.write("")
    # 底部引导语
    st.markdown(f"<div style='text-align: center; color: #1677ff; font-weight: bold; font-size: 18px;'>{t['welcome_action']}</div>", unsafe_allow_html=True)
    st.write("")
```

# ================= 乘机流程 =================

with tab2:
    st.markdown(f'

{t["process_title"]}', unsafe_allow_html=True)
    col_p1, col_p2 = st.columns(2, gap="medium")
    with col_p1:
        st.markdown(f'{t["p1_t"]}{t["p1_d"]}', unsafe_allow_html=True)
        st.markdown(f'{t["p3_t"]}{t["p3_d"]}', unsafe_allow_html=True)
    with col_p2:
        st.markdown(f'{t["p2_t"]}{t["p2_d"]}', unsafe_allow_html=True)
        st.markdown(f'{t["p4_t"]}{t["p4_d"]}', unsafe_allow_html=True)

# ================= 行李规定 =================

with tab3:
    st.markdown(f'

{t["lug_title"]}', unsafe_allow_html=True)
    col_l1, col_l2 = st.columns(2, gap="medium")
    with col_l1:
        st.markdown(f'{t["lug_carry_t"]}{t["lug_carry_d"]}', unsafe_allow_html=True)
    with col_l2:
        st.markdown(f'{t["lug_check_t"]}{t["lug_check_d"]}', unsafe_allow_html=True)

# ================= AI 安检 =================

with tab4:
    st.markdown(f'

{t["ai_title"]}', unsafe_allow_html=True)
    st.markdown(f'{t["ai_desc"]}', unsafe_allow_html=True)
    col_input, col_result = st.columns([1, 1.2], gap="large")
    with col_input:
        with st.container(border=True):
            st.write(t["ai_ph"])
            item = st.text_input("item_input", label_visibility="collapsed")
            st.write("")
            if st.button(t["ai_btn"], type="primary", use_container_width=True):
                if not item:
                    st.warning(t["ai_warn"])
                else:
                    with st.spinner(t["ai_spin"]):
                        url = '[https://open.bigmodel.cn/api/paas/v4/chat/completions](https://open.bigmodel.cn/api/paas/v4/chat/completions)'
                        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {MY_API_KEY}'}
                        data = {
                            "model": "glm-4-flash",
                            "messages": [{"role": "system", "content": t["ai_prompt"]}, {"role": "user", "content": f"请判断：{item}"}],
                            "temperature": 0.1,
                            "top_p": 0.7
                        }
                        try:
                            response = requests.post(url, headers=headers, json=data, timeout=10)
                            response.raise_for_status()
                            ai_text = response.json()['choices'][0]['message']['content']
                            ai_text = ai_text.replace('`json', '').replace('`', '').strip()
                            st.session_state.ai_result = json.loads(ai_text)
                            st.session_state.ai_item = item
                        except Exception as e:
                            st.error(f"{t['ai_err']} {e}")
                            st.session_state.ai_result = None
    with col_result:
        if st.session_state.ai_result is None:
            st.markdown(f'{t["res_empty"]}', unsafe_allow_html=True)
        else:
            res = st.session_state.ai_result
            color = "#ff4d4f" if res['type'] == 'danger' else ("#faad14" if res['type'] == 'warn' else "#52c41a")
            html_card = f'{res["tip"]}{st.session_state.ai_item}{res["desc"]}{t["res_basis"]}依据民航局安检规定，具体以机场现场为准。'
            st.markdown(html_card, unsafe_allow_html=True)

# ================= 乘机常识 =================

with tab5:
    st.markdown(f'

{t["tips_title"]}', unsafe_allow_html=True)
    col_t1, col_t2 = st.columns(2, gap="medium")
    with col_t1:
        st.markdown(f'{t["tips_q1"]}  
{t["tips_a1"]}', unsafe_allow_html=True)
    with col_t2:
        st.markdown(f'{t["tips_q2"]}  
{t["tips_a2"]}', unsafe_allow_html=True)
    st.markdown(f'{t["tips_q3"]}  
{t["tips_a3"]}', unsafe_allow_html=True)
