import streamlit as st
import requests
import json

# 1. 开启宽屏模式
st.set_page_config(page_title="飞行随身查", page_icon="✈️", layout="wide")

# ==========================================
# 🌐 多语言字典
# ==========================================
texts = {
    "zh": {
        "app_title": "飞行随身查",
        "app_subtitle": "Flight Carry-On Checker",
        "lang_btn": "EN",
        "hero_tag": "TRAVEL SMART · PACK WITH CONFIDENCE",
        "hero_title": "出发前查一查，\n让每一次出行更安心。",
        "hero_desc": "输入物品名称和容器规格，快速获取中国大陆、港澳台及国际航线的随身携带与托运建议。",
        "feat1": "合规出行\n基于航空规则",
        "feat2": "快速查询\n即刻获取结果",
        "feat3": "安心启程\n让旅途更轻松",
        
        "tab1": "快速查询",
        "tab2": "物品资料库",
        "tab3": "规则说明",
        "tab4": "最近查询",
        
        "form_title": "查一下这件物品",
        "form_desc": "选择航线、输入名称与规格，快速获取携带建议。",
        "route_label": "航线类型",
        "route_1": "中国大陆",
        "route_2": "港澳台",
        "route_3": "国际",
        "item_label": "物品名称",
        "item_ph": "例如：眼药水、充电宝、洗面奶",
        "capacity_label": "容器标注容量 / 规格",
        "capacity_ph": "例如 100",
        "carry_label": "携带方式",
        "carry_1": "随身携带",
        "carry_2": "托运行李",
        "btn_search": "立即查询",
        
        "res_empty": "请在左侧输入物品信息并点击查询",
        "res_ok": "✅ 可以携带",
        "res_warn": "⚠️ 限量携带",
        "res_danger": "❌ 禁止携带",
        "res_basis": "判断依据",
        "res_btn_save": "保存本次查询",
        "res_btn_copy": "复制结果文字",
        "res_tip": "结果仅供参考，最终以出发机场安检、承运航空公司目的地海关要求为准。",
        
        # 注意这里：不用大括号，用 [item] 代替
        "ai_prompt": "你是一个专业的航空安检专家。请根据物品：[item]，容量：[cap]，航线：[route]。判断能否带上飞机。必须严格返回纯JSON格式：{\"type\": \"danger/warn/ok\", \"tip\": \"一句话结论\", \"desc\": \"详细解释，说明托运和随身要求\"}"
    },
    "en": {
        "app_title": "Flight Carry-On Checker",
        "app_subtitle": "Travel Smart",
        "lang_btn": "中",
        "hero_tag": "TRAVEL SMART · PACK WITH CONFIDENCE",
        "hero_title": "Check before you go,\ntravel with peace of mind.",
        "hero_desc": "Enter item name and capacity to get carry-on and checked baggage advice for Mainland China, HK/Macao/Taiwan, and International flights.",
        "feat1": "Compliance\nBased on rules",
        "feat2": "Fast Query\nInstant results",
        "feat3": "Peace of Mind\nTravel easier",
        
        "tab1": "Quick Check",
        "tab2": "Item Database",
        "tab3": "Rules",
        "tab4": "Recent",
        
        "form_title": "Check an Item",
        "form_desc": "Select route, enter name and capacity to get advice.",
        "route_label": "Flight Route",
        "route_1": "Mainland",
        "route_2": "HK/Macau/TW",
        "route_3": "International",
        "item_label": "Item Name",
        "item_ph": "e.g., eye drops, power bank",
        "capacity_label": "Capacity / Specs",
        "capacity_ph": "e.g. 100",
        "carry_label": "Carry Method",
        "carry_1": "Carry-on",
        "carry_2": "Checked",
        "btn_search": "Search Now",
        
        "res_empty": "Enter item info on the left and click search",
        "res_ok": "✅ Allowed",
        "res_warn": "⚠️ Restricted",
        "res_danger": "❌ Forbidden",
        "res_basis": "Basis",
        "res_btn_save": "Save",
        "res_btn_copy": "Copy Text",
        "res_tip": "For reference only. Final decision rests with security and airline.",
        
        "ai_prompt": "You are a professional aviation security expert. Based on item: [item], capacity: [cap], route: [route]. Judge if it can be brought on a plane. You MUST return strictly in JSON format: {\"type\": \"danger/warn/ok\", \"tip\": \"One sentence conclusion\", \"desc\": \"Detailed explanation for carry-on and checked\"}"
    }
}

if "lang" not in st.session_state:
    st.session_state.lang = "zh"
if "search_result" not in st.session_state:
    st.session_state.search_result = None
