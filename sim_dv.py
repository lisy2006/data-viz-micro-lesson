import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

# ========== 页面基础配置：宽屏+深色主题 ==========
st.set_page_config(page_title="数据可视化——动态柱状图与折线图交互仿真", layout="wide")
plt.style.use('dark_background')
# 顶部标题栏（和截图标题样式一致）
st.markdown("""
<div style="display:flex;align-items:center;margin-bottom:15px;">
<span style="background-color:#348ede;color:white;padding:4px 8px;border-radius:6px;margin-right:8px;font-weight:bold;">DV</span>
<h3 style="margin:0;color:white;">数据可视化 —— 动态柱状图与折线图 交互仿真</h3>
<span style="margin-left:15px;background-color:#1f2940;color:#8cf;padding:4px 10px;border-radius:12px;font-size:12px;">Streamlit 实时仿真</span>
<span style="margin-left:auto;color:#4cd964;">● 实时刷新</span>
</div>
""", unsafe_allow_html=True)


# 三栏布局：左控制面板｜中间图表｜右侧AI+标签要点
col_left, col_mid, col_right = st.columns([2,4,2])

# ========== 左侧：控制面板 月度营收滑块 + 智能预警【min=-50，可输入负数演示报错】 ==========
with col_left:
    st.subheader("控制面板 · 月度营收（万元）")
    m1 = st.slider("1月", min_value=-50, max_value=300, value=120)
    m2 = st.slider("2月", min_value=-50, max_value=300, value=150)
    m3 = st.slider("3月", min_value=-50, max_value=300, value=135)
    m4 = st.slider("4月", min_value=-50, max_value=300, value=170)
    m5 = st.slider("5月", min_value=-50, max_value=300, value=160)
    m6 = st.slider("6月", min_value=-50, max_value=300, value=145)
    st.caption("提示：拖动滑块修改数据，右侧图表毫秒级刷新；数值异常时系统自动预警。")

    # 智能预警逻辑
    revenue_list = [m1,m2,m3,m4,m5,m6]
    warn_flag = False
    error_flag = False
    warn_msg = ""
    for idx, val in enumerate(revenue_list):
        month_name = f"{idx+1}月"
        if val < 0:
            error_flag = True
            warn_msg += f"{month_name}营收负数！"
        elif val > 250:
            warn_flag = True
            warn_msg += f"{month_name}营收过高({val}) "
    if error_flag:
        st.error(f"数据异常：{warn_msg}营收不能为负数！", icon="🚨")
    elif warn_flag:
        st.warning(f"预警提醒：{warn_msg}超出常规营收区间！", icon="⚠️")
    else:
        st.success("数据正常", icon="✅")


# 构造数据集
months = ["1月","2月","3月","4月","5月","6月"]
revenue = [m1,m2,m3,m4,m5,m6]
df = pd.DataFrame({"月份":months, "营收":revenue})

# ========== 中间区域：柱状图 + 折线图 ==========
with col_mid:
    # 柱状图
    fig_bar = px.bar(df, x="月份", y="营收", title="柱状图｜分类对比：比大小看差异", color_discrete_sequence=["#4285F4"])
    fig_bar.update_layout(height=320, paper_bgcolor="#0E1117", plot_bgcolor="#0E1117", font_color="#eee")
    st.plotly_chart(fig_bar, use_container_width=True)

    # 折线图
    fig_line = px.line(df, x="月份", y="营收", title="折线图｜时间趋势：看趋势找规律", color_discrete_sequence=["#a28bff"])
    fig_line.update_layout(height=320, paper_bgcolor="#0E1117", plot_bgcolor="#0E1117", font_color="#eee")
    st.plotly_chart(fig_line, use_container_width=True)

# ========== 右侧区域：AI数字人 + 切换标签卡片 ==========
with col_right:
    try:
        st.image("ai_teacher.png", use_container_width=True)
        st.markdown("<p style='color:#ddd;font-size:13px;text-align:center;margin:4px 0 12px 0'>AI数字人讲师 · 数据可视化</p>", unsafe_allow_html=True)

        # 标签页，点击切换内容
        tab1, tab2, tab3, tab4 = st.tabs(["片头导入","仿真交互演示","核心知识点","随堂自测"])

        with tab1:
            st.markdown("#### 本节要点")
            st.markdown("""
            - 真实案例：企业月度营收
            - 沉浸式数据可视化
            - 先甄别数据，再可视化
            """)

        with tab2:
            st.markdown("#### 本节要点")
            st.markdown("""
            - 拖动滑块修改数据
            - 图表毫秒级实时刷新
            - 智能预警：过高/负数异常检测
            """)

        with tab3:
            st.markdown("#### 本节要点")
            st.markdown("""
            - 柱状图 → 分类对比
            - 折线图 → 时间趋势
            - 易错点：只会画图、不会选图
            """)

        with tab4:
            st.markdown("#### 随堂自测")
            q = "观察一年销售额随月份的变化趋势，应选择哪种图表？"
            optA = "A.柱状图"
            optB = "B.折线图"
            optC = "C.饼图"
            optD = "D.散点图"
            answer = st.radio(q, [optA,optB,optC,optD])
            if st.button("提交答案"):
                if answer == optB:
                    st.success("回答正确！折线图适合展示时间序列连续变化趋势，柱状图侧重类别数值对比。")
                else:
                    st.error("回答错误，正确答案：B 折线图。折线图用于展现随时间变化的波动趋势。")

    except:
        st.warning("图片缺失(ai_teacher.png)")

# 底部结束语
st.markdown("<div style='text-align:center;font-size:18px;margin-top:30px'>以上就是本节课的全部内容，谢谢观看！</div>", unsafe_allow_html=True)
