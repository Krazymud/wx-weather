import json
from datetime import date
from datetime import datetime, timedelta

from lunardate import LunarDate
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage
import requests
import os

# START_DATE 哪天在一起的，格式：YYYY-MM-DD,示例："2021-03-14"
# APP_KEY 和风天气key，需去和风天气申请
# BIRTHDAY 生日,格式：YYYY-MM-DD，示例："2025-02-02"
# APP_ID 微信公众号的appid
# APP_SECRET 微信公众号app_secret
# USER_IDS 微信公众号的user_id,多个用;（分号）隔开，示例："xxx;xxx"
# TEMPLATE_ID_NIGHT 白天模板id
# TEMPLATE_ID_NIGHT 晚上模板id
# NAME 呢称，示例："小A"
# CITY 城市,示例："北京"
# 和风天气的url格式https://your_api_host/geo/v2/city/lookup

# 哪天在一起的
start_date = 'START_DATE'
# 和风天气key
appKey = '7f0d029f0a2d46f680275879139f8e81'
# 生日
birthday = '1998-06-06'
# 微信公众号的appid和app_secret
app_id = "wx8ca13ecd97e07749"
app_secret = "bd0a64c5716f7478ade3c235ba5f9c73"
# 微信公众号的user_id,多个用;（分号）隔开
user_ids = "ollgl3OQx5INiRKhdovFPsJmD9GQ"
# 白天模板id
template_id_day = "lVE0caMOKtpX1ewQhhCE1XwPKyTGbtimeg4ylGaCXAc"
# 晚上模板id
template_id_night = "lVE0caMOKtpX1ewQhhCE1XwPKyTGbtimeg4ylGaCXAc"
# 呢称
name = '宝宝'
# 城市
city = '汕尾市'
#deepseek prompt“
prompt = '生成一句不落俗套的描写关于爱情、情侣的文案，精炼有趣，文字中不要直接出现“爱情、情侣”。返回的答案只提供句子，不要说其他任何内容'
deepseek_api_key = 'sk-5df9ef28aca241bbbbc2fef869cdd927'

# 当前时间
today = datetime.now()
# YYYY年MM月DD日
today_date = today.strftime("%Y年%m月%d日")



# 构建请求体
headers = {"Content-Type": "application/x-www-form-urlencoded"}
params = {
    "key": appKey,
    "location": city
}
print(params)
# 根据城市名查找地理位置
url = "https://m96mthd8c3.re.qweatherapi.com/geo/v2/city/lookup"

resp = requests.get(url, params=params, headers=headers)
if resp.status_code == 200:
    print("Status Code:", resp.status_code)  # 应该是 200
    print("Response Text:", resp.text)  # 查看返回的内容
    resp_json = json.loads(requests.get(url, params, headers=headers).text)
else:
    print("Status Code:", resp.status_code) 
    exit(1)  # 退出程序或处理错误

city_id = resp_json["location"][0]["id"]
params["location"] = city_id

# 根据城市地理位置获取当前实时天气
url = "https://m96mthd8c3.re.qweatherapi.com/v7/weather/now"
realtime_json = json.loads(requests.get(url, params, headers=headers).text)
# 实时天气状况
realtime = realtime_json["now"]
# 当前温度 拼接 当前天气
now_temperature = realtime["temp"] + "度 " + realtime["text"]

# 根据城市地理位置获取3天天气状况
url = "https://m96mthd8c3.re.qweatherapi.com/v7/weather/3d"
day_forecast_json = json.loads(requests.get(url, params, headers=headers).text)

# -----------------------今天天气状况-----------------------------
# 天气状况
day_forecast_today = day_forecast_json["daily"][0]
# 日出时间
day_forecast_today_sunrise = day_forecast_today["sunrise"]
# 日落时间
day_forecast_today_sunset = day_forecast_today["sunset"]
# 天气
day_forecast_today_weather = day_forecast_today["textDay"]
# 最低温度
day_forecast_today_temperature_min = day_forecast_today["tempMin"]+"度"
# 最高温度
day_forecast_today_temperature_max = day_forecast_today["tempMax"]+"度"
# 夜间天气
day_forecast_today_night = day_forecast_today["textNight"]
# 白天风向
day_forecast_today_windDirDay = day_forecast_today["windDirDay"]
# 夜间风向
day_forecast_today_windDirNight = day_forecast_today["windDirNight"]
# 风力等级
day_forecast_today_windScaleDay = day_forecast_today["windScaleDay"]
# -----------------------今天天气状况-----------------------------


# -----------------------明天天气状况-----------------------------
# 天气状况
day_forecast_tomorrow = day_forecast_json["daily"][1]
# 天气
day_forecast_tomorrow_weather = day_forecast_tomorrow["textDay"]
# 日出时间
day_forecast_tomorrow_sunrise = day_forecast_tomorrow["sunrise"]
# 日落时间
day_forecast_tomorrow_sunset = day_forecast_tomorrow["sunset"]
# 最低温度
day_forecast_tomorrow_temperature_min = day_forecast_tomorrow["tempMin"] + "℃"
# 最高温度
day_forecast_tomorrow_temperature_max = day_forecast_tomorrow["tempMax"] + "℃"
# 夜间天气
day_forecast_tomorrow_night = day_forecast_today["textNight"]
# 白天风向
day_forecast_tomorrow_windDirDay = day_forecast_today["windDirDay"]
# 夜间风向
day_forecast_tomorrow_windDirNight = day_forecast_today["windDirNight"]
# 风力等级
day_forecast_tomorrow_windScaleDay = day_forecast_today["windScaleDay"]
# -----------------------明天天气状况-----------------------------


