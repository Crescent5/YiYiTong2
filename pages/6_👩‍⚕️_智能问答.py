import json
import streamlit as st
from openai import OpenAI
from typing import Iterator, List, Dict
import random
import datetime

# 配置信息
model_name = "医易通智能问答"
model_version = "专业增强版"

client = OpenAI(api_key="sk-CXx3Cs76mQCYLhq8nrTdGb1qGijoQPXAjS8khPm29k8GU5Yt", 
               base_url="https://api.moonshot.cn/v1")
st.set_page_config(page_title=model_name, page_icon="🌿", layout="wide")
st.title(f"{model_name} {model_version}")

# 中医术语数据库扩展
TCM_TERMS_DATABASE = {
    "阴虚火旺": {
        "category": "阴阳失衡",
        "symptoms": ["五心烦热", "潮热盗汗", "口干咽燥", "失眠多梦", "舌红少苔", "大便干结"],
        "related": ["阴虚", "火旺", "阴阳失调", "肝肾阴虚"],
        "classics": "《黄帝内经·素问》'阴虚则内热'",
        "formulas": ["六味地黄丸", "知柏地黄丸", "天王补心丹"],
        "acupoints": ["太溪穴", "三阴交", "涌泉穴"]
    },
    "肝气郁结": {
        "category": "脏腑失调",
        "symptoms": ["胁肋胀痛", "胸闷善太息", "情绪抑郁", "月经不调", "乳房胀痛", "咽部异物感"],
        "related": ["肝郁脾虚", "气滞血瘀", "肝火上炎", "肝胆湿热"],
        "classics": "《丹溪心法》'气血冲和，万病不生，一有怫郁，诸病生焉'",
        "formulas": ["逍遥散", "柴胡疏肝散", "丹栀逍遥散"],
        "acupoints": ["太冲穴", "期门穴", "内关穴"]
    },
    "气血不足": {
        "category": "气血津液",
        "symptoms": ["面色苍白", "头晕眼花", "心悸气短", "疲乏无力", "月经量少", "舌淡苔白"],
        "related": ["气虚", "血虚", "气血两虚", "心脾两虚"],
        "classics": "《景岳全书》'人有阴阳，即为气血。阳主气，故气全则神旺；阴主血，故血盛则形强'",
        "formulas": ["八珍汤", "归脾汤", "十全大补丸"],
        "acupoints": ["足三里", "气海穴", "血海穴"]
    },
    "痰湿内阻": {
        "category": "病理产物",
        "symptoms": ["身体困重", "胸闷脘痞", "痰多易咳", "头晕嗜睡", "舌苔厚腻"],
        "related": ["脾虚湿盛", "痰瘀互结", "湿热内蕴"],
        "classics": "《金匮要略》'病痰饮者，当以温药和之'",
        "formulas": ["二陈汤", "平胃散", "温胆汤"],
        "acupoints": ["丰隆穴", "中脘穴", "阴陵泉"]
    },
    "肾阳不足": {
        "category": "脏腑失调",
        "symptoms": ["腰膝酸冷", "畏寒肢凉", "性欲减退", "夜尿频多", "舌淡胖苔白"],
        "related": ["命门火衰", "脾肾阳虚", "肾气不固"],
        "classics": "《医贯》'命门之火，乃水中之火，相依而永不相离也'",
        "formulas": ["金匮肾气丸", "右归丸", "真武汤"],
        "acupoints": ["关元穴", "命门穴", "肾俞穴"]
    }
}

