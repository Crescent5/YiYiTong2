import streamlit as st
import random
import pandas as pd
from datetime import datetime
import requests
import json

# 设置页面
st.set_page_config(
    page_title="中医专业知识科普系统",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 中医知识数据库
@st.cache_data
def load_tcm_knowledge():
    categories = {
        "中医基础理论": [
            {
                "id": "theory_1",
                "title": "阴阳学说",
                "content": """
阴阳学说是中医理论的核心之一，它认为宇宙间的一切事物都包含着阴阳相互对立的两个方面。

**基本概念：**
- 阴阳是对自然界相互关联的某些事物和现象对立双方的概括
- 阴阳之间存在着对立制约、互根互用、消长平衡和相互转化的关系

**临床应用：**
- 诊断疾病：分析疾病的阴阳属性
- 指导治疗：确定治疗原则，如"寒者热之，热者寒之"
- 药物分类：区分药物的阴阳属性
                """,
                "image": "https://img.zcool.cn/community/01yinYang.jpg",
                "video": "https://example.com/videos/yinyang.mp4",
                "audio": "https://example.com/audio/yinyang.mp3",
                "source": "《黄帝内经·素问》",
                "tags": ["阴阳", "理论基础", "哲学"]
            },
            {
                "id": "theory_2",
                "title": "五行学说",
                "content": """
五行学说将自然界的事物分为木、火、土、金、水五类，并以相生相克的关系说明事物间的联系。

**五行特性：**
- 木：生长、升发、条达、舒畅
- 火：温热、升腾、明亮
- 土：生化、承载、受纳
- 金：清洁、肃降、收敛
- 水：寒凉、滋润、向下运行

**相生相克关系：**
- 相生：木→火→土→金→水→木
- 相克：木→土→水→火→金→木

**临床应用：**
- 解释生理病理现象
- 指导诊断和治疗
- 药物归经理论的基础
                """,
                "image": "https://img.zcool.cn/community/01wuXing.jpg",
                "video": "https://example.com/videos/wuxing.mp4",
                "audio": "https://example.com/audio/wuxing.mp3",
                "source": "《黄帝内经·素问》",
                "tags": ["五行", "相生相克", "理论基础"]
            },
            # 更多内容...
        ],
        "中医诊断学": [
            {
                "id": "diagnosis_1",
                "title": "四诊法",
                "content": """
四诊是中医诊断疾病的基本方法，包括望、闻、问、切四种诊法。

**望诊：**
- 望神：观察患者的精神状态
- 望色：观察面部和肌肤颜色
- 望舌：观察舌质、舌苔的变化
- 望形态：观察形体姿态

**闻诊：**
- 听声音：语言、呼吸、咳嗽等声音
- 嗅气味：口气、体气、排泄物气味

**问诊：**
- 问寒热：有无发热、恶寒
- 问汗：有无汗出，汗出的特点
- 问头身：头痛、身痛等情况
- 问二便：大小便情况
- 问饮食：食欲、口味等
- 问胸腹：胸腹部不适
- 问睡眠：失眠、多梦等
- 问经带：妇女月经、白带情况

**切诊：**
- 脉诊：通过触摸脉搏诊断疾病
- 按诊：触摸按压身体部位诊断疾病

**临床应用：**
四诊合参，全面收集病情资料，为辨证论治提供依据。
                """,
                "image": "https://img.zcool.cn/community/01siZhen.jpg",
                "video": "https://example.com/videos/sizhen.mp4",
                "audio": "https://example.com/audio/sizhen.mp3",
                "source": "《难经》",
                "tags": ["四诊", "望闻问切", "诊断方法"]
            },
            # 更多内容...
        ],
        # 其他分类...
    }
    return categories

# Kimi API调用函数
def call_kimi_api(prompt):
    """
    调用Kimi AI API获取回复
    """
    api_key = "sk-CXx3Cs76mQCYLhq8nrTdGb1qGijoQPXAjS8khPm29k8GU5Yt"
    api_url = "https://api.moonshot.cn/v1/chat/completions"
    
    if api_key == "你的Kimi_API密钥":
        return "请先在侧边栏设置Kimi API密钥"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 构建系统提示词
    system_prompt = """你是一个中医专家，精通中医理论和临床实践。
    请根据用户的问题，提供专业、准确的中医知识解答。
    回答要详细、实用，并适当引用中医经典著作。
    请确保回答内容格式清晰，使用适当的换行和分段。"""
    
    payload = {
        "model": "moonshot-v1-8k",
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
if "tcm_knowledge" not in st.session_state:
    st.session_state.tcm_knowledge = load_tcm_knowledge()
if "current_category" not in st.session_state:
    st.session_state.current_category = "中医基础理论"
if "displayed_items" not in st.session_state:
    st.session_state.displayed_items = []
if "show_all" not in st.session_state:
    st.session_state.show_all = False
if "favorites" not in st.session_state:
    st.session_state.favorites = {}
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "知识浏览"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# 获取所有知识项
def get_all_items():
    all_items = []
    for category, items in st.session_state.tcm_knowledge.items():
        for item in items:
            item_with_category = item.copy()
            item_with_category["category"] = category
            all_items.append(item_with_category)
    return all_items

# 搜索功能
def search_items(query):
    if not query:
        return []
    
    results = []
    all_items = get_all_items()
    
    for item in all_items:
        # 搜索标题、内容、标签和分类
        search_text = f"{item['title']} {item['content']} {' '.join(item['tags'])} {item['category']}"
        if query.lower() in search_text.lower():
            results.append(item)
    
    return results

# 获取随机知识项目
def get_random_items(category, count=3):
    items = st.session_state.tcm_knowledge[category]
    if count >= len(items) or st.session_state.show_all:
        return items
    return random.sample(items, min(count, len(items)))

# 刷新功能
def refresh_items():
    st.session_state.displayed_items = get_random_items(st.session_state.current_category)
    st.session_state.show_all = False

# 显示全部功能
def show_all_items():
    st.session_state.displayed_items = get_random_items(st.session_state.current_category, 10)
    st.session_state.show_all = True

# 收藏功能
def toggle_favorite(item_id, category):
    if item_id in st.session_state.favorites:
        del st.session_state.favorites[item_id]
    else:
        # 找到对应的项目
        for item in st.session_state.tcm_knowledge[category]:
            if item["id"] == item_id:
                st.session_state.favorites[item_id] = {
                    "title": item["title"],
                    "category": category,
                    "content": item["content"][:100] + "..." if len(item["content"]) > 100 else item["content"]
                }
                break

# 发送消息函数
def send_message():
    if st.session_state.user_input.strip():
        # 添加用户消息到聊天历史
        st.session_state.chat_history.append({
            "role": "user", 
            "content": st.session_state.user_input,
            "time": datetime.now().strftime("%H:%M:%S")
        })
        
        # 获取AI回复
        ai_response = call_kimi_api(st.session_state.user_input)
        
        # 添加AI回复到聊天历史
        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": ai_response,
            "time": datetime.now().strftime("%H:%M:%S")
        })
        
        # 清空输入框
        st.session_state.user_input = ""

