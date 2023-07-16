import os
import warnings
warnings.filterwarnings('ignore')
from TradeStrategyFcn_001218 import *
import logging
logging.basicConfig(filename="log.log",
                        format='%(asctime)s %(message)s',
                        filemode='a')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)
logger.info('new caculate metrics run --------------------------------------------------------------')
ExcelName = r'./Report_Tag.xlsx'
TagDefinition = "UpDown" # UpDown or TrueFalse
m = 5 # [days]
BuyRepeatDays = 3
SellRepeatDays = 3
EnterCommission = 0.005
ExitCommission = 0.01
PlotIndex = 1
SumBaseEfficiencyV=0
SumEfficiencyV=0

#Accuracy_report_Edit = readmatrix('/home/alinezhad/History_risk/Accuracy-model/History_Risk.xlsx', 'Range', 'A2' );

NewFolderName = 'Efficiency'
os.makedirs(NewFolderName, exist_ok=True)
xl = pd.ExcelFile(ExcelName)
Sheets=xl.sheet_names  # see all sheet names
NamadNameV = [Sheet.replace( "_", "-" ) for Sheet in Sheets]
index=list(range(1,len(NamadNameV)+1))
EfficiencyV = np.zeros( (len( Sheets ), 1) )
BaseEfficiencyV = EfficiencyV
TotalTransactionsNoV = np.zeros( (len( Sheets ), 1) )
PositiveTransactionsNoV = TotalTransactionsNoV
InDaysNoV = EfficiencyV
TestDaysNoV = EfficiencyV
columns=['Date','Open','High','Low','close','Volume','Tag','Label','proba']
colName=["Namad Name", "Efficiency (%)", "Buy & Hold Efficiency (%)", "In-Days No.", "Test Days No.", "Efficiency per Day (%)", "Buy & Hold Efficiency per Day (%)", "Total Transactions No.", "Positive Transactions No.", "Win Rate", "Better Efficiency", "Better Efficiency per Day", "Positive Efficiency"]
EfficiencyDf=pd.DataFrame(columns=colName)
# EfficiencyDf["Namad Name"]=NamadNameV
# EfficiencyDf.index=EfficiencyDf["Namad Name"]
# EfficiencyDf.drop(EfficiencyDf.columns[0],axis=1)
print(EfficiencyDf.head())
for i in range(0, len( Sheets )):
    A=pd.read_excel(ExcelName,sheet_name=i)
    if TagDefinition =="UpDown":
        A.loc[A['Tag']==0,'Tag']=-1
        A.loc[A['Label'] == 0, 'Label'] = -1
    elif  TagDefinition=="TrueFalse":
        A['RealMove']=int(A['Close']>= A['Close'].shift(-m))
        A['PredMove']=1
        A.loc[A['Tag']==1,'RealMove']=A.loc[A['Tag']==1,'RealMove']
        A.loc[A['Tag'] == 0, 'RealMove'] = -1*A.loc[A['Tag'] == 0, 'RealMove']

    data=A.copy()
    fig,EfficiencyV, BaseEfficiencyV, InDaysNoV, TestDaysNoV, TotalTransactionsNoV, PositiveTransactionsNoV = TradeStrategyFcn_001218(data,BuyRepeatDays, SellRepeatDays, EnterCommission, ExitCommission, PlotIndex)
    print(f'sheet :{Sheets[i]} processed')
    EfficiencyV = (EfficiencyV - 1) * 100
    BaseEfficiencyV = (BaseEfficiencyV - 1) * 100

    EfficiencyPerDayV = EfficiencyV / InDaysNoV if InDaysNoV!=0 else 0
    BaseEfficiencyPerDayV = BaseEfficiencyV / TestDaysNoV if TestDaysNoV!=0 else 0
    BetterEfficiencyV = np.zeros( (len( Sheets ), 1) )
    BetterEfficiencyV=int( EfficiencyV > BaseEfficiencyV )
    BetterEfficiencyPerDayV= int(EfficiencyPerDayV > BaseEfficiencyPerDayV )
    PositiveEfficiencyV=int( EfficiencyV > 0 )
    WinRate=PositiveTransactionsNoV / TotalTransactionsNoV if TotalTransactionsNoV!=0 else 0
    EfficiencyDf.loc[index[i],EfficiencyDf.columns] = [NamadNameV[i],EfficiencyV, BaseEfficiencyV, InDaysNoV, TestDaysNoV, EfficiencyPerDayV,
              BaseEfficiencyPerDayV, TotalTransactionsNoV, PositiveTransactionsNoV,
              WinRate, BetterEfficiencyV, BetterEfficiencyPerDayV,
              PositiveEfficiencyV]
    SumBaseEfficiencyV+=BaseEfficiencyV
    SumEfficiencyV+=EfficiencyV
    logger.info(f'EfficiencyV : {EfficiencyV}, BaseEfficiencyV :{BaseEfficiencyV}, InDaysNoV :{InDaysNoV}, TestDaysNoV : {TestDaysNoV}, TotalTransactionsNoV : {TotalTransactionsNoV}, PositiveTransactionsNoV : {PositiveTransactionsNoV} , WinRate : {WinRate}')
    print(f'EfficiencyV : {EfficiencyV}, BaseEfficiencyV :{BaseEfficiencyV}, InDaysNoV :{InDaysNoV}, TestDaysNoV : {TestDaysNoV}, TotalTransactionsNoV : {TotalTransactionsNoV}, PositiveTransactionsNoV : {PositiveTransactionsNoV} , WinRate : {WinRate}')

    if PlotIndex == 1:
         EfficiencyString = f'Live Test Efficiency = {np.round((EfficiencyV - 1) * 100, 1)}  % of {np.round((BaseEfficiencyV - 1) * 100, 1)} % ( {np.round(((EfficiencyV - 1) / (BaseEfficiencyV - 1)), 2) * 100} %)'
         InDaysString = f'In-Days No = {InDaysNoV} of {TestDaysNoV} ( {np.round((InDaysNoV / TestDaysNoV), 2) * 100} %)'
         fig.suptitle(f'{NamadNameV[i]}  || {EfficiencyString} || {InDaysString}')
         fig.savefig(  f'./{NewFolderName}/{NamadNameV[i]}.jpg' )


ExcelName ='Efficiency.xlsx'
os.chdir(NewFolderName)
EfficiencyDf.to_excel(ExcelName)
logger.info(f'SumBaseEfficiencyV ={SumBaseEfficiencyV} ')
print(SumBaseEfficiencyV )
logger.info(f'SumEfficiencyV ={SumEfficiencyV} ')
print( SumEfficiencyV )