# 季节养生建议增强
SEASONAL_ADVICE = {
    "春季": {
        "principle": "疏肝理气，养阳防风",
        "foods": ["韭菜", "香椿", "荠菜", "春笋"],
        "activity": "晨起散步，舒展筋骨",
        "warning": "忌过早减衣，防倒春寒"
    },
    "夏季": {
        "principle": "清热解暑，养心健脾",
        "foods": ["绿豆", "西瓜", "荷叶", "苦瓜"],
        "activity": "午间小憩，避免烈日",
        "warning": "忌过度贪凉，防暑湿"
    },
    "秋季": {
        "principle": "滋阴润燥，养肺防燥",
        "foods": ["梨", "百合", "银耳", "芝麻"],
        "activity": "早睡早起，收敛神气",
        "warning": "忌辛辣燥热，防秋燥"
    },
    "冬季": {
        "principle": "温补阳气，养肾防寒",
        "foods": ["羊肉", "核桃", "桂圆", "黑豆"],
        "activity": "早睡晚起，避寒就温",
        "warning": "忌过度出汗，防寒邪"
    }
}

# 体质类型建议扩展
CONSTITUTION_ADVICE = {
    "气虚质": {
        "features": "气短懒言，易疲乏，易感冒",
        "foods": ["山药", "大枣", "鸡肉", "黄芪"],
        "avoid": ["生冷", "油腻", "过度劳累"]
    },
    "阳虚质": {
        "features": "畏寒肢冷，喜热饮，精神不振",
        "foods": ["羊肉", "韭菜", "核桃", "肉桂"],
        "avoid": ["生冷", "寒凉食物", "熬夜"]
    },
    "阴虚质": {
        "features": "手足心热，口燥咽干，喜冷饮",
        "foods": ["银耳", "百合", "梨", "麦冬"],
        "avoid": ["辛辣", "燥热食物", "熬夜"]
    },
    "痰湿质": {
        "features": "形体肥胖，腹部肥满，口黏苔腻",
        "foods": ["薏米", "赤小豆", "冬瓜", "荷叶"],
        "avoid": ["肥甘厚味", "甜食", "久坐"]
    },
    "湿热质": {
        "features": "面垢油光，口苦苔黄，大便黏滞",
        "foods": ["绿豆", "苦瓜", "黄瓜", "芹菜"],
        "avoid": ["辛辣", "油腻", "烟酒"]
    },
    "血瘀质": {
        "features": "面色晦暗，易有瘀斑，舌质紫暗",
        "foods": ["山楂", "玫瑰花", "黑木耳", "红糖"],
        "avoid": ["寒凉", "生冷", "情绪抑郁"]
    },
    "气郁质": {
        "features": "情绪低落，敏感多疑，胁肋胀痛",
        "foods": ["佛手", "陈皮", "薄荷", "茉莉花"],
        "avoid": ["生闷气", "过度思虑", "久坐少动"]
    },
    "特禀质": {
        "features": "过敏体质，易患哮喘、荨麻疹",
        "foods": ["乌梅", "防风", "灵芝", "蝉蜕"],
        "avoid": ["过敏原", "发物", "剧烈运动"]
    }
}

# 中医典籍数据库
TCM_CLASSICS = {
    "黄帝内经": {
        "era": "战国至秦汉",
        "content": "中医理论奠基之作，分为《素问》和《灵枢》",
        "famous": "'上工治未病，不治已病'、'正气存内，邪不可干'"
    },
    "伤寒论": {
        "era": "东汉",
        "author": "张仲景",
        "content": "外感热病诊疗经典，创立六经辨证体系",
        "famous": "'观其脉证，知犯何逆，随证治之'"
    },
    "金匮要略": {
        "era": "东汉",
        "author": "张仲景",
        "content": "内科杂病诊疗经典，与《伤寒论》合称《伤寒杂病论》",
        "famous": "'见肝之病，知肝传脾，当先实脾'"
    },
    "温病条辨": {
        "era": "清代",
        "author": "吴鞠通",
        "content": "温病学代表作，创立三焦辨证",
        "famous": "'治上焦如羽，非轻不举；治中焦如衡，非平不安；治下焦如权，非重不沉'"
    }
}

