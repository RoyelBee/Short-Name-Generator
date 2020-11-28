# Import all library
import pandas as pd
import pyodbc as db
import re
import datetime

# server connections
skf_conn = db.connect('DRIVER={SQL Server};'
                      'SERVER=---------;'
                      'DATABASE=ARCHIVESKF;'
                      'UID=------;PWD=-----------')

hnd_conn = db.connect('DRIVER={SQL Server};'
                      'SERVER=--------;'
                      'DATABASE=ARCHND;'
                      'UID=----;PWD=--------')

skf_full_name_query = """SELECT  CustomerInformation.IDCUST,CustomerInformation.NAMECUST,
            CustomerInformation.CUSTYPEDESC, customerinformation.AUDTORG
            from ARCHIVESKF.dbo.CustomerInformation LEFT OUTER JOIN
            ARCHIVESKF.dbo.Customer_ShortName ON Rtrim(ltrim(CustomerInformation.IDCUST)) =
            Rtrim(ltrim(Customer_ShortName.IDCUST))
            AND CustomerInformation.AUDTORG = Customer_ShortName.AUDTORG
            where Customer_ShortName.IDCUST is null
             """

hnd_full_name_query = """ select IDCUST,NAMECUST,CUSTYPEDESC,AUDTORG from CustomerInformation 
                        where IDCUST not in (select IDCUST from Customer_ShortName)
                         """

dag_full_name_query = """ SELECT   [IDCUST],[NAMECUST],[CUSTYPEDESC],[AUDTORG]                    
                        from ARCDAG.dbo.CustomerInformation  where IDCUST not in (select IDCUST from ARCDAG.dbo.Customer_ShortName) """


def Short_Name_Generator(company, full_name_query, conn):
    full_namedf = pd.read_sql_query(full_name_query, conn)

    connection = db.connect('DRIVER={SQL Server};'
                            'SERVER=137.116.139.217;'
                            'DATABASE=ARCHIVESKF;'
                            'UID=sa;PWD=erp@123')

    short_name_pattern = """select * from ShortNamePattern
                            where company = ? """
    patterns = pd.read_sql_query(short_name_pattern, connection, params={company})

    # Convert patterns dataFrame to dictionary
    key = patterns.set_index('actual')['short'].to_dict()

    # Create a new dataFrame and store processed data in it
    df = pd.DataFrame()
    df['short_name'] = full_namedf['NAMECUST'].replace(key, regex=True)
    df['short_custtype'] = full_namedf['CUSTYPEDESC'].replace(key, regex=True)

    # Create a new dataframe for both Full Name and Short Name
    newdf = pd.DataFrame()
    newdf['IDCUST'] = full_namedf.IDCUST.astype(str).str.strip()
    newdf['NAMECUST'] = full_namedf.NAMECUST.str.strip()
    newdf['Short Name'] = df.short_name.str.strip()
    newdf['CUSTYPEDESC'] = full_namedf.CUSTYPEDESC.str.strip()
    newdf['Short Cust Type'] = df.short_custtype.str.strip()
    newdf['AUDTORG'] = full_namedf.AUDTORG.str.strip()

    # Color functions
    def color_negative_red(val):
        color = 'red' if len(val) > 20 else 'black'
        return 'color: %s' % color

    a = newdf.style.applymap(color_negative_red)
    # Save output
    company = patterns.company.iloc[0]
    day = datetime.datetime.now()
    day = day.strftime("%A")
    a.to_excel('./Data/' + company + '_' + day + '_Short_Name_Output.xlsx', index=False)
    print(company, ' Short Name Generated')


Short_Name_Generator('SKF', skf_full_name_query, skf_conn)
Short_Name_Generator('HND', hnd_full_name_query, hnd_conn)
