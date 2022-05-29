#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import altair as alt


# reading in files
demog_HYS = pd.read_csv('assets/demog_HYS.csv')
demog_STJ = pd.read_csv('assets/demog_STJ.csv')

inc_rank_HYS=pd.read_csv('assets/income_rank_HYS.csv')
inc_rank_STJ=pd.read_csv('assets/income_rank_STJ.csv')

mosaic_HYS=pd.read_csv('assets/mosaic_hh_HYS.csv')
mosaic_STJ=pd.read_csv('assets/mosaic_hh_STJ.csv')

restaur_HYS=pd.read_csv('assets/rest_exp_HYS.csv')
restaur_STJ=pd.read_csv('assets/rest_exp_STJ.csv')

alc_HYS=pd.read_csv('assets/alc_HYS.csv')
alc_STJ=pd.read_csv('assets/alc_STJ.csv')


# In[2]:


def basic(file):
    '''clean up columns in reports'''
    new_file=pd.DataFrame(file)
    new_file=new_file[5:131]
    new_file.reset_index(inplace=True, drop=True)
    basic_columns= ['group', '2000_census', '2000_perc', '2010_census', '2010_perc',
                '2020_census', '2020_perc', '2025_project', '2025_project_perc',
                '2000-2010_percChange', '2020-2025_percChange']
    new_file.columns=basic_columns
    basic=new_file[['group', '2000_census', '2000_perc', '2010_census', '2010_perc','2020_census',
                    '2020_perc', '2025_project', '2025_project_perc',
                '2000-2010_percChange', '2020-2025_percChange']]
    basic.drop('2000-2010_percChange', axis=1, inplace=True)
    basic.set_index('group', inplace=True)
    basic=basic[basic.index.notnull()]
    basic=basic.dropna(how='all')
    basic.reset_index(inplace=True)
    
    return basic
    
def demog(file):
    '''get basic demography info in reports'''
    new_file=basic(file)
    keep=['group','Total Population','Male','White','Hispanic ','15 to 19','20 to 24','25 to 34',
          '35 to 44','45 to 54','$75,000 - $99,999','$100,000 - $149,999','$150,000 +','Average Hhld Income',
          'Median Hhld Income','Per Capita Income',]
    new=new_file.loc[new_file['group'].isin(keep)]
    new['2020-2025_percChange'] = new['2020-2025_percChange'].str.replace('%', '')
    new['2020-2025_percChange'] = new['2020-2025_percChange'].astype(float)
    new.reset_index(drop=True, inplace=True)
    new=new.drop(9)
    new.reset_index(drop=True, inplace=True)
    
    return new    


def income(file):
    new_file=file.set_index('Rank by Income Report')
    new=new_file[new_file.index.notnull()]
    new=new.dropna(how='all')
    new.reset_index(inplace=True)
    new.columns=new.iloc[0]
    new=new.drop(0).dropna(axis=1)
    
    return new

def mosaic(file):
    new=file
    col=['category', 'hh_count', 'perc']
    new.columns=col
    new['perc'] = new['perc'].str.replace('%', '')
    new=new.set_index('category')
    new=new[new.index.notnull()].dropna()
    new['perc'] = new['perc'].astype(float)
    new['hh_count'] = new['hh_count'].str.replace(',', '')
    new['hh_count'] = new['hh_count'].astype(float)
    new=new[new.hh_count > 0]
    
    return new

def restaur(file):
    new_file=file.set_index('Consumer Expenditure Restaurant Detail Summary')
    new_file=new_file[new_file.index.notnull()]
    new_file.reset_index(inplace=True)
    new=new_file[10:32]
    new.reset_index(inplace=True, drop=True)
    new.rename(columns={'Unnamed: 1':'spent'}, inplace=True)
    new['spent'] = new['spent'].str.replace('$', '')
    new['spent'] = new['spent'].str.replace(',', '')
    new['spent'] = new['spent'].astype(float)
    
    return new

def ethn(df):
    eth=pd.DataFrame(df.iloc[2])
    eth.columns=eth.iloc[0]
    eth['Hispanic']=df.iloc[3]
    eth.drop('group', inplace=True)
    
    return eth


# In[3]:


alc_HYS=alc_HYS[21:34]
alc_HYS.reset_index(drop=True, inplace=True)