# 系统提示词全面升级
SYSTEM_PROMPT = f"""
你是一位资深中医专家，负责将复杂的中医术语转化为年轻人易懂的现代语言，同时保持专业性和准确性。今天是{datetime.datetime.now().strftime('%Y年%m月%d日')}，当前季节是{random.choice(list(SEASONAL_ADVICE.keys()))}。

【核心任务】
1. 术语验证：首先确认用户输入是否为规范中医术语，必要时要求用户确认
2. 现代转化：用【】标注现代对应词（不超过5字）
3. 专业解释：包含中医定义、经典出处、中西医机理对照、常见表现
4. 实用建议：分季节、体质提供具体可行的养生方案
5. 趣味元素：添加冷知识、生活比喻和emoji表情
6. 扩展内容：提供经典方剂、穴位保健、食疗方案和日常调理建议

【输出结构】
🌟 术语转换：[原术语] → 【现代词】

📖 核心解释：
  
  - 中医定义：专业解释（含经典出处）
  
  - 现代医学对应：西医解释（如适用）
  
  - 核心机理：用流程图/比喻说明（如"就像手机后台程序太多导致发烫"）
  
  - 🧾 典型症状：3-6个关键表现（含舌脉特征）

💡 养生锦囊（分人群）：

  👨‍👩‍👧 通用建议：四季皆宜的基础养生法

  🌸 春季专项：{SEASONAL_ADVICE['春季']['principle']}
  
  🔥 夏季专项：{SEASONAL_ADVICE['夏季']['principle']}
  
  🍂 秋季专项：{SEASONAL_ADVICE['秋季']['principle']}
  
  ❄️ 冬季专项：{SEASONAL_ADVICE['冬季']['principle']}
  
  🧬 分体质调理：针对{", ".join(CONSTITUTION_ADVICE.keys())}的建议

⚕️ 专业方案：

  💊 经典方剂：2-3个常用方（含组成和用量）

  🧴 中成药推荐：常见品牌和用法
  
  👐 穴位保健：3个关键穴位+按摩方法
  
  🥗 食疗方案：详细食谱（含烹饪法）

⚠️ 禁忌提醒：关键注意事项

🔬 冷知识：有趣的中医小知识（含现代研究）

📌 文末注：⚠️本解释仅供参考，具体请咨询执业中医师

【专业要求】
1. 解释需引用经典著作（《黄帝内经》《伤寒论》等）
2. 区分不同体质({', '.join(CONSTITUTION_ADVICE.keys())})的建议
3. 包含现代医学的对应解释
4. 剂量精确到克，时间精确到时辰
5. 提供穴位定位方法和按摩技巧
6. 包含1-2项现代研究成果

【风格指南】
1. 对年轻人使用"梗文化"表达（如"肝论文"比喻伤肝）
2. 每部分添加相关emoji增强可读性
3. 专业术语后括号标注拼音（如"阴虚 yīn xū"）
4. 关键内容用🔑标注
5. 使用表格对比不同体质/季节的建议

【示例参考】
输入：阴虚火旺
输出：
🌟【身体过热2.0版】← 原术语：阴虚火旺(yīn xū huǒ wàng)

📖 
  
  - 中医定义：体内"阴液"不足导致虚火上升（《黄帝内经》"阴虚则内热"）
  
  - 现代医学：植物神经功能紊乱+慢性炎症状态
  
  - 核心机理：阴液不足→无法制约阳气→虚火内生

  🧾 典型症状：
   
    ① 五心烦热（手脚心+胸口发热） 🔑
    
    ② 午后潮热（下午3-5点明显）
    
    ③ 失眠多梦（入睡难+多梦）
    
    ④ 口干咽燥（喜冷饮）
    
    ⑤ 舌红少苔（舌象特征）
    
    ⑥ 脉细数（脉象特征）
💡 
  👨‍👩‍👧 通用建议：晚上11点前睡"美容充电"
  （换行，区分开每个季节）

  🌸 春季：枸杞菊花茶（枸杞5g+菊花3g）
  
  🔥 夏季：西洋参3g泡水
  
  🧬 分体质：(输出为一个表格，要求格式正确)
  
    | 体质   | 建议方案               |
    |--------|------------------------|
    | 阴虚质 | 银耳百合羹（银耳10g+百合15g） |
    | 气虚质 | 生脉饮（人参3g+麦冬10g+五味子6g）|

    
⚕️
  💊 经典方剂：

    • 六味地黄丸（熟地24g+山茱萸12g+山药12g+泽泻9g+丹皮9g+茯苓9g）
  
    • 知柏地黄丸（六味地黄丸+知母6g+黄柏6g）
  
  🧴 中成药：同仁堂知柏地黄丸（8粒/次，2次/日）
 
    👐 穴位保健：
    
    • 太溪穴（内踝后方凹陷处）：按揉3分钟/次，2次/日
    
    • 涌泉穴（足底前1/3凹陷处）：睡前按摩5分钟

  🥗 食疗：雪梨1个+麦冬10g+冰糖5g炖煮30分钟

  ⚠️ 忌：熬夜刷剧、吃辣条、过量健身、辛辣食物

  🔬 冷知识：按揉太溪穴能增加唾液分泌，缓解口干（现代研究证实）

  📌 ⚠️本解释仅供参考，具体请咨询执业中医师
"""

