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

# st.sidebar.markdown('회사 이름과 기간을 입력하세요')

# 기본 csv파일
data = pd.read_csv('./culture_space.csv', 
                   encoding="utf-8" )
data.replace('-', 0, inplace = True)
data_og = data.copy() # 원본 저장

# 3번 
df = data.transpose()
df.rename(columns=df.iloc[0], inplace=True)
df = df.drop(df.index[0])
newdf = df.reset_index()
newdf = newdf[(newdf['자치구']=='대공연장(1000석 이상)') 
              | (newdf['자치구']=='일반공연장(300~999석)') 
              | (newdf['자치구']=='소공연장(300석 미만)')]
newdf['index'] = newdf['index'].apply(lambda x : float(x))
newdf['index'] = newdf['index'].apply(lambda x : math.floor(x))
newdf = newdf.loc[:,['index', '자치구', '서울']]

option = st.sidebar.selectbox(
    '보고 싶은 항목을 선택해주세요',

    ('서울시 공연장 증감 추이', 
     '서울시 공공공연장과 민간공연장 수 차이', 
     '서울시 대/일반/소 공연장 수 차이', 
     '구 별 지도'))

accept = st.sidebar.button("확인")

if accept:
    if option == '서울시 공연장 증감 추이':
        st.write('서울시 공연장 증감 추이')

    elif option == '서울시 공공공연장과 민간공연장 수 차이':
        st.write('서울시 공공공연장과 민간공연장 수 차이')

    elif option == '서울시 대/일반/소 공연장 수 차이':
        st.write('서울시 대/일반/소 공연장 수 차이')
        fig = px.bar(newdf,
              x="자치구",
              y="서울",
              title='서울시 대/일반/소 공연장 수 차이',
              hover_data=['서울'],
              color = '자치구',
             facet_col = 'index',
              labels={'index':'연도', '서울':'공연장 수', '자치구':'공연장 규모'},
             text = '서울'
              )
        # fig.show()
        st.write(fig)

    else:
        st.write('구 별 지도')
else:
    st.write('좌측 사이드바에서 보고 싶은 항목을 선택해주세요 :sunglasses:')