from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk
from PIL import Image
import time

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

st.title("タイトル表示")
st.header("ヘッダーの表示")
st.subheader("サブヘッダーの表示")
st.text("テキストの表示")

df = pd.DataFrame({
    'first columns':[1,2,3,4],
    'second columns':[40,30,20,10],
})

st.write(df)

#カラムソート可能
st.dataframe(df)

st.dataframe(df,width = 200, height=200)

st.dataframe(df.style.highlight_max(axis=0))

#カラムソート不可能
st.table(df)

x = 100
x

"""
# マジックコマンドを使ってみる
文字列を入力
```Python
import streamlit as pt
print('Hello Streamlit')
```
"""

df_ = pd.DataFrame(np.random.randn(20,3),columns=['a','b','c'])
df_

#折れ線グラフ
st.line_chart(df_)
#面グラフ
st.area_chart(df_)
#棒グラフ
st.bar_chart(df_)

fig = plt.figure(figsize = (10,5))
ax = plt.axes()
x = [105,210,301,440,500]
y = [10,20,30,50,60]
ax.plot(x,y)

st.pyplot(fig)

tokyo_lat = 35.69
tokyo_lon = 139.69

df_tokyo = pd.DataFrame(
    np.random.randn(1000,2) / [50,50] + [tokyo_lat,tokyo_lon],
    columns=['lat','lon']
)

df_tokyo

st.map(df_tokyo)

view = pdk.ViewState(latitude=tokyo_lat, longitude=tokyo_lon, pitch=50,zoom=11)

hexagon_layer = pdk.Layer('HexagonLayer',
    data = df_tokyo,
    get_position = ['lon','lat'],
    elevation_scale=6,
    radius=200,
    extruded=True
    )

layer_map = pdk.Deck(layers=hexagon_layer, initial_view_state=view)

st.pydeck_chart(layer_map)

#ボタンの設定
option_button = st.button('ボタン')
if option_button == True:
    st.write('ボタンが押されました')
else:
    st.write('ボタンを押してください。')

#ラジオボタン
option_radio = st.radio(
    "好きな果物を選んでください。",
    ('リンゴ','バナナ','オレンジ','その他')
)
st.write('あなたが選んだ果物は：', option_radio)

#チェックボックス
option_check = st.checkbox('Dataframeの表示')
if option_check == True:
    st.write(df)

#セレクトボックス
option_select = st.selectbox(
    "好きな果物を選んでください。",
    ('リンゴ','バナナ','オレンジ','その他')
)
st.write('あなたが選んだ果物は：', option_select)

#マルチセレクト
option_multi = st.multiselect(
    "好きな色を選んでください。",
    ['緑','黄色','赤','青'],
    ['黄色','赤']
)
st.write('あなたが選んだ果物は：', option_multi)


#スライダー
age = st.slider('あなたの年齢を教えてください。',min_value=0,max_value=130,step=1,value=20)
st.write('私の年齢は：', age)

values = st.slider(
    '数値の範囲を入力してください。',
    0.0,100.0,(25.0,75.0)
)
st.write('values：', values)

#サイドバー
height = st.sidebar.slider('あなたの身長を入力してください。', min_value=0,max_value=200,step=1,value=170)
st.write('私の身長は：', height)
gender = st.sidebar.selectbox('あなたの性別を教えてください。', ['男性','女性'])
st.write('私の性別は：', gender)

#プログレスバー
progress_button = st.button('プログレスボタン')
if progress_button == True:
    st.write('処理を開始します')
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1)
    st.text('処理が終了しました')
else:
    st.write('プログレスボタンを押してください。')



"""
with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
"""