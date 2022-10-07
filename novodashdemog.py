
# !pip install streamlit -q
# !pip install plotly
# %%writefile app.py
import pandas as pd
import numpy as np
import streamlit as st
import warnings 
warnings.filterwarnings('ignore')
import plotly.express as px
import plotly.graph_objects as gp
df1 = pd.read_excel("ADSL.xlsx")
df_bas = df1[['USUBJID', 'ARM','AGE','AGEGR1','RACE', 'SEX', 'ETHNIC','BMIBL', 'BMIBLGR1', 'HEIGHTBL','WEIGHTBL', 'EDUCLVL']]
df_bas.dropna(inplace=True)
def bmi_cat(df):    
    if (df['BMIBL'] < 18.5):
        return 'Underweight'
    elif (df['BMIBL']>=18.5) & (df['BMIBL'] <  24.9):
        return 'Healthy'
    elif (df['BMIBL']>=24.9) & (df['BMIBL'] <  29.9):
        return 'Overweight'
    else:
        return "Obese"
df = df_bas.assign(BMI_Grp=df_bas.apply(bmi_cat, axis=1))
df=pd.DataFrame(df.groupby(['ARM','BMI_Grp','RACE']).agg("count")['USUBJID'])
df=df.reset_index()
df.rename(columns={'USUBJID':'COUNT'},inplace=True) 
df_bas_1 = df_bas[['ARM','AGEGR1','SEX']].value_counts()
df_bas_1 = df_bas_1.reset_index()
df_bas_1 = df_bas_1.sort_values(by=['ARM','AGEGR1','SEX'])
df_bas_1 = df_bas_1.reset_index(drop=True)
df_bas_1.rename({0:'Count'},axis=1,inplace=True)
data=df_bas_1.pivot_table(index=['ARM','AGEGR1'],columns='SEX',values='Count')
data = data.reset_index()
agegr = data['AGEGR1']
agegr2 = [1 if i=='<65' else 2 if i=='65-80' else 3 for i in agegr]
data['age_cat'] = agegr2
data_a = data[data['ARM']=='ARM A']
data_b = data[data['ARM']=='ARM B']
data_c = data[data['ARM']=='ARM C']
y_age = data_a['age_cat']
x_M = data_a['M']
x_F = data_a['F'] * -1
y_age2 = data_b['age_cat']
x_M2 = data_b['M']
x_F2 = data_b['F'] * -1
y_age3 = data_c['age_cat']
x_M3 = data_c['M']
x_F3 = data_c['F'] * -1
import streamlit as st
st.header("Demographics and baseline characteristics by treatment")
chart_selector = st.sidebar.selectbox("Select the type of chart", ['Sunburst Chart','Population Pyramid A','Population Pyramid B','Population Pyramid C','Boxplot for BMI'])
import plotly.express as px
import plotly.graph_objects as gp
if chart_selector=='Sunburst Chart':
  st.write("### Sunburst Chart for Participants Description")
  sunb = px.sunburst(df, 
                 path=['ARM','BMI_Grp','RACE'], 
                 values='COUNT',
                 color='COUNT', color_continuous_scale='pinkyl')
  sunb.update_layout(margin = dict(t=0, l=0, r=0, b=0),uniformtext=dict(minsize=10))
  st.plotly_chart(sunb,use_container_width = True)
if chart_selector=='Boxplot for BMI':
  st.write("### Boxplots for BMI in each arm by age groups")
  boxy = px.box(df_bas, x="SEX", y="BMIBL", color="ARM",facet_col="AGEGR1")
  st.plotly_chart(boxy,use_container_width = True)
if chart_selector=="Population Pyramid A":
  st.write("### Population Pyramid of Treatment A")
  # Creating instance of the figure
  fig = gp.Figure()
  # Adding Male data to the figure
  fig.add_trace(gp.Bar(y= y_age, x = x_M, 
                     name = 'Male', 
                     orientation = 'h'))
  
  # Adding Female data to the figure
  fig.add_trace(gp.Bar(y = y_age, x = x_F,
                     name = 'Female', orientation = 'h'))
  
  # Updating the layout for our graph
  fig.update_layout(barmode = 'relative',
                 bargap = 0.5, bargroupgap = 0.1,autosize=False,
      width=800,
      height=400,
                 xaxis = dict(tickvals = [-20, -10,
                                          0, 10, 20],
                                
                              ticktext = ['20', '10', '0', 
                                          '10', '20'],
                                
                              title = 'Population',
                              title_font_size = 14),
                  yaxis = dict(tickvals=[1,2,3],
                              ticktext = ['<65','65-80','>80'],                         
                              title = 'Age Group',
                              title_font_size = 14), 
                 )
  st.plotly_chart(fig,use_container_width = True)
if chart_selector=="Population Pyramid B":
  st.write("### Population Pyramid of Treatment B")
  # Creating instance of the figure
  fig = gp.Figure()
  # Adding Male data to the figure
  fig.add_trace(gp.Bar(y= y_age2, x = x_M2, 
                     name = 'Male', 
                     orientation = 'h'))
  
  # Adding Female data to the figure
  fig.add_trace(gp.Bar(y = y_age2, x = x_F2,
                     name = 'Female', orientation = 'h'))
  
  # Updating the layout for our graph
  fig.update_layout(barmode = 'relative',
                 bargap = 0.5, bargroupgap = 0.1,autosize=False,
      width=800,
      height=400,
                 xaxis = dict(tickvals = [-20, -10,
                                          0, 10, 20],
                                
                              ticktext = ['20', '10', '0', 
                                          '10', '20'],
                                
                              title = 'Population',
                              title_font_size = 14),
                  yaxis = dict(tickvals=[1,2,3],
                              ticktext = ['<65','65-80','>80'],                         
                              title = 'Age Group',
                              title_font_size = 14), 
                 )
  st.plotly_chart(fig,use_container_width = True)
if chart_selector=="Population Pyramid C":
  st.write("## Population Pyramid of Treatment C")
  # Creating instance of the figure
  fig = gp.Figure()
  # Adding Male data to the figure
  fig.add_trace(gp.Bar(y= y_age3, x = x_M3, 
                     name = 'Male', 
                     orientation = 'h'))
  
  # Adding Female data to the figure
  fig.add_trace(gp.Bar(y = y_age3, x = x_F3,
                     name = 'Female', orientation = 'h'))
  
  # Updating the layout for our graph
  fig.update_layout(barmode = 'relative',
                 bargap = 0.5, bargroupgap = 0.1,autosize=False,
      width=800,
      height=400,
                 xaxis = dict(tickvals = [-20, -10,
                                          0, 10, 20],
                                
                              ticktext = ['20', '10', '0', 
                                          '10', '20'],
                                
                              title = 'Population',
                              title_font_size = 14),
                  yaxis = dict(tickvals=[1,2,3],
                              ticktext = ['<65','65-80','>80'],                         
                              title = 'Age Group',
                              title_font_size = 14), 
                 )
  st.plotly_chart(fig,use_container_width = True)

# ! streamlit run app.py & npx localtunnel --port 8501
