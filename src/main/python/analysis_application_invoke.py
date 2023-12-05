import requests
import datetime
import json
import mysql.connector as mysql
import bidict

login_cookie = 'SameSite=none; isg=BO_vi1PK1ghPxdIWdI0B2ZjGfAX5lEO2Sl07DwF8qN5lUA5SCmT6BkRG0sDuMxsu; l=fBIIqffnPRQvgAZwBOfChurza779AIdbYuPzaNbMi9fP_r_J5CfcW1Eev-dvCn1VestD83-aK9byBLyJqP5R7-5zKdGItC0Z3dLHR3zC.; tfstk=eE6WjjNwRwBV2fholzZV5YCsyjJn2awaPDtdjMHrvLpJdBQVxBByUM8dRZb69ubFaJHdlEWyzgJJdMQ2eBfy8U8BdMb6VPyaQgjkKLUa7RPOoM4vp9p2TPIlqpm07PyaQgDClJPcx9cjsraCVWDoUv94jXzsllrNhnLHSa92mnWXJQLTIEMp0ttWNFI54U0w5yArOmOipnGucoGnt-2PdJX6Wn46wnx4aoZj_BOJmn93coGntQKD0NEbcfRC.; arms_user_parent_id=31320025; SameSite=none; XSRF-TOKEN=sxvtyUt4; aliyun_site=CN; login_aliyunid="chenhouzhang @ 31320025"; login_aliyunid_pk=31320025; login_aliyunid_sc=3R5H3e3HY2c8gwLZuY5GmS7K.1115vwDKiwGsUF7bV41gcmQucqqT4kqxsCbZ2cgngxqkp7z1.2mWNaj2owJrbmLKNMJmSC9ET9hjg3ronohWA5EkC7bRheA69Ght1XVHjoTu22VTDVs; login_aliyunid_ticket=3R5H3e3HY2c8gwLZuY5GmS7J.1118FLbBit88eciSLsSR4enxHHzzZmH7EtTG2Pt3eLUGzL19MTWLLibTvR147DgYnkkgkCyVuqADoioawoppDMm2QRDx78QxFBEkf2SDCZeguuqC1zdjsbK3wkz1bcSG2GJF2GjfMQ8R2LGU61LaP6qGtBmP4FbwXhoyxxH23MoYiH48yB3.2mWNaj25y9DYqQLgJPHpZFduhwTLLAfJmPKTmD1tvUAjTmbarMLx2PgzttGrnPEW7X; login_current_pk=205542499515429257; mfa_skip_cookie=sxDFil3X_Vs2KvTNa32xHyyVWN1GwpNvhO7Dfwlj0koR_Dij0qXf32TUWdbVyp953QjOq2pDZ61J102DEfNqB3Cgwn1Osb*1; login_aliyunid_csrf=_csrf_tk_1662001045752809; login_disaster=master; ORG_ID=6077b956afdac3288fbb56d1; LOGIN_ALIYUN_PK_FOR_TB=205542499515429257; TEAMBITION_SESSIONID=eyJ1aWQiOiI2NTRjOGMyNTY1NGVhYWRkYzZmNDFlOTkiLCJhdXRoVXBkYXRlZCI6MTcwMTY1NTU5ODc1OSwidXNlciI6eyJfaWQiOiI2NTRjOGMyNTY1NGVhYWRkYzZmNDFlOTkiLCJuYW1lIjoi6ZmI5Y6a55KLIiwiZW1haWwiOiJhY2NvdW50c182NTRjOGMyNTY1NGVhYWRkYzZmNDFlOTNAbWFpbC50ZWFtYml0aW9uLmNvbSIsImF2YXRhclVybCI6Imh0dHBzOi8vdGNzLWRldm9wcy5hbGl5dW5jcy5jb20vdGh1bWJuYWlsLzExMno1YzAwNzQ4MDA4MzdjNjgzYmYyM2YxNDRiYTE4NGIyNy93LzEwMC9oLzEwMCIsInJlZ2lvbiI6IiIsImxhbmciOiIiLCJpc1JvYm90IjpmYWxzZSwib3BlbklkIjoiIiwicGhvbmVGb3JMb2dpbiI6IiIsImNyZWF0ZWQiOiIyMDIzLTExLTA5VDA3OjM3OjA5LjU2OVoifSwibG9naW5Gcm9tIjoiIn0=; TEAMBITION_SESSIONID.sig=rYD24o0_P1CV3jmiReM2c6D2sNQ; ak_user_locale=zh_CN; currentRegionId=cn-beijing; aliyun_lang=zh; cna=IXPTHdEggWMCAbaWOaSes+l7; t=5246eb89c6547f85bb90e996ee6f7e12'
url = "https://arms.console.aliyun.com/api/trace.json?action=TraceAction&eventSubmitDoGetDatas=1&source=nil"
headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8", "Cookie": login_cookie}
apps = bidict.bidict({
    "voucher-service": "inaop@b245f0483fb7500",
    "voucher-task-service": "inaop@b0aad5e0aead514"
})


class QueryFilters:
    def __init__(self, pid):
        self.regionId = "cn-beijing"
        self.pid = pid


class QueryData:
    def __init__(self, start_time, end_time, pid):
        self.dimensions = ["rpc"]
        self.metric = "appstat.incall"
        self.measures = ["rt", "count", "error"]
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

    def __str__(self):
        return "query=" + json.dumps(self, default=lambda o: o.__dict__)


def execute_and_save(query_data):
    r = requests.post(url, headers=headers, data=str(query_data))
    j = json.loads(r.text)

    connection = mysql.connect(host='localhost',
                               port=3306,
                               user='root',
                               password='root',
                               database='akira',
                               charset='utf8mb4',
                               auth_plugin='mysql_native_password')

    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `application_invoke_analysis` (`app_name`, `interface_name`, `request_date`, `response_time`, `request_cnt`) VALUES (%s, %s, %s, %s, %s)"
            cursor.executemany(sql, list(
                map(lambda e: (apps.inverse.get(query_data.filters.pid), e['rpc'], query_data.get_date(), int(e['rt']), int(e['count'])),
                    filter(lambda x: "/health" != x['rpc'], j["data"]["data"]))))
        connection.commit()


def analysis_yesterday():
    for app in apps:
        query_data = QueryData.of_yesterday(app)
        execute_and_save(query_data)


def analysis_date(year, month, day, app):
    query_data = QueryData.of_date(year, month, day, app)
    execute_and_save(query_data)


analysis_yesterday()
# analysis_date(2023, 12, 3, "voucher-service")
