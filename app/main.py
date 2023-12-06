import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.io as pio # Plotly input output
import plotly.express as px # 빠르게 그리는 방법
import plotly.graph_objects as go # 디테일한 설정
import plotly.figure_factory as ff # 템플릿 불러오기
from plotly.subplots import make_subplots # subplot 만들기
from plotly.validators.scatter.marker import SymbolValidator # Symbol 꾸미기에 사용됨
import matplotlib.pyplot as plt  # 그래프 그리는 용도
import matplotlib.font_manager as fm  # 폰트 관련 용도
import seaborn as sns
import math
import streamlit as st
import datetime
import io
import plotly.figure_factory as ff

st.header('서울시 공연장 관련 통계 분석 및 시각화', divider='rainbow')

# 기본 csv파일
data = pd.read_csv('./culture_space.csv', 
                   encoding="utf-8" )
data.replace('-', 0, inplace = True)
data_og = data.copy() # 원본 저장

df = data.transpose()
df.rename(columns=df.iloc[0], inplace=True)
df = df.drop(df.index[0])
newdf = df.reset_index()
newdf['index'] = newdf['index'].apply(lambda x : float(x))
newdf['index'] = newdf['index'].apply(lambda x : math.floor(x))

# 데이터 설명
for_prac = data_og.copy()

# 1번
연도 = ["2013","2014","2015","2016","2017","2018","2019","2020","2021","2022"]
연도 = pd.DataFrame(연도)
서울 = [304, 344, 381, 389, 397, 408, 412, 417, 421, 436]
서울 = pd.DataFrame(서울)
dat = pd.concat([연도,서울], axis = 1)
dat.columns = ["연도","서울"]

# 2번, 3번 
newdf2 = newdf[(newdf['자치구']=='공공공연장') 
              | (newdf['자치구']=='민간공연장')]
newdf2 = newdf2.loc[:,["index", "자치구", "서울"]]

newdf = newdf[(newdf['자치구']=='대공연장(1000석 이상)') 
              | (newdf['자치구']=='일반공연장(300~999석)') 
              | (newdf['자치구']=='소공연장(300석 미만)')]
newdf = newdf.loc[:,['index', '자치구', '서울']]

# 4번



# 사이드 바
moccha = st.sidebar.selectbox(
    '목차를 선택해주세요',

    ('데이터 설명',
     '그래프'))

if moccha == '그래프':
    option = st.sidebar.selectbox(
        '그래프를 선택해주세요',

        ('서울시 공연장 증감 추이', 
        '서울시 공연장 종류에 따른 수 차이', 
        '서울시 공연장 규모에 따른 수 차이', 
        '구 별 지도'))

accept = st.sidebar.button("확인")

# 사이드 바 확인 버튼 누르면 실행
if moccha == '그래프' and accept:
    if option == '서울시 공연장 증감 추이':
        fig = px.line(dat, x="연도", y="서울", line_shape="linear", line_group=None, color_discrete_sequence=["blue"])
        fig.update_layout(
            title='서울시 연도별 공연장 수 추이',
            xaxis_title='연도',
            yaxis_title='공연장 수',
        )
        st.write(fig)
        st.divider()

    elif option == '서울시 공연장 종류에 따른 수 차이':
        fig2 =px.bar(newdf,
                x="자치구",
                y="서울",
                facet_col='index',
                color='자치구',
                text = "서울",
                labels={'index':'y', '서울':'공연장 수', '자치구':''},
                title='서울시 공연장 종류에 따른 수 차이')
        st.write(fig2)
        st.divider()

    elif option == '서울시 공연장 규모에 따른 수 차이':
        fig = px.bar(newdf,
              x="자치구",
              y="서울",
              title='서울시 공연장 규모에 따른 수 차이',
              hover_data=['서울'],
              color = '자치구',
             facet_col = 'index',
              labels={'index':'y', '서울':'공연장 수', '자치구':''},
             text = '서울' )
        st.write(fig)
        st.divider()

    else:
        

        st.divider()
elif moccha == '데이터 설명' and accept:
    st.subheader('데이터 설명')
    st.write(for_prac)
    st.divider()
    data_explain = """
    1. "-" 로 되어있는 값은 공연장이 없는 곳이라고 생각하고 0으로 처리하여 사용했습니다. 위에 데이터는 0으로 처리한 후의 데이터 입니다.
    2. 2013년 2022년까지 서울시 공연장 수에 대한 데이터입니다.
    3. 서울 전체의 공연장 수와 각 구의 공연장 수에 대한 데이터로 이루어져 있습니다.
    4. 연도별로 서울시 공연장 수를 공연장의 종류와 규모로 나누어서 볼 수 있습니다.
    5. 공연장의 종류로는 공공 공연장과 민간 공영장이 있습니다.
    6. 공연장의 규모로는 '대(1000석이상), 일반(300~999석), 소(300석미만)'가 있습니다.
    """
    st.markdown(data_explain)

    st.subheader('데이터 출처')
    st.write('https://data.seoul.go.kr/dataList/164/S/2/datasetView.do?stcSrl=164')
else:
    st.write('좌측 사이드바에서 보고 싶은 항목을 선택해주세요 :sunglasses:')