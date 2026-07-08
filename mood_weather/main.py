import pygame

from emotion_mapper import map_emotion_to_weather
from particles import ParticleSystem
from utils import save_screenshot
from weather_scene import WeatherScene

# 窗口基础设置
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Mood Weather"

# UI 颜色设置
TEXT_COLOR = (34, 42, 58)
SOFT_TEXT_COLOR = (76, 88, 112)
LIGHT_TEXT_COLOR = (248, 250, 255)
TEXT_SHADOW_COLOR = (255, 255, 255)
POSTCARD_BORDER_COLOR = (255, 255, 255)
NOTICE_COLOR = (255, 255, 255)
NOTICE_BG_COLOR = (70, 85, 105)
NOTICE_DURATION = 150  # 保存成功提示显示的帧数，约 2.5 秒

# 天气副标题映射
WEATHER_SUBTITLES = {
    "sunny": "Sunny Mood",
    "rainy": "Rainy Mood",
    "foggy": "Foggy Mood",
    "storm": "Storm Mood",
    "starry_night": "Starry Night Mood",
    "snowy_night": "Snowy Night Mood",
    "sunrise": "Sunrise Mood",
}


def ask_mood_text():
    """在终端询问用户当前心情。"""
    mood_text = input("请输入你现在的心情：")

    # 如果用户直接按回车，给一个简单的默认文字
    if not mood_text:
        mood_text = "我想重新开始"

    return mood_text


def create_weather_scene(mood_text):
    """根据心情文字创建天气场景。"""
    weather_type = map_emotion_to_weather(mood_text)
    scene = WeatherScene(weather_type, mood_text, WINDOW_WIDTH, WINDOW_HEIGHT)
    particles = ParticleSystem(weather_type, WINDOW_WIDTH, WINDOW_HEIGHT)
    return scene, particles


def create_font(size):
    """创建字体对象。"""
    # 微软雅黑通常可以显示中文；如果找不到，Pygame 会自动使用默认字体
    return pygame.font.SysFont("Microsoft YaHei", size)


def handle_events(screen, scene, particles, notice_timer):
    """处理用户输入和窗口事件。"""
    for event in pygame.event.get():
        # 点击窗口关闭按钮时退出
        if event.type == pygame.QUIT:
            return False, scene, particles, notice_timer

        if event.type == pygame.KEYDOWN:
            # 按 ESC 或 Q 时退出
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                return False, scene, particles, notice_timer

            # 按 R 时，回到终端重新输入心情，并创建新的天气场景和粒子系统
            if event.key == pygame.K_r:
                mood_text = ask_mood_text()
                scene, particles = create_weather_scene(mood_text)

            # 按 S 时，保存当前画面截图
            if event.key == pygame.K_s:
                save_screenshot(screen)
                notice_timer = NOTICE_DURATION

        # 鼠标移动时，在鼠标位置添加柔和光轨
        if event.type == pygame.MOUSEMOTION:
            particles.add_mouse_trail(event.pos[0], event.pos[1])

        # 鼠标左键点击时，根据当前天气添加特殊效果
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            particles.add_click_effect(event.pos[0], event.pos[1])

    return True, scene, particles, notice_timer


def draw_text(screen, font, text, x, y, color=TEXT_COLOR, shadow=True):
    """在窗口中绘制一行文字。"""
    if shadow:
        shadow_surface = font.render(text, True, TEXT_SHADOW_COLOR)
        screen.blit(shadow_surface, (x + 2, y + 2))

    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_center_text(screen, font, text, center_x, y, color=TEXT_COLOR):
    """绘制水平居中的文字。"""
    text_surface = font.render(text, True, color)
    shadow_surface = font.render(text, True, TEXT_SHADOW_COLOR)
    x = center_x - text_surface.get_width() // 2
    screen.blit(shadow_surface, (x + 2, y + 2))
    screen.blit(text_surface, (x, y))


def draw_postcard_border(screen):
    """绘制半透明明信片边框。"""
    border_rect = pygame.Rect(28, 28, WINDOW_WIDTH - 56, WINDOW_HEIGHT - 56)

    # 外层柔和白边
    pygame.draw.rect(screen, POSTCARD_BORDER_COLOR, border_rect, width=4, border_radius=14)

    # 内层细线，让画面更像印刷明信片
    inner_rect = border_rect.inflate(-18, -18)
    pygame.draw.rect(screen, (255, 255, 255), inner_rect, width=1, border_radius=10)


def draw_mood_panel(screen, font, mood_text):
    """绘制心情文字区域。"""
    panel_width = 760
    panel_height = 64
    panel_x = (WINDOW_WIDTH - panel_width) // 2
    panel_y = 142

    panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    pygame.draw.rect(panel_surface, (255, 255, 255, 116), (0, 0, panel_width, panel_height), border_radius=18)
    screen.blit(panel_surface, (panel_x, panel_y))

    # 心情文字过长时，简单截断，避免遮挡画面
    display_text = mood_text
    if len(display_text) > 28:
        display_text = display_text[:28] + "..."

    draw_center_text(screen, font, display_text, WINDOW_WIDTH // 2, panel_y + 16, SOFT_TEXT_COLOR)


def draw_action_hint(screen, font):
    """在右下角绘制操作提示。"""
    hint = "S 保存明信片 | R 重新输入 | Q 退出"
    text_surface = font.render(hint, True, LIGHT_TEXT_COLOR)
    padding_x = 18
    padding_y = 10
    box_width = text_surface.get_width() + padding_x * 2
    box_height = text_surface.get_height() + padding_y * 2
    box_x = WINDOW_WIDTH - box_width - 50
    box_y = WINDOW_HEIGHT - box_height - 50

    hint_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    pygame.draw.rect(hint_surface, (36, 45, 60, 130), (0, 0, box_width, box_height), border_radius=12)
    screen.blit(hint_surface, (box_x, box_y))
    screen.blit(text_surface, (box_x + padding_x, box_y + padding_y))


def draw_notice(screen, font):
    """绘制截图保存成功提示。"""
    message = "已保存情绪天气明信片"
    text_surface = font.render(message, True, NOTICE_COLOR)
    padding_x = 18
    padding_y = 10
    box_width = text_surface.get_width() + padding_x * 2
    box_height = text_surface.get_height() + padding_y * 2
    box_x = WINDOW_WIDTH - box_width - 50
    box_y = WINDOW_HEIGHT - box_height - 108

    notice_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    pygame.draw.rect(notice_surface, (*NOTICE_BG_COLOR, 165), (0, 0, box_width, box_height), border_radius=12)
    screen.blit(notice_surface, (box_x, box_y))
    screen.blit(text_surface, (box_x + padding_x, box_y + padding_y))


def draw_ui(screen, title_font, subtitle_font, mood_font, hint_font, notice_font, scene, notice_timer):
    """绘制明信片风格 UI 层。"""
    draw_postcard_border(screen)

    # 顶部标题和天气副标题
    subtitle = WEATHER_SUBTITLES.get(scene.weather_type, "Mood Weather")
    draw_center_text(screen, title_font, "Mood Weather", WINDOW_WIDTH // 2, 62, TEXT_COLOR)
    draw_center_text(screen, subtitle_font, subtitle, WINDOW_WIDTH // 2, 112, SOFT_TEXT_COLOR)

    # 中上方心情文字，不遮挡主体画面
    draw_mood_panel(screen, mood_font, scene.mood_text)

    # 右下角操作提示
    draw_action_hint(screen, hint_font)

    if notice_timer > 0:
        draw_notice(screen, notice_font)


def main():
    """程序入口：读取心情，创建窗口并运行主循环。"""
    # 程序启动时，先从终端读取用户输入
    mood_text = ask_mood_text()

    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    scene, particles = create_weather_scene(mood_text)
    title_font = create_font(44)
    subtitle_font = create_font(25)
    mood_font = create_font(25)
    hint_font = create_font(20)
    notice_font = create_font(23)

    clock = pygame.time.Clock()
    running = True
    notice_timer = 0

    while running:
        running, scene, particles, notice_timer = handle_events(screen, scene, particles, notice_timer)

        scene.update()
        particles.update()

        scene.draw(screen)
        particles.draw(screen)
        draw_ui(screen, title_font, subtitle_font, mood_font, hint_font, notice_font, scene, notice_timer)

        if notice_timer > 0:
            notice_timer -= 1

        # 更新窗口显示
        pygame.display.flip()

        # 控制帧率，避免程序占用过高
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()