# -----------------------后天天气状况-----------------------------
# 天气状况
day_forecast_T2 = day_forecast_json["daily"][2]
# 天气
day_forecast_T2_textDay = day_forecast_T2["textDay"]
# 最低温度
day_forecast_T2_temperature_min = day_forecast_T2["tempMin"] + "℃"
# 最高温度
day_forecast_T2_temperature_max = day_forecast_T2["tempMax"] + "℃"
# -----------------------后天天气状况-----------------------------


# 距离春节还有多少天
def days_until_spring_festival(year=None):
    """
    计算距离下一个春节还有多少天。
    如果未提供年份，则默认为当前年份。
    """
    if year is None:
        year = datetime.now().year  # 获取当前年份

    # 获取当年春节的日期（农历正月初一转换为公历）
    spring_festival_lunar = LunarDate(year, 1, 1)
    spring_festival_solar = spring_festival_lunar.toSolarDate()

    # 获取当前日期
    today = datetime.now().date()

    # 计算差值，注意需要将日期转换为同类型的对象才能相减
    days_until = (spring_festival_solar - today).days

    # 如果春节已经过去，则计算到下一年的春节
    if days_until <= 0:
        days_until = days_until_spring_festival(year + 1)

    return days_until


# 在一起多天计算
def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days+1


# 生日计算
def get_birthday():
    # 从生日字符串中提取月份和日期
    month_day = birthday[5:]  # 获取 "06-08" 部分
    next = datetime.strptime(f"{date.today().year}-{month_day}", "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


# 彩虹屁接口
def get_words():
    url = "https://api.deepseek.com/chat/completions"

    payload = json.dumps({
        "messages": [
        {
            "content": "You are a helpful assistant",
            "role": "system"
        },
        {
            "content": prompt,
            "role": "user"
        }
        ],
        "model": "deepseek-v4-pro",
        "thinking": {
            "type": "enabled"
        },
        "reasoning_effort": "high",
        "max_tokens": 4096,
        "response_format": {
        "type": "text"
        },
        "stop": None,
        "stream": False,
        "stream_options": None,
        "temperature": 1,
        "top_p": 1,
        "tools": None,
        "tool_choice": "none",
        "logprobs": False,
        "top_logprobs": None
        })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f"Bearer {deepseek_api_key}"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text
    #words = requests.get("https://api.shadiao.pro/chp")
    #if words.status_code != 200:
    #    return get_words()
    #text = words.json()['data']['text']
    #return text
    # 按照20个字符分割字符串
    # chunk_size = 20
    # split_notes = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    # 分配note N 如果split_notes元素少于5，则用空字符串填充
    # [note1, note2, note3, note4, note5] = (split_notes + [""] * 5)[:5]
    # return note1, note2, note3, note4, note5


if __name__ == '__main__':
    # 获取微信客户端
    client = WeChatClient(app_id, app_secret)

    # 获取微信模板消息接口
    wm = WeChatMessage(client)

    # 获取彩虹屁
    note = get_words()

    # 获取当前UTC时间
    now_utc = datetime.utcnow()
    # 转换为北京时间（UTC+8）
    beijing_time = now_utc + timedelta(hours=8)
    # 获取当前小时数
    hour_of_day = beijing_time.hour
    # 默认发当天
    strDay = "today"
    # 如果当前时间大于15点，也就是晚上，则发送明天天气
    # if hour_of_day > 15:
    #    strDay = "tomorrow"
    #    template_id_day = template_id_night

    print("当前时间：" + str(beijing_time)+"即将推送："+strDay+"信息")

    data = {"name": {"value": name},
            "today": {"value": today_date},
            "city": {"value": city},
            "weather": {"value": globals()[f'day_forecast_{strDay}_weather']},
            "now_temperature": {"value": now_temperature},
            "min_temperature": {"value": globals()[f'day_forecast_{strDay}_temperature_min']},
            "max_temperature": {"value": globals()[f'day_forecast_{strDay}_temperature_max']},
            "love_date": {"value": "待定！"},
            "birthday": {"value": str(get_birthday())+"天"},
            "diff_date1": {"value": str(days_until_spring_festival())+"天"},
            "sunrise": {"value": globals()[f'day_forecast_{strDay}_sunrise']},
            "sunset": {"value": globals()[f'day_forecast_{strDay}_sunset']},
            "textNight": {"value": globals()[f'day_forecast_{strDay}_night']},
            "windDirDay": {"value": globals()[f'day_forecast_{strDay}_windDirDay']},
            "windDirNight": {"value": globals()[f'day_forecast_{strDay}_windDirNight']},
            "windScaleDay": {"value": globals()[f'day_forecast_{strDay}_windScaleDay']},
            "note": {"value": note}
            }
    # print(data)

    # 拆分user_ids
    user_ids = user_ids.split(";")
    for e in user_ids:
        print(e)
        res = wm.send_template(e, template_id_day, data)
        print(res)
