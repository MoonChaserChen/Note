import requests
import datetime
import json
import mysql.connector as mysql
import bidict

login_cookie = 'SameSite=none; isg=BMzM0XUtxZ_OwdGvU1zysAfnnyz-BXCv5Rz41iaNAXcYsW67TRUZPyJHUTmJ4qgH; l=fBIIqffnPRQvgaWvXO5IEurza77TaIR0zkPzaNbMiIEGa12JNF1l1NCOMkp5ldtfgTCjUe-ybJXhzdIrd34NwgfCRbkpO7eEzxv9-etzR; tfstk=eetJlk2GvxeRdYVNo03mLBg52tKJ83prcQJ_x6fuRIdvtpbuqpGy9epBgMYkd4kKvLvO-wGPqHdAOsrhK4lrved1gMvlZ6AA9ICxLUYk-DLp1g_er6fl9Mpe6ThijcvyUMSSsfmiz_dBjMMVVzapULSU3fcijcvzvDPbTMR325FQ6upwjTg9zW56Jm7heaCpxs4dVnZGz195Mk62DTFN1L1YAkIrgCATpaVG694-HHaU8a6qZ2rp1zk3fIBAsxj38y7xvtCiH4aU8a6VH1D0hyzFkDC..; arms_user_parent_id=31320025; SameSite=none; XSRF-TOKEN=Hc3yvO6l; aliyun_site=CN; login_aliyunid="chenhouzhang @ 31320025"; login_aliyunid_pk=31320025; login_aliyunid_sc=3R5H3e3HY2c8gwLZuY5GmS7K.1115uSqNkRDey18rj9bM6ibymTRewY2awUCZYJJoavYZC1Wq.2mWNaj2N8886Ub8JRVY36rW7izo8XtjP4U86FXHEuWgr78eYqT1NJJ8yUugjozxZSJ; login_aliyunid_ticket=3R5H3e3HY2c8gwLZuY5GmS7J.1118Ua8zjW6cqX2NnNbRchTP6WtmYJ6ccdrFm8Xy6HsDhwXibTQ4YtHBiodh9ZxfMF36a4cVE3LewPyRwsPkGQQcu4ADvxJB9QgTE5W5auST8mwdXPSMfdSvdHUccGGtr237ZCSPFYiHtZMQSWiGapq3d6fXRgvVMdPKDhgBwyVK1kFXzXM.1QDta7VV2HBsagv54DAQDSdzjaxQazdrGq6aLBhJ2M8SKyVmzDi5udMzAJ8XKcAkz; login_current_pk=205542499515429257; mfa_skip_cookie=sxDFil3X_Vs2KvTNa32xH1beYEmdwOVXiVeciutrNs4R_Dij0qXf32TUWdbVyp953QjOq2pDZ61J102DEfNqB3Cgwn1Osb*1; login_aliyunid_csrf=_csrf_tk_1030502861506052; login_disaster=master; currentRegionId=cn-beijing; _samesite_flag_=true; _tb_token_=5ee0533635e63; cookie2=14e2a2eb9d50ce0422d6df3ee85961b7; t=5246eb89c6547f85bb90e996ee6f7e12; ORG_ID=6077b956afdac3288fbb56d1; LOGIN_ALIYUN_PK_FOR_TB=205542499515429257; TEAMBITION_SESSIONID=eyJ1aWQiOiI2NTRjOGMyNTY1NGVhYWRkYzZmNDFlOTkiLCJhdXRoVXBkYXRlZCI6MTcwMjg3MDE4OTk2MSwidXNlciI6eyJfaWQiOiI2NTRjOGMyNTY1NGVhYWRkYzZmNDFlOTkiLCJuYW1lIjoi6ZmI5Y6a55KLIiwiZW1haWwiOiJhY2NvdW50c182NTRjOGMyNTY1NGVhYWRkYzZmNDFlOTNAbWFpbC50ZWFtYml0aW9uLmNvbSIsImF2YXRhclVybCI6Imh0dHBzOi8vdGNzLWRldm9wcy5hbGl5dW5jcy5jb20vdGh1bWJuYWlsLzExMno1YzAwNzQ4MDA4MzdjNjgzYmYyM2YxNDRiYTE4NGIyNy93LzEwMC9oLzEwMCIsInJlZ2lvbiI6IiIsImxhbmciOiIiLCJpc1JvYm90IjpmYWxzZSwib3BlbklkIjoiIiwicGhvbmVGb3JMb2dpbiI6IiIsImNyZWF0ZWQiOiIyMDIzLTExLTA5VDA3OjM3OjA5LjU2OVoifSwibG9naW5Gcm9tIjoiIn0=; TEAMBITION_SESSIONID.sig=v3xWm3b2Sr507hnc4JOwq9NI6tc; aliyun_lang=zh; cna=IXPTHdEggWMCAbaWOaSes+l7'
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
# analysis_date(2023, 12, 15)
# analysis_date(2023, 12, 11, ["payment-service"])
