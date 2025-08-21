# 中医智能问诊系统 - 医易通中医训练平台
import streamlit as st
import requests
import json
import time
from datetime import datetime

# ================== 配置区域 ==================
# 在此处输入您的Kimi API密钥
KIMI_API_KEY = "sk-CXx3Cs76mQCYLhq8nrTdGb1qGijoQPXAjS8khPm29k8GU5Yt"  # 替换为您的实际API密钥
# =============================================

# 初始化全局配置
KIMI_API_URL = "https://api.moonshot.cn/v1/chat/completions"
KIMI_MODEL = "moonshot-v1-8k"

# 初始化Session State
def init_session_state():
    if "patient_messages" not in st.session_state:
        st.session_state.patient_messages = []
    
    if "consultation_started" not in st.session_state:
        st.session_state.consultation_started = False
    
    if "consultation_ended" not in st.session_state:
        st.session_state.consultation_ended = False
    
    if "diagnosis_summary" not in st.session_state:
        st.session_state.diagnosis_summary = None
    
    if "diagnosis_score" not in st.session_state:
        st.session_state.diagnosis_score = None
    
    if "knowledge_gaps" not in st.session_state:
        st.session_state.knowledge_gaps = None
    
    if "recommendations" not in st.session_state:
        st.session_state.recommendations = None
    
    if "correct_pattern" not in st.session_state:
        st.session_state.correct_pattern = None
    
    if "user_diagnosis" not in st.session_state:
        st.session_state.user_diagnosis = None
    
    if "diagnosis_result" not in st.session_state:
        st.session_state.diagnosis_result = None