alc_STJ=alc_STJ[21:34]
alc_STJ.reset_index(drop=True, inplace=True)


# In[ ]:





# In[ ]:





# In[4]:


demogHYS=demog(demog_HYS)
demogSTJ=demog(demog_STJ)

incomeHYS=income(inc_rank_HYS)
incomeSTJ=income(inc_rank_STJ)

mosaicHYS=mosaic(mosaic_HYS)
mosaicSTJ=mosaic(mosaic_STJ)


# In[5]:


mosaicHYS=mosaicHYS.sort_values('perc', ascending=False)
mosaicSTJ=mosaicSTJ.sort_values('perc', ascending=False)


# In[6]:


mosaicHYS.drop('Total Households', inplace=True)


# In[7]:


mosaicHYS.reset_index(inplace=True)


# In[8]:


mosaicHYS


# In[9]:


mosaicSTJ


# In[10]:


mosaicHYS['best']= False


# In[11]:


mosaicHYS['best'][0]=True
mosaicHYS['best'][2]=True
mosaicHYS['best'][5]=True


# In[12]:


mosaicHYS=mosaicHYS.replace(to_replace ='\w\d\d\s', value = '', regex = True)


# In[13]:


mosaicHYS['category'][5]='Digitally Savvy'


# In[14]:


# mosaicHYS['category'][1]=''
# mosaicHYS['category'][3]=''
# mosaicHYS['category'][4]=''
# mosaicHYS['category'][6:]=''


# In[15]:


mosaicHYS


# In[ ]:





# In[16]:


mos_HYS=alt.Chart(mosaicHYS).mark_bar().encode(
    x=alt.X('perc:Q',
           title='Percent of households with this profile',
           axis=alt.Axis(grid=False,
                         labels=False,
                        titleColor='#002569',
                        titleFont='corbel',
                        titleFontSize=15)),
    y=alt.Y('category',
            
            sort='-x',
            title='',
           ),
    color=alt.condition(
        alt.datum.best==True,
        alt.value('#F1AD02'),
        alt.value('lightgray'))
)


text = alt.Chart(mosaicHYS).mark_text(dx=-13,fontWeight='bold').encode(
    x=alt.X('perc:Q'),
    y=alt.Y('category',
           sort='-x',),
    color=alt.condition(
        alt.datum.best==True,
        alt.value('#002569'),
        alt.value('lightgray')),

    text=alt.Text('perc:Q', format='.1f')
)

mos_HYS = mos_HYS + text


# In[17]:


base=alt.Chart(mosaicHYS)

footer=base.mark_text(size=11,
                      color='#002569',
                      font='corbel',
                      opacity=0.5,
                      fontWeight=100,
                      lineBreak='\n',
                      align='left',
text='Data Source: [4]. All household profiles shown; rounded to the nearest tenth of a percent.\nSum of bar values equals 100%.'
).properties(height=25
)


# In[18]:


mos_HYS = mos_HYS & footer


# In[19]:


mos_HYS.configure_title(font='corbel',
                        color='#002569',
                        fontSize=16
).configure_axis(
ticks=False,
domain=False,
labelPadding=12,
labelColor='#002569',
labelFont='corbel',
labelFontSize=15,
    titleX=133
).configure_view(
strokeWidth=0,
).properties(
    title=
    {"text":"Hays, KS",
    "subtitle":'Mosaic Profiles',
    "subtitleFont":'corbel',
    "subtitleFontSize":16,
    "subtitleFontWeight": 'bold',
    "subtitleColor":'#002569',
    },

).configure_title(
font='corbel',
fontSize=24,
fontWeight='bold',
color='#002569',
offset=10,
).configure_scale(
bandPaddingInner=0.075
).configure_concat(
spacing=0
)


# In[20]:


# from altair_saver import save
# save(mos_HYS, 'mos_HYS.png', scale_factor=2.0)


# In[ ]:





# In[ ]:





# In[21]:


mosaicSTJ.drop('Total Households', inplace=True)


# In[22]:


mosaicSTJ.reset_index(inplace=True)


# In[23]:


mosaicSTJ=mosaicSTJ.replace(to_replace ='\w\d\d\s', value = '', regex = True)


# In[24]:


mos_STJ=alt.Chart(mosaicSTJ).mark_bar().encode(
    x=alt.X('perc:Q',
           title='Percent of households with this profile',
           axis=alt.Axis(grid=False,
                         labels=False,
                        titleColor='#002569',
                        titleFont='corbel',
                        titleFontSize=15)),
    y=alt.Y('category',
            sort='-x',
            title='',
           ),
    color=alt.condition(
        alt.datum.best==True,
        alt.value('#F1AD02'),
        alt.value('lightgray'))
)


text = alt.Chart(mosaicSTJ).mark_text(dx=-13,fontWeight='bold').encode(
    x=alt.X('perc:Q'),
    y=alt.Y('category',
           sort='-x',),
    color=alt.condition(
        alt.datum.best==True,
        alt.value('#002569'),
        alt.value('lightgray')),

    text=alt.Text('perc:Q', format='.1f')
)

mos_STJ = mos_STJ + text


# In[25]:


base2=alt.Chart(mosaicSTJ)

footer=base2.mark_text(size=11,
                      color='#002569',
                      font='corbel',
                      opacity=0.5,
                      fontWeight=100,
                      align='left',
                       lineBreak='\n',
                    
text='Data Source: [4]. All household profiles shown; rounded to the nearest tenth of a percent.\nSum of bar values equals 100%.'
).properties(height=25
)


# In[26]:


mos_STJ = mos_STJ & footer


# In[27]:


mos_STJ.configure_title(font='corbel',
                        color='#002569',
                        fontSize=16
).configure_axis(
ticks=False,
domain=False,
labelPadding=12,
labelColor='#002569',
labelFont='corbel',
labelFontSize=15,
titleX=133
).configure_view(
strokeWidth=0,
).properties(
    title=
    {"text":"St. Joseph, MI",
    "subtitle":'Mosaic Profiles',
    "subtitleFont":'corbel',
    "subtitleFontSize":16,
    "subtitleFontWeight": 'bold',
    "subtitleColor":'#002569',
    },

).configure_title(
font='corbel',
fontSize=24,
fontWeight='bold',
color='#002569',
offset=10,
).configure_scale(
bandPaddingInner=0.075
).configure_concat(
spacing=0
)


# In[ ]:





# In[ ]:





# In[ ]:





# In[28]:


h=restaur(restaur_HYS)
s=restaur(restaur_STJ)

HYSrestaur_2019=(sum(h['spent'][2:8]) + h['spent'][10]).round(2)
STJrestaur_2019=(sum(s['spent'][2:8]) + s['spent'][10]).round(2)

HYSrestaur_2025=(sum(h['spent'][13:19]) + h['spent'][21]).round(2)
STJrestaur_2025=(sum(s['spent'][13:19]) + s['spent'][21]).round(2)


# In[29]:


columns=['year', 'city', ]
spent_rest=pd.DataFrame()


# In[30]:


def rest_df(df, year, city):
    if year==2019:
        dfa=df[2:8]
        dfb=df[10:11]
    elif year==2025:
        dfa=df[13:19]
        dfb=df[21:22]
    dfnew=pd.concat([dfa, dfb])
    dfnew['city']=city
    dfnew['year']=year
    if city=='HYS':
        if year == 2019:
            dfnew['avg_inc']=66751
        elif year==2025:
            dfnew['avg_inc']=73593
    else:
        if year == 2019:
            dfnew['avg_inc']=79904
        elif year==2025:
            dfnew['avg_inc']=93615
    dfnew.reset_index(drop=True, inplace=True)
    return dfnew


# In[31]:


hys_a=rest_df(h, 2019, 'HYS')
hys_b=rest_df(h, 2025, 'HYS')

stj_a=rest_df(s, 2019, 'STJ')
stj_b=rest_df(s, 2025, 'STJ')


# In[32]:


hys_df=hys_a.merge(hys_b, how='outer')
stj_df=stj_a.merge(stj_b, how='outer')


# In[33]:


demogHYS


# In[34]:


demogSTJ


# In[35]:


rest_df=hys_df.merge(stj_df, how='outer')


# In[36]:


rest_df


# In[37]:


HYSspent19=round(sum(rest_df['spent'][:7]), 2)
HYSspent19


# In[38]:


STJspent19=round(sum(rest_df['spent'][14:21]), 2)
STJspent19


# In[39]:


STJspent19=round(sum(rest_df['spent'][21:]), 2)
STJspent19


