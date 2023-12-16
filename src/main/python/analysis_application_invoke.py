import requests
import datetime
import json
import mysql.connector as mysql
import bidict

login_cookie = 'SameSite=none; isg=BLW1Lq7dPAhVbFiEIqubCyb4xjdvMmlEpFMxPTfa1Cx5DtcA_IIyFCHIWFI4VYH8; l=fBIIqffnPRQvgRPXXO5BFurza77tNIR0zkPzaNbMiIEGa6_eGF9KMNCTJ1zlPdtfgTCjUe-ybJXhzdQ-K34NwgfCRbkpO7eE4xv9-etzR; tfstk=eaYHk-ve9Owb8SzX6pQI5Q8eWIk9fJ_59LUReaBrbOWsO_ddphXkQdUdpLhBjav6KWEpwQWkEdB689WR2aXkpdpdLLKdU_WwFgIeyDtuEBvFpkLkNzfyaLGCeXsHOB_5zxHvrqdBOG0jzb3xfA0NxakxHV3vOB_5zH3RMoIXfb2h5fYjlgB0gh25z8NSHtOFIrV6W9lNnq6_zz8Gt-B2TuazzFfhYg-l_o7xkz1ZwFq7XM51stBKfhOYUhekgfcg0GsF16oEsfqS-M51sthisoocY11EY; arms_user_parent_id=31320025; SameSite=none; XSRF-TOKEN=88S5sNG3; aliyun_site=CN; login_aliyunid="chenhouzhang @ 31320025"; login_aliyunid_pk=31320025; login_aliyunid_sc=3R5H3e3HY2c8gwLZuY5GmS7K.1115p4xGwFJbApD7EsVk8BhYGYsET1aQMY5iuY2SSDP6zE25.2mWNaj37eRtizt5SsyS835Vw1zyCAyK1LVXpMRGcGHcudVUmmA6HKqb5kRcaX5ESk1; login_aliyunid_ticket=3R5H3e3HY2c8gwLZuY5GmS7J.1118FZViSsDNQ3sNiWw3uxXcg4hLgvWTYnfvyLArq1WpdhVH2cBA3ztFdx9dg5JVE8arNtkFqyWk6tJybJjXDfmWSB8CJJ7LSCL1i7Fne6KrERXQTyy2avg9SW3aBPEt2NwKYHi6V8CrScBiGTYmJjvNadbYXX1CVN9hSyedvr43r9yQxyx.2mWNaj2GuXjaA1VdLSCzy5RHPtCuzQAcXnkZTcQHinmc7syBWCmigFVteMY1rLA8h7; login_current_pk=205542499515429257; mfa_skip_cookie=sxDFil3X_Vs2KvTNa32xH2OAR1wRCiBogDONeuf30SAR_Dij0qXf32TUWdbVyp953QjOq2pDZ61J102DEfNqB3Cgwn1Osb*1; login_aliyunid_csrf=_csrf_tk_1662001045752809; login_disaster=master; currentRegionId=cn-hangzhou; ORG_ID=6077b956afdac3288fbb56d1; cr_token=cd54a8a6-71a6-401c-9ba2-5259b0c35a8a; help_csrf=NMp9j6nEnaQL6q6T6MfENqZw1H4xISJbbM%2BrRRcStmftRWAO0OMUXmO0QoNzreb6hbzIbD3HX8Rw270rPgQdNGh9pJtEwcKhgaYxhrzQBT5ymB6g20wX202bflrQBdV4BYJtn3cIXo%2B%2BFaHZXFrLLg%3D%3D; aliyun_lang=zh; LOGIN_ALIYUN_PK_FOR_TB=205542499515429257; TEAMBITION_SESSIONID=eyJ1aWQiOiI2NTRjOGMyNTY1NGVhYWRkYzZmNDFlOTkiLCJhdXRoVXBkYXRlZCI6MTcwMjAwMTY2MzExMCwidXNlciI6eyJfaWQiOiI2NTRjOGMyNTY1NGVhYWRkYzZmNDFlOTkiLCJuYW1lIjoi6ZmI5Y6a55KLIiwiZW1haWwiOiJhY2NvdW50c182NTRjOGMyNTY1NGVhYWRkYzZmNDFlOTNAbWFpbC50ZWFtYml0aW9uLmNvbSIsImF2YXRhclVybCI6Imh0dHBzOi8vdGNzLWRldm9wcy5hbGl5dW5jcy5jb20vdGh1bWJuYWlsLzExMno1YzAwNzQ4MDA4MzdjNjgzYmYyM2YxNDRiYTE4NGIyNy93LzEwMC9oLzEwMCIsInJlZ2lvbiI6IiIsImxhbmciOiIiLCJpc1JvYm90IjpmYWxzZSwib3BlbklkIjoiIiwicGhvbmVGb3JMb2dpbiI6IiIsImNyZWF0ZWQiOiIyMDIzLTExLTA5VDA3OjM3OjA5LjU2OVoifSwibG9naW5Gcm9tIjoiIn0=; TEAMBITION_SESSIONID.sig=rKUKec_yO5qlM3kPj1S-JYZH28E; ak_user_locale=zh_CN; cna=IXPTHdEggWMCAbaWOaSes+l7; t=5246eb89c6547f85bb90e996ee6f7e12'
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


analysis_yesterday()
# analysis_date(2023, 12, 12)
analysis_date(2023, 12, 11, ["payment-service"])