if "search_item" not in st.session_state:
    st.session_state.search_item = ""

t = texts[st.session_state.lang]

if "MY_API_KEY" in st.secrets:
    MY_API_KEY = st.secrets["MY_API_KEY"]
else:
    MY_API_KEY = "本地测试Key"

# ==========================================
# 🎨 注入宽屏专属 CSS (强力修复深色模式)
# ==========================================
st.markdown("""
<style>
    .block-container { max-width: 1200px !important; padding-top: 1rem !important; }
    header {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background-color: #f8fafc !important; }
    
    /* 强制锁定文字颜色为深色 */
    p, h1, h2, h3, h4, h5, h6, span, div {
        color: #333333 !important;
        -webkit-text-fill-color: #333333 !important;
    }
    .hero-box p, .hero-box span, .hero-box div {
        color: white !important;
        -webkit-text-fill-color: white !important;
    }

    /* 修复单选按钮文字颜色 */
    div[data-testid="stRadio"] label p {
        color: #333 !important;
        -webkit-text-fill-color: #333 !important;
    }

    /* 隐藏原生 Tab 边框，改成胶囊样式 */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #1677ff !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: white !important;
        -webkit-text-fill-color: white !important;
        font-weight: bold !important;
    }
    button[data-baseweb="tab"] p {
        color: #666 !important;
        -webkit-text-fill-color: #666 !important;
        font-weight: 500 !important;
        font-size: 15px !important;
    }
    div[data-baseweb="tab-highlight"] { display: none; }
    
    /* Hero Banner */
    .hero-box {
        background: linear-gradient(105deg, #1677ff 0%, #4d94ff 100%);
        border-radius: 16px; padding: 40px 50px; color: white;
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 25px; box-shadow: 0 10px 30px rgba(22, 119, 255, 0.15);
    }
    .hero-text { z-index: 2; max-width: 600px; }
    .hero-tag { font-size: 12px; letter-spacing: 2px; font-weight: bold; opacity: 0.8; margin-bottom: 15px; }
    .hero-title { font-size: 36px; font-weight: bold; line-height: 1.3; margin-bottom: 15px; white-space: pre-line; }
    .hero-desc { font-size: 15px; opacity: 0.9; margin-bottom: 30px; line-height: 1.5; }
    .hero-features { display: flex; gap: 40px; }
    .feat-item { font-size: 14px; font-weight: bold; display: flex; flex-direction: column; gap: 4px; white-space: pre-line;}
    .feat-item span { font-size: 12px; font-weight: normal; opacity: 0.8; }
    
    /* 表单卡片与结果卡片 */
    .form-card, .result-card {
        background: white !important; border-radius: 16px; padding: 30px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
    }
    .form-title { font-size: 22px; font-weight: bold; color: #333 !important; margin-bottom: 5px; }
    .form-desc { font-size: 14px; color: #888 !important; margin-bottom: 25px; }
    
    /* 强制输入框白底黑字 */
    div[data-testid="stTextInput"] input {
        border-radius: 10px !important; border: 1px solid #e2e8f0 !important;
        padding: 12px 15px !important; font-size: 15px !important;
        background-color: #ffffff !important;
        color: #333333 !important;
        -webkit-text-fill-color: #333333 !important;
    }
    
    button[kind="primary"] {
        background: #1677ff !important; border-radius: 10px !important;
        height: 45px !important; font-weight: bold !important;
    }
    
    /* 结果卡片内部 */
    .result-card { min-height: 400px; }
    .tag-ok { background: #dcfce7; color: #166534 !important; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: bold; display: inline-block; margin-bottom: 15px;}
    .tag-warn { background: #fef08a; color: #854d0e !important; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: bold; display: inline-block; margin-bottom: 15px;}
    .tag-danger { background: #fee2e2; color: #991b1b !important; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: bold; display: inline-block; margin-bottom: 15px;}
    .res-title { font-size: 24px; font-weight: bold; color: #333 !important; margin-bottom: 10px; }
    .res-desc { font-size: 15px; color: #555 !important; line-height: 1.6; margin-bottom: 25px; }
    
    .basis-box { background: #f8fafc; border-radius: 10px; padding: 20px; margin-bottom: 25px; border: 1px solid #f1f5f9;}
    .basis-title { font-size: 14px; font-weight: bold; color: #1677ff !important; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 🚀 顶部导航栏
# ==========================================
col_logo, col_lang = st.columns([8, 1])
with col_logo:
    st.markdown(f"### ✈️ {t['app_title']} \n<span style='font-size:12px;color:#888;'>{t['app_subtitle']}</span>", unsafe_allow_html=True)
with col_lang:
    if st.button(t["lang_btn"], type="secondary"):
        st.session_state.lang = "en" if st.session_state.lang == "zh" else "zh"
        st.rerun()

st.write("")

# ==========================================
# 🚀 Hero 横幅
# ==========================================
st.markdown(f"""
<div class="hero-box">
    <div class="hero-text">
        <div class="hero-tag">{t['hero_tag']}</div>
        <div class="hero-title">{t['hero_title']}</div>
        <div class="hero-desc">{t['hero_desc']}</div>
        <div class="hero-features">
            <div class="feat-item">🛡️ {t['feat1']}</div>
            <div class="feat-item">⚡ {t['feat2']}</div>
            <div class="feat-item">🧳 {t['feat3']}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 🚀 核心 Tabs 区域
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

with tab1:
    col_left, col_right = st.columns([1.2, 1], gap="large")

    # ---------- 左侧：查询表单 ----------
    with col_left:
        st.markdown(f"""
        <div class="form-card">
            <div class="form-title">🔍 {t['form_title']}</div>
            <div class="form-desc">{t['form_desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write(t["route_label"])
        route = st.radio("route", [t["route_1"], t["route_2"], t["route_3"]], horizontal=True, label_visibility="collapsed")
        
        item_name = st.text_input(t["item_label"], placeholder=t["item_ph"])
        
        col_cap, col_unit = st.columns([3, 1])
        with col_cap:
            capacity = st.text_input(t["capacity_label"], placeholder=t["capacity_ph"])
        with col_unit:
            st.write(" ") 
            st.write("ml")
            
        st.write(t["carry_label"])
        carry_method = st.radio("carry", [t["carry_1"], t["carry_2"]], horizontal=True, label_visibility="collapsed")
        
        st.write("")
        if st.button(t["btn_search"], type="primary", use_container_width=True):
            if not item_name:
                st.warning("请输入物品名称")
            else:
                with st.spinner("AI 正在判断中..."):
                    url = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
                    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {MY_API_KEY}'}
                    
                    # 使用 replace 避免花括号报错
                    prompt = t["ai_prompt"].replace("[item]", item_name).replace("[cap]", capacity).replace("[route]", route)
                    
                    data = {
                        "model": "glm-4-flash",
                        "messages": [{"role": "system", "content": prompt}],
                        "temperature": 0.1
                    }
                    try:
                        response = requests.post(url, headers=headers, json=data, timeout=10)
                        response.raise_for_status()
                        ai_text = response.json()['choices'][0]['message']['content']
                        ai_text = ai_text.replace('```json', '').replace('```', '').strip()
                        result = json.loads(ai_text)
                        
                        st.session_state.search_result = result
                        st.session_state.search_item = f"{item_name} · {capacity}ml"
                    except Exception as e:
                        st.error(f"查询失败: {e}")

    # ---------- 右侧：结果展示 ----------
    with col_right:
        if st.session_state.search_result is None:
            st.markdown(f"""
            <div class="result-card" style="display:flex; align-items:center; justify-content:center;">
                <div style="color:#94a3b8; font-size:15px;">{t['res_empty']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            res = st.session_state.search_result
            item_title = st.session_state.search_item
            
            if res['type'] == 'ok':
                tag_class = "tag-ok"
                tag_text = t['res_ok']
            elif res['type'] == 'warn':
                tag_class = "tag-warn"
                tag_text = t['res_warn']
            else:
                tag_class = "tag-danger"
                tag_text = t['res_danger']
                
            st.markdown(f"""
            <div class="result-card">
                <div class="{tag_class}">{tag_text}</div>
                <div class="res-title">{item_title}</div>
                <div class="res-desc">{res['desc']}</div>
                
                <div class="basis-box">
                    <div class="basis-title">📋 {t['res_basis']}</div>
                    <div style="font-size:14px; color:#555;">{res['tip']}</div>
                </div>
                
                <div style="display:flex; gap:10px; margin-bottom:20px;">
                    <button style="flex:1; padding:10px; background:#1677ff; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">{t['res_btn_save']}</button>
                    <button style="flex:1; padding:10px; background:white; color:#333; border:1px solid #ccc; border-radius:8px; font-weight:bold; cursor:pointer;">{t['res_btn_copy']}</button>
                </div>
                
                <div style="font-size:12px; color:#94a3b8; text-align:center;">{t['res_tip']}</div>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.info("物品资料库正在建设中...")
with tab3:
    st.info("规则说明正在建设中...")
with tab4:
    st.info("最近查询记录为空...")
