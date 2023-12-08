'''
cd ~/.virtualenvs/ClientCallTracker/VirtualEnvironment
source venv/bin/activate
python3 ~/.virtualenvs/ClientCallTracker/VirtualEnvironment/ProjectFiles/NinjaLogRunner.py

'''

import NinjaLogLib

def main():
    print('\n', '\n', '\n', '\n', '\n', '––––––––––BEGIN––––––––––', '\n', '\n', '\n', '\n', '\n', )

    NinjaLogLib.fixCSV_March_3_2023()

    '''
    # time = NinjaLogLib.GetTimeStamp()
    # x = NinjaLogLib.readFile('KvCoreValuations')
    # NinjaLogLib.IterateDataFrame(x, time)
    # x,y = NinjaLogLib.IterateDataFrame(x, time)
    # NinjaLogLib.SendEmail(x)
    # NinjaLogLib.SendEmail(y)

    # DataFrame_1 = NinjaLogLib.Bookmark_IterateDataFrame(1, 'TestData_11-25-22', 'Test_CMAs_Sent_11-25-22')
    # DataFrame_2 = NinjaLogLib.Bookmark_IterateDataFrame(3, 'TestHandwrittenNotes', 'TestHandwrittenNotes_Ledger')

    # NinjaLogLib.Combine_csv_files('KvCoreValuations','CMA_List')
    # NinjaLogLib.MultipleAddressColumnsIntoSingle('CMA_List')


    # DataFrame_1 = NinjaLogLib.Bookmark_IterateDataFrame(1, 'MasterCMA_List', 'ContinuousOngoing_CMAs_Sent_')
    # DataFrame_2 = NinjaLogLib.Bookmark_IterateDataFrame(3, 'MasterHandwrittenNote_List', 'ContinuousOngoing_HandwrittenNotes_Sent_')    # use Call list for handwritten note list
    # DataFrame_2 = NinjaLogLib.Bookmark_IterateDataFrame(3, 'Continuous-Ongoing-Input-Save', 'ContinuousOngoing_HandwrittenNotes')
    # DataFrame_3 = NinjaLogLib.IterateDataFrame('ContinuousOngoing_Calls_Made_')
    DataFrame = NinjaLogLib.IterateDataFrame('ContinuousOngoing_NinjaMaxCRM_')
    # DataFrame = NinjaLogLib.IterateDataFrame('ContinuousOngoing_NinjaMax_TestData_')


    # DataFrame = NinjaLogLib.IterateDataFrame('Continuous-Ongoing-Input-Save')
    # print('\n DataFrame_3: \n', DataFrame_3, '\n')

    # NinjaLogLib.SendEmailWithTwoDFs(DataFrame_1, DataFrame_2)
    # NinjaLogLib.SendEmailWithThreeDFs(DataFrame_1, DataFrame_2, DataFrame_3)
    NinjaLogLib.SendEmail(DataFrame)

    # EmailDataFrame = NinjaLogLib.CombineDFsForEmail(DataFrame_1,DataFrame_2)
    # NinjaLogLib.SendEmail2(EmailDataFrame, 'Combined DataFrames')


    # NinjaLogLib.MultipleAddressColumnsIntoSingle()
    # NinjaLogLib.CreateFileWithTimeStamp(x, time)
    '''


    print('\n', '\n', '\n', '\n', '\n', '––––––––––END––––––––––', '\n', '\n', '\n', '\n', '\n', )

main()
# define a hybrid module
# if __name__ == '__main__':
#     main()
#






# — — — — — — — — — — — — — — — — — — — — — — — — Notes