# 页面布局
st.title("🌿 中医专业知识科普系统")
st.markdown("探索中医博大精深的理论知识体系，了解常见疾病的预防与治疗方法")

# 侧边栏导航
with st.sidebar:
    st.header("导航菜单")
    
    # 页面选择
    page_options = ["知识浏览", "我的收藏", "AI问答", "多媒体资源"]
    current_page = st.radio("选择页面", page_options, index=page_options.index(st.session_state.current_page))
    
    if current_page != st.session_state.current_page:
        st.session_state.current_page = current_page
        st.rerun()
    
    st.divider()
    
    # 搜索功能
    if st.session_state.current_page == "知识浏览":
        st.header("搜索功能")
        search_query = st.text_input("搜索中医知识", value=st.session_state.search_query, placeholder="输入关键词搜索...")
        
        if search_query != st.session_state.search_query:
            st.session_state.search_query = search_query
            st.session_state.search_results = search_items(search_query)
            st.rerun()
        
        if st.session_state.search_query:
            st.write(f"找到 {len(st.session_state.search_results)} 个相关结果")
            
            if st.button("清除搜索"):
                st.session_state.search_query = ""
                st.session_state.search_results = []
                st.rerun()
        
        st.divider()
        
        # 分类选择
        st.header("知识分类")
        categories = list(st.session_state.tcm_knowledge.keys())
        selected_category = st.selectbox(
            "选择知识分类",
            categories,
            index=categories.index(st.session_state.current_category),
            key="category_select"
        )
        
        # 更新当前分类
        if selected_category != st.session_state.current_category:
            st.session_state.current_category = selected_category
            st.session_state.displayed_items = get_random_items(selected_category)
            st.session_state.show_all = False
            st.rerun()
        
        st.divider()
        st.header("显示选项")
        
        # 显示数量选择
        if not st.session_state.show_all:
            display_count = st.slider(
                "显示知识点数量",
                min_value=1,
                max_value=len(st.session_state.tcm_knowledge[st.session_state.current_category]),
                value=min(3, len(st.session_state.tcm_knowledge[st.session_state.current_category])),
                key="display_count"
            )
        
        # 操作按钮
        col1, col2 = st.columns(2)
        with col1:
            st.button("刷新内容", on_click=refresh_items, use_container_width=True)
        with col2:
            st.button("显示全部", on_click=show_all_items, use_container_width=True)
    

