import numpy as np 
import  pandas as pd 
import matplotlib.pyplot as plt 
import scipy as sp 
import seaborn as sns


def rename_loc_columns():

    col_loc_obj = ['Data','DataInvio','DataInizio','DataUltimaAzione','IP','URL', 'CorsoIscrita','AltroCorsoIstrita',
              'CorsoDiLaura','AltroCorsoDiLaura','ConseguitoIlTitolo','ConseguitoIlTitoloAltro','ComuneDiResidenza',
              'Genere','GenereAltroe','Settembre2019','PrimaDellEmergenza','PrimaDellEmergenzaAltro','CheZonaPadova',
               'PendolareComuna','CollegaviDiSolito', 'DovutoSpostarti','DovutoSpostartiAltro', 'ComuneSpostatoLockdown',
              'ZonaSpostatoPadova','PrimaSemestre20<>21','PrimaSemestre20<>21Altro','ComunePrimaS20<>21','ZonaPrimaS20<>21',
              'PerFrequentareCorso','PerFrequentareCorsoAltro','DoveViveviOttFeb','PendolareDicomuneOttFeb','ComuneCorsoOnline',
              'QuantePersoneAlloggio','ConChiDaranteLockdown','ConChiDaranteLockdownAltro','PCoMAC','Tablet','Smartphone',
              'StrementoAltro', 'Retedomestica', 'ReteDelloSmartphone', 'RetePubblica','RetePrivata','ReteUniversitaria',
               'AltraReteUniNonUnipd','ReteAltro','AttivitaDiStudio', 'Lavoro','SvagoTempoLibero','AcquistoBeniServizi',
              'EsamiAltro','NonEsamiAttivitaStudio','NonEsamiLavoro', 'NonEsamiSvagoTempoLibero','NonEsamiAcquistoBeniServizi',
              'NonEsamialtro','MiaStanzaPersonale','SpazioCondivisoConAltri','SpazioPubblico', 'Biblioteca', 'AulaStudio','Parco',
              'Altro','Suggerimenti','AuleStudio','AuleDipartimenti','Biblioteche','Mense','Piazze','Locali','Musei','ParchiPublici',
              'StuttureSportiveCUS','MancatiAltro','Classifica1','Classifica2','Classifica3','Classifica4','CosaPensiDiFare','CosaPensiDiFareAltro',
              'PrenderoCasa','VivroPadova','NonPrendereMezziPubbicidiTrasporto','VivoAPadova','LimiteroSpostamentiDentroCitta',
               'NonUseroPubbliciTrasporto','AndroPiazzaSPritz','SpritzBarSottoCasa','CasaFuouriNonImporta','AndroMensa',
              'MangeroCasa','LimiteroFrequentazioniAltre','NonUsciroTorneroCasaMoltoPresto','FrequenteroCinemaTeatriCentriCulturali',
              'FrequenteroLuoghiPubbliciAperto','ContinueroFareVitasociale','CercheroLavorettoPadova','CercheroLavorettoOnline',
              'FaroSpesaGrandeCateneSupermercati','SpesaViciniCasa']

    col_loc_num  = ['IDRisposta', 'UtimaPagina','Seme','DataNascita','MetodologiaDidattica','QualitaRete',
                'EsperienzadidatticaDistanza','😀Familiari','😀Amici','😀AltriStudenti','😀Gruppi',
               '😀Altro','ChimataTelefonica','ZoomMeetJitsi','TelegramWhatapp','SocialMedia','GamingTech',
                'InterazioniDalVivo','chiamataTelefonica','VideoChiamata','Chat','SocialNetwork','InterazioniPersona',
               'CommunicazioneTecnologie','Studi','PiaceLavoro','LavorareGruppo','EntusiastaProjettoAccademico',
                'InterrotoProgettoAccademico','NoProspettiveChiareFuturo','AffrontareDifficotaFinanziarie','MantengoReteRelazion']

    
    return col_loc_obj, col_loc_num



def fill_nan(data):
    
    cols = list(data[data.columns[data.isna().any()]]) # get columns with nan values 
    data=data.fillna(data.mode().iloc[0])
    
    return data

   
def fill_missing_values(data, cols):
    
    for col in cols:
        
        if col == 'URL':
            data[col] = data[col].fillna('https://www.google.com')
        
        elif col=='CorsoIscrita' or col =='CorsoDiLaura' or col=='PerFrequentareCorso' or col=='ConChiDaranteLockdown' or 'PrimaSemestre20<>21':
            data[col] = data[col].fillna('Altro')
            
        elif col == 'DataNascita':
            data[col] = data[col].fillna(2020)

        elif col == 'Genere' or  col=='GenereAltroe':
            data[col] = data[col].fillna('Preferisco non rispondere')

        elif col == 'ComuneDiResidenza' or col=='ConseguitoIlTitoloAltro': #or col == 'Nationality' or col == 'OnlineLessonsCountry' or col == 'BScDegreeCountry':
            data[col] = data[col].fillna('Sconosciuto')
        
        else:
            data[col] = data[col].fillna('non specificato')
        
    return data


def clean_data_column(data, col, listA, listB):
    
    for i in range(len(listA)):
        data.loc[data[col].str.contains(listA[i], case=False),col] = listB[i]
    
    return data
