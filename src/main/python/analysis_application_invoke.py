import requests
import datetime
import json
import mysql.connector as mysql
import bidict

login_cookie = 'SameSite=none; isg=BFpacDQK6yoanme1EWJMiiUBqQZ8i95lx7ourGTSiu2-1_4RTxt4dcphpyPLHFb9; l=fBIIqffnPRQvg1ZfXO5Bnurza77ToIdcGkPzaNbMiIEGa6TXuFgOwNCT-3ZdadtfgTCj1e-ybJXhzdIsE34NwgfCRbkpO7eEqxAX-etzR; tfstk=eO6XkKVe5NByyWhmPrZPRf-tRc9g0uWbL8n1xMLZ3fpAPds1PxRToK56WaQRgCFc7RwOYaRO3KSVPUTRvhr0os5s5UQR0x8wHF16zN5V015V1V9cUskwurv1XwR_8yyULijDndUU8aELeXJi5Knx1JScm0pT8yyULA_TGVsXY4Zm2Ss7sxDqCOb7I-yVbGXWcQdPm3BREl-WGeIvv3xlFvAXJiLSCgko8eaMgfiWtAKSiuZSsf2u3OwGdeKuRIKk4Sr7VXR6M3xWIuZSsfAvq37LVuGe1; arms_user_parent_id=31320025; SameSite=none; XSRF-TOKEN=92pCgesY; aliyun_site=CN; login_aliyunid="chenhouzhang @ 31320025"; login_aliyunid_pk=31320025; login_aliyunid_sc=3R5H3e3HY2c8gwLZuY5GmS7K.1115sK6FZsPxg7W5Etx5kpWiMHyv27WsuT6FtfQShem7sZ4r.2mWNaj2BsyZpYwwkFUc719rTxHYQWEvykx5boX8cjDFjevZQCG3NUJC4NknN5waAQV; login_aliyunid_ticket=3R5H3e3HY2c8gwLZuY5GmS7J.1118HVvamNjW6jfxET14mBzpHXjUMn8QERKA6JASEaWn9oB6A2nCjCTEYsUDzwugCmzDU1fbrjhxDGmrMuhWrVDy3tnNiPAYLRzBJDjTzpGnxmU9VKrYYkvCZUShq7HJomMgG7UrJGBzabCeGcWunQJpnuUjqx97NEFTif8hkSL3LYsGNeL.2mWNaj2BF4CwGosmk7uTb7GwSGtktcPT4PAHMv9pdKeyupZEoZx9vRycXKMqz9GoRw; login_current_pk=205542499515429257; mfa_skip_cookie=sxDFil3X_Vs2KvTNa32xH2OAR1wRCiBogDONeuf30SAR_Dij0qXf32TUWdbVyp953QjOq2pDZ61J102DEfNqB3Cgwn1Osb*1; login_aliyunid_csrf=_csrf_tk_1030502861506052; login_disaster=master; ORG_ID=6077b956afdac3288fbb56d1; currentRegionId=cn-beijing; aliyun_lang=zh; LOGIN_ALIYUN_PK_FOR_TB=205542499515429257; TEAMBITION_SESSIONID=eyJ1aWQiOiI2NTRjOGMyNTY1NGVhYWRkYzZmNDFlOTkiLCJhdXRoVXBkYXRlZCI6MTcwMjAwMTY2MzExMCwidXNlciI6eyJfaWQiOiI2NTRjOGMyNTY1NGVhYWRkYzZmNDFlOTkiLCJuYW1lIjoi6ZmI5Y6a55KLIiwiZW1haWwiOiJhY2NvdW50c182NTRjOGMyNTY1NGVhYWRkYzZmNDFlOTNAbWFpbC50ZWFtYml0aW9uLmNvbSIsImF2YXRhclVybCI6Imh0dHBzOi8vdGNzLWRldm9wcy5hbGl5dW5jcy5jb20vdGh1bWJuYWlsLzExMno1YzAwNzQ4MDA4MzdjNjgzYmYyM2YxNDRiYTE4NGIyNy93LzEwMC9oLzEwMCIsInJlZ2lvbiI6IiIsImxhbmciOiIiLCJpc1JvYm90IjpmYWxzZSwib3BlbklkIjoiIiwicGhvbmVGb3JMb2dpbiI6IiIsImNyZWF0ZWQiOiIyMDIzLTExLTA5VDA3OjM3OjA5LjU2OVoifSwibG9naW5Gcm9tIjoiIn0=; TEAMBITION_SESSIONID.sig=rKUKec_yO5qlM3kPj1S-JYZH28E; cna=IXPTHdEggWMCAbaWOaSes+l7; t=5246eb89c6547f85bb90e996ee6f7e12'
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
            sql = "INSERT IGNORE INTO `application_invoke_analysis` (`app_name`, `interface_name`, `request_date`, `response_time`, `request_cnt`) VALUES (%s, %s, %s, %s, %s)"
            cursor.executemany(sql, list(
                map(lambda e: (apps.inverse.get(query_data.filters.pid), e['rpc'], query_data.get_date(), int(e['rt']), int(e['count'])),
                    filter(lambda x: "/health" != x['rpc'], j["data"]["data"]))))
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
analysis_date(2023, 12, 15)
# analysis_date(2023, 12, 11, ["payment-service"])