# 主内容区
if st.session_state.current_page == "知识浏览":
    # 显示搜索结果或分类内容
    if st.session_state.search_query and st.session_state.search_results:
        st.header(f"搜索结果: '{st.session_state.search_query}'")
        
        for i, item in enumerate(st.session_state.search_results):
            with st.container():
                st.markdown("---")
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    try:
                        st.image(item['image'], caption=item['title'], use_column_width=True)
                    except:
                        st.image("https://via.placeholder.com/300x200/4CAF50/white?text=中医知识", 
                                caption=item['title'], use_column_width=True)
                
                with col2:
                    st.subheader(f"{i+1}. {item['title']}")
                    st.caption(f"分类: {item['category']}")
                    st.markdown(item['content'])
                    st.caption(f"来源: {item['source']}")
                    
                    # 收藏按钮
                    is_favorite = item['id'] in st.session_state.favorites
                    if st.button("❤️ 收藏" if not is_favorite else "💖 已收藏", 
                                key=f"fav_{item['id']}_{i}",
                                on_click=toggle_favorite, 
                                args=(item['id'], item['category'])):
                        st.rerun()
                    
                    # 标签显示
                    if 'tags' in item and item['tags']:
                        st.write("**标签:**")
                        for tag in item['tags']:
                            st.markdown(f"`{tag}`", unsafe_allow_html=True)
    else:
        # 显示分类内容
        if not st.session_state.displayed_items:
            st.session_state.displayed_items = get_random_items(st.session_state.current_category)
        
        st.header(f"{st.session_state.current_category}")
        
        # 显示知识项目
        for i, item in enumerate(st.session_state.displayed_items):
            with st.container():
                st.markdown("---")
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    try:
                        st.image(item['image'], caption=item['title'], use_column_width=True)
                    except:
                        st.image("https://via.placeholder.com/300x200/4CAF50/white?text=中医知识", 
                                caption=item['title'], use_column_width=True)
                
                with col2:
                    st.subheader(f"{i+1}. {item['title']}")
                    st.markdown(item['content'])
                    st.caption(f"来源: {item['source']}")
                    
                    # 收藏按钮
                    is_favorite = item['id'] in st.session_state.favorites
                    if st.button("❤️ 收藏" if not is_favorite else "💖 已收藏", 
                                key=f"fav_{item['id']}_{i}",
                                on_click=toggle_favorite, 
                                args=(item['id'], st.session_state.current_category)):
                        st.rerun()
                    
                    # 标签显示
                    if 'tags' in item and item['tags']:
                        st.write("**标签:**")
                        for tag in item['tags']:
                            st.markdown(f"`{tag}`", unsafe_allow_html=True)
                    
                    # 多媒体内容
                    if 'video' in item or 'audio' in item:
                        st.write("**多媒体资源:**")
                        if 'video' in item:
                            st.video(item['video'])
                        if 'audio' in item:
                            st.audio(item['audio'])

elif st.session_state.current_page == "我的收藏":
    st.header("我的收藏")
    
    if not st.session_state.favorites:
        st.info("您还没有收藏任何内容。在知识浏览页面可以收藏您感兴趣的内容。")
    else:
        for item_id, item in st.session_state.favorites.items():
            with st.container():
                st.markdown("---")
                st.subheader(item['title'])
                st.caption(f"分类: {item['category']}")
                st.markdown(item['content'])
                
                # 取消收藏按钮
                if st.button("❌ 取消收藏", key=f"unfav_{item_id}"):
                    toggle_favorite(item_id, item['category'])
                    st.rerun()

elif st.session_state.current_page == "AI问答":
    st.header("中医AI问答")
    st.markdown("向AI中医专家提问，获取专业解答")
    
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
                    # 使用st.markdown并设置unsafe_allow_html=True以保留换行
                    st.markdown(message["content"].replace('\n', '<br>'), unsafe_allow_html=True)
                    st.caption(f"中医助手 - {message['time']}")
    
    # 输入区域
    st.text_input("请输入您的问题：", 
                 key="user_input", 
                 on_change=send_message,
                 placeholder="例如：什么是阴阳学说？如何调理气虚？")
    
    st.button("发送", on_click=send_message)
    
    # 示例问题
    st.divider()
    st.subheader("示例问题")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("什么是中医的五行学说？"):
            st.session_state.user_input = "什么是中医的五行学说？"
            send_message()
    
    with col2:
        if st.button("如何通过舌诊判断健康状况？"):
            st.session_state.user_input = "如何通过舌诊判断健康状况？"
            send_message()

elif st.session_state.current_page == "多媒体资源":
    st.header("中医多媒体资源")
    st.markdown("观看中医相关的视频和收听音频内容")
    
    # 获取所有有多媒体内容的知识项
    multimedia_items = []
    for category, items in st.session_state.tcm_knowledge.items():
        for item in items:
            if 'video' in item or 'audio' in item:
                item_with_category = item.copy()
                item_with_category["category"] = category
                multimedia_items.append(item_with_category)
    
    if not multimedia_items:
        st.info("暂无多媒体资源。")
    else:
        for item in multimedia_items:
            with st.container():
                st.markdown("---")
                st.subheader(item['title'])
                st.caption(f"分类: {item['category']}")
                
                # 显示多媒体内容
                if 'video' in item:
                    st.video(item['video'])
                if 'audio' in item:
                    st.audio(item['audio'])
                
                st.markdown(item['content'])
                st.caption(f"来源: {item['source']}")

# 页脚
st.divider()
st.markdown("""
<div style='text-align: center'>
    <p>温馨提示：本系统提供的中医知识仅供参考，不能替代专业医疗建议。如有健康问题，请咨询专业医师。</p>
    <p>中医博大精深，需要系统学习和长期实践才能掌握其精髓。</p>
</div>
""", unsafe_allow_html=True)
