"""情绪映射模块。

把用户输入的中文心情文字转换为对应的天气类型。
"""

# 用字典管理天气类型和对应的关键词
EMOTION_KEYWORDS = {
    "sunny": ["开心", "快乐", "幸福", "兴奋", "期待"],
    "rainy": ["难过", "伤心", "失落", "想哭"],
    "foggy": ["焦虑", "压力", "迷茫", "混乱"],
    "storm": ["生气", "烦躁", "愤怒"],
    "starry_night": ["孤独", "安静", "想念"],
    "snowy_night": ["平静", "放松", "治愈"],
    "sunrise": ["希望", "重新开始", "未来", "恢复"],
}


# 没有匹配到关键词时，使用这个默认天气
DEFAULT_WEATHER = "sunrise"


def map_emotion_to_weather(text):
    """根据心情文字返回天气类型字符串。"""
    # 如果传入空内容，也返回默认天气
    if not text:
        return DEFAULT_WEATHER

    # 逐个检查关键词，只要文字里包含某个关键词，就返回对应天气
    for weather_type, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return weather_type

    return DEFAULT_WEATHER


if __name__ == "__main__":
    # 简单测试：直接运行本文件时，会打印几句测试结果
    test_sentences = [
        "今天很开心，感觉一切都很顺利。",
        "我有点难过，好像快要想哭了。",
        "最近压力很大，脑子也很混乱。",
        "现在很安静，我突然有点想念以前。",
        "虽然累，但我相信未来会慢慢恢复。",
        "这是一句没有明显情绪关键词的话。",
    ]

    for sentence in test_sentences:
        weather = map_emotion_to_weather(sentence)
        print(f"{sentence} -> {weather}")
