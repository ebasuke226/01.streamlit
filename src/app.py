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

import plotly.express as px


"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


####ダッシュボード開発開始

st.title("日本の賃金ダッシュボード")

df_jp_ind = pd.read_csv('./analysis/csv_data/雇用_医療福祉_一人当たり賃金_全国_全産業.csv', encoding='shift_jis')
df_jp_category = pd.read_csv('./analysis/csv_data/雇用_医療福祉_一人当たり賃金_全国_大分類.csv', encoding='shift_jis')
df_pref_ind = pd.read_csv('./analysis/csv_data/雇用_医療福祉_一人当たり賃金_都道府県_全産業.csv', encoding='shift_jis')

st.header('2019年：一人当たりの平均賃金のヒートマップ')

jp_lat_lon = pd.read_csv('./analysis/csv_data/pref_lat_lon.csv')
jp_lat_lon = jp_lat_lon.rename(columns={'pref_name':'都道府県名'})

df_pref_map = df_pref_ind[(df_pref_ind['年齢'] == '年齢計') & (df_pref_ind['集計年'] == 2019)]
df_pref_map = pd.merge(df_pref_map,jp_lat_lon, on='都道府県名')
#正規化
df_pref_map['一人当たり賃金（相対値）'] =  ((df_pref_map['一人当たり賃金（万円）']-df_pref_map['一人当たり賃金（万円）'].min())/(df_pref_map['一人当たり賃金（万円）'].max()-df_pref_map['一人当たり賃金（万円）'].min()))

view = pdk.ViewState(
    longitude=139.691648,
    latitude=35.689185,
    zoom=4,
    pitch=40.5,
)

layer = pdk.Layer(
    "HeatmapLayer",
    data=df_pref_map,
    opacity=0.4,
    get_position=["lon", "lat"],
    threshold=0.3,
    get_weight = '一人当たり賃金（相対値）'
)

layer_map = pdk.Deck(
    layers=layer,
    initial_view_state=view,
)

st.pydeck_chart(layer_map)

show_df = st.checkbox('Show DataFrame')
if show_df == True:
    st.write(df_pref_map)

st.header('■集計年別の一人当たり賃金（万円）の推移')

df_ts_mean = df_jp_ind[(df_jp_ind["年齢"] == "年齢計")]
df_ts_mean = df_ts_mean.rename(columns={'一人当たり賃金（万円）': '全国_一人当たり賃金（万円）'})

df_pref_mean = df_pref_ind[(df_pref_ind["年齢"] == "年齢計")]
pref_list = df_pref_mean['都道府県名'].unique()
option_pref = st.selectbox(
    '都道府県',
    (pref_list))
df_pref_mean = df_pref_mean[df_pref_mean['都道府県名'] == option_pref]

df_mean_line = pd.merge(df_ts_mean, df_pref_mean, on='集計年')
df_mean_line = df_mean_line[['集計年', '全国_一人当たり賃金（万円）', '一人当たり賃金（万円）']]
df_mean_line = df_mean_line.set_index('集計年')
st.line_chart(df_mean_line)

#バブルチャート
st.header('■年齢階級別の全国一人あたり平均賃金（万円）')

df_mean_bubble = df_jp_ind[df_jp_ind['年齢'] != '年齢計']

fig = px.scatter(df_mean_bubble,
                x="一人当たり賃金（万円）",
                y="年間賞与その他特別給与額（万円）",
                range_x=[150,700],
                range_y=[0,150],
                size="所定内給与額（万円）",
	            size_max = 38,
                color="年齢",
                animation_frame="集計年",#何の推移を見たいのか？を定義
                animation_group="年齢")

st.plotly_chart(fig)


#横棒グラフ
st.header('■産業別の賃金推移')

year_list = df_jp_category["集計年"].unique()
option_year = st.selectbox(
    '集計年',
    (year_list))

wage_list = ['一人当たり賃金（万円）', '所定内給与額（万円）', '年間賞与その他特別給与額（万円）']
option_wage = st.selectbox(
    '賃金の種類',
    (wage_list))

df_mean_categ = df_jp_category[(df_jp_category["集計年"] == option_year)]

max_x = df_mean_categ[option_wage].max() + 50

fig = px.bar(df_mean_categ,
            x=option_wage,
            y="産業大分類名",
            color="産業大分類名",
            animation_frame="年齢",
            range_x=[0,max_x],
            orientation='h',
            width=800,
            height=500)
st.plotly_chart(fig)


st.text('出典：RESAS（地域経済分析システム）')
st.text('本結果はRESAS（地域経済分析システム）を加工して作成')


####ダッシュボード開発終了

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