"""天气场景模块。

这里负责根据天气类型绘制基础背景。
当前阶段只使用 Pygame 基础图形，不依赖外部图片。
"""

import random

import pygame


class WeatherScene:
    """天气场景类：保存天气信息，并负责更新和绘制画面。"""

    def __init__(self, weather_type, mood_text, screen_width, screen_height):
        """初始化天气场景。"""
        self.weather_type = weather_type
        self.mood_text = mood_text
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.frame_count = 0

        # 为星空提前生成固定星星，避免每一帧闪烁得太乱
        self.stars = self._create_stars(80)

    def update(self):
        """更新场景状态。"""
        self.frame_count += 1

    def draw(self, screen):
        """根据天气类型绘制画面。"""
        if self.weather_type == "sunny":
            self._draw_sunny(screen)
        elif self.weather_type == "rainy":
            self._draw_rainy(screen)
        elif self.weather_type == "foggy":
            self._draw_foggy(screen)
        elif self.weather_type == "storm":
            self._draw_storm(screen)
        elif self.weather_type == "starry_night":
            self._draw_starry_night(screen)
        elif self.weather_type == "snowy_night":
            self._draw_snowy_night(screen)
        elif self.weather_type == "sunrise":
            self._draw_sunrise(screen)
        else:
            # 其他天气类型暂时使用 sunrise 作为柔和默认背景
            self._draw_sunrise(screen)

    def _draw_vertical_gradient(self, screen, top_color, bottom_color):
        """绘制从上到下的竖向渐变背景。"""
        for y in range(self.screen_height):
            ratio = y / self.screen_height
            color = self._mix_color(top_color, bottom_color, ratio)
            pygame.draw.line(screen, color, (0, y), (self.screen_width, y))

    def _draw_ground(self, screen, color, height):
        """绘制地面。"""
        ground_y = self.screen_height - height
        pygame.draw.rect(screen, color, (0, ground_y, self.screen_width, height))

    def _draw_cloud(self, screen, x, y, color, scale=1.0):
        """用几个圆形拼出柔软的云。"""
        x = int(x)
        y = int(y)
        parts = [
            (0, 18, 42),
            (35, 5, 48),
            (78, 18, 42),
            (42, 25, 55),
        ]
        for offset_x, offset_y, radius in parts:
            center = (int(x + offset_x * scale), int(y + offset_y * scale))
            pygame.draw.circle(screen, color, center, int(radius * scale))

        rect = pygame.Rect(int(x), int(y + 20 * scale), int(115 * scale), int(38 * scale))
        pygame.draw.rect(screen, color, rect, border_radius=int(18 * scale))

    def _draw_transparent_cloud(self, screen, x, y, color, alpha, scale=1.0):
        """绘制带透明度的云雾。"""
        width = int(150 * scale)
        height = int(90 * scale)
        cloud_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        local_color = (*color, alpha)
        self._draw_cloud(cloud_surface, 18 * scale, 10 * scale, local_color, scale)
        screen.blit(cloud_surface, (int(x), int(y)))

    def _draw_sunny(self, screen):
        """绘制晴天：蓝色渐变天空、太阳、白云、草地。"""
        self._draw_vertical_gradient(screen, (139, 202, 246), (216, 239, 255))

        pygame.draw.circle(screen, (255, 224, 128), (820, 130), 72)
        pygame.draw.circle(screen, (255, 239, 176), (820, 130), 48)

        self._draw_cloud(screen, 120, 125, (250, 252, 255), 1.0)
        self._draw_cloud(screen, 455, 90, (245, 250, 255), 0.85)
        self._draw_cloud(screen, 680, 230, (248, 252, 255), 0.75)

        self._draw_ground(screen, (145, 212, 142), 145)
        pygame.draw.ellipse(screen, (119, 195, 126), (-120, 545, 520, 190))
        pygame.draw.ellipse(screen, (132, 205, 137), (520, 535, 620, 210))

    def _draw_rainy(self, screen):
        """绘制雨天：蓝灰天空、深色云、暗色地面。"""
        self._draw_vertical_gradient(screen, (114, 139, 164), (174, 190, 204))

        self._draw_cloud(screen, 90, 105, (91, 106, 128), 1.25)
        self._draw_cloud(screen, 350, 80, (82, 98, 120), 1.35)
        self._draw_cloud(screen, 665, 115, (96, 111, 132), 1.15)

        pygame.draw.rect(screen, (133, 151, 171), (0, 250, self.screen_width, 70))

        self._draw_ground(screen, (91, 105, 107), 155)
        pygame.draw.rect(screen, (76, 88, 91), (0, self.screen_height - 88, self.screen_width, 88))

    def _draw_foggy(self, screen):
        """绘制雾天：灰蓝紫天空、慢速云层、朦胧地面。"""
        self._draw_vertical_gradient(screen, (125, 141, 176), (198, 204, 218))

        # 云层缓慢横向移动，营造迷茫和压力感
        cloud_offset = (self.frame_count * 0.25) % (self.screen_width + 220)
        cloud_positions = [(-180, 110, 1.35), (160, 80, 1.15), (520, 130, 1.25), (850, 95, 1.1)]
        for x, y, scale in cloud_positions:
            moved_x = x + cloud_offset
            if moved_x > self.screen_width + 80:
                moved_x -= self.screen_width + 420
            self._draw_transparent_cloud(screen, moved_x, y, (232, 236, 244), 118, scale)

        # 远处模糊山影
        pygame.draw.polygon(screen, (132, 145, 169), [(0, 520), (180, 395), (360, 520), (520, 420), (710, 520), (1000, 430), (1000, 700), (0, 700)])
        pygame.draw.polygon(screen, (151, 162, 184), [(0, 560), (240, 460), (460, 560), (690, 455), (1000, 565), (1000, 700), (0, 700)])

        # 半透明雾带，横向漂浮的主体由 particles.py 处理，这里画底层雾感
        for index, y in enumerate((315, 390, 470)):
            alpha = 70 - index * 10
            fog_surface = pygame.Surface((self.screen_width, 70), pygame.SRCALPHA)
            pygame.draw.rect(fog_surface, (235, 240, 247, alpha), (0, 12, self.screen_width, 42), border_radius=22)
            screen.blit(fog_surface, (0, y))

        self._draw_ground(screen, (121, 136, 151), 130)

    def _draw_storm(self, screen):
        """绘制暴风雨：暗紫红天空、快速深色云层、压抑地面。"""
        self._draw_vertical_gradient(screen, (52, 32, 66), (111, 58, 82))

        # 快速云层，用 frame_count 做横向偏移
        cloud_offset = (self.frame_count * 1.4) % (self.screen_width + 260)
        storm_clouds = [(-210, 70, 1.55), (100, 45, 1.45), (420, 85, 1.65), (760, 55, 1.35)]
        for x, y, scale in storm_clouds:
            moved_x = x + cloud_offset
            if moved_x > self.screen_width + 120:
                moved_x -= self.screen_width + 520
            self._draw_cloud(screen, moved_x, y, (45, 42, 62), scale)
            self._draw_cloud(screen, moved_x + 70, y + 28, (64, 48, 72), scale * 0.85)

        # 天空下方的红紫压暗层
        pygame.draw.rect(screen, (92, 55, 76), (0, 260, self.screen_width, 120))

        self._draw_ground(screen, (48, 44, 50), 150)
        pygame.draw.rect(screen, (38, 36, 42), (0, self.screen_height - 80, self.screen_width, 80))

    def _draw_starry_night(self, screen):
        """绘制星夜：深蓝紫天空、月亮、星星、远山剪影。"""
        self._draw_vertical_gradient(screen, (31, 32, 82), (82, 67, 126))

        pygame.draw.circle(screen, (249, 236, 178), (790, 115), 54)
        pygame.draw.circle(screen, (45, 43, 94), (812, 98), 54)

        for x, y, radius, color in self.stars:
            pygame.draw.circle(screen, color, (x, y), radius)

        mountain_color = (39, 43, 74)
        points = [(0, 560), (120, 420), (260, 555), (390, 400), (535, 560), (700, 430), (850, 555), (1000, 455), (1000, 700), (0, 700)]
        pygame.draw.polygon(screen, mountain_color, points)

        self._draw_ground(screen, (29, 34, 58), 95)

    def _draw_snowy_night(self, screen):
        """绘制雪夜：安静冷色夜空、月亮、雪层。"""
        self._draw_vertical_gradient(screen, (29, 48, 86), (91, 111, 148))

        # 柔和月亮和月晕
        moon_surface = pygame.Surface((180, 180), pygame.SRCALPHA)
        pygame.draw.circle(moon_surface, (214, 230, 255, 45), (90, 90), 82)
        pygame.draw.circle(moon_surface, (241, 247, 255, 230), (90, 90), 46)
        pygame.draw.circle(moon_surface, (59, 78, 116, 255), (106, 74), 42)
        screen.blit(moon_surface, (690, 48))

        # 少量静态星点，保持安静感
        for x, y, radius, color in self.stars[:45]:
            soft_color = self._mix_color(color, (210, 228, 255), 0.45)
            pygame.draw.circle(screen, soft_color, (x, y), max(1, radius - 1))

        # 远山和厚雪层
        pygame.draw.polygon(screen, (50, 70, 104), [(0, 550), (160, 430), (320, 550), (510, 420), (720, 555), (900, 455), (1000, 535), (1000, 700), (0, 700)])
        pygame.draw.polygon(screen, (224, 236, 248), [(0, 580), (160, 455), (320, 580), (510, 447), (720, 582), (900, 480), (1000, 560), (1000, 700), (0, 700)])
        pygame.draw.ellipse(screen, (238, 246, 253), (-120, 575, 620, 190))
        pygame.draw.ellipse(screen, (229, 240, 250), (390, 565, 780, 205))

    def _draw_sunrise(self, screen):
        """绘制日出：粉橙蓝渐变天空、地平线太阳、柔和云层。"""
        self._draw_vertical_gradient(screen, (121, 190, 232), (255, 196, 169))

        horizon_y = 500

        self._draw_cloud(screen, 85, 150, (255, 226, 218), 1.1)
        self._draw_cloud(screen, 405, 120, (255, 236, 222), 0.9)
        self._draw_cloud(screen, 655, 190, (255, 220, 208), 1.0)

        pygame.draw.circle(screen, (255, 205, 121), (500, horizon_y), 105)
        pygame.draw.rect(screen, (255, 196, 169), (0, horizon_y, self.screen_width, 120))

        pygame.draw.rect(screen, (112, 154, 145), (0, horizon_y + 60, self.screen_width, 140))
        pygame.draw.rect(screen, (86, 128, 124), (0, horizon_y + 130, self.screen_width, 70))

    def _create_stars(self, count):
        """创建固定位置的星星。"""
        random.seed(8)
        stars = []
        for _ in range(count):
            x = random.randint(25, self.screen_width - 25)
            y = random.randint(25, int(self.screen_height * 0.55))
            radius = random.choice([1, 1, 2, 2, 3])
            color = random.choice([(255, 246, 196), (226, 236, 255), (255, 221, 236)])
            stars.append((x, y, radius, color))
        return stars

    def _mix_color(self, start_color, end_color, ratio):
        """按比例混合两种颜色。"""
        red = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        green = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        blue = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        return red, green, blue