#!/bin/bash
weather_data=$(curl -s "wttr.in/?format=j1" 2>/dev/null)

if [ -n "$weather_data" ]; then
    location=$(echo "$weather_data" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('nearest_area',[{}])[0].get('areaName',[{}])[0].get('value','Unknown'))" 2>/dev/null || echo "未知")
    temp_c=$(echo "$weather_data" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('current_condition',[{}])[0].get('temp_C','N/A'))" 2>/dev/null || echo "N/A")
    desc=$(echo "$weather_data" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('current_condition',[{}])[0].get('weatherDesc',[{}])[0].get('value','N/A'))" 2>/dev/null || echo "N/A")
    humidity=$(echo "$weather_data" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('current_condition',[{}])[0].get('humidity','N/A'))" 2>/dev/null || echo "N/A")
    
    message="🌤️ 当前天气提醒
━━━━━━━━━━━━━━━
📍 位置: $location
🌡️ 温度: ${temp_c}°C
☁️ 天气: $desc
💧 湿度: ${humidity}%"
else
    message="⚠️ 无法获取天气数据，请检查网络连接"
fi

echo "$message"
