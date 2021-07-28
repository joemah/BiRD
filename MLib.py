#!/usr/bin/env python
# coding: utf-8

# In[5]:
from plotly.subplots import make_subplots
from matplotlib.lines import Line2D
from termcolor import colored
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import warnings
import plotly.express as px
warnings.filterwarnings('ignore')
from plotly.offline import iplot, init_notebook_mode
import chart_studio.plotly as py
import plotly.graph_objs as go
import cufflinks as cf
cf.go_offline(connected=True)
init_notebook_mode(connected=True)



def get_col_names():
    
    cols_obj = ['DateSubmited','Language','DateStarted','LastActionDate','IP','TypeOfStudent','DegreeLevel','FieldOfStudy', 
            'Nationality','Gender','BScDegreeCountry', 'EnrolmentDate@Unipd', 'HomeB4Covid','PositionPadovaB4Covid','CountryB4Covid',
            'ActionFirstLockDown2020','Residency1stLockDown2020','PositionPadova2020LockDown','ActionFirstSemester20<>21','OtherActionFirstSemester20<>21',
            'ResidencyFirstSemester20<>21','OtherResidencyFirstSemester20<>21','LocationPadova(Oct-Apr)20/21','PostponeUnipdEnrolment',
            'WhyRemainedPD','FutureDecisions','OtherFutureDecisions','NumFlatMates','NumFlateOtherMates','HousingQuarantine',
            'OtherHousingQuarantine','OnlineLessonsCountry','HomeWiFi', 'MobileData','PublicWiFi',
            'UniversityWiFi','[Other]','TeachingMode','AdviceOnlineLessons','StudyHalls','UniArea','Libraries','Canteens',
            'Museums','PublicParks','Squares','CUSportsStructures','Not@All','LimitMovementsCity','AvoidPublicTransport',
            'Drink@Squares','DrinkNearHome','FlexibleHomeOutside','Eat@Canteen','Eat@Home','LimitHangingOutPeople',
            'NoOutingWithoutCurfew','VisitCinemasTheatersCultCenters','VisitPublicPlaces','MaintainSocialLife',
            'PartTimeJobInPadova','OnlinePartTimeJob','ShopInBigSupermarkets','ShopInSmallShops']
    
    cols_num = ['ResponseID','LastPage','Seed','DoB','Graduation','Internships','LearnItalian','Exams','QofLectures',
           'QofInstruction','StudentCommunity','NewFriends','Traveling','🚫StudyAbroadIfRestrictions','🚫StudyAbroadOnline',
            '❤️StudyUnipd','RateOnlineLessons','RateWiFiQuality','RateExpOnlineLectures','😀Family','😀Friends',
            '😀Students','😀Group','😀Other','Face2Face','PhoneCall','ZoomMeetSkypeJitsi','TelegramWhatsAppMessenger',
            'SocialMedia','GameTech', 'face2Face','phoneCall','MeetZoomSkypeJitsi','WhatsAppTelegramMessenger','socialMedia',
            'gameTech','ContentWithInteract','LangBarrierShpsPharm','VisaPermitHealthInsuarance','Accommodation/Rent',
            'LangBarrierMedAssistance','MedAssistance','Transport','NoneOfAbove','ForeignStudent','CountryOrigin',
            'Ethnicity','NotIncluded', 'Accommodated']
    
    return cols_obj, cols_num


# In[6]:


def check_null_dublicates(data):
    
    isNan = data.isnull().sum().any()
    if isNan == True:
        print("There are NaN values in the dataset")
    else:
        print("There are No NaN values in the dataset")

    isDup = data.duplicated().sum().any()
    if isDup == True:
        print("There are Duplicate rows in the dataset")
    else:
        print("There are No Duplicate rows in the dataset")
        


# In[7]:
def clean_data_column(data, col, listA, listB):
    
    for i in range(len(listA)):
        data.loc[data[col].str.contains(listA[i], case=False),col] = listB[i]
    
    return data
    

def fill_nan(data):
    
    cols = list(data[data.columns[data.isna().any()]]) # get columns with nan values 
    data=data.fillna(data.mode().iloc[0])
    
    return data


# In[8]:


def MakePlots(data, col,col2,barmode,opacity,rend, title):
    
    data = data.groupby(by=[col, col2]).size().reset_index(name="counts")
    fig = px.bar(data_frame=data, x=col, y="counts", color=col2, barmode=barmode,opacity=opacity)
    fig.update_layout(xaxis={'categoryorder':'category ascending'},
                      height=600, width=1000, title=title)
    fig.show(renderer=rend)
    


# In[9]:


def plot_bar_polar(data, col, col2,height,width,barmode,rend,title):
    
    data = data.groupby(by=[col, col2]).size().reset_index(name="frequency")
    fig = px.bar_polar(data, r="frequency", color=col, title=title,height=height, width=width,
        theta=col2, template="plotly_dark", barmode=barmode,
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig.show(renderer=rend)


# In[10]:


def plot_dostributions(data, cols, title,nbins,opacity,bool, barmode='group'):
    
    layout1 = cf.Layout(width=1000, height=650,title=title)
    data[cols].iplot(kind='hist', xTitle='Value',bins=nbins, theme = 'polar', layout=layout1,
                     histnorm='percent',opacity=opacity,barmode=barmode,online=bool,
                  yTitle='% count')
    

# In[11]:


def get_numerical_data(data):
    
    data = data.copy()
    data[data.select_dtypes(['object']).columns] = data.select_dtypes(['object']).apply(
                                                        lambda x: x.astype('category'))
    cat_columns = data.select_dtypes(['category']).columns
    data[cat_columns] = data[cat_columns].apply(lambda x: x.cat.codes)
    
    return data


# In[ ]:

def use_bar(data, cols, opacity,rend,title, barmode='group'):

    pd.options.plotting.backend = "plotly"
    data = data.groupby(by=cols).size().reset_index(name="counts")
    fig = data.plot.bar(x=cols, y='counts',barmode=barmode,opacity=opacity)
    fig.update_layout(xaxis={'categoryorder':'category ascending'},
                      height=600, width=1000, title=title)
    
    fig.show(renderer=rend)



# In[12]:


def plot_heatmap(data):
    
    correlation = data.corr(method='pearson')
    df_lt = correlation.where(np.tril(np.ones(correlation.shape)).astype(np.bool))
    fig = px.imshow(df_lt, origin='upper', title='Correlation between features',
                    width=1200,height=1100, aspect='equal')
    #fig.update_layout(width=1200, height=1200, title='')
    fig.show()


# In[ ]:




