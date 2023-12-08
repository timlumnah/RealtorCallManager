
'''
cd ~/.virtualenvs/ClientCallTracker/VirtualEnvironment
source venv/bin/activate
python3 ~/.virtualenvs/ClientCallTracker/VirtualEnvironment/ProjectFiles/NinjaLogRunner.py

DuplicateCalls_DF.csv file & rename as ClientCalls.csv
ClientCalls.csv is input file, DuplicateCalls_DF.csv is output file
'''

import time
import datetime
# from datetime import datetime
import pytz
from datetime import timedelta
from pytz import timezone
import pandas as pd
import numpy as np
import csv
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import os
import ezgmail


# ___________________________________________________
def readFile(FileName):
    import fileinput
    Directory = "~/.virtualenvs/ClientCallTracker/VirtualEnvironment/ProjectFiles/Input/"
    Extension = ".csv"
    FileName = Directory + FileName
    FileName += Extension

    # print ('\nreadFile(FileName) = ', FileName)
    # Change the parse_dates to be universal to call, cma, and handwritten note csv files.
    print('\n FileName (Line 37): \n', FileName, '\n')
    DataFrame = pd.read_csv(FileName, parse_dates=['LastContactDate','NextContactDate'])
    print('\nDataFrame = \n', DataFrame)

    return DataFrame

# ___________________________________________________
def fixCSV_March_3_2023():
    FileName = 'ContinuousOngoing_NinjaMaxCRM_'
    Directory = "~/.virtualenvs/ClientCallTracker/VirtualEnvironment/ProjectFiles/Input/"
    Extension = ".csv"
    FileName = Directory + FileName
    FileName += Extension

    # df = pd.readFile('ContinuousOngoing_NinjaMaxCRM_')

    # Code created by ChatGPT

    df = pd.read_csv(FileName)

    # Check if last column is empty
    if df.iloc[:, -1].isnull().values.any():

        # Calculate new datetime by adding number of days from "Interval_Days" column
        new_date = df['LastContactDate'] + pd.to_timedelta(df['Interval_Days'], unit='d')

        # Populate empty cells with new datetime
        df.iloc[:, -1].fillna(new_date, inplace=True)

    # Save updated CSV file
    # df.to_csv('updated_csv_file.csv', index=False)

    # ---------------

    CreateFile(df, FileName, TimeStamp=True)

# ___________________________________________________
def GetTimeStamp():
    t = datetime.datetime.now()
    t -= datetime.timedelta(hours=4)
    # print("The time is: ", t)
    return t

# ___________________________________________________
def UpdateNextContact(ClientCalls_DF, time, row, CallFrequency):
    # print('\nEntered UpdateNextContact() Function Successfully')
    ClientCalls_DF['NextContactDate'][row] = ClientCalls_DF['LastContactDate'][row] + datetime.timedelta(days = CallFrequency)
    # print('\n CallFrequency (Line 53): \n', CallFrequency, '\n')

# ___________________________________________________
def MultipleAddressColumnsIntoSingle(FileName):
    ClientCalls_DF = readFile(FileName)
    y = 0
    for row in ClientCalls_DF.itertuples():
        completeAddress = str(ClientCalls_DF['Address'][y]) + ', ' + str(ClientCalls_DF['City'][y]) + ', ' + str(ClientCalls_DF['State'][y]) + ', ' + str(ClientCalls_DF['Zip'][y])
        print(ClientCalls_DF['FirstName'][y],ClientCalls_DF['LastName'][y], 'completeAddress: ', completeAddress)
        ClientCalls_DF['Address'][y] = completeAddress
        y+=1

    ClientCalls_DF = ClientCalls_DF.drop(columns=['City', 'State', 'Zip'])
    # columns=['A', 'B', 'C', 'D']
    # print('ClientCalls_DF: \n', ClientCalls_DF)
    CreateFile(ClientCalls_DF, 'AddressSplice', TimeStamp=True)


# ___________________________________________________
def CombineDFsForEmail(DataFrame_1, DataFrame_2):

    # DataFrame_1 = CallsToMakeToday_DF
    # DataFrame_2 = CMAsToMakeToday_DF
    # DataFrame_3 = HandwrittenNotesToMakeToday_DF

    Title = 'New DataFrame'
    MarkerList = [['','','','','',''],['','',Title,'','','']]
    MarkerDataFrame = pd.DataFrame(MarkerList, columns = ['FirstName','LastName','Address','LastContactDate','NextContactDate','CID'])
    print('\nMarkerDataFrame: \n', MarkerDataFrame, '\n')

    # EmailDataFrame = pd.concat([SentDataFrame, SubjectPropertyDataFrame],ignore_index=True)
    EmailDataFrame = pd.concat([DataFrame_1, MarkerDataFrame, DataFrame_2],ignore_index=True)

    return EmailDataFrame

# ___________________________________________________
def IterateDataFrame(InputFileName):

    print('\n InputFileName (Line 90): \n', InputFileName, '\n')
    # CMA DF row: FirstName, LastName, Address, CID
    # HandwrittenNotes DF row: FirstName, LastName, Address, CID
    # Could Just Change 'Phone' column to 'ContactMethod' in ClientCalls & Address in the CMA and HandwrittenNotes.  This would be universal enough, because all other fields are the same.
    ClientCalls_DF = readFile(InputFileName)
    # print('\n ClientCalls_DF: \n', ClientCalls_DF, '\n')

    CallsToMakeTodayList = []  # this is the list that will end up getting emailed
    Date = GetTimeStamp()
    y = 0
    # for i, row in enumerate(ClientCalls_DF.itertuples(), 1):
    for row in ClientCalls_DF.itertuples():
        # print('Successfully entered for loop at line 104')
    # for row in enumerate(ClientCalls_DF.itertuples()):
    # for row in ClientCalls_DF.iterrows():
        # CallFrequency = int(ClientCalls_DF['Interval_Days'][row])
        # CallFrequency = ClientCalls_DF['Interval_Days'][row]
        # CallFrequency = 5
        # CallFrequency = int(ClientCalls_DF['Interval_Days'][y])
        CallFrequency = 1

        if ClientCalls_DF['LastContactDate'][y] == 'new':
            # print("New Client: ", ClientCalls_DF['FirstName'][y], ClientCalls_DF['LastName'][y])
            # print('Successfully entered if statement at line 114')
            ClientCalls_DF['LastContactDate'][y] = Date
            UpdateNextContact(ClientCalls_DF, time, y, CallFrequency)

        # Check to see if the client needs to be contacted
        if Date > ClientCalls_DF['NextContactDate'][y]:
            # print('Successfully entered if statement at line 119')
            IndividualClientList = [ClientCalls_DF['Name'][y],ClientCalls_DF['Phone'][y],ClientCalls_DF['Email'][y],
                ClientCalls_DF['Address'][y],ClientCalls_DF['City'][y],
                ClientCalls_DF['State'][y],ClientCalls_DF['Zip'][y],
                ClientCalls_DF['KvCoreLink'][y],ClientCalls_DF['GoogleLink'][y],
                ]
            CallsToMakeTodayList.append(IndividualClientList)
            ClientCalls_DF['LastContactDate'][y] = Date
            UpdateNextContact(ClientCalls_DF, time, y, CallFrequency)
            # print('\n IndividualClientList = \n', IndividualClientList)

        y += 1

    CallsToMakeToday_DF = pd.DataFrame(CallsToMakeTodayList, columns = ['Name', 'Phone','Email',
        'Address','City','State','Zip','KvCoreLink', 'GoogleLink',
        ])

    print('\nCallsToMakeTodayList: \n', CallsToMakeTodayList, '\n')
    print('\nCallsToMakeToday_DF: \n', CallsToMakeToday_DF, '\n')

    OutputFileName = 'NinjaMaxCRM_'
    # OutputFileName = 'NinjaMax_TestData_'
    print('\n OutputFileName = \n', OutputFileName)
    CreateFileWithTimeStamp(ClientCalls_DF, GetTimeStamp(), OutputFileName)

    return CallsToMakeToday_DF


# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
def CreateFile(dataframe, file_name, TimeStamp):
    # TimeNow = datetime.now() - timedelta(hours = 4)
    TimeNow = GetTimeStamp()
    Date = TimeNow.strftime("%Y-%m-%d-%H-%M")
    # Date = time.strftime("%Y-%m-%d-%H-%M")
    Directory = '~/.virtualenvs/ClientCallTracker/VirtualEnvironment/ProjectFiles/Output/'
    # FileName = "Postions_"
    FileName = file_name
    Extension = ".csv"

    if TimeStamp == True:
        FileName = Directory + FileName + Date + Extension
        # print("\nOutput FileName: ",FileName)
        dataframe.to_csv(FileName, index = False)
    else:
        FileName = Directory + FileName + Extension
        # print("\nOutput FileName: ",FileName)
        dataframe.to_csv(FileName, index = False)