def clear_chat_history():
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT},
                               {"role": "assistant", "content": "您好！我是中医术语解读专家🌿，输入任何中医术语，我将为您提供专业且通俗的解释！\n\n例如：'阴虚火旺'、'肝气郁结'、'气血不足'等"}]

def init_chat_history():
    if "messages" not in st.session_state:
        clear_chat_history()
    
    for message in st.session_state.messages[1:]:  # 跳过系统消息
        avatar = '👤' if message["role"] == "user" else '🌿'
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
    
    return st.session_state.messages

def query(messages: List[Dict[str, str]]) -> Iterator[str]:
    response = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=messages,
        temperature=0.7,  # 稍高的温度增加创造性
        top_p=0.9,  
        max_tokens=1500,  # 增加token限制获取更详细内容
        stream=True
    )
    
    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

def get_related_terms(term):
    """获取相关术语推荐"""
    if term in TCM_TERMS_DATABASE:
        return TCM_TERMS_DATABASE[term].get("related", [])
    return []

def display_term_info(term):
    """在侧边栏显示术语详细信息"""
    if term in TCM_TERMS_DATABASE:
        info = TCM_TERMS_DATABASE[term]
        with st.sidebar.expander(f"📚 {term} 专业档案", expanded=True):
            st.write(f"**分类**: {info['category']}")
            
            st.subheader("典型症状")
            cols = st.columns(2)
            for i, symptom in enumerate(info['symptoms']):
                cols[i%2].write(f"- {symptom}")
            
            if 'classics' in info:
                st.subheader("经典出处")
                st.info(info['classics'])
            
            if 'formulas' in info and info['formulas']:
                st.subheader("经典方剂")
                for formula in info['formulas']:
                    st.write(f"- {formula}")
            
            if 'acupoints' in info and info['acupoints']:
                st.subheader("特效穴位")
                for point in info['acupoints']:
                    st.write(f"- {point}")
            
            if 'related' in info and info['related']:
                st.subheader("相关术语")
                for related_term in info['related']:
                    st.write(f"- {related_term}")

def get_seasonal_advice():
    """获取季节养生建议"""
    current_season = random.choice(list(SEASONAL_ADVICE.keys()))
    advice = SEASONAL_ADVICE[current_season]
    return f"**{current_season}养生**: {advice['principle']}\n- � 推荐食物: {', '.join(advice['foods'])}\n- 🏃‍♂️ 活动建议: {advice['activity']}\n- ⚠️ 注意事项: {advice['warning']}"

