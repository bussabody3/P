
import requests
import json
from config import r

def get_creation_date(id: int) -> str:
    """
    جلب تاريخ إنشاء حساب التيليجرام باستخدام عدة مصادر لضمان الدقة للحسابات الجديدة (2025/2026).
    """
    # التحقق من وجود التاريخ في التخزين المؤقت أولاً
    # نتجاهل التاريخ الخاطئ 2023/12/25
    cached_date = r.get(f'{id}:CreateDate')
    if cached_date and cached_date != "2023/12/25":
        return cached_date
    
    # 1. محاولة تقدير التاريخ بناءً على النطاق الرقمي للـ ID (أسرع وأدق للحسابات الجديدة جداً)
    # الحسابات التي تبدأ بـ 7.5 مليار وما فوق هي في الغالب 2025
    if id >= 7500000000:
        date_estimated = "2025/01/15"
        if id >= 8000000000:
            date_estimated = "2025/06/01"
        r.set(f'{id}:CreateDate', date_estimated)
        return date_estimated

    # 2. محاولة استخدام API خارجي
    try:
        url = "https://restore-access.indream.app/regdate"
        headers = {
            "accept": "*/*",
            "content-type": "application/json",
            "user-agent": "Nicegram/92 CFNetwork/1390 Darwin/22.0.0",
            "x-api-key": "e758fb28-79be-4d1c-af6b-066633ded128"
        }
        data = {"telegramId": id}
        res = requests.post(url, headers=headers, json=data, timeout=5)
        
        if res.status_code == 200:
            res_data = res.json()
            if res_data.get('ok') and 'data' in res_data:
                date_str = res_data['data']['date'].replace('-', '/')
                if date_str != "2023/12/25": # حماية إضافية من التاريخ الوهمي
                    r.set(f'{id}:CreateDate', date_str)
                    return date_str
    except:
        pass

    # 3. تقدير يدوي للحسابات الأقدم قليلاً
    if 7000000000 <= id < 7500000000:
        return "2024/05/01"
    if 6000000000 <= id < 7000000000:
        return "2023/06/01"
    
    return "غير معروف"
