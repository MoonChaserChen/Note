import requests
import datetime
import json
import mysql.connector as mysql
import bidict

login_cookie = 'SameSite=none; isg=BDs7nJ3R2sgI1ua6mAl9vYz6yBmlkE-S3hFv4y35eTonjF9uv2Eq4pGKpqzCt6eK; l=fBIIqffnPRQvgZ9aXO5Churza77OfIOcGkPzaNbMiIEGC6EJdkvTumKQVHbpS1tRRLXPgXLk4hyhKaJt_eoUJPDfqZWZwb2zx2GkCeOH4yaIn; tfstk=euHBlcA4P4HaWICh5etZlFGD9gyuq29V9gZ-m0BF2JeLF73Zq7HUL0z-PV0bwH0rTLB-5PkU8DyL5Vim4HDET07S5V0CLTyp-bMsPqiE4XoPPMDslTWe-BmRF7yJuEJ23Dj3E8L41CUZ5Dbz-MIW3Konv82JuEJ2xQ2TFiEcotSDZmdlK9WWTsf6dpa_WAZQ65ozXPz94lNQkDFgjeMTAZ4xvP6RFgJlurTuT_s_iTE1tht1Z_vMLY9ohrEMlWEgbB-6fsP79lq_Eht1Z_VLjluvfh14N; arms_user_parent_id=31320025; SameSite=none; XSRF-TOKEN=tiqD8KjA; aliyun_site=CN; login_aliyunid="chenhouzhang @ 31320025"; login_aliyunid_pk=31320025; login_aliyunid_sc=3R5H3e3HY2c8gwLZuY5GmS7K.1115x43B5wmFe81DHqF4pz1S9kQvFDteHhthAkNCYfg89Joo.2mWNaj325Eddx9X9heSkdnJWDr8BKFXnh1iboVMgFxenXAsXApfxry31P8fpkep7wj; login_aliyunid_ticket=3R5H3e3HY2c8gwLZuY5GmS7J.1118fqzB5oe946foee7scR45Dap3SYQsxeMrpwdrbwDGgviQQ73cb6CYyMKJenHjKDGEu68VX3LMQwgjCAgNt4QUfwtCSMgumDEPZs5oPUtCNAMNfSXzJ9WyxeaRamvLUhZHApQyU6UbWZBZj6ZWjNF9EQhcK6Qe7awCEu79ngyutwYQm3m.2mWNaj2wpfE6Xagz8fgVE2hAHezWyCn9kNg2aKdawJzRzX9ny9Ls56nWA345bXyibK; login_current_pk=205542499515429257; login_aliyunid_csrf=_csrf_tk_1700103466329810; login_disaster=master; ORG_ID=6077b956afdac3288fbb56d1; LOGIN_ALIYUN_PK_FOR_TB=205542499515429257; TEAMBITION_SESSIONID=eyJ1aWQiOiI2NTRjOGMyNTY1NGVhYWRkYzZmNDFlOTkiLCJhdXRoVXBkYXRlZCI6MTcwMzI5Mzk0ODYzMywidXNlciI6eyJfaWQiOiI2NTRjOGMyNTY1NGVhYWRkYzZmNDFlOTkiLCJuYW1lIjoi6ZmI5Y6a55KLIiwiZW1haWwiOiJhY2NvdW50c182NTRjOGMyNTY1NGVhYWRkYzZmNDFlOTNAbWFpbC50ZWFtYml0aW9uLmNvbSIsImF2YXRhclVybCI6Imh0dHBzOi8vdGNzLWRldm9wcy5hbGl5dW5jcy5jb20vdGh1bWJuYWlsLzExMno1YzAwNzQ4MDA4MzdjNjgzYmYyM2YxNDRiYTE4NGIyNy93LzEwMC9oLzEwMCIsInJlZ2lvbiI6IiIsImxhbmciOiIiLCJpc1JvYm90IjpmYWxzZSwib3BlbklkIjoiIiwicGhvbmVGb3JMb2dpbiI6IiIsImNyZWF0ZWQiOiIyMDIzLTExLTA5VDA3OjM3OjA5LjU2OVoifSwibG9naW5Gcm9tIjoiIn0=; TEAMBITION_SESSIONID.sig=HYn2MITa4foWzA3SWHBuUmxqypQ; aliyun_choice=CN; mfa_skip_cookie=sxDFil3X_Vs2KvTNa32xH1beYEmdwOVXiVeciutrNs4R_Dij0qXf32TUWdbVyp953QjOq2pDZ61J102DEfNqB3Cgwn1Osb*1; c_csrf_token=bd8e479c-1de1-f94a-ff5c-54ed6b940131; currentRegionId=cn-beijing; t=5246eb89c6547f85bb90e996ee6f7e12; aliyun_lang=zh; cna=IXPTHdEggWMCAbaWOaSes+l7'
url = "https://arms.console.aliyun.com/api/trace.json?action=TraceAction&eventSubmitDoGetDatas=1&source=nil"
headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8", "Cookie": login_cookie}
apps = bidict.bidict({
    "voucher-service": "inaop@b245f0483fb7500",
    "voucher-task-service": "inaop@b0aad5e0aead514",
    "order-service": "inaop@18456e5eec96ef2",
    "payment-service": "inaop@f5efc9eee2cd94b"
})


