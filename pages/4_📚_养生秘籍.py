import streamlit as st
import pandas as pd

# 页面配置
st.set_page_config(
    page_title="中医非药物治疗养生科普",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 2rem;
        color: #2E8B57;
        border-bottom: 2px solid #2E8B57;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .therapy-card {
        background-color: #f8fff8;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
        margin-bottom: 1rem;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 主标题
st.markdown('<div class="main-header">🌿 中医非药物治疗养生科普</div>', unsafe_allow_html=True)

# 侧边栏导航
st.sidebar.title("导航菜单")
section = st.sidebar.radio("选择治疗类型", [
    "概览介绍",
    "针灸疗法",
    "艾灸疗法", 
    "推拿按摩",
    "拔罐疗法",
    "刮痧疗法",
    "气功导引",
    "药膳食疗",
    "注意事项"
])

# 概览介绍
if section == "概览介绍":
    st.markdown('<div class="section-header">📚 中医非药物治疗概览</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("""
        ### 什么是中医非药物治疗？
        
        中医非药物治疗是指不通过内服药物，而是运用各种物理方法和自然疗法来调理身体、
        防治疾病的治疗方法。这些方法源远流长，具有独特的理论体系和丰富的临床经验。
        
        ### 主要特点：
        - **自然安全**：多数方法无化学药物副作用
        - **整体调理**：注重人体整体平衡
        - **个体化治疗**：根据个人体质辨证施治
        - **预防为主**：强调"治未病"理念
        """)
    
    with col2:
        st.image("https://via.placeholder.com/300x200/2E8B57/FFFFFF?text=中医养生", 
                caption="中医养生智慧")
    
    # 疗法对比表格
    st.subheader("📊 主要非药物治疗方法对比")
    
    therapy_data = {
        "治疗方法": ["针灸", "艾灸", "推拿", "拔罐", "刮痧", "气功"],
        "主要作用": ["疏通经络、调和气血", "温通经脉、散寒除湿", "舒筋活络、理气活血", "祛风散寒、活血化瘀", "解表透疹、清热解毒", "调息养神、强身健体"],
        "适用人群": ["各类疼痛、内科疾病", "寒性体质、虚寒证", "肌肉酸痛、疲劳", "风寒湿痹、瘀血证", "外感发热、中暑", "亚健康、慢性病"],
        "疗程频率": ["1-3次/周", "2-4次/周", "2-5次/周", "1-2次/周", "1次/周", "每日练习"]
    }
    
    df = pd.DataFrame(therapy_data)
    st.dataframe(df, use_container_width=True)

# 针灸疗法
elif section == "针灸疗法":
    st.markdown('<div class="section-header">📍 针灸疗法</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["基本介绍", "常用穴位", "适应症", "操作视频"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            <div class="therapy-card">
            <h3>📖 针灸简介</h3>
            <p>针灸是中医的重要组成部分，通过刺激特定穴位来调节人体气血运行，达到治疗疾病的目的。</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("""
            ### 针灸的作用原理
            
            1. **疏通经络**：解除经络阻塞，恢复气血正常运行
            2. **调和阴阳**：调整人体阴阳平衡状态
            3. **扶正祛邪**：增强机体抗病能力，驱除病邪
            4. **调节脏腑**：通过经络联系调节内脏功能
            """)
        
        with col2:
            st.image("https://via.placeholder.com/300x200/2E8B57/FFFFFF?text=针灸演示", 
                    caption="针灸操作示意图")
    
    with tab2:
        st.subheader("🧘 常用保健穴位")
        
        acupoints = {
            "足三里": "胃经要穴，调理脾胃，增强免疫力",
            "合谷穴": "止痛要穴，治疗头面五官疾病", 
            "内关穴": "心包经络穴，宁心安神，和胃降逆",
            "关元穴": "培元固本，调理生殖系统",
            "百会穴": "清头醒脑，升阳固脱",
            "涌泉穴": "肾经井穴，滋阴降火，宁神开窍"
        }
        
        for point, desc in acupoints.items():
            st.markdown(f"**{point}**：{desc}")
    
    with tab3:
        st.subheader("🎯 针灸主要适应症")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("""
            ### 疼痛性疾病
            - 头痛、偏头痛
            - 颈椎病、腰椎病
            - 关节炎、肩周炎
            - 各种急慢性疼痛
            """)
            
        with col2:
            st.write("""
            ### 内科疾病  
            - 消化系统疾病
            - 呼吸系统疾病
            - 神经系统疾病
            - 妇科疾病
            """)
    
    with tab4:
        st.video("https://www.youtube.com/watch?v=example")  # 替换为实际教学视频链接

# 艾灸疗法
elif section == "艾灸疗法":
    st.markdown('<div class="section-header">🔥 艾灸疗法</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="therapy-card">
    <h3>🌱 艾灸简介</h3>
    <p>艾灸是利用艾叶制成的艾绒燃烧产生的温热刺激穴位，通过经络的传导达到温通气血、扶正祛邪目的的治疗方法。</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 艾灸方法分类")
        
        moxibustion_methods = {
            "直接灸": "艾炷直接放在皮肤上施灸",
            "间接灸": "艾炷与皮肤之间隔物施灸", 
            "艾条灸": "手持艾条在穴位上方熏烤",
            "温针灸": "针刺后在针柄上插艾条施灸",
            "温灸器灸": "使用专用灸具施灸"
        }
        
        for method, desc in moxibustion_methods.items():
            st.write(f"**{method}**：{desc}")
    
    with col2:
        st.subheader("💪 主要功效")
        st.write("""
        - ✅ 温经散寒
        - ✅ 扶阳固脱  
        - ✅ 消瘀散结
        - ✅ 防病保健
        - ✅ 引热外行
        """)
    
    st.markdown("""
    <div class="warning-box">
    ⚠️ <strong>注意事项：</strong>实热证、阴虚发热者慎用；颜面、五官、大血管处不宜直接灸；孕妇腹部和腰骶部不宜灸。
    </div>
    """, unsafe_allow_html=True)

# 推拿按摩
elif section == "推拿按摩":
    st.markdown('<div class="section-header">💆 推拿按摩</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["基本手法", "常用部位", "自我保健"])
    
    with tab1:
        st.subheader("🖐️ 主要推拿手法")
        
        techniques = {
            "推法": "用指、掌或肘部着力于一定部位进行单方向直线推动",
            "拿法": "用大拇指和食、中两指对称用力提拿筋肉", 
            "按法": "用指、掌或肘在体表特定部位逐渐用力下压",
            "摩法": "用手掌或指腹在体表作环形摩擦移动",
            "揉法": "用手掌大鱼际、掌根或手指罗纹面吸定于一定部位作轻柔缓和的回旋揉动",
            "捏法": "用拇指和其余手指相对用力挤压肌肤"
        }
        
        for tech, desc in techniques.items():
            st.markdown(f"**{tech}**：{desc}")
    
    with tab2:
        st.subheader("🎯 常用按摩部位")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("""
            ### 头面部按摩
            - 太阳穴：缓解头痛
            - 印堂穴：安神醒脑
            - 风池穴：缓解颈项强痛
            """)
            
        with col2:
            st.write("""
            ### 四肢部按摩  
            - 合谷穴：止痛要穴
            - 足三里：保健要穴
            - 涌泉穴：滋阴降火
            """)
    
    with tab3:
        st.subheader("🏠 自我保健按摩")
        st.write("""
        ### 每日自我按摩建议：
        
        1. **晨起按摩**：干梳头100次，按摩面部
        2. **工间休息**：按摩眼周、颈部
        3. **睡前按摩**：按摩腹部、足底
        4. **疲劳时**：按摩太阳穴、风池穴
        """)

# 拔罐疗法
elif section == "拔罐疗法":
    st.markdown('<div class="section-header">🫙 拔罐疗法</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="therapy-card">
        <h3>💨 拔罐原理</h3>
        <p>拔罐是以罐为工具，利用燃火、抽气等方法产生负压，使之吸附于体表，造成局部瘀血，达到通经活络、行气活血、消肿止痛、祛风散寒等作用的疗法。</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("🫙 拔罐种类")
        
        cup_types = {
            "火罐": "传统拔罐，用火焰在罐内燃烧产生负压",
            "气罐": "现代拔罐，用抽气枪产生负压，更安全",
            "玻璃罐": "透明材质，便于观察皮肤变化",
            "竹罐": "传统材质，兼具药效和负压作用"
        }
        
        for cup_type, desc in cup_types.items():
            st.write(f"**{cup_type}**：{desc}")
    
    with col2:
        st.image("https://via.placeholder.com/300x200/2E8B57/FFFFFF?text=拔罐演示", 
                caption="拔罐操作示意图")

# 刮痧疗法
elif section == "刮痧疗法":
    st.markdown('<div class="section-header">🌀 刮痧疗法</div>', unsafe_allow_html=True)
    
    st.write("""
    ### 什么是刮痧？
    
    刮痧是通过特制的刮痧器具和相应的手法，蘸取一定的介质，在体表进行反复刮动、摩擦，
    使皮肤局部出现红色粟粒状，或暗红色出血点等"出痧"变化，从而达到活血透痧的作用。
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 刮痧手法")
        st.write("""
        - **补法**：力度小，速度慢，时间短
        - **泻法**：力度大，速度快，时间长  
        - **平补平泻**：力度速度适中
        """)
        
    with col2:
        st.subheader("🎯 主要功效")
        st.write("""
        - 活血化瘀
        - 调整阴阳
        - 舒筋通络
        - 信息调整
        - 排除毒素
        """)
    
    st.markdown("""
    <div class="warning-box">
    ⚠️ <strong>刮痧禁忌：</strong>有出血倾向的疾病、严重心脑血管疾病、局部皮肤破损或炎症、过度疲劳和饥饿者不宜刮痧。
    </div>
    """, unsafe_allow_html=True)

# 气功导引
elif section == "气功导引":
    st.markdown('<div class="section-header">🧘 气功导引</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["基本概念", "常见功法", "练习要点"])
    
    with tab1:
        st.write("""
        ### 什么是气功？
        
        气功是通过调身、调息、调心相结合，以内外兼修、动静相兼的自我身心锻炼方法。
        通过特定的姿势、呼吸和意念的调节，来培养正气、预防疾病、增进健康。
        """)
        
        st.subheader("三大要素")
        st.write("""
        - **调身**：调整身体姿势，使身体放松自然
        - **调息**：调节呼吸，使之深长细匀  
        - **调心**：调节心神，排除杂念，进入入静状态
        """)
    
    with tab2:
        st.subheader("🏃 常见养生功法")
        
        qigong_forms = {
            "八段锦": "八节动作，柔和缓慢，圆活连贯",
            "五禽戏": "模仿虎、鹿、熊、猿、鸟五种动物动作",
            "太极拳": "以柔克刚，以静制动，阴阳相济",
            "六字诀": "通过嘘、呵、呼、呬、吹、嘻六字调理脏腑",
            "易筋经": "强筋健骨，改善身体柔韧性和力量"
        }
        
        for form, desc in qigong_forms.items():
            st.markdown(f"**{form}**：{desc}")
    
    with tab3:
        st.subheader("📋 练习要点")
        st.write("""
        ### 练习注意事项
        
        1. **循序渐进**：从简单开始，逐渐增加难度
        2. **持之以恒**：坚持每日练习，效果更佳
        3. **环境适宜**：选择空气清新、环境安静的地方
        4. **衣着宽松**：穿宽松舒适的衣物，便于活动
        5. **避免过饱过饥**：饭后1小时内不宜练习
        """)

# 药膳食疗
elif section == "药膳食疗":
    st.markdown('<div class="section-header">🍲 药膳食疗</div>', unsafe_allow_html=True)
    
    st.write("""
    ### 什么是药膳？
    
    药膳是在中医学、烹饪学和营养学理论指导下，严格按药膳配方，将中药与某些具有药用价值的食物相配伍，
    采用我国独特的饮食烹调技术和现代科学方法制作而成的具有一定色、香、味、形的美味食品。
    """)
    
    # 体质与食疗建议
    st.subheader("🧬 不同体质的食疗建议")
    
    constitution_data = {
        "体质类型": ["气虚质", "阳虚质", "阴虚质", "痰湿质", "湿热质", "血瘀质"],
        "主要表现": ["气短乏力、易出汗", "畏寒怕冷、四肢不温", "口干咽燥、手足心热", "形体肥胖、胸闷痰多", "面垢油光、口苦苔黄", "面色晦暗、肌肤甲错"],
        "推荐食材": ["山药、大枣、鸡肉", "羊肉、韭菜、核桃", "银耳、百合、鸭肉", "薏米、赤小豆、冬瓜", "绿豆、苦瓜、黄瓜", "山楂、黑木耳、玫瑰花"],
        "禁忌食材": ["萝卜、空心菜", "冷饮、西瓜", "辛辣、温燥食物", "油腻、甜腻食物", "辛辣、油腻食物", "寒凉、收涩食物"]
    }
    
    df = pd.DataFrame(constitution_data)
    st.dataframe(df, use_container_width=True)
    
    # 季节食疗
    st.subheader("🍂 四季食疗养生")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write("**春季**")
        st.write("养肝为主，宜食辛甘发散之品：韭菜、香椿、春笋")
    
    with col2:
        st.write("**夏季**") 
        st.write("养心为主，宜食清热解暑之品：西瓜、绿豆、荷叶")
    
    with col3:
        st.write("**秋季**")
        st.write("养肺为主，宜食滋阴润燥之品：梨、银耳、蜂蜜")
    
    with col4:
        st.write("**冬季**")
        st.write("养肾为主，宜食温补之品：羊肉、核桃、桂圆")

# 注意事项
elif section == "注意事项":
    st.markdown('<div class="section-header">⚠️ 注意事项</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="warning-box">
    <h3>🔴 重要提醒</h3>
    <p>以下内容仅为中医养生科普知识，不能替代专业医疗建议。如有疾病，请及时就医。</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚫 通用禁忌症")
        st.write("""
        - 严重心脑血管疾病
        - 出血性疾病
        - 恶性肿瘤
        - 急性传染病
        - 精神疾病发作期
        - 极度虚弱或疲劳状态
        - 过饥过饱、醉酒状态
        """)
    
    with col2:
        st.subheader("👩‍⚕️ 专业建议")
        st.write("""
        - 选择正规医疗机构
        - 由专业医师操作
        - 治疗前详细告知病史
        - 治疗后注意观察反应
        - 出现不适及时就医
        - 配合医生建议的治疗方案
        """)
    
    st.subheader("📞 紧急情况处理")
    st.write("""
    如果在非药物治疗过程中出现以下情况，请立即停止并就医：
    
    - 剧烈疼痛无法忍受
    - 出血不止
    - 意识模糊或晕厥
    - 严重过敏反应
    - 其他异常严重反应
    """)

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
<p>🌿 中医养生智慧 · 传承千年文化 · 服务现代健康 🌿</p>
<p><small>本页面内容仅供参考，具体治疗请在专业医师指导下进行</small></p>
</div>
""", unsafe_allow_html=True)