# In[40]:


HYSspent25=round(sum(rest_df['spent'][7:14]), 2)
HYSspent25


# In[41]:


columns=['city', 'year', 'total_spent', 'avg_inc']
cit=['Hays', 'Hays', 'St. Joseph', 'St. Joseph']
yr=['2019', '2025', '2019', '2025']
sp=[2925.2, 3066.24, 3283.72, 3508.19]
ai=[66751, 73593, 79904, 93615]
perc_spent=pd.DataFrame(list(zip(cit, yr, sp, ai)),
               columns=columns)


# In[42]:


perc=[]
for c in perc_spent['total_spent']:
    x=round(c/perc_spent['avg_inc'], 3)*100
    perc.append(x)


# In[43]:


x


# In[44]:


perc_spent['perc_of_inc']=x


# In[45]:


perc_spent


# In[46]:


rest_spend=alt.Chart(perc_spent).mark_line(point=True, strokeWidth=4, ).encode(
    x=alt.X('year:O',
    axis=alt.Axis(grid=False,
                  domain=False,
                 labelAngle=0,
                  labelColor='#002569', 
                  labelFont='corbel',
                  labelFontSize=18,
                  labelFontWeight='bold',
                 ticks=False,
                 title='')),
    y=alt.Y('perc_of_inc:Q',
            axis=alt.Axis(grid=False,
                         ticks=False,
                         domain=False,
                          labels=False,
                          title=''
                         ),
           scale=alt.Scale(domain=[3.3, 5.7])),
    color=alt.Color('city', scale=alt.Scale(range=['#F1AD02', 'lightgray'], domain=['Hays', 'St. Joseph']))
).properties(width=375, height=750)


# In[47]:


rest_spend


# In[48]:


textA = rest_spend.mark_text(
    align='left',
    baseline='middle',
    dx=10,
    dy=-3,
    size=12,
    fontWeight='bold'
).encode(
    text='perc_of_inc',
)


# In[49]:


textA


# In[50]:



newer=rest_spend + textA


# In[51]:


newer.configure_axis(
ticks=False,
domain=False,
labelPadding=12,
labelColor='#002569',
labelFont='corbel',
labelFontSize=15,
    titleX=133
)


# In[ ]:





# In[52]:


annot=[['2019', 'HAYS:\n▸ higher spending\n‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎proportionally'],
       ['2025', '▸ less decline\n‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎in spending']]

text_df=pd.DataFrame(annot, columns=['year', 'note'])


# In[53]:


text_df


# In[54]:




textB = alt.Chart(text_df).mark_text(
    align='left',
    baseline='middle',
    dx=70,
    dy=-140,
    color='#002569',
    size=13,
    font='corbel',
    lineBreak='\n',
    text=text_df['note'][0]
).properties(width=375, height=750)

textB

textC = alt.Chart(text_df).mark_text(
    align='left',
    baseline='middle',
    dx=70,
    dy=-93,
    color='#002569',
    size=13,
    font='corbel',
    lineBreak='\n',
    text=text_df['note'][1]
).properties(width=375, height=750)

footer2=base2.mark_text(size=11,
                      color='#002569',
                      font='corbel',
                      opacity=0.5,
                      fontWeight=100,
                      align='left',
                        dx=-50,
text='Data Source: [4]. Rounded to the nearest tenth of a percent.'
).properties(width=375, height=25
)


# In[55]:


textC


# In[56]:


newest=newer+textB+textC&footer2


# In[57]:


newest.configure_title(
font='corbel',
fontSize=22,
fontWeight='bold',
color='#002569',
offset=10,
).configure_scale(
bandPaddingInner=0.075
).configure_concat(
spacing=0
).configure_legend(labelFont='corbel',
                       labelColor='#002569',
                       labelFontWeight='bold',
                       labelFontSize=14,
                       offset=10,
                       title=None,
                       orient='top',
).configure_view(
strokeWidth=0,
).properties(
    title=
    {"text":"Restaurant Spending Differences",
    "subtitle":'expressed as percent of average income',
    "subtitleFont":'corbel',
    "subtitleFontSize":16,
    "subtitleFontWeight": 'bold',
    "subtitleColor":'#002569',
     "align":'left',
     'dy':-10

    },

).configure_point(size=100)