# ___________________________________________________
def CreateFileWithTimeStamp(ClientCalls_DF, time, FileName):
    # https://www.freecodecamp.org/news/how-to-get-the-current-time-in-python-with-datetime/#howtogetthecurrenttimeofatimezonewithdatetime
    Date = time
    Date = Date.strftime("%Y-%m-%d")
    Date = str(Date)
    Directory = "~/.virtualenvs/ClientCallTracker/VirtualEnvironment/ProjectFiles/Output/"
    Extension = ".csv"

    File_1 = Directory + FileName + Date + Extension
    '''
    FileName = Directory + FileName
    FileName += Date
    FileName += Extension
    '''
    print("\n Output File Created At: ",File_1)
    ClientCalls_DF.to_csv(File_1, index=False)

    # Repeat into Input folder | Update a continuous/ongoing file in input folder to keep track of all calls.
    Directory = "~/.virtualenvs/ClientCallTracker/VirtualEnvironment/ProjectFiles/Input/"
    prefix = 'ContinuousOngoing_'
    File_2 = Directory + prefix + FileName + Extension

    print("\n Input File Updated At: ",File_2)
    ClientCalls_DF.to_csv(File_2, index=False)


# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
def Combine_csv_files(File_1, File_2):      # https://www.freecodecamp.org/news/how-to-combine-multiple-csv-files-with-8-lines-of-code-265183e0854/
    # Combine_csv_files()
    '''
    Combines all in a folder

    os.chdir("/Users/Tim/Desktop/MasterProgram-8-6-22/InputClientData/VirtualEnvironment/ProjectFiles/Output")
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
    '''
    # os.chdir("/Users/Tim/Desktop/MasterProgram-8-6-22/InputClientData/VirtualEnvironment/ProjectFiles/Output")
    # extension = 'csv'


    Directory = "~/.virtualenvs/ClientCallTracker/VirtualEnvironment/ProjectFiles/Input/"
    Extension = ".csv"
    File_1 = Directory + File_1 + Extension
    File_2 = Directory + File_2 + Extension
    combined_csv = pd.concat(pd.read_csv(File_1),pd.read_csv(File_2))
    combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')




# ___________________________________________________
def SendEmail2(DataFrame, Subject):

    html_Calls = DataFrame.to_html()
    string_Calls = DataFrame.to_string()

    '''
    html_test = """\
    <html>
      <head></head>
      <body>
        {0}
      </body>
    </html>
    """.format(DataFrame.to_html())
    '''

    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    message = MIMEMultipart("alternative")

    html = """\
    <html>
      <head></head>
      <body>
        {0}
      </body>
    </html>
    """.format(DataFrame.to_html())

    ezgmail.send('tim@bhhspagerealty.com', Subject, html, mimeSubtype='html')




