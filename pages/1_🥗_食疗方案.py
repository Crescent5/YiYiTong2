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
            "image": "https://img.zcool.cn/community/01b3b05c0c7c46a801208f8b1c9332.jpg@2o.jpg",
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
            "image": "https://img.zcool.cn/community/01d3fc5c0c7c46a801208f8b9c3f3a.jpg@2o.jpg",
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
            "image": "https://img.zcool.cn/community/01a6c15c0c7c46a801208f8b0a9c3a.jpg@2o.jpg",
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
            "image": "https://img.zcool.cn/community/01e9d15c0c7c46a801208f8b1a9c3a.jpg@2o.jpg",
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
            "image": "https://img.zcool.cn/community/01f9c15c0c7c46a801208f8b1a9c3a.jpg@2o.jpg",
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
            "image": "https://img.zcool.cn/community/01c9c15c0c7c46a801208f8b1a9c3a.jpg@2o.jpg",
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
            "image": "https://img.zcool.cn/community/01d9c15c0c7c46a801208f8b1a9c3a.jpg@2o.jpg",
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
            "image": "https://img.zcool.cn/community/01e9c15c0c7c46a801208f8b1a9c3a.jpg@2o.jpg",
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
            "image": "https://img.zcool.cn/community/01f9c15c0c7c46a801208f8b1a9c3a.jpg@2o.jpg",
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
            "image": "https://img.zcool.cn/community/01a9c15c0c7c46a801208f8b1a9c3a.jpg@2o.jpg",
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
            "image": "https://img.zcool.cn/community/01b9c15c0c7c46a801208f8b1a9c3a.jpg@2o.jpg",
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
            "image": "https://img.zcool.cn/community/01c9c15c0c7c46a801208f8b1a9c3a.jpg@2o.jpg",
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
            "image": "https://img.zcool.cn/community/01d9c15c0c7c46a801208f8b极客时间海报.jpg",
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
            "image": "https://img.zcool.cn/community/01e9c15c0c7c46a801208f8b1a9c3a.jpg@2o.jpg",
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
            "image": "https://img.zcool.cn/community/01f9c15c0c7c46a801208f8b1a9c3a.jpg@2o.jpg",
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
            "image": "https://img.zcool.cn/community/01a9c15c0c7c46a801208f8b1a9c3a.jpg@2o.jpg",
            "description": "健脾祛湿的经典汤品",
            "ingredients": "茯苓20g，芡实20g，莲子20g，山药20g，猪肚或瘦肉适量",
            "method": "1. 肉类焯水备用；\n2. 将所有材料放入锅中，加水大火煮沸；\n3. 转小火炖煮1.5小时；\n4. 加盐调味即可。",
            "benefits": "健脾祛湿，补肾固精，增强免疫力",
            "suitable_for": "脾虚湿盛、消化不良、免疫力低下者",
            "season": "长夏季节",
            "keywords": ["健脾", "祛湿", "补肾", "免疫"]
        },
        {
            "name": "薄荷柠檬茶",
            "image": "https://img.zcool.cn/community/01b9c15c0c7c46a801208f8b1a9c3a.jpg@2o.jpg",
            "description": "清凉解暑的夏季饮品",
            "ingredients": "新鲜薄荷叶10片，柠檬2片，蜂蜜适量，热水500ml",
            "method": "1. 将薄荷叶和柠檬片放入杯中；\n2. 加入热水，浸泡5分钟；\n3. 加入蜂蜜调味即可饮用。",
            "benefits": "清凉解暑，提神醒脑，缓解头痛",
            "suitable_for": "暑热烦渴、头晕头痛、咽喉不适者",
            "season": "夏季",
            "keywords": ["清凉", "解暑", "提神", "醒脑"]
        },
        {
            "name": "核桃芝麻粥",
            "image": "https://img.zcool.cn/community/01c9c15c0c7c46a801208f极客时间海报.jpg",
            "description": "补脑乌发的养生粥品",
            "ingredients": "核桃仁30g，黑芝麻20g，大米100g，冰糖适量，水适量",
            "method": "1. 大米洗净；\n2. 将所有材料放入锅中加水大火煮沸；\n3. 转小火煮30分钟至粥稠；\n4. 加入冰糖搅拌至溶解即可。",
            "benefits": "补脑益智，乌发养颜，补肾固精",
            "suitable_for": "用脑过度、白发脱发、记忆力减退者",
            "season": "秋冬季节",
            "keywords": ["补脑", "乌发", "补肾", "益智"]
        },
        {
            "name": "生姜紫苏茶",
            "image": "https://img.zcool.cn/community/01d9c极客时间海报.jpg",
            "description": "散寒解表的养生茶饮",
            "ingredients": "生姜3片，紫苏叶10g，红糖适量，水500ml",
            "method": "1. 将生姜和紫苏叶放入锅中；\n2. 加水煮沸5分钟；\n3. 加入红糖搅拌至溶解即可饮用。",
            "benefits": "散寒解表，理气宽中，缓解感冒症状",
            "suitable_for": "风寒感冒、胃脘胀满、恶心呕吐者",
            "season": "冬季",
            "keywords": ["散寒", "解表", "理气", "感冒"]
        },
        {
            "name": "木瓜炖雪蛤",
            "image": "https://img.zcool.cn/community/01e9c15c0c7c46a801208f8b1a9c3极客时间海报.jpg",
            "description": "美容养颜的滋补甜品",
            "ingredients": "木瓜1个，雪蛤5g，冰糖适量，牛奶或椰汁适量",
            "method": "1. 雪蛤提前泡发；\n2. 木瓜去皮去籽，切块；\n3. 将雪蛤和冰糖放入木瓜中；\n4. 上锅蒸20分钟；\n5. 加入牛奶或椰汁即可。",
            "benefits": "美容养颜，滋阴润肺，丰胸通乳",
            "suitable_for": "皮肤干燥、肺燥咳嗽、产后乳汁不足者",
            "season": "四季皆宜",
            "keywords": ["美容", "滋阴", "润肺", "丰胸"]
        },
    
        {
            "name": "葱豉豆腐汤",
            "image": "",
            "description": "发散风寒的汤品",
            "ingredients": "豆腐250g，淡豆豉12g，葱白15g，调料、清水适量。",
            "method": "将豆腐洗净、切块，淡豆豉洗净，葱白洗净、拍扁切段，备用；在锅中放入适量油，用中火将油烧热后，放入豆腐块，将豆腐块煎至金黄色，再放人淡豆豉、适量清水，武火煮沸后，改用文火煮约半小时，放入葱白，煮至葱香飘出，调料调味即可。每日1次，连服2~3日。",
            "benefits": "发散风寒、芳香通窍",
            "suitable_for": "适用于防治伤风感冒及久吹空调引起的不适，常见有恶寒、发热、头痛、鼻塞、鼻流清涕、打喷嚏、咽喉痒痛、咳嗽等表现者，有预防和缓解感冒症状的作用。",
            "season": "",
            "keywords": ["风寒", "感冒", "鼻塞"]
        },
    {
        "name": "芫荽汤",
        "image": "",
        "description": "透发痘疹的汤品",
        "ingredients": "鲜芫荽150g，鲜胡萝卜200g，鲜荸荠100g，干板栗15g。",
        "method": "将芫荽、胡萝卜、荸荠、板栗洗净、切碎，备用；再将以上四味食材一同放入锅中，加入适量清水，煎煮至沸腾，去渣取汁饮用即可。以上煎煮后取汤两碗为1日量，分作两次温热饮用，连续饮用3~5日。",
        "benefits": "透发痘疹",
        "suitable_for": "适用于防治小儿水痘、疹出不畅等。",
        "season": "",
        "keywords": ["水痘", "疹出不畅"]
    },
    {
        "name": "银花茶",
        "image": "",
        "description": "辛凉解表的茶饮",
        "ingredients": "金银花20g，绿茶6g，白糖50g。",
        "method": "将金银花和绿茶置于茶杯中，用150ml开水冲泡5~10分钟，放人白糖溶化即可。每日1次，连服2~3日。",
        "benefits": "辛凉解表、清热解毒",
        "suitable_for": "适用于预防外感风热有恶寒发热、口渴咽干等表现者。",
        "season": "",
        "keywords": ["风热", "清热解毒", "口渴"]
    },
    {
        "name": "菊花粥",
        "image": "",
        "description": "疏风清热的粥品",
        "ingredients": "菊花末10g，粳米50g，冰糖20g。",
        "method": "将干菊花去蒂、洗净、研末，粳米洗净，备用；将粳米、冰糖中加入清水500ml一同煮至米开汤未稠时，放入干菊花末，改用文火慢煮至粥稠停火，焖5分钟即可。每日2次，稍温服食。",
        "benefits": "疏风清热、清肝明目",
        "suitable_for": "适用于防治外感风热有头痛、目赤等表现者；肝经风热有目赤肿痛等表现者；也可用于健康人群用眼过度、眼睛干涩等。",
        "season": "",
        "keywords": ["风热", "明目", "头痛"]
    },
    {
        "name": "葛粉羹",
        "image": "",
        "description": "解肌生津的羹品",
        "ingredients": "葛根粉250g，菊花15g，淡豆豉150g，生姜9g，葱白9g，盐3g。",
        "method": "将葱白洗净、切丝，菊花、淡豆豉、生姜洗净，备用；将生姜、菊花、淡豆豉放入清水中，用文火煮20分钟后，去渣取汁；用武火将药汁煮沸，调入葛根粉，加入适量清水调至成芡汁，继续熬制至成熟，加盐调味，放入葱白即可。可早晚空腹随量服用。",
        "benefits": "解肌生津、除烦",
        "suitable_for": "适用于外感风热有口干、口渴、心烦等表现者的日常调理。",
        "season": "",
        "keywords": ["风热", "口干", "心烦"]
    },
    {
        "name": "五神汤",
        "image": "",
        "description": "发汗解表的汤品",
        "ingredients": "荆芥10g，苏叶10g，生姜10g，茶叶6g，红糖30g。",
        "method": "将生姜洗净、切丝，荆芥、苏叶洗净，备用；将荆芥、苏叶、生姜、茶叶一同放于文火上煮至沸腾后，加入红糖溶化即可。按需服用。",
        "benefits": "发汗解表",
        "suitable_for": "适用于风寒感冒者，常见恶寒、流涕、喷嚏、咳嗽等，也可作为寒冷环境下的御寒之品。",
        "season": "",
        "keywords": ["风寒", "感冒", "咳嗽"]
    },
    {
        "name": "生姜粥",
        "image": "",
        "description": "发汗解表的粥品",
        "ingredients": "生姜20g，粳米100g，葱白2根。",
        "method": "将生姜、葱白洗净、切丝，粳米洗净，备用；将粳米放于锅中，加入适当清水煮粥，粥将熟时，放入生姜、葱白，再煮沸一二次即可。每日1~2次，连服3~5日。",
        "benefits": "发汗解表、温胃止呕、温肺止咳",
        "suitable_for": "适用于风寒感冒、胃寒呕吐、肺寒咳嗽者，也可作预防感冒之用。",
        "season": "",
        "keywords": ["风寒", "呕吐", "咳嗽"]
    },
    {
        "name": "清爽茶",
        "image": "",
        "description": "清热祛湿解暑的茶饮",
        "ingredients": "干荷叶3g，鲜荷叶10g，生山楂5g，普洱茶2g。",
        "method": "将荷叶、山楂洗净、切丝，备用；将荷叶丝、山楂丝、普洱茶放入茶壶中用少量沸水冲洗摇晃数次后，迅速将沸水倒出以洗茶；再将沸水倒入茶壶中，盖上壶盖，浸泡10分钟后即可饮用。待茶水饮尽，加入沸水再次浸泡续饮即可。本品可服用1个月以上，如见效，可连续服用2~3个月或更长时间。",
        "benefits": "清热祛湿解暑",
        "suitable_for": "适用于盛夏酷暑燥热季节引起的不适，有头晕、头痛、发热、乏力等表现者，也可用于暑季健康人群的保健养生之用。",
        "season": "",
        "keywords": ["清热", "解暑", "头晕"]
    },
    {
        "name": "马齿苋绿豆粥",
        "image": "",
        "description": "清热解毒的粥品",
        "ingredients": "鲜马齿苋120g，绿豆60g。",
        "method": "将马齿苋、绿豆洗净，备用；将二者同煮成粥即可。每日分2次服用。",
        "benefits": "清热解毒、凉血止痢",
        "suitable_for": "适用于热毒壅盛，有腹泻、痢疾、肠痈、夏季暑热等表现者，少量服用也可用于健康人群湿热体质者。",
        "season": "",
        "keywords": ["清热", "解毒", "腹泻"]
    },
    {
        "name": "三鲜三花茶",
        "image": "",
        "description": "清热生津的茶饮",
        "ingredients": "鲜竹心、鲜荷梗、南沙参、绿豆各30g，丝瓜花、扁豆花各20朵，南瓜花5朵。",
        "method": "将各味食材洗净，备用；将绿豆、南沙参放入锅中加水同煮，煮至绿豆开花后，再加入其他食材煮约半小时，去渣取汁即可。每日代茶饮。",
        "benefits": "清热生津、祛暑",
        "suitable_for": "适用于有汗多、口渴、心烦溺黄、肢倦神疲等表现者饮用。",
        "season": "",
        "keywords": ["清热", "生津", "祛暑"]
    },
    {
        "name": "黄花菜饮",
        "image": "",
        "description": "清热止血的饮品",
        "ingredients": "黄花菜60g，藕60g，白茅根30g。",
        "method": "将黄花菜泡发、洗净，藕、白茅根洗净，备用；将洗净的黄花菜、藕、白茅根放入清水中煎汤即可。每日2次。",
        "benefits": "清热止血",
        "suitable_for": "适用于上消化道出血者，也可作为有胃热或肝火表现的健康人群的日常调护。",
        "season": "",
        "keywords": ["清热", "止血", "胃热"]
    },
    {
        "name": "秋梨白藕汁",
        "image": "",
        "description": "清热润肺的饮品",
        "ingredients": "秋梨500g，白藕500g。",
        "method": "将秋梨洗净、去皮及核、切碎，白藕洗净、去节、切碎，备用；将备好的秋梨、白藕包裹于纱布中，绞挤出汁即可。代茶饮。",
        "benefits": "清热润肺、止咳化痰",
        "suitable_for": "适用于肺热咳嗽、口燥咽干者，也可作为秋季燥咳者养生保健之用。",
        "season": "",
        "keywords": ["润肺", "止咳", "化痰"]
    },
    {
        "name": "菊槐绿茶饮",
        "image": "",
        "description": "疏风清热的茶饮",
        "ingredients": "菊花、槐花、绿茶各3g。",
        "method": "将槐花、菊花洗净，备用；将槐花、菊花、绿茶一同放入茶杯中，用沸水冲泡、加盖闷泡5分钟即可。代茶饮。",
        "benefits": "疏风清热、清肝明目",
        "suitable_for": "适用于肝火偏旺，有头痛、眩晕、目赤肿痛等表现者的日常调理。",
        "season": "",
        "keywords": ["清热", "明目", "头痛"]
    },
    {
        "name": "竹叶粥",
        "image": "",
        "description": "清热泻火的粥品",
        "ingredients": "竹叶15g，栀子10g，粳米100g，盐3g。",
        "method": "将竹叶、栀子、粳米洗净，备用；将竹叶、栀子水煎后，去渣取汁，再将粳米放入药汁中煮粥，粥熟，加盐调味即可。温服，每日1次，连服3~5日。",
        "benefits": "清热泻火解毒",
        "suitable_for": "适用于有口渴多饮、心烦、目赤、口舌生疮等表现者，也可用于急躁易怒人群的养生调护。",
        "season": "",
        "keywords": ["清热", "泻火", "口舌生疮"]
    },
    {
        "name": "五仁粥",
        "image": "",
        "description": "滋养肝肾的粥品",
        "ingredients": "黑芝麻10g，松子仁10g，核桃仁10g，桃仁（去皮、尖，炒）10g，甜杏仁10g,粳米200g。",
        "method": "将黑芝麻、松子仁、核桃仁、桃仁、甜杏仁混合碾碎，与淘洗干净的粳米一同入锅，加水2000ml，用武火烧开后转用文火熬煮成稀粥，食用时可调入适量白糖。每日早晚温服。",
        "benefits": "滋养肝肾、润燥滑肠",
        "suitable_for": "适用于中老年人及气血亏虚人群之习惯性便秘、排便无力及肠燥便秘等。",
        "season": "",
        "keywords": ["便秘", "润燥", "肝肾"]
    },
    {
        "name": "白胡椒炖猪肚",
        "image": "",
        "description": "温中暖胃的炖品",
        "ingredients": "白胡椒粒10g，猪肚500g，食盐适量。",
        "method": "将白胡椒粒在锅中微火煸炒至香味出，然后加水适量，再将猪肚清洗干净，切丝后放入锅内，文火炖1小时以上，至猪肚丝软烂，加食盐调味即可。不于时，可作日常食养保健。",
        "benefits": "温中暖胃、行气止痛",
        "suitable_for": "适用于脾胃虚寒人群，常见腹胀食少、腹痛而喜温喜按、口淡不渴、四肢发凉、大便稀溏，或四肢浮肿、怕冷喜暖、小便清长或不利等表现。正常人群亦可食用。",
        "season": "",
        "keywords": ["暖胃", "止痛", "脾胃虚寒"]
    },
    {
        "name": "茯苓粥",
        "image": "",
        "description": "利水消肿的粥品",
        "ingredients": "茯苓30g，粳米30g，大枣7枚。",
        "method": "先将茯苓研粉，备用。把梗米加适量水煮沸，然后放入红枣煮粥，粥成时再加入茯苓粉搅匀，稍煮即可。作早餐食用，或不拘时服食。",
        "benefits": "利水消肿、渗湿健脾、宁心安神",
        "suitable_for": "适用于湿热质和痰湿质人群，常见小便不利、水肿胀满、痰饮咳逆、呕啰、泄泻、遗精、淋浊、惊悸、健忘等表现。",
        "season": "",
        "keywords": ["消肿", "健脾", "安神"]
    },
    {
        "name": "杏仁粥",
        "image": "",
        "description": "降气化痰的粥品",
        "ingredients": "甜杏仁10g，粳米50g，冰糖或食盐适量。",
        "method": "将杏仁去皮尖，加水煮至软烂，取杏仁水煮粳米成粥，调入冰糖或食盐温热食，每日2次。",
        "benefits": "降气化痰、止咳平喘",
        "suitable_for": "适用于痰浊阻肺、肺气上逆所致之咳嗽气喘及脾胃不足、肠燥便秘者食用。",
        "season": "",
        "keywords": ["化痰", "止咳", "便秘"]
    },
    {
        "name": "二花调经茶",
        "image": "",
        "description": "活血祛瘀的茶饮",
        "ingredients": "玫瑰花、月季花各9g（鲜品各用18g)，红茶3g。",
        "method": "上三味研为粗末，置有盖的杯中，倒人沸水泡闷10分钟，不拘时温服。每日1剂，连服数日。尤于经前3~5日饮用，效果最佳。",
        "benefits": "活血祛瘀、理气止痛",
        "suitable_for": "适用于气滞血瘀证者日常保健饮用，常见表现为月经不调，月经或先期或后期，或先后不定期，月经量少，色黯或夹较多血块，精神抑郁，乳房胸胁胀痛，纳食减少。还可用于气滞血瘀型痛经。",
        "season": "",
        "keywords": ["调经", "痛经", "血瘀"]
    },
    {
        "name": "益母草煮鸡蛋",
        "image": "",
        "description": "活血调经的食疗方",
        "ingredients": "益母草30~60g，鸡蛋2枚。",
        "method": "鸡蛋洗净，与益母草加水同煮，待鸡蛋熟后剥去蛋壳，人益母草水中煮片刻，吃蛋饮汤。每日1剂，连服5~7日。",
        "benefits": "活血调经、养血益气、利水消肿",
        "suitable_for": "适用于气血瘀滞之月经不调、痛经、闭经、崩漏、产后恶露不行等，亦可作妇人产后调补之方。",
        "season": "",
        "keywords": ["调经", "痛经", "产后"]
    },
    {
        "name": "茯苓龙眼粥",
        "image": "",
        "description": "养心安神的粥品",
        "ingredients": "茯苓15g，龙眼肉20g，粳米100g，白糖或冰糖少许。",
        "method": "将茯苓、龙眼肉洗去浮灰备用。将粳米淘洗净，放入砂锅中，注入适量水，放入茯苓、龙眼肉，用文火煮至粥熟，可适当放入少许白糖或冰糖调味即成。",
        "benefits": "养心安神",
        "suitable_for": "适用于中老年人平素心血不足者保健食用，常见失眠多梦、心情烦躁、头晕心悸等。",
        "season": "",
        "keywords": ["安神", "失眠", "心悸"]
    },
    {
        "name": "甘麦大枣汤",
        "image": "",
        "description": "养心安神的汤品",
        "ingredients": "甘草10g，小麦20g，大枣3枚。",
        "method": "小麦用水清洗干净备用；大枣洗干净后用手掰开，或用刀切成两半。将小麦、甘草、大枣放在锅中，加水1000ml，武火煮开后调成文火煮炖20分钟即可。每日2次，早晚服用。",
        "benefits": "养心安神",
        "suitable_for": "适用于白天精神恍惚，夜晚烦躁难眠等，对更年期妇女心烦易怒、情绪波动大等也具有调养作用。",
        "season": "",
        "keywords": ["安神", "失眠", "更年期"]
    },
    {
        "name": "海带绿豆粥",
        "image": "",
        "description": "清热利尿的粥品",
        "ingredients": "海带50g，绿豆60g，粳米100g。",
        "method": "海带清洗干净，切碎；绿豆充分浸泡，与粳米一同加水熬煮30分钟，放入海带再熬煮15分钟即可。每日1次。",
        "benefits": "清热利尿、化痰醒神",
        "suitable_for": "适用于血压偏高的中老年人群，常见视物模糊、头晕眼胀、心情烦躁。亦可作为易怒、情绪波动较大等亚健康或健康人群日常食养保健。",
        "season": "",
        "keywords": ["清热", "利尿", "降压"]
    },
    {
        "name": "健脾益气粥",
        "image": "",
        "description": "健脾益气的粥品",
        "ingredients": "生黄芪10g，党参10g，茯苓6g，炒白术6g，薏苡仁10g，大米200g，大枣20g。",
        "method": "将生黄芪、炒白术装入纱布包内，放入锅中，加3000ml清水浸泡40分钟备用；将党参、茯苓蒸软后切成颗粒状备用；将薏苡仁浸泡回软后，放入锅中煎30分钟备用。大米、大枣放入浸泡药材包及薏苡仁煮后的锅中，武火煮开改文火熬煮2小时，取出纱布包，放入党参、茯苓即可。",
        "benefits": "健脾益气",
        "suitable_for": "适用于脾气亏虚之各类人群，常见平素痰多、倦怠乏力、食少便溏等。亦可用于亚健康或健康人群日常食养保健。",
        "season": "",
        "keywords": ["健脾", "益气", "乏力"]
    },
    {
        "name": "甘麦大枣羹",
        "image": "",
        "description": "补气养血的羹品",
        "ingredients": "大枣（去核）60g，百合100g，甘草10g，鸡蛋10个，淮小麦500g。",
        "method": "将甘草洗净，煎取汁液备用；小麦洗净，大枣洗净，切成小块，百合洗净后切碎，鸡蛋破壳人碗打匀备用。将甘草汁煮沸加入小麦、大枣及百合同煮约30分钟，倒入鸡蛋液，煮沸搅匀即可。",
        "benefits": "补气、养血、安神",
        "suitable_for": "适用于情志不调的人群，常见烦躁易怒、失眠、焦虑、乏力等。亦可用于亚健康或健康人群日常食养保健。",
        "season": "",
        "keywords": ["补气", "养血", "安神"]
    },
    {
        "name": "川芎红花茶",
        "image": "",
        "description": "活气行血的茶饮",
        "ingredients": "川芎、红花、茶叶各3克。",
        "method": "共同水煎取汁。",
        "benefits": "活气行血，化瘀止痛",
        "suitable_for": "本方适用于瘀血所致的头刺痛、夜晚尤甚。",
        "season": "",
        "keywords": ["化瘀", "止痛", "头痛"]
    },
    {
        "name": "石决明粥",
        "image": "",
        "description": "清火平肝的粥品",
        "ingredients": "石决明30克、粳米100克",
        "method": "石决明择净，放入清水适量的浸泡五到十分钟，煎取汁，加粳米煮为稀粥。",
        "benefits": "清火平肝，潜阳熄风",
        "suitable_for": "本方对肝阳上亢所致的眩晕头痛，烦躁易怒，目赤肿痛，口苦耳鸣，肢麻震颤甚为有效。",
        "season": "",
        "keywords": ["平肝", "眩晕", "头痛"]
    },
    {
        "name": "生姜葱白粥",
        "image": "",
        "description": "辛温解表的粥品",
        "ingredients": "糯米50克，生姜五克，葱白30克，米醋20毫升。",
        "method": "糯米洗净，加入适量水与生姜同煮，煮开后加入葱白，待粥成后加入米醋，搅匀起锅。",
        "benefits": "辛温解表，散寒宣肺",
        "suitable_for": "风寒感冒导致咳嗽的患者。",
        "season": "",
        "keywords": ["风寒", "感冒", "咳嗽"]
    },
    {
        "name": "橘皮茶",
        "image": "",
        "description": "温肺化痰的茶饮",
        "ingredients": "橘子十个，紫苏叶十克，冰糖少许。",
        "method": "橘子刷洗干净、剥皮。将橘皮放在阳光下通风处曝晒2~3天，水分完全蒸发晒干至可折断的程度。将晒干的橘皮放入铁锅中炒10分钟，放凉，再放入密封容器中即可长期保存。每次取橘皮10克，以开水200毫升泡软后，加入紫苏叶浸泡15分钟，加入冰糖调味。",
        "benefits": "温肺化痰，理气止咳",
        "suitable_for": "脾虚痰湿体质者，此外，对于平素体胖痰多、乏力困倦、食欲不振、大便偏稀、腹中胀满者平素常饮，也可达到理气健脾、燥湿化痰的目的。",
        "season": "",
        "keywords": ["化痰", "止咳", "痰湿"]
    },
    {
        "name": "冰糖雪梨",
        "image": "",
        "description": "生津滋肺的甜品",
        "ingredients": "雪梨100克、冰糖30~60克、白萝卜100克。",
        "method": "将带皮雪梨洗净去核，白萝卜去皮、切块，与冰糖一起置瓷杯内或放碗内，置蒸锅内，隔水蒸至冰糖溶化。",
        "benefits": "生津滋肺，润燥止咳",
        "suitable_for": "患者患风燥伤肺导致的以干燥表现为主，兼有感冒症状的咳嗽效果甚好。",
        "season": "",
        "keywords": ["润肺", "止咳", "干燥"]
    },
    {
        "name": "桑叶杏仁梨皮粥",
        "image": "",
        "description": "滋阴清热的粥品",
        "ingredients": "桑叶10克、杏仁10克、粳米50克、雪梨100克、冰糖少许。",
        "method": "将带皮雪梨洗净去核，白萝卜去皮、切块，与冰糖一起置瓷杯内或放碗内，置蒸锅内，隔水蒸至冰糖溶化。",
        "benefits": "滋阴清热，润肺止咳",
        "suitable_for": "用于口舌咽干、干咳少痰者。能使燥热除而肺津复，而诸症自愈。",
        "season": "",
        "keywords": ["滋阴", "清热", "干咳"]
    },
    {
        "name": "萝卜蜜汤",
        "image": "",
        "description": "清热降气的汤品",
        "ingredients": "白萝卜汁250毫升，蜂蜜30毫升。",
        "method": "两汁混匀后一同煎煮5分钟。",
        "benefits": "清热降气，化痰止咳",
        "suitable_for": "用于痰热之咳哮者。",
        "season": "",
        "keywords": ["清热", "化痰", "咳嗽"]
    },
    {
        "name": "珠玉二宝粥",
        "image": "",
        "description": "益气养阴的粥品",
        "ingredients": "山药50克、薏苡仁50克、柿霜饼25克。",
        "method": "山药、薏苡仁打碎煮烂成粥，然后将柿霜饼切成小块，加入其中再煮10分钟即可。",
        "benefits": "益气养阴，补脾益肺",
        "suitable_for": "适用于一切肺脾气（阴）亏虚之疾病。",
        "season": "",
        "keywords": ["益气", "养阴", "补脾"]
    },
    {
        "name": "霍香粥",
        "image": "",
        "description": "醒脾和胃的粥品",
        "ingredients": "粳米100克、藿香25克、白砂糖10克。",
        "method": "鲜藿香清水洗净，煎汁去渣，待用。锅中加入适量的清水，放入已洗净的粳米熬粥，粥熟后入藿香汁，再煮沸，放入白糖调味搅匀即成。",
        "benefits": "醒脾和胃，化湿止呕",
        "suitable_for": "恶心呕吐。",
        "season": "",
        "keywords": ["和胃", "止呕", "化湿"]
    },
    {
        "name": "葛根枳棋子饮",
        "image": "",
        "description": "发表散邪的饮品",
        "ingredients": "葛根20g，葛花10g，枳棋子15g。",
        "method": "水煎2次，取汁600~800ml，于2小时内分3~5次饮服。",
        "benefits": "发表散邪，清热除烦",
        "suitable_for": "适用于急性酒精中毒所致的头痛头晕，烦热口渴等症。",
        "season": "",
        "keywords": ["解酒", "头痛", "烦热"]
    },
    {
        "name": "橘味醒酒羹",
        "image": "",
        "description": "解酒和中的羹品",
        "ingredients": "糖水橘子250g，冰糖莲子250g，青梅25g，红枣50g，白糖300g，白醋30ml，桂花少许。",
        "method": "青梅切丁，红枣洗净去核，置小碗中加水蒸熟。糖水橘子、莲子倒入铝锅或不锈钢锅中，再加入青梅、红枣、白糖、白醋、桂花、清水，煮开，晾凉后频频食用。",
        "benefits": "解酒和中除暖，清热生津止渴",
        "suitable_for": "适用于醉酒所致的暖气呕逆、吞酸嘈杂、不思饮食等症。",
        "season": "",
        "keywords": ["解酒", "呕逆", "生津"]
    },
    {
        "name": "健脾消食蛋羹",
        "image": "",
        "description": "补脾益气的蛋羹",
        "ingredients": "山药15g，茯苓15g，莲子15g，山楂20g，麦芽15g，鸡内金30g，槟榔15g,鸡蛋若干枚，食盐，酱油适量。",
        "method": "上述药物除鸡蛋外共研为末，每次5g，加鸡蛋1枚调匀蒸熟，加适量食盐或酱油调味后直接食用，每日1~2次。",
        "benefits": "补脾益气，消食开胃",
        "suitable_for": "适用于脾胃虚弱，食积内停之证，症见纳食减少，脘腹胀满，暖腐吞酸，大便溏泻，脉象虚弱等。",
        "season": "",
        "keywords": ["健脾", "消食", "开胃"]
    },
    {
        "name": "白术猪肚粥",
        "image": "",
        "description": "健脾消食的粥品",
        "ingredients": "白术30g，槟榔10g，生姜10g，猪肚1副，粳米100g，葱白3茎，食盐适量。",
        "method": "前3味药装入纱布包内扎口，猪肚洗净，将药放入猪肚中缝口，用水适量煮猪肚令熟，取汁。以其汁煮米粥，即将熟时人葱白及食盐调味，空腹食用。",
        "benefits": "健脾消食，理气导滞",
        "suitable_for": "适用于脾虚气滞型脘腹胀满，纳差纳呆者。",
        "season": "",
        "keywords": ["健脾", "消食", "腹胀"]
    },
    {
        "name": "小儿七星茶",
        "image": "",
        "description": "健脾益胃的茶饮",
        "ingredients": "薏苡仁15g，甘草4g，山楂10g，生麦芽15g，淡竹叶10g，钩藤10g，蝉蜕4g。",
        "method": "上药共为粗末，水煎代茶饮用。",
        "benefits": "健脾益胃，消食导滞，安神定志",
        "suitable_for": "适用于小儿脾虚伤食或疳积证，症见纳差腹胀，吐奶或呕吐，大便稀溏，或面黄肌瘦，厌食，大便时干时稀，多汗易惊，睡卧不安，手足心热等。",
        "season": "",
        "keywords": ["健脾", "消食", "安神"]
    },
    {
        "name": "益脾饼",
        "image": "",
        "description": "健脾益气的饼品",
        "ingredients": "白术30g，红枣250g，干姜6g，鸡内金50g，食盐适量。",
        "method": "白术、干姜入纱布袋内，扎紧袋口，入锅，下红枣、加水1000ml，武火煮沸，改用文火熬1小时，去药袋，红枣去核，枣肉捣泥。鸡内金研为细末，与面粉混匀，倒人枣泥，加面粉与少量食盐和成面团，将面团再分成若干个小面团、制成薄饼。平底锅内倒少量菜油，放入面饼烙熟即可，空腹食用。",
        "benefits": "健脾益气，温中散寒，开胃消食",
        "suitable_for": "主治牌胃寒湿所致纳食减少，大便溏泻等症。",
        "season": "",
        "keywords": ["健脾", "温中", "消食"]
    },
    {
        "name": "萝卜饼",
        "image": "",
        "description": "健胃理气的饼品",
        "ingredients": "白萝卜250g，面粉250g，精猪肉100g，葱、姜、盐、香油各适量。",
        "method": "将萝卜洗净，切成细丝，放入油锅内，煸炒至五成熟时盛起备用。猪肉剁细，加入葱、姜、盐、油等调料，与白萝卜丝一起调成馅心。面粉清水适量，揉成面团，软硬程度与饺子皮相同，然后分成50g一个的小面团，擀成薄片，当中放白萝卜馅心，制成夹心小饼，将饼放入锅内烙熟即成。每日适量空腹食用。",
        "benefits": "健胃理气，消食化痰",
        "suitable_for": "主治老年人食欲不振，消化不良，食后腹胀及喘咳痰多等症。",
        "season": "",
        "keywords": ["健胃", "消食", "化痰"]
    },
    {
        "name": "期颐饼",
        "image": "",
        "description": "健脾消食的饼品",
        "ingredients": "生芡实180g，鸡内金90g，面粉250g，白糖适量。",
        "method": "将鸡内金洗净粉碎过筛，并用开水浸泡半日，再加入粉碎过筛的芡实粉及面粉、白糖，混匀，制成极薄小饼，烙成焦黄色，随意食之。",
        "benefits": "健脾消食，除湿化痰",
        "suitable_for": "主治脾虚食滞，痰湿郁积，症见食纳不佳，消化不良，胸脘满闷，大便稀溏，咳嗽痰多者。",
        "season": "",
        "keywords": ["健脾", "消食", "化痰"]
    },
    {
        "name": "健脾消积饼",
        "image": "",
        "description": "补脾益气的饼品",
        "ingredients": "山药15g，麦芽15g，茯苓15g，山楂20g，莲肉15g，鸡内金30g，槟榔15g,面粉适量，食盐及白膏适量。",
        "method": "上药共研细末，每次5g，与适量面粉混匀，烙成小饼食用。每日2次。",
        "benefits": "补脾益气，消积开胃",
        "suitable_for": "主治小儿疳积，脾胃虚弱，症见食少难消，腹胀便溏，面黄消瘦等症。",
        "season": "",
        "keywords": ["健脾", "消积", "开胃"]
    },
    {
        "name": "山楂麦芽茶",
        "image": "",
        "description": "消食化滞的茶饮",
        "ingredients": "山楂10g，生麦芽10g。",
        "method": "山楂洗净，切片，与麦芽同置杯中，加盖泡30分钟，代茶饮用。",
        "benefits": "消食化滞",
        "suitable_for": "适用于伤食、食积证，或大病初愈，胃弱纳差的病证。",
        "season": "",
        "keywords": ["消食", "化滞", "开胃"]
    },
    {
        "name": "甘露茶",
        "image": "",
        "description": "消食开胃的茶饮",
        "ingredients": "炒山楂24g，生谷芽30g，麸炒神曲45g，炒枳壳24g，姜炙厚朴24g，橘皮120g，陈茶叶90g。",
        "method": "上药干燥，共制为末，和匀过筛，分袋包装，每袋9g。每日1~2次，每次1袋，开水冲泡，代茶温饮。",
        "benefits": "消食开胃，行气导滞",
        "suitable_for": "适用于伤食，食积气滞证。",
        "season": "",
        "keywords": ["消食", "开胃", "行气"]
    },
    {
        "name": "荸荠内金饼",
        "image": "",
        "description": "开胃消食的饼品",
        "ingredients": "荸荠600g，鸡内金25g，天花粉20g，玫瑰20g，白糖150g，菜油、面粉、糯米粉适量。",
        "method": "将鸡内金制成粉末，加人天花粉、玫瑰、白糖、熟猪油60g，面粉10g拌匀做成饼馅。荸荠去皮洗净，用刀拍烂，剁成细泥，加入糯米100g拌匀上蒸笼蒸熟。趁热把刚蒸熟的荸荠糯米泥分成汤圆大小，逐个包入饼馅，压成扁圆形，撒上细干淀粉备用。炒锅置旺火上，倒入菜油烧至八成热，把包入饼馅的荸荠饼下入油锅内炸至金黄色，用漏勺捞起入盘，撒上白糖即可当点心直接食用。",
        "benefits": "开胃消食，清热止渴",
        "suitable_for": "主治胸中烦热口渴，脘腹痞闷，恶心厌食，纳食减少，苔黄腻，脉滑数等症。",
        "season": "",
        "keywords": ["开胃", "消食", "清热"]
    },
    {
        "name": "牛乳饼",
        "image": "",
        "description": "补虚损的饼品",
        "ingredients": "牛乳50g，面粉250g，白糖30g，素油250g。",
        "method": "将面粉与白糖、牛乳及适量清水拌匀，揉成面团，擀成直径3cm，厚2cm的薄饼，放入油锅中煎炸，以两面金黄为度。每日早晚食用，佐粳米粥更佳。",
        "benefits": "补虚损，益牌胃",
        "suitable_for": "主治虚弱劳损，反胃噎膈，消渴便秘等症。",
        "season": "",
        "keywords": ["补虚", "益胃", "便秘"]
    },
    {
        "name": "神曲丁香茶",
        "image": "",
        "description": "温中健胃的茶饮",
        "ingredients": "神曲15g，丁香15g。",
        "method": "上两药放入茶杯中，沸水冲泡，代茶饮用。",
        "benefits": "温中健胃，消食导滞",
        "suitable_for": "适用于胃寒食滞而纳呆，胃脘饱胀，呕吐呃逆症。",
        "season": "",
        "keywords": ["温中", "健胃", "消食"]
    },
    {
        "name": "磁石粥",
        "image": "",
        "description": "重镇安神的粥品",
        "ingredients": "磁石30g，粳米100g，生姜、大葱各适量，或加猪腰子，去内膜，洗净切细。",
        "method": "先将磁石捣碎，于砂锅内煎煮1小时，滤汁去渣，再加入粳米、生姜、大葱，同煮为粥。供晚餐食用，温热服。",
        "benefits": "重镇安神",
        "suitable_for": "适用于心神不安引起的心烦失眠、心慌、惊悸、神志不宁、头晕头痛等。",
        "season": "",
        "keywords": ["安神", "失眠", "惊悸"]
    },
    {
        "name": "百合粥",
        "image": "",
        "description": "宁心安神的粥品",
        "ingredients": "百合30g，或干百合粉20g，糯米50g，冰糖适量。",
        "method": "将百合剥皮，去须，切碎，与洗净的糯米同入砂锅中，加水适量，煮至米烂汤稠，加入冰糖即成，温热服用。",
        "benefits": "宁心安神，润肺止咳",
        "suitable_for": "适用于热病后期余热未清引起的精神恍惚，心神不安，以及妇女更年期综合征等；亦可用于肺燥引起的咳嗽、痰中带血等病症。",
        "season": "",
        "keywords": ["安神", "润肺", "咳嗽"]
    },
    {
        "name": "酸枣仁粥",
        "image": "",
        "description": "养心安神的粥品",
        "ingredients": "酸枣仁10g，熟地10g，粳米100g。",
        "method": "将酸枣仁放入砂锅内，用文火炒至外皮鼓起并呈微黄色，取出，放凉，捣碎，与熟地共煎，取汁待用。将粳米淘洗干净，加水适量煮至粥稠时，加入药汁，再煮3~5分钟即可食用，温热服。",
        "benefits": "养心安神",
        "suitable_for": "适用于心肝血虚引起的心悸、心烦、失眠、多梦等症。",
        "season": "",
        "keywords": ["安神", "失眠", "心悸"]
    },
    {
        "name": "柏子仁粥",
        "image": "",
        "description": "养心安神的粥品",
        "ingredients": "柏子仁15g，粳米100g，蜂蜜适量。",
        "method": "将柏子仁去皮、壳、杂质，捣烂，同粳米一起放人锅内，加水适量用慢火煮至粥稠时，加入蜂蜜，搅拌均匀即可食用。温热服。",
        "benefits": "养心安神，润肠通便",
        "suitable_for": "适用于心血不足引起的虚烦不眠，惊悸怔忡，健忘，以及习惯性便秘，老年性便秘等。另外，对血虚脱发亦有一定的治疗效果。",
        "season": "",
        "keywords": ["安神", "便秘", "健忘"]
    },
    {
        "name": "甘麦大枣汤",
        "image": "",
        "description": "养心安神的汤品",
        "ingredients": "甘草20g，小麦100g，大枣10枚。",
        "method": "将甘草放入砂锅内，加清水500g，大火烧开，小火煎至剩200g，去渣，取汁，备用。将大枣洗净，去杂质，同小麦一起放入锅内，加水适量，用文火煮至麦熟时加入甘草汁，再煮沸后即食用，空腹温热服。",
        "benefits": "养心安神，和中缓急",
        "suitable_for": "适用于心气虚所引起的心神不宁，精神恍惚，失眠等。",
        "season": "",
        "keywords": ["安神", "失眠", "心气虚"]
    },
    {
        "name": "玉竹卤猪心",
        "image": "",
        "description": "补心宁神的卤品",
        "ingredients": "玉竹50g，猪心1个，葱、姜、盐、花椒、白糖、味精、麻油、卤汁各适量。",
        "method": "先煎玉竹2次，合并滤液，猪心剖开洗净血水后，与葱、姜、花椒等共入药汁中，置砂锅内，武火煮开后，文火煮至猪心六成熟，捞出晾干。再将猪心置卤汁中，文火煮熟，捞出切片，稍加调料即成，佐餐食用。",
        "benefits": "补心宁神，养阴生津",
        "suitable_for": "适用于心阴不足引起的心悸、心烦、心神不宁、多梦失眠等。",
        "season": "",
        "keywords": ["安神", "心悸", "失眠"]
    },
    {
        "name": "龙眼纸包鸡",
        "image": "",
        "description": "养心安神的菜肴",
        "ingredients": "龙眼肉20g，胡桃肉100g，嫩鸡肉400g，鸡蛋2个，胡荽100g，火腿20g.食盐6g，砂糖6g，味精2g，淀粉25g，麻油5g，花生油150g，生姜5g，葱20g，胡椒粉3g。",
        "method": "胡桃肉去皮后入油锅炸熟，切成细粒；龙眼肉切成粒，待用。鸡肉切成片，用盐、味精、胡椒粉调拌腌渍，再用淀粉加清水调湿后与蛋清调成糊。取玻璃纸摊平，鸡肉片上浆后摆在纸上，加少许胡椒、姜、葱片、火腿、胡桃仁、龙眼肉，然后折成长方形纸包；炒锅置火上，入花生油，加热至六成熟时，把包好的鸡肉下锅炸熟，捞出装盘即成，作为菜肴食用。",
        "benefits": "养心安神，健脾益气",
        "suitable_for": "适用于气血两虚引起的心悸、失眠、健忘、病后体虚、食少乏力、眩晕、面色无华等。",
        "season": "",
        "keywords": ["安神", "失眠", "健忘"]
    },
    {
        "name": "人参炖乌骨鸡",
        "image": "",
        "description": "养阴安神的炖品",
        "ingredients": "乌骨鸡2只，人参100g，母鸡1只，猪肘500g，味精、料酒、味精、葱、姜、胡椒各适量。",
        "method": "将乌骨鸡宰杀，去毛，去爪，去头，去内脏；将腿插在肚子里，出水。将人参用温水洗净，并将猪肘刮洗干净，出水；把葱切成段，姜切成片备用。将大砂锅置旺火上，加足量清水，放入母鸡、猪肘、葱段、姜片，沸后掠去浮沫，移小火上慢炖，炖至母鸡和猪肘五成烂时，将乌骨鸡和人参加入同炖，用精盐、料酒、味精、胡椒粉调好味，炖至鸡酥烂即可，可作菜肴食用。",
        "benefits": "养阴安神，清热除烦",
        "suitable_for": "适用于阴虚内热引起的虚烦少寐，心悸神疲，无心烦热等症。",
        "season": "",
        "keywords": ["安神", "阴虚", "心悸"]
    },
    {
        "name": "枣泥锅饼",
        "image": "",
        "description": "健脾益气的饼品",
        "ingredients": "红枣500g，芝麻油100g，白糖250g，面粉1000g，鸡蛋4个。",
        "method": "红枣去核后水浸2小时，再上蒸笼蒸至枣肉软烂，去枣皮制成枣泥；将白糖放入油锅中翻炒，与面粉、鸡蛋一起拌成糊状，摊成薄饼，微火烙烤，然后将枣泥放饼中间，包折成方形薄饼，再人油锅两面煎黄即成。经常适量食用。",
        "benefits": "健脾益气，养心补血",
        "suitable_for": "主治气血两虚，脾胃受损，食少体倦，少气懒言，心悸健忘等症。",
        "season": "",
        "keywords": ["健脾", "补血", "心悸"]
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
                try:
                    st.image(recipe['image'], caption=recipe['name'], use_column_width=True)
                except:
                    st.image("https://via.placeholder.com/300x200/4CAF50/white?text=食谱图片", 
                            caption=recipe['name'], use_column_width=True)
            
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