# In[ ]:





# In[ ]:





# In[ ]:





# In[58]:


demogHYS


# In[59]:


demogSTJ


# In[60]:


col=['city', 'year', 'White/Hispanic',]
cit=['Hays', 'Hays', 'Hays', 'Hays', 'St. Joseph', 'St. Joseph','St. Joseph', 'St. Joseph']
yr=['2000', '2010', '2020', '2025', '2000', '2010', '2020', '2025']
numb=[19356, 19897, 19916, 20003, 8193, 7662, 7537, 7452]
# pop=[19598, 20350, 20564, 20741, 8924, 8396, 8341, 8320]


ethn_df=pd.DataFrame(list(zip(cit, yr, numb,)),
               columns=col)


# In[ ]:





# In[61]:


ethn_df


# In[ ]:





# In[62]:


# percs = [(n / p)*100 for n,p in zip(numb, pop)]


# In[63]:


# ethn_df['Growth']=percs


# In[64]:


# ethn_df['Percent White or Hispanic']=round(ethn_df['Percent White or Hispanic'], 1)


# In[ ]:





# In[65]:


import math


# In[66]:


ethn_HYS=ethn_df[:4]
ethn_STJ=ethn_df[4:]


# In[67]:


logsH=[]

for item in ethn_HYS['White/Hispanic']:
    x=math.log(item)
    logsH.append(x)


# In[68]:


logsH


# In[69]:


logsS=[]

for item in ethn_STJ['White/Hispanic']:
    x=math.log(item)
    logsS.append(x)


# In[70]:


logsS


# In[71]:


ethn_df


# In[ ]:





# In[72]:


###  BEER


# In[73]:


alc_STJ


# In[74]:


alc_HYS


# In[75]:


cols=['Beverage', 'City', 'Preferences']
alco=['Beer', 'Wine', 'Other', 'Beer', 'Wine', 'Other']
cities=['Hays', 'Hays', 'Hays', 'St. Joseph', 'St. Joseph', 'St. Joseph']
prefs=[118, 85, 93, 95, 117, 92]


# In[76]:


alc_df=pd.DataFrame(list(zip(alco, cities, prefs,)),
               columns=cols)


# In[77]:


alc_df['average']=100


# In[ ]:





# In[78]:


alc_df


# In[79]:


alc_chart=alt.Chart(alc_df).mark_bar().encode(
    x=alt.X('City:N',
            axis=alt.Axis(gridColor='#002569',
                         labels=False,
                         ticks=False,
                         domain=False,
                         title='')),
    y=alt.Y('Preferences:Q',
            axis=alt.Axis(grid=False,
                          labels=False,
                          ticks=False,
                          domain=False,
                          title='')),
    color=alt.Color('City:N', scale=alt.Scale(range=['#F1AD02', 'lightgray'], domain=['Hays', 'St. Joseph'])),
).properties(width=50)

alc_chart


# In[ ]:





# In[80]:


rule = alt.Chart(alc_df).mark_rule(color='#6ED0FF', strokeDash=[5,2]).encode(
    y='average:Q',
)
rule


# In[81]:


alco_chart=alc_chart+rule


# In[82]:


alco_chart=alco_chart.facet(column=alt.Column('Beverage:N',
                      title='',
                      header=alt.Header(labelFont='corbel',
                                       labelFontSize=16,
                                       labelColor='#002569',
                                       labelPadding=2,
                                       labelOrient='bottom',
                                       labelFontStyle='bold')),
                                       spacing=20,)


# In[83]:


alco_chart


# In[ ]:





# In[ ]:





# In[ ]:





# In[84]:


alco_chart.configure_title(
font='corbel',
fontSize=22,
fontWeight='bold',
color='#002569',
offset=10,


).configure_legend(labelFont='corbel',
                       labelColor='#002569',
                       labelFontWeight='bold',
                       labelFontSize=14,
                       offset=10,
                       title=None,
).configure_view(
strokeWidth=0,
).properties(
    title=
    {"text":"Alcoholic Beverage Preferences",
    "subtitle":'compared to national average',
    "subtitleFont":'corbel',
    "subtitleFontSize":16,
    "subtitleFontWeight": 'bold',
    "subtitleColor":'#002569',
     "align":'left',
     'dy':-10

    },
)


# In[ ]:




