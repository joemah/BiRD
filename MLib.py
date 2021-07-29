#!/usr/bin/env python
# coding: utf-8

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
        


def clean_data_column(data, col, listA, listB):
    
    for i in range(len(listA)):
        data.loc[data[col].str.contains(listA[i], case=False),col] = listB[i]
    
    return data
    

def fill_nan(data):
    
    cols = list(data[data.columns[data.isna().any()]]) # get columns with nan values 
    data=data.fillna(data.mode().iloc[0])
    
    return data



def get_numerical_data(data):
    
    data = data.copy()
    data[data.select_dtypes(['object']).columns] = data.select_dtypes(['object']).apply(
                                                        lambda x: x.astype('category'))
    cat_columns = data.select_dtypes(['category']).columns
    data[cat_columns] = data[cat_columns].apply(lambda x: x.cat.codes)
    
    return data



def replace_missing_value(data, cols):
    
    for col in cols:
        
        
        if col == 'Gender':
            data[col] = data[col].fillna('I prefer not to say')
        
        elif col == 'TypeOfStudent':
            
            data[col] = data[col].fillna('Other')
            
        elif col == 'DoB':
            
            data[col] = data[col].fillna(2020)
        elif col == 'WhyRemainedPD':
            
            data[col] = data[col].fillna('Lockdown')
        
        elif col == 'AdviceOnlineLessons':

            data[col] = data[col].fillna('No advice')
        
        elif col == 'CountryB4Covid' or col == 'Nationality' or col == 'OnlineLessonsCountry' or col == 'BScDegreeCountry':
            data[col] = data[col].fillna('Unknown')
        
        else:
            data[col] = data[col].fillna('NotSpecified')
        
    return data

