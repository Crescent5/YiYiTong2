import streamlit as st
import random
import pandas as pd
import time
from datetime import datetime
import requests
import json

# 设置页面
st.set_page_config(
    page_title="食疗养生方案推荐系统",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 食疗方案数据库
@st.cache_data
def load_recipes():
    recipes = [
        {
            "name": "红枣枸杞银耳羹",
            "image": "https://img.cdn1.vip/i/69a5836de0c2f_1772454765.webp",
            "description": "滋补养颜的经典甜品",
            "ingredients": "银耳30g，红枣10颗，枸杞15g，冰糖适量，清水1000ml",
            "method": "1. 银耳提前泡发，撕成小朵；\n2. 红枣、枸杞洗净；\n3. 将所有材料放入锅中，加水大火煮沸；\n4. 转小火慢炖1小时至银耳软糯；\n5. 加入冰糖搅拌至溶解即可。",
            "benefits": "滋阴润肺，养颜美容，补气血，安神助眠",
            "suitable_for": "气血不足、皮肤干燥、失眠多梦者",
            "season": "秋冬季节",
            "keywords": ["补血", "养颜", "失眠", "润肺"]
        },
        {
            "name": "山药薏米粥",
            "image": "https://img.cdn1.vip/i/69a583df45874_1772454879.webp",
            "description": "健脾祛湿的养生粥品",
            "ingredients": "山药200g，薏米50g，糯米50g，红枣5颗，水适量",
            "method": "1. 薏米提前浸泡2小时；\n2. 山药去皮切块；\n3. 将所有材料放入锅中，加水大火煮沸；\n4. 转小火煮40分钟至粥稠即可。",
            "benefits": "健脾益胃，祛湿利水，增强免疫力",
            "suitable_for": "脾胃虚弱、水肿、湿气重者",
            "season": "春夏季节",
            "keywords": ["健脾", "祛湿", "水肿", "免疫力"]
        },
        {
            "name": "菊花枸杞茶",
            "image": "https://img.cdn1.vip/i/69a5847f31d7c_1772455039.webp",
            "description": "清肝明目的养生茶饮",
            "ingredients": "干菊花10g，枸杞15g，冰糖适量，热水500ml",
            "method": "1. 将菊花和枸杞放入茶壶；\n2. 加入热水，盖上盖子焖5分钟；\n3. 加入冰糖调味即可饮用。",
            "benefits": "清肝明目，清热解毒，降血压",
            "suitable_for": "眼睛疲劳、高血压、肝火旺盛者",
            "season": "夏季",
            "keywords": ["明目", "降压", "清热", "肝火"]
        },
        {
            "name": "姜枣红糖水",
            "image": "https://img.cdn1.vip/i/69a584ecb2ddf_1772455148.webp",
            "description": "温中散寒的暖身饮品",
            "ingredients": "生姜30g，红枣10颗，红糖适量，水800ml",
            "method": "1. 生姜切片，红枣去核；\n2. 将材料放入锅中加水煮沸；\n3. 转小火煮15分钟；\n4. 加入红糖搅拌至溶解即可。",
            "benefits": "温中散寒，补血活血，缓解痛经",
            "suitable_for": "体寒、经期不适、风寒感冒初期者",
            "season": "冬季",
            "keywords": ["驱寒", "痛经", "补血", "感冒"]
        },
        {
            "name": "黑芝麻糊",
            "image": "https://img.cdn1.vip/i/69a584ec1a7e7_1772455148.webp",
            "description": "滋补肝肾的养生糊品",
            "ingredients": "黑芝麻100g，糯米粉50g，冰糖适量，水500ml",
            "method": "1. 黑芝麻炒香磨粉；\n2. 糯米粉用小火炒至微黄；\n3. 将黑芝麻粉和糯米粉混合，加水调匀；\n4. 小火加热搅拌至糊状，加冰糖调味。",
            "benefits": "滋补肝肾，乌发养颜，润肠通便",
            "suitable_for": "白发脱发、便秘、肝肾不足者",
            "season": "四季皆宜",
            "keywords": ["乌发", "补肾", "便秘", "养颜"]
        },
        {
            "name": "绿豆薏仁汤",
            "image": "https://img.cdn1.vip/i/69a585ec88a4f_1772455404.webp",
            "description": "清热解毒的夏季饮品",
            "ingredients": "绿豆100g，薏仁50g，冰糖适量，水1500ml",
            "method": "1. 绿豆和薏仁提前浸泡2小时；\n2. 将材料放入锅中加水大火煮沸；\n3. 转小火煮40分钟至豆烂；\n4. 加入冰糖搅拌至溶解即可。",
            "benefits": "清热解毒，利水消肿，降火",
            "suitable_for": "暑热烦渴、水肿、痤疮者",
            "season": "夏季",
            "keywords": ["清热", "解毒", "消肿", "降火"]
        },
        {
            "name": "百合莲子汤",
            "image": "https://img.cdn1.vip/i/69a5862d58e1f_1772455469.webp",
            "description": "清心安神的养生甜汤",
            "ingredients": "干百合30g，莲子50g，冰糖适量，水1000ml",
            "method": "1. 莲子和百合提前浸泡2小时；\n2. 将材料放入锅中加水大火煮沸；\n3. 转小火煮40分钟至软烂；\n4. 加入冰糖搅拌至溶解即可。",
            "benefits": "清心安神，润肺止咳，健脾补肾",
            "suitable_for": "失眠多梦、咳嗽、心神不宁者",
            "season": "秋季",
            "keywords": ["安神", "止咳", "失眠", "润肺"]
        },
        {
            "name": "当归黄芪鸡汤",
            "image": "https://img.cdn1.vip/i/69a587118252c_1772455697.webp",
            "description": "补气养血的滋补汤品",
            "ingredients": "鸡肉500g，当归10g，黄芪15g，枸杞10g，红枣5颗，姜片适量",
            "method": "1. 鸡肉焯水备用；\n2. 将所有材料放入锅中，加水大火煮沸；\n3. 转小火炖煮1.5小时；\n4. 加盐调味即可。",
            "benefits": "补气养血，增强免疫力，调理月经",
            "suitable_for": "气血不足、体虚乏力、月经不调者",
            "season": "秋冬季节",
            "keywords": ["补气", "养血", "免疫力", "调经"]
        },
        {
            "name": "山楂决明子茶",
            "image": "https://img.cdn1.vip/i/69a5873482677_1772455732.webp",
            "description": "降脂消食的养生茶饮",
            "ingredients": "山楂干15g，决明子10g，菊花5g，水500ml",
            "method": "1. 将所有材料放入茶壶；\n2. 加入热水，盖上盖子焖10分钟；\n3. 过滤后即可饮用。",
            "benefits": "降脂消食，清肝明目，润肠通便",
            "suitable_for": "高血脂、消化不良、便秘者",
            "season": "四季皆宜",
            "keywords": ["降脂", "消食", "明目", "通便"]
        },
        {
            "name": "银耳雪梨羹",
            "image": "https://img.cdn1.vip/i/69a587a0267d5_1772455840.webp",
            "description": "润肺止咳的秋季甜品",
            "ingredients": "银耳20g，雪梨1个，冰糖适量，枸杞10g，水1000ml",
            "method": "1. 银耳泡发撕小朵，雪梨去皮切块；\n2. 将所有材料放入锅中加水大火煮沸；\n3. 转小火煮40分钟；\n4. 加入冰糖和枸杞再煮5分钟即可。",
            "benefits": "润肺止咳，清热化痰，生津止渴",
            "suitable_for": "咳嗽痰多、咽喉干燥、肺热者",
            "season": "秋季",
            "keywords": ["润肺", "止咳", "化痰", "清热"]
        },
        {
            "name": "冬瓜排骨汤",
            "image": "https://img.cdn1.vip/i/69a587c13e95e_1772455873.webp",
            "description": "清热利湿的滋补汤品",
            "ingredients": "排骨500g，冬瓜300g，姜片适量，盐适量",
            "method": "1. 排骨焯水备用；\n2. 冬瓜去皮切块；\n3. 将排骨和姜片放入锅中，加水大火煮沸；\n4. 转小火炖煮1小时；\n5. 加入冬瓜再煮20分钟，加盐调味即可。",
            "benefits": "清热利湿，消肿解毒，补充蛋白质",
            "suitable_for": "湿热体质、水肿、夏季暑热者",
            "season": "夏季",
            "keywords": ["清热", "利湿", "消肿", "解毒"]
        },
        {
            "name": "桂圆红枣茶",
            "image": "https://img.cdn1.vip/i/69a587e181942_1772455905.webp",
            "description": "补血安神的养生茶饮",
            "ingredients": "桂圆肉20g，红枣10颗，红糖适量, 水800ml",
            "method": "1. 红枣去核；\n2. 将桂圆和红枣放入锅中加水煮沸；\n3. 转小火煮15分钟；\n4. 加入红糖搅拌至溶解即可。",
            "benefits": "补血安神，健脾养心，改善气色",
            "suitable_for": "贫血、失眠、心悸、面色萎黄者",
            "season": "秋冬季节",
            "keywords": ["补血", "安神", "健脾", "养心"]
        },
        {
            "name": "双耳汤",
            "image": "https://img.cdn1.vip/i/69a588e3843e9_1772456163.webp",
            "description": "滋阴润肺的养生汤品",
            "ingredients": "银耳15g，黑木耳15g，冰糖适量，水1000ml",
            "method": "1. 银耳和黑木耳提前泡发；\n2. 将材料放入锅中加水大火煮沸；\n3. 转小火煮40分钟；\n4. 加入冰糖搅拌至溶解即可。",
            "benefits": "滋阴润肺，补肾健脑，降血脂",
            "suitable_for": "肺燥咳嗽、血管硬化、高血脂者",
            "season": "秋季",
            "keywords": ["滋阴", "润肺", "降脂", "补肾"]
        },
        {
            "name": "茯苓粥",
            "image": "https://img.cdn1.vip/i/69a58904447d7_1772456196.webp",
            "description": "健脾宁神的养生粥品",
            "ingredients": "茯苓粉30g，大米100g，红枣5颗，水适量",
            "method": "1. 大米洗净，红枣去核；\n2. 将所有材料放入锅中加水大火煮沸；\n3. 转小火煮30分钟至粥稠即可。",
            "benefits": "健脾渗湿，宁心安神，利水消肿",
            "suitable_for": "脾虚湿盛、失眠多梦、水肿者",
            "season": "四季皆宜",
            "keywords": ["健脾", "安神", "利水", "消肿"]
        },
        {
            "name": "玫瑰花茶",
            "image": "https://img.cdn1.vip/i/69a5898709771_1772456327.webp",
            "description": "理气解郁的养生花茶",
            "ingredients": "干玫瑰花10g，蜂蜜适量，热水500ml",
            "method": "1. 将玫瑰花放入茶壶；\n2. 加入热水，盖上盖子焖5分钟；\n3. 加入蜂蜜调味即可饮用。",
            "benefits": "理气解郁，活血散瘀，美容养颜",
            "suitable_for": "情绪不畅、肝胃气痛、面色暗沉者",
            "season": "春季",
            "keywords": ["理气", "解郁", "活血", "美容"]
        },
        {
            "name": "四神汤",
            "image": "https://img.cdn1.vip/i/69a589a63c729_1772456358.webp",
            "description": "健脾祛湿的经典汤品",
            "ingredients": "茯苓20g，芡实20g，莲子20g，山药20g，猪肚或瘦肉适量",
            "method": "1. 肉类焯水备用；\n2. 将所有材料放入锅中，加水大火煮沸；\n3. 转小火炖煮1.5小时；\n4. 加盐调味即可。",
            "benefits": "健脾祛湿，补肾固精，增强免疫力",
            "suitable_for": "脾虚湿盛、消化不良、免疫力低下者",
            "season": "长夏季节",
            "keywords": ["健脾", "祛湿", "补肾", "免疫"]
        }
]
    return recipes

# Kimi API调用函数
def call_kimi_api(prompt):
    """
    调用Kimi AI API获取回复
    需要填写API密钥和端点URL
    """
    # 这里需要填写你的Kimi API密钥和端点
    api_key = "sk-CXx3Cs76mQCYLhq8nrTdGb1qGijoQPXAjS8khPm29k8GU5Yt"  # 请替换为实际的API密钥
    api_url = "https://api.moonshot.cn/v1/chat/completions"  # 请确认API端点是否正确
    
    if api_key == "你的Kimi_API密钥":
        return "请先在侧边栏设置Kimi API密钥"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 构建系统提示词，确保回复专业且与食疗相关
    system_prompt = """你是一个中医食疗专家，精通各种食物的药用价值和养生功效。
    请根据用户的症状或需求，推荐合适的食疗方案，包括食谱、制作方法、功效和适用人群。
    回答要专业、详细且实用，避免笼统的建议。"""
    
    payload = {
        "model": "moonshot-v1-8k",  # 根据实际情况调整模型名称
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.Timeout:
        return "请求超时，请稍后再试"
    except Exception as e:
        return f"抱歉，暂时无法获取AI回复。错误信息: {str(e)}"

# 初始化会话状态
if "recipes" not in st.session_state:
    st.session_state.recipes = load_recipes()
if "displayed_recipes" not in st.session_state:
    st.session_state.displayed_recipes = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "season_filter" not in st.session_state:
    st.session_state.season_filter = "不限"
if "health_goal_filter" not in st.session_state:
    st.session_state.health_goal_filter = []

# 随机选择食谱
def get_random_recipes():
    num_recipes = random.randint(10, min(20, len(st.session_state.recipes)))
    return random.sample(st.session_state.recipes, num_recipes)

# 刷新功能
def refresh_recipes():
    st.session_state.displayed_recipes = get_random_recipes()
    st.session_state.chat_history.append({
        "role": "system", 
        "content": f"已刷新食谱推荐，为您推荐{len(st.session_state.displayed_recipes)}种养生食疗方案",
        "time": datetime.now().strftime("%H:%M:%S")
    })
    st.rerun()  # 强制重新运行应用

# 智能回复函数
def get_ai_response(user_input):
    # 调用Kimi API获取回复
    return call_kimi_api(user_input)

# 发送消息函数
def send_message():
    if st.session_state.user_input.strip():
        # 添加用户消息到聊天历史
        # st.session_state.chat_history.append({
        #     "role": "user", 
        #     "content": st.session_state.user_input,
        #     "time": datetime.now().strftime("%H:%M:%S")
        # })
        
        # 获取AI回复
        ai_response = get_ai_response(st.session_state.user_input)
        
        # 添加AI回复到聊天历史
        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": ai_response,
            "time": datetime.now().strftime("%H:%M:%S")
        })
        
        # 清空输入框
        st.session_state.user_input = ""
        st.rerun()  # 强制重新运行应用以更新聊天界面

# 更新筛选条件
def update_filters():
    st.session_state.season_filter = st.session_state.season_select
    st.session_state.health_goal_filter = st.session_state.health_goal_select

# 页面布局
st.title("🥗 食疗养生方案推荐系统")
st.markdown("为您提供个性化的传统中医食疗方案，促进健康与平衡")

# 侧边栏
with st.sidebar:
    st.header("个性化设置")
    
    # 使用session_state来保持筛选状态
    season = st.selectbox(
        "选择当前季节", 
        ["春", "夏", "秋", "冬", "不限"],
        index=["春", "夏", "秋", "冬", "不限"].index(st.session_state.season_filter),
        key="season_select",
        on_change=update_filters
    )
    
    health_goal = st.multiselect(
        "选择健康目标",
        ["补气养血", "清热降火", "安神助眠", "美容养颜", "健脾祛湿", "润肺止咳"],
        default=st.session_state.health_goal_filter,
        key="health_goal_select",
        on_change=update_filters
    )
    
    st.divider()
    st.header("聊天功能")
    st.markdown("描述您的症状或健康需求，获取个性化建议")
    

# 主内容区
tab1, tab2 = st.tabs(["食疗方案推荐", "智能咨询"])

with tab1:
    if not st.session_state.displayed_recipes:
        refresh_recipes()
    
    st.subheader("今日推荐养生食疗方案")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        st.button("刷新推荐", on_click=refresh_recipes, type="primary")
    with col2:
        st.write(f"当前显示 {len(st.session_state.displayed_recipes)} 个食谱")
    
    # 根据筛选条件过滤食谱
    filtered_recipes = st.session_state.displayed_recipes
    if st.session_state.season_filter != "不限":
        filtered_recipes = [r for r in filtered_recipes if st.session_state.season_filter in r["season"]]
    if st.session_state.health_goal_filter:
        filtered_recipes = [r for r in filtered_recipes if any(g in r["benefits"] for g in st.session_state.health_goal_filter)]
    
    st.write(f"筛选后显示 {len(filtered_recipes)} 个食谱")
    
    # 显示筛选后的食谱
    for i, recipe in enumerate(filtered_recipes):
        # 使用容器而不是expander来避免嵌套问题
        with st.container():
            st.markdown("---")
            col1, col2 = st.columns([1, 2])
            
             with col1:
                # 使用占位图，避免图片加载问题
                st.image(recipe['image'], caption=recipe['name'], use_column_width=True)
            
            with col2:
                st.subheader(f"{i+1}. {recipe['name']}")
                st.caption(recipe['description'])
                
                with st.expander("查看食谱详情", expanded=False):
                    st.markdown(f"**主要食材:** {recipe['ingredients']}")
                    st.markdown(f"**食疗作用:** {recipe['benefits']}")
                    st.markdown(f"**适用人群:** {recipe['suitable_for']}")
                    st.markdown(f"**推荐季节:** {recipe['season']}")
                    
                    # 使用st.text_area显示制作方法
                    st.markdown("**详细制作方法:**")
                    st.text_area(
                        label="",
                        value=recipe['method'],
                        height=150,
                        key=f"method_{i}",
                        disabled=True
                    )

with tab2:
    st.subheader("智能食疗咨询")
    st.markdown("请描述您的症状或健康需求，我会为您推荐合适的食疗方案")
    
    # 显示聊天记录
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(message["content"])
                    st.caption(f"您 - {message['time']}")
            elif message["role"] == "assistant":
                with st.chat_message("assistant"):
                    st.markdown(message["content"])
                    st.caption(f"食疗助手 - {message['time']}")
            else:  # system message
                st.info(f"{message['content']} - {message['time']}")
    
    # 输入区域
    st.text_input("请输入您的症状或健康需求：", 
                 key="user_input", 
                 on_change=send_message,
                 placeholder="例如：最近经常失眠，有什么食疗建议吗？")
    
    st.button("发送", on_click=send_message)

# 页脚
st.divider()
st.markdown("""
<div style='text-align: center'>
    <p>温馨提示：本系统提供的食疗方案仅供参考，不能替代专业医疗建议。如有严重健康问题，请咨询专业医师。</p>
</div>
""", unsafe_allow_html=True)