# 调用Kimi API
def call_kimi_api(prompt, system_prompt=None, temperature=0.7, max_tokens=2000):
    headers = {
        "Authorization": f"Bearer {KIMI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "model": KIMI_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }
    
    try:
        response = requests.post(KIMI_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"API调用失败: {str(e)}")
        return None

# 生成诊断总结
def generate_diagnosis_summary():
    prompt = f"""
    作为中医教育专家，请基于以下医患对话记录生成诊断报告：
    
    **任务要求**：
    1. 分析医生（用户）的中医诊断过程
    2. 评估诊断质量（0-100分）
    3. 指出医生遗漏的四诊信息
    4. 提供中医知识补充建议
    
    **对话记录**：
    {st.session_state.patient_messages}
    
    **输出格式**：
    {{
        "summary": "诊断总结内容",
        "score": 85,
        "knowledge_gaps": ["遗漏问题1", "遗漏问题2"],
        "recommendations": ["建议1", "建议2"]
    }}
    """
    
    result = call_kimi_api(
        prompt, 
        system_prompt="你是一名资深中医教育专家，负责评估医学生的诊断能力并提供反馈",
        temperature=0.3
    )
    
    try:
        # 提取JSON部分
        json_str = result[result.find("{"):result.rfind("}")+1]
        return json.loads(json_str)
    except:
        st.error("总结生成失败，请重试")
        return None

# 获取初始病人症状和正确证型
def get_initial_symptoms():
    patterns = [
        "肝气郁结证", "心脾两虚证", "痰湿内阻证", 
        "肾阳不足证", "气血亏虚证", "阴虚火旺证"
    ]
    
    symptoms = [
        "胁肋胀痛3个月，情绪波动时加重，伴胸闷善太息",
        "心悸失眠2个月，健忘多梦，食欲不振，面色萎黄",
        "头重如裹1个月，肢体困重，脘腹胀满，大便粘腻",
        "腰膝酸软冷痛半年，畏寒肢冷，夜尿频多",
        "头晕乏力3个月，气短懒言，月经量少色淡",
        "五心烦热2个月，潮热盗汗，口干咽燥，舌红少苔"
    ]
    
    prompt = f"""
    请为中医问诊训练创建一个病例：
    1. 从以下证型中随机选择一个作为正确诊断：{patterns}
    2. 从以下症状中选择对应证型的典型症状：{symptoms}
    3. 生成病人详细的中医四诊信息（尽量避免专业术语，表达口语化，日常化）：
       - 主诉（含持续时间）
       - 现病史（症状变化、加重缓解因素）
       - 既往史
       - 舌象描述
       - 脉象描述
    
    输出格式：
    {{
        "correct_pattern": "正确中医证型",
        "presentation": "病人详细症状描述",
        "tongue": "舌象描述",
        "pulse": "脉象描述"
    }}
    """
    
    result = call_kimi_api(
        prompt,
        system_prompt="你是一名中医标准化病人(SP)，负责提供详细的中医四诊信息",
        temperature=0.4
    )
    
    try:
        json_str = result[result.find("{"):result.rfind("}")+1]
        return json.loads(json_str)
    except:
        return {
            "correct_pattern": "肝气郁结证",
            "presentation": "我最近三个月经常感到胁肋胀痛，特别是在情绪波动时加重。伴有胸闷，喜欢叹气，食欲也不太好。",
            "tongue": "舌质淡红，苔薄白",
            "pulse": "脉弦"
        }

# 评估用户诊断
def evaluate_diagnosis(user_diagnosis):
    prompt = f"""
    作为中医专家，请评估医生提交的诊断：
    
    **病例信息**：
    {st.session_state.patient_messages[-5:]}
    
    **医生诊断**：{user_diagnosis}
    **正确证型**：{st.session_state.correct_pattern}
    
    **评估要求**：
    1. 判断诊断是否正确（完全正确/部分正确/错误）
    2. 分析诊断依据是否充分
    3. 解释正确证型的辨证要点
    4. 提供改进建议
    
    输出格式：
    {{
        "result": "诊断结果评价",
        "analysis": "详细分析",
        "key_points": ["辨证要点1", "辨证要点2"]
    }}
    """
    
    result = call_kimi_api(
        prompt,
        system_prompt="你是一名资深中医专家，负责评估医学生的辨证诊断能力",
        temperature=0.3
    )
    
    try:
        json_str = result[result.find("{"):result.rfind("}")+1]
        return json.loads(json_str)
    except:
        return {
            "result": "部分正确",
            "analysis": "医生抓住了主要证候特征，但忽略了关键鉴别点",
            "key_points": ["胁痛与情绪相关", "脉弦是重要指征"]
        }

# 界面布局
def main():
    st.set_page_config(
        page_title="医易通中医诊断训练平台",
        page_icon="🌿",
        layout="wide"
    )
    
    init_session_state()
    
    st.title("🌿 医易通中医智能问诊系统")
    st.caption("AI标准化病人 | 中医四诊训练 | 证型诊断 | 实时反馈与评分 | 知识点查漏补缺")
    
    # 侧边栏配置
    with st.sidebar:
        st.image("https://www.moonshot.cn/favicon.ico", width=50)
        st.subheader("中医训练控制")
        
        if not st.session_state.consultation_started:
            if st.button("开始新病例", type="primary", use_container_width=True):
                st.session_state.consultation_started = True
                st.session_state.consultation_ended = False
                
                # 获取初始症状
                case_data = get_initial_symptoms()
                initial_message = f"主诉: {case_data['presentation']}\n\n舌象: {case_data['tongue']}\n脉象: {case_data['pulse']}"
                
                st.session_state.patient_messages = [{
                    "role": "patient",
                    "content": initial_message
                }]
                st.session_state.correct_pattern = case_data["correct_pattern"]
                st.rerun()
        
        if st.session_state.consultation_started and not st.session_state.consultation_ended:
            if st.button("结束问诊并诊断", type="primary", use_container_width=True):
                st.session_state.consultation_ended = True
                st.rerun()
        
        if st.session_state.consultation_ended:
            if st.button("开始新病例", type="primary", use_container_width=True):
                init_session_state()
                st.rerun()
        
        st.divider()
        st.info("""
        **中医训练流程：**
        1. 点击"开始新病例"
        2. 使用中医四诊方法询问
        3. 进行中医辨证分析
        4. 提交最终证型诊断
        5. 查看诊断评估报告
        
        **中医四诊要点：**
        - 望诊：神色、形态、舌象
        - 闻诊：声音、气味
        - 问诊：寒热、汗出、疼痛、饮食等
        - 切诊：脉象、按诊
        """)
        
        st.divider()
        st.caption("中医诊断训练系统 v2.0 | 使用Kimi大模型")

    # 主聊天区域
    if st.session_state.consultation_started:
        st.subheader("🩺 中医四诊问诊")
        
        for msg in st.session_state.patient_messages:
            avatar = "🤖" if msg["role"] == "patient" else "👨‍⚕️"
            role = "病人" if msg["role"] == "patient" else "医生"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(f"**{role}**: {msg['content']}")
    
    # 医生输入区域（中医问诊）
    if st.session_state.consultation_started and not st.session_state.consultation_ended:
        if prompt := st.chat_input("使用中医四诊方法询问..."):
            st.session_state.patient_messages.append({"role": "doctor", "content": prompt})
            
            with st.chat_message("doctor", avatar="👨‍⚕️"):
                st.markdown(f"**医生**: {prompt}")
            
            with st.chat_message("patient", avatar="🤖"):
                message_placeholder = st.empty()
                full_response = ""
                
                # 构建完整对话历史
                conversation_history = "\n".join(
                    [f"{'病人' if msg['role']=='patient' else '医生'}: {msg['content']}" 
                     for msg in st.session_state.patient_messages]
                )
                
                # 中医专业系统提示词
                system_prompt = """
                你是一名标准化病人(SP)，正在接受中医医生的问诊。请遵守以下规则：
                1. 只描述症状，不做自我诊断
                2. 根据医生问诊回答相关问题
                3. 症状描述日常化，少用专业术语
                4. 回答详细，每次回答描述清楚自己的症状
                5. 可描述舌象、脉象等中医特有体征
                6. 不主动提供未询问的信息
                
                典型症状描述方式：
                - 疼痛性质：胀痛、刺痛、冷痛、隐痛等
                - 寒热表现：畏寒、五心烦热、潮热等
                - 汗出情况：自汗、盗汗、大汗淋漓等
                - 饮食口味：口苦、口淡无味、食欲不振等
                - 二便情况：大便溏泄、小便清长等
                """
                
                # 调用API
                response = call_kimi_api(
                    prompt=prompt,
                    system_prompt=system_prompt + f"\n当前对话历史:\n{conversation_history}",
                    temperature=0.4
                )
                
                if response:
                    # 模拟流式输出
                    for chunk in response.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        message_placeholder.markdown(f"**病人**: {full_response}▌")
                    message_placeholder.markdown(f"**病人**: {full_response}")
                    
                    st.session_state.patient_messages.append({
                        "role": "patient",
                        "content": full_response
                    })
    
    # 诊断提交区域
    if st.session_state.consultation_ended and st.session_state.user_diagnosis is None:
        st.divider()
        st.subheader("🩺 中医证型诊断")
        
        with st.form("diagnosis_form"):
            st.info("请根据问诊信息提交中医证型诊断")
            st.write(f"**主诉**: {st.session_state.patient_messages[0]['content'].split('舌象')[0]}")
            
            user_diagnosis = st.text_input("中医证型诊断", 
                                          placeholder="例如：肝气郁结证、心脾两虚证等",
                                          help="请输入标准中医证型名称")
            
            submitted = st.form_submit_button("提交诊断")
            if submitted and user_diagnosis:
                st.session_state.user_diagnosis = user_diagnosis
                with st.spinner("正在评估您的诊断..."):
                    st.session_state.diagnosis_result = evaluate_diagnosis(user_diagnosis)
                    st.rerun()
    
    # 显示诊断评估报告
    if st.session_state.user_diagnosis and st.session_state.diagnosis_result:
        st.divider()
        st.subheader("📊 中医诊断评估报告")
        
        # 诊断结果
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("您的诊断", st.session_state.user_diagnosis)
        with col2:
            st.metric("正确证型", st.session_state.correct_pattern)
        with col3:
            result_text = st.session_state.diagnosis_result["result"]
            
            # 根据结果类型设置不同的容器样式
            if "完全正确" in result_text:
                st.success(f"诊断结果: {result_text}")
            elif "部分正确" in result_text:
                st.warning(f"诊断结果: {result_text}")
            elif "错误" in result_text:
                st.error(f"诊断结果: {result_text}")
            else:
                st.info(f"诊断结果: {result_text}")
        
        # 诊断分析
        st.subheader("🔍 诊断分析")
        st.info(st.session_state.diagnosis_result["analysis"])
        
        # 辨证要点
        st.subheader("📌 关键辨证要点")
        for point in st.session_state.diagnosis_result.get("key_points", []):
            st.success(f"- {point}")
        
        # 生成详细总结
        if st.session_state.diagnosis_summary is None:
            with st.spinner("正在生成详细评估报告..."):
                summary = generate_diagnosis_summary()
                if summary:
                    st.session_state.diagnosis_summary = summary.get("summary", "")
                    st.session_state.diagnosis_score = summary.get("score", 0)
                    st.session_state.knowledge_gaps = summary.get("knowledge_gaps", [])
                    st.session_state.recommendations = summary.get("recommendations", [])
                st.rerun()
        
        if st.session_state.diagnosis_summary:
            st.divider()
            st.subheader("📋 综合评估报告")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("诊断能力评分", f"{st.session_state.diagnosis_score}/100")
                st.progress(st.session_state.diagnosis_score / 100)
                
                st.subheader("⚠️ 需要加强的知识点")
                for gap in st.session_state.knowledge_gaps:
                    st.error(f"- {gap}")
            
            with col2:
                st.subheader("📝 评估总结")
                st.info(st.session_state.diagnosis_summary)
                
                st.subheader("💡 学习建议")
                for rec in st.session_state.recommendations:
                    st.success(f"- {rec}")
        
        # 中医经典推荐
        with st.expander("📚 中医经典学习资源"):
            if st.session_state.knowledge_gaps:
                st.markdown(f"""
                **推荐学习以下中医经典著作**:
                
                1. **核心经典**  
                《黄帝内经》- {st.session_state.correct_pattern}相关章节  
                《伤寒论》- 相关证候的辨证论治
                
                2. **方剂学习**  
                《方剂学》- {st.session_state.correct_pattern}常用方剂  
                《中药学》- 相关证型常用药物
                
                3. **临床医案**  
                《古今医案按》- 相关证型经典案例  
                《临证指南医案》- 叶天士诊疗经验
                """)
            else:
                st.success("您的辨证诊断非常准确，体现了扎实的中医功底！")

if __name__ == "__main__":
    main()