# ___________________________________________________
def Bookmark_IterateDataFrame(NumberOfSubjects, TotalDataSetFile, OngoingLedgerFile):
    # cycles through a list of leads one at a time
    # https://stackoverflow.com/questions/15943769/how-do-i-get-the-row-count-of-a-pandas-dataframe

    MainDataFrame = readFile(TotalDataSetFile)
    SentDataFrame = readFile(OngoingLedgerFile)

    LengthMainDF = len(MainDataFrame.index)
    LengthSentDF = len(SentDataFrame.index)

    SubjectPropertyList = []

    if LengthMainDF < LengthSentDF:

        LengthSentDF = LengthSentDF - LengthMainDF   # you will eventually need division to determine how many times to reduce LengthSentDF value

    if NumberOfSubjects == 1:
        SubjectPropertyIndex = LengthSentDF
        SubjectProperty = MainDataFrame.iloc[[SubjectPropertyIndex]]

        [SubjectProperty2] = SubjectProperty.values.tolist()  # unpack list: https://stackoverflow.com/questions/45986524/remove-the-outer-list-of-a-double-list

        SubjectPropertyList.append(SubjectProperty2)

        FileName = 'CMAs_Sent_'


    elif NumberOfSubjects > 1:
        a = 0
        while a < NumberOfSubjects:
            SubjectPropertyIndex = LengthSentDF + a
            SubjectProperty = MainDataFrame.iloc[[SubjectPropertyIndex]]
            # print('\nSubjectProperty: \n', SubjectProperty, '\n')
            [SubjectProperty2] = SubjectProperty.values.tolist()  # unpack list: https://stackoverflow.com/questions/45986524/remove-the-outer-list-of-a-double-list
            # print('\nSubjectProperty2: \n', SubjectProperty2, '\n')
            # SubjectPropertyList.append(SubjectProperty)
            SubjectPropertyList.append(SubjectProperty2)
            # print('\nSubjectPropertyList: \n', SubjectPropertyList, '\n')
            a += 1

        FileName = 'HandwrittenNotes_Sent_'

    # print('\nSubjectPropertyList: \n', SubjectPropertyList, '\n')

    SubjectPropertyDataFrame = pd.DataFrame(SubjectPropertyList, columns = ['FirstName','LastName','Address','LastContactDate','NextContactDate','CID'])
    # print('\nSubjectPropertyDataFrame: \n', SubjectPropertyDataFrame, '\n')
    SentDataFrame = pd.concat([SentDataFrame, SubjectPropertyDataFrame],ignore_index=True)
    # print('\nSentDataFrame: \n', SentDataFrame, '\n')

    # CreateFile(SentDataFrame, FileName, TimeStamp=True)
    CreateFileWithTimeStamp(SentDataFrame, GetTimeStamp(), FileName)
    # SendEmail2(SubjectPropertyDataFrame, TotalDataSetFile)

    return SubjectPropertyDataFrame


# ___________________________________________________
def SendEmailWithThreeDFs(DataFrame_1, DataFrame_2, DataFrame_3):
    # SendEmailWithTwoDFs()
    # SendEmailWithTwoDFs(DataFrame_1, DataFrame_2)
    # html_Calls = ClientCalls_DF.to_html()
    # string_Calls = ClientCalls_DF.to_string()

    '''
    html_test = """\
    <html>
      <head></head>
      <body>
        {0}
      </body>
    </html>
    """.format(ClientCalls_DF.to_html())
    '''

    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    message = MIMEMultipart("alternative")


    # food_list = [['A','B'], ['Apple','banana'], ['Fruit','Fruit']]


    '''
    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""

    html = """\
    <html>
      <body>
        <p>Hi,<br>
           How are you?<br>
           <a href="http://www.realpython.com">Real Python</a>
           has many great tutorials.
        </p>
      </body>
    </html>
    """
    '''

    '''
    html = """\
    <html>
      <head></head>
      <body>
        {0}
      </body>
    </html>
    """.format(ClientCalls_DF.to_html())
    '''

    html = """\
    <html>
      <head></head>
      <body>
        <center><h1>CMA</h1></center>
        {0}
        <br><br>
        <center><h1>Handwritten Notes</h1></center>
        {1}
        <br><br>
        <center><h1>Calls To Make</h1></center>
        {2}
      </body>
    </html>
    """.format(DataFrame_1.to_html(),DataFrame_2.to_html(),DataFrame_3.to_html())


    ezgmail.send('tim@bhhspagerealty.com', '(Test) Ninja Max Update', html, mimeSubtype='html')


# ___________________________________________________
def SendEmail(ClientCalls_DF):

    html_Calls = ClientCalls_DF.to_html()
    string_Calls = ClientCalls_DF.to_string()


    html_test = """\
    <html>
      <head></head>
      <body>
        {0}
      </body>
    </html>
    """.format(ClientCalls_DF.to_html())

    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    message = MIMEMultipart("alternative")


    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           How are you?<br>
           <a href="http://www.realpython.com">Real Python</a>
           has many great tutorials.
        </p>
      </body>
    </html>
    """

    html = """\
    <html>
      <head></head>
      <body>
        {0}
      </body>
    </html>
    """.format(ClientCalls_DF.to_html())

    ezgmail.send('tim@bhhspagerealty.com', 'NinjaMax Client Update', html, mimeSubtype='html')




# ___________________________________________________
def main():

    print('\n', '\n', '\n', '\n', '\n', '––––––––––BEGIN––––––––––', '\n', '\n', '\n', '\n', '\n', )


# define a hybrid module
if __name__ == '__main__':
    main()