class QueryFilters:
    def __init__(self, pid):
        self.regionId = "cn-beijing"
        self.pid = pid


class QueryData:
    def __init__(self, start_time, end_time, pid):
        self.dimensions = ["rpc"]
        self.metric = ""
        self.measures = []
        self.intervalMillis = 2147483647
        self.startTime = start_time
        self.endTime = end_time
        self.filters = QueryFilters(pid)

    @staticmethod
    def of_yesterday(_app):
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)
        start = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
        end = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59)
        return QueryData(int(start.timestamp() * 1000), int(end.timestamp() * 1000), apps[_app])

    @staticmethod
    def of_date(year, month, day, app):
        start = datetime.datetime(year, month, day, 0, 0, 0)
        end = datetime.datetime(year, month, day, 23, 59, 59)
        return QueryData(int(start.timestamp() * 1000), int(end.timestamp() * 1000), apps[app])

    def get_date(self):
        return datetime.datetime.fromtimestamp(self.startTime / 1000)

    def init_invoke(self):
        self.metric = "appstat.incall"
        self.measures = ["rt", "count", "error"]

    def init_exception(self):
        self.metric = "appstat.exception"
        self.measures = ["count"]

    def __str__(self):
        return "query=" + json.dumps(self, default=lambda o: o.__dict__)


class ApplicationInvokeAnalysis:
    def __init__(self):
        self.app_name = None
        self.interface_name = None
        self.request_date = None
        self.response_time = None
        self.request_cnt = None
        self.error_cnt = 0
        self.exception_cnt = 0

    def to_tuple(self):
        return self.app_name, self.interface_name, self.request_date, self.response_time, self.request_cnt, self.error_cnt, self.exception_cnt


def execute_and_save(query_data: QueryData):
    query_data.init_invoke()
    r1 = requests.post(url, headers=headers, data=str(query_data))
    j1 = json.loads(r1.text)
    query_data.init_exception()
    r2 = requests.post(url, headers=headers, data=str(query_data))
    j2 = json.loads(r2.text)

    aia_list = []
    for e in j1["data"]["data"]:
        if e['rpc'] == '/health':
            continue
        aia = ApplicationInvokeAnalysis()
        aia.app_name = apps.inverse.get(query_data.filters.pid)
        aia.interface_name = e['rpc']
        aia.request_date = query_data.get_date()
        aia.request_cnt = int(e['count'])
        aia.response_time = int(e['rt'])
        if e.get('error'):
            aia.error_cnt = e['error']
        for ele in j2["data"]["data"]:
            if e['rpc'] == ele['rpc']:
                aia.exception_cnt = int(ele['count']) if ele.get('count') else 0
        aia_list.append(aia)

    connection = mysql.connect(host='localhost',
                               port=3306,
                               user='root',
                               password='root',
                               database='akira',
                               charset='utf8mb4',
                               auth_plugin='mysql_native_password')

    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO `application_invoke_analysis` (`app_name`, `interface_name`, `request_date`, `response_time`, `request_cnt`, `error_cnt`, `exception_cnt`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            l = list(map(lambda x: x.to_tuple(), aia_list))
            cursor.executemany(sql, l)
        connection.commit()


def analysis_yesterday():
    for app in apps:
        query_data = QueryData.of_yesterday(app)
        execute_and_save(query_data)


def analysis_date(year, month, day, ana_apps=apps.keys()):
    for app in ana_apps:
        query_data = QueryData.of_date(year, month, day, app)
        execute_and_save(query_data)


# analysis_yesterday()
# analysis_date(2023, 12, 23)
analysis_date(2023, 12, 25, ["voucher-service"])
