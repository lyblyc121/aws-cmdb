import pandas as pd
from pandasql import sqldf

bill = pd.read_csv(
    filepath_or_buffer="/Users/jianxlin/Documents/PythonWorkspace/usage/tmp/abc-aws-billing-detailed-line-items-with-resources-and-tags-ACTS-Ningxia-2020-08.csv.zip")
bill.columns = bill.columns.str.replace(':', '')
bill.rename(columns={"UnBlendedCost": "Cost", "UnBlendedRate": "Rate"}, inplace=True)
bill.fillna("NULL", inplace=True)
usage_start_date = "2020-08-01 00:00:00"
usage_end_date = "2020-09-01 00:00:00"

sql = """
    select sum(Cost) as Rounding
    from bill 
    where RecordType = 'Rounding'
"""
rounding = sqldf(sql, {"bill": bill})
rounding["userproject"] = "aiops"
print(rounding)



def run(_sql=None, _bill=None):
    b = sqldf(_sql, {"bill": _bill})
    pd.set_option('display.max_rows', 10000)  # 具体的行数或列数可自行设置
    pd.set_option('display.max_columns', 100)
    print(b)
    return b


sql = """
    select *
    from bill
    where SubscriptionId = "NULL"

    """ % locals()

print('SubscriptionId = "NULL" ')

run(sql, bill)

"""
"""
