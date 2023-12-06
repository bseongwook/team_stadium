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

st.header('서울시 공연장 관련 통계 분석 및 시각화')

# 기본 csv파일
data = pd.read_csv('./culture_space.csv', 
                   encoding="utf-8" )
data.replace('-', 0, inplace = True)
data_og = data.copy() # 원본 저장

# 1번
연도 = ["2013","2014","2015","2016","2017","2018","2019","2020","2021","2022"]
연도 = pd.DataFrame(연도)
서울 = [304, 344, 381, 389, 397, 408, 412, 417, 421, 436]
서울 = pd.DataFrame(서울)
dat = pd.concat([연도,서울], axis = 1)
dat.columns = ["연도","서울"]

# 2번, 3번 
df = data.transpose()
df.rename(columns=df.iloc[0], inplace=True)
df = df.drop(df.index[0])
newdf = df.reset_index()
newdf['index'] = newdf['index'].apply(lambda x : float(x))
newdf['index'] = newdf['index'].apply(lambda x : math.floor(x))

newdf2 = newdf[(newdf['자치구']=='공공공연장') 
              | (newdf['자치구']=='민간공연장')]
newdf2 = newdf2.loc[:,["index", "자치구", "서울"]]

newdf = newdf[(newdf['자치구']=='대공연장(1000석 이상)') 
              | (newdf['자치구']=='일반공연장(300~999석)') 
              | (newdf['자치구']=='소공연장(300석 미만)')]
newdf = newdf.loc[:,['index', '자치구', '서울']]

# 4번



# 사이드 바
option = st.sidebar.selectbox(
    '보고 싶은 항목을 선택해주세요',

    ('서울시 공연장 증감 추이', 
     '서울시 공연장 종류에 따른 수 차이', 
     '서울시 공연장 규모에 따른 수 차이', 
     '구 별 지도'))

accept = st.sidebar.button("확인")

# 사이드 바 확인 버튼 누르면 실행
if accept:
    if option == '서울시 공연장 증감 추이':
        fig = px.line(dat, x="연도", y="서울", line_shape="linear", line_group=None, color_discrete_sequence=["blue"])
        fig.update_layout(
            title='서울시 연도별 공연장 수 추이',
            xaxis_title='연도',
            yaxis_title='공연장 수',
        )
        st.write(fig)

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

    else:
        st.write('구 별 지도')
else:
    st.write('좌측 사이드바에서 보고 싶은 항목을 선택해주세요 :sunglasses:')