def get_constitution_advice():
    """获取体质建议摘要"""
    selected = random.sample(list(CONSTITUTION_ADVICE.keys()), 3)
    result = []
    for const in selected:
        info = CONSTITUTION_ADVICE[const]
        result.append(f"**{const}**: {info['features']}\n- ✅ 宜食: {', '.join(info['foods'][:3])}\n- ❌ 忌: {', '.join(info['avoid'][:2])}")
    return result

def get_classic_info():
    """获取典籍信息"""
    classic = random.choice(list(TCM_CLASSICS.keys()))
    info = TCM_CLASSICS[classic]
    return f"**{classic}**\n- 📜 内容: {info['content']}\n- 🔖 名句: {info.get('famous', '')}"

def main():
    messages = init_chat_history()
    
    # 侧边栏 - 中医知识库
    with st.sidebar:
        st.header("📚 中医知识库")
        
        # 季节养生
        with st.expander("🌦️ 季节养生指南", expanded=True):
            st.info(get_seasonal_advice())
        
        # 体质调理
        with st.expander("🧬 体质调理要点", expanded=True):
            for advice in get_constitution_advice():
                st.info(advice)
        
        # 经典著作
        with st.expander("📜 中医经典著作", expanded=True):
            st.info(get_classic_info())
        
        # 术语数据库
        with st.expander("🔍 中医术语库", expanded=True):
            st.write("已收录术语:")
            cols = st.columns(3)
            for i, term in enumerate(TCM_TERMS_DATABASE.keys()):
                cols[i%3].button(term, key=f"term_{term}", use_container_width=True)
        
        # 实用工具
        with st.expander("⚙️ 实用工具", expanded=True):
            st.button("随机中医小知识", use_container_width=True)
            st.button("今日养生茶推荐", use_container_width=True)
            st.button("穴位定位查询", use_container_width=True)
        
        # 学习资源
        with st.expander("🎓 学习资源", expanded=True):
            st.link_button("《黄帝内经》全文", "https://example.com")
            st.link_button("中药数据库", "https://example.com")
            st.link_button("穴位图谱", "https://example.com")
    
    # 主聊天区
    if prompt := st.chat_input("输入中医术语，如'阴虚火旺'"):
        # 显示用户消息
        with st.chat_message("user", avatar='👤'):
            st.markdown(prompt)
        
        # 添加用户消息时保留系统消息
        messages.append({"role": "user", "content": prompt})
        
        # 在侧边栏显示术语信息
        display_term_info(prompt)
        
        # 获取相关术语推荐
        related_terms = get_related_terms(prompt)
        
        # 显示助手回复
        with st.chat_message("assistant", avatar='🌿'):
            full_response = []
            placeholder = st.empty()
            
            # 流式输出
            for chunk in query(messages):
                full_response.append(chunk)
                placeholder.markdown("".join(full_response))
            
            final_response = "".join(full_response)
            messages.append({"role": "assistant", "content": final_response})
            
            # 显示相关术语推荐
            if related_terms:
                st.divider()
                st.subheader("🔍 相关术语推荐")
                cols = st.columns(3)
                for i, term in enumerate(related_terms[:3]):
                    if cols[i].button(term, key=f"related_{term}", use_container_width=True):
                        # 点击后自动查询相关术语
                        messages.append({"role": "user", "content": term})
                        st.rerun()
    
    # 底部功能区
    st.divider()
    st.subheader("📚 中医学习资源")
    col1, col2, col3, col4 = st.columns(4)
    col1.link_button("经典著作", "https://example.com/classics")
    col2.link_button("中药图谱", "https://example.com/herbs")
    col3.link_button("穴位查询", "https://example.com/acupoints")
    col4.link_button("方剂大全", "https://example.com/formulas")
    
    # 清空按钮
    if st.button("清空对话", key="clear_button", use_container_width=True):
        clear_chat_history()
        st.rerun()

if __name__ == "__main__":
    main()
