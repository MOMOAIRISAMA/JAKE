# Mood Weather | 心情天气生成器

这是一个 Python Pygame 数字艺术交互项目骨架。

用户未来可以输入一句心情，程序会根据文字生成动态天气场景。

## 当前版本

第一步只实现最基础的可运行窗口：

- 窗口大小：1000x700
- 窗口标题：Mood Weather
- 背景颜色：浅蓝色
- 按 `ESC` 或 `Q` 退出

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行项目

```bash
python main.py
```

## 文件结构

```text
mood_weather/
├── main.py
├── weather_scene.py
├── particles.py
├── emotion_mapper.py
├── utils.py
├── requirements.txt
├── README.md
├── screenshots/
└── assets/
```

## 下一步计划

后续可以逐步加入：

- 心情文字输入
- 简单情绪分类
- 雨、雪、阳光等基础天气场景
- 粒子动画
- 截图保存
