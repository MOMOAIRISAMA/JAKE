"""天气粒子模块。

这里放置不同天气使用的小粒子效果。
粒子只做简单移动、漂浮和闪烁，不使用复杂物理模拟。
"""

import random

import pygame


class Particle:
    """基础粒子类。"""

    def __init__(self, screen_width, screen_height):
        """保存屏幕尺寸，并设置一个基础位置。"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)

    def update(self):
        """更新粒子状态。子类会重写这个方法。"""
        pass

    def draw(self, screen):
        """绘制粒子。子类会重写这个方法。"""
        pass


class RainParticle(Particle):
    """雨滴粒子。"""

    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.reset(random_y=True)

    def reset(self, random_y=False):
        """重置雨滴位置和速度。"""
        self.x = random.randint(0, self.screen_width)
        self.y = random.randint(-self.screen_height, 0) if random_y else random.randint(-80, -10)
        self.length = random.randint(14, 24)
        self.speed = random.uniform(7.0, 11.0)
        self.color = random.choice([(188, 213, 230), (168, 198, 220), (210, 228, 240)])

    def update(self):
        """让雨滴向下落。"""
        self.y += self.speed
        self.x -= 1.2

        if self.y > self.screen_height + self.length:
            self.reset()

    def draw(self, screen):
        """绘制一条短斜线作为雨滴。"""
        start_pos = (int(self.x), int(self.y))
        end_pos = (int(self.x - 4), int(self.y + self.length))
        pygame.draw.line(screen, self.color, start_pos, end_pos, 2)


class StormRainParticle(Particle):
    """暴风雨中的快速斜向雨滴。"""

    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.reset(random_y=True)

    def reset(self, random_y=False):
        """重置暴雨雨滴。"""
        self.x = random.randint(-120, self.screen_width + 80)
        self.y = random.randint(-self.screen_height, 0) if random_y else random.randint(-120, -10)
        self.length = random.randint(20, 34)
        self.speed_y = random.uniform(10.0, 15.0)
        self.speed_x = random.uniform(-5.5, -3.0)
        self.color = random.choice([(168, 182, 207), (194, 202, 224), (147, 161, 188)])

    def update(self):
        """让暴雨快速斜向下落。"""
        self.x += self.speed_x
        self.y += self.speed_y

        if self.y > self.screen_height + self.length or self.x < -180:
            self.reset()

    def draw(self, screen):
        """绘制更长、更倾斜的雨线。"""
        start_pos = (int(self.x), int(self.y))
        end_pos = (int(self.x - 10), int(self.y + self.length))
        pygame.draw.line(screen, self.color, start_pos, end_pos, 2)


class FogParticle(Particle):
    """横向漂浮的半透明雾气。"""

    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.reset(random_x=True)

    def reset(self, random_x=False):
        """重置雾气位置。"""
        self.width = random.randint(180, 320)
        self.height = random.randint(34, 62)
        self.x = random.randint(-self.width, self.screen_width) if random_x else -self.width - random.randint(10, 120)
        self.y = random.randint(220, self.screen_height - 120)
        self.speed_x = random.uniform(0.25, 0.75)
        self.alpha = random.randint(38, 72)
        self.color = random.choice([(232, 238, 246), (222, 228, 240), (214, 224, 240)])

    def update(self):
        """让雾气慢慢横向漂浮。"""
        self.x += self.speed_x
        if self.x > self.screen_width + 40:
            self.reset()

    def draw(self, screen):
        """绘制柔软的半透明雾带。"""
        fog_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.ellipse(fog_surface, (*self.color, self.alpha), (0, 0, self.width, self.height))
        pygame.draw.ellipse(fog_surface, (*self.color, self.alpha // 2), (20, 8, self.width - 40, self.height - 12))
        screen.blit(fog_surface, (int(self.x), int(self.y)))


class SnowParticle(Particle):
    """缓慢飘落的雪花。"""

    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.reset(random_y=True)

    def reset(self, random_y=False):
        """重置雪花位置和速度。"""
        self.x = random.randint(0, self.screen_width)
        self.y = random.randint(-self.screen_height, 0) if random_y else random.randint(-60, -8)
        self.radius = random.choice([2, 2, 3, 4])
        self.speed_y = random.uniform(0.7, 1.8)
        self.speed_x = random.uniform(-0.45, 0.45)
        self.alpha = random.randint(145, 230)

    def update(self):
        """让雪花慢慢下落并轻轻左右漂移。"""
        self.x += self.speed_x
        self.y += self.speed_y

        if self.y > self.screen_height + 10:
            self.reset()
        if self.x < -10:
            self.x = self.screen_width + 10
        elif self.x > self.screen_width + 10:
            self.x = -10

    def draw(self, screen):
        """绘制柔和小雪花。"""
        size = self.radius * 4 + 4
        snow_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (size // 2, size // 2)
        pygame.draw.circle(snow_surface, (245, 250, 255, self.alpha // 3), center, self.radius * 2)
        pygame.draw.circle(snow_surface, (250, 253, 255, self.alpha), center, self.radius)
        screen.blit(snow_surface, (self.x - center[0], self.y - center[1]))


class GlowParticle(Particle):
    """柔和发光光点。"""

    def __init__(self, screen_width, screen_height, direction="up"):
        self.direction = direction
        super().__init__(screen_width, screen_height)
        self.reset(random_y=True)

    def reset(self, random_y=False):
        """重置光点位置和速度。"""
        self.x = random.randint(0, self.screen_width)

        if self.direction == "up":
            self.y = random.randint(0, self.screen_height) if random_y else self.screen_height + random.randint(10, 80)
            self.speed_y = random.uniform(-0.4, -1.0)
        else:
            self.y = random.randint(0, self.screen_height) if random_y else random.randint(-80, -10)
            self.speed_y = random.uniform(0.2, 0.7)

        self.speed_x = random.uniform(-0.25, 0.25)
        self.radius = random.randint(3, 7)
        self.color = random.choice([(255, 228, 132), (255, 240, 170), (255, 215, 110)])

    def update(self):
        """让光点缓慢漂浮。"""
        self.x += self.speed_x
        self.y += self.speed_y

        if self.direction == "up" and self.y < -20:
            self.reset()
        elif self.direction != "up" and self.y > self.screen_height + 20:
            self.reset()

        if self.x < -20:
            self.x = self.screen_width + 20
        elif self.x > self.screen_width + 20:
            self.x = -20

    def draw(self, screen):
        """绘制简单的圆形光点。"""
        center = (int(self.x), int(self.y))
        pygame.draw.circle(screen, self.color, center, self.radius)
        pygame.draw.circle(screen, (255, 248, 210), center, max(1, self.radius // 2))


class StarParticle(Particle):
    """闪烁星星粒子。"""

    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.reset()

    def reset(self):
        """重置星星位置和闪烁状态。"""
        self.x = random.randint(20, self.screen_width - 20)
        self.y = random.randint(20, int(self.screen_height * 0.55))
        self.radius = random.choice([1, 1, 2, 2, 3])
        self.twinkle = random.randint(0, 60)
        self.twinkle_speed = random.choice([1, 1, 2])
        self.base_color = random.choice([(255, 246, 200), (226, 236, 255), (255, 224, 238)])

    def update(self):
        """更新星星闪烁节奏。"""
        self.twinkle += self.twinkle_speed
        if self.twinkle > 120:
            self.twinkle = 0

    def draw(self, screen):
        """绘制会轻微变亮变暗的星星。"""
        if self.twinkle < 60:
            brightness = 150 + self.twinkle
        else:
            brightness = 270 - self.twinkle

        color = tuple(min(255, int(channel * brightness / 210)) for channel in self.base_color)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

        if self.radius >= 2 and self.twinkle < 35:
            pygame.draw.line(screen, color, (self.x - 4, self.y), (self.x + 4, self.y), 1)
            pygame.draw.line(screen, color, (self.x, self.y - 4), (self.x, self.y + 4), 1)


class MouseTrailParticle:
    """鼠标移动时产生的短暂光点。"""

    def __init__(self, x, y, color):
        """记录鼠标位置、颜色和生命周期。"""
        self.x = x + random.uniform(-4, 4)
        self.y = y + random.uniform(-4, 4)
        self.color = color
        self.radius = random.randint(8, 14)
        self.life = 28
        self.max_life = 28
        self.speed_x = random.uniform(-0.35, 0.35)
        self.speed_y = random.uniform(-0.45, 0.15)

    def update(self):
        """让光点轻微漂浮并逐渐消失。"""
        self.x += self.speed_x
        self.y += self.speed_y
        self.radius *= 0.94
        self.life -= 1

    def is_alive(self):
        """判断光点是否还需要保留。"""
        return self.life > 0 and self.radius > 1

    def draw(self, screen):
        """绘制带透明度的柔和光点。"""
        alpha = int(120 * self.life / self.max_life)
        glow_radius = max(2, int(self.radius * 2))
        dot_radius = max(1, int(self.radius))
        surface_size = glow_radius * 2 + 4

        glow_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
        center = (surface_size // 2, surface_size // 2)
        pygame.draw.circle(glow_surface, (*self.color, alpha // 3), center, glow_radius)
        pygame.draw.circle(glow_surface, (*self.color, alpha), center, dot_radius)

        screen.blit(glow_surface, (self.x - center[0], self.y - center[1]))


class ClickDot:
    """点击特效中使用的小光点。"""

    def __init__(self, x, y, speed_x, speed_y, color, radius):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color
        self.radius = radius

    def update(self):
        """移动光点，并让它慢慢变小。"""
        self.x += self.speed_x
        self.y += self.speed_y
        self.radius *= 0.95

    def draw(self, screen, alpha):
        """绘制柔和小光点。"""
        radius = max(1, int(self.radius))
        surface_size = radius * 4 + 4
        dot_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
        center = (surface_size // 2, surface_size // 2)
        pygame.draw.circle(dot_surface, (*self.color, alpha // 4), center, radius * 2)
        pygame.draw.circle(dot_surface, (*self.color, alpha), center, radius)
        screen.blit(dot_surface, (self.x - center[0], self.y - center[1]))


class ClickEffect:
    """鼠标点击时触发的短暂特殊效果。"""

    def __init__(self, weather_type, x, y, screen_width, screen_height):
        self.weather_type = weather_type
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.life = 42
        self.max_life = 42
        self.radius = 8
        self.dots = []
        self.lightning_points = []
        self._create_effect()

    def _create_effect(self):
        """根据天气类型创建不同点击效果。"""
        if self.weather_type == "sunny":
            self._create_sunny_ring()
        elif self.weather_type == "starry_night":
            self._create_stardust_burst()
        elif self.weather_type == "sunrise":
            self._create_sunrise_glow()
        elif self.weather_type == "storm":
            self._create_lightning()

    def _create_sunny_ring(self):
        """晴天：点击处生成一圈金色扩散光点。"""
        color = (255, 217, 91)
        directions = [(-1, 0), (-0.7, -0.7), (0, -1), (0.7, -0.7), (1, 0), (0.7, 0.7), (0, 1), (-0.7, 0.7)]
        for speed_scale in (2.0, 3.0, 4.0):
            for dx, dy in directions:
                self.dots.append(ClickDot(self.x, self.y, dx * speed_scale, dy * speed_scale, color, 6))

    def _create_stardust_burst(self):
        """星夜：点击处生成一小片星尘爆发。"""
        colors = [(240, 230, 255), (255, 242, 196), (220, 230, 255)]
        for _ in range(30):
            speed_x = random.uniform(-3.0, 3.0)
            speed_y = random.uniform(-3.0, 3.0)
            color = random.choice(colors)
            radius = random.randint(2, 4)
            self.dots.append(ClickDot(self.x, self.y, speed_x, speed_y, color, radius))

    def _create_sunrise_glow(self):
        """日出：点击处生成向上漂浮的暖色光点。"""
        colors = [(255, 178, 132), (255, 211, 137), (255, 151, 158)]
        for _ in range(24):
            speed_x = random.uniform(-1.2, 1.2)
            speed_y = random.uniform(-3.2, -1.0)
            color = random.choice(colors)
            radius = random.randint(4, 7)
            self.dots.append(ClickDot(self.x, self.y, speed_x, speed_y, color, radius))

    def _create_lightning(self):
        """暴风：点击处或天空生成一道简单闪电。"""
        start_x = max(40, min(self.screen_width - 40, self.x))
        start_y = 0
        end_y = max(120, min(self.y, self.screen_height - 120))
        points = [(start_x, start_y)]
        current_x = start_x
        current_y = start_y

        while current_y < end_y:
            current_x += random.randint(-34, 34)
            current_x = max(20, min(self.screen_width - 20, current_x))
            current_y += random.randint(34, 58)
            points.append((current_x, min(current_y, end_y)))

        self.lightning_points = points
        self.life = 18
        self.max_life = 18

    def update(self):
        """更新点击特效。"""
        self.life -= 1
        self.radius += 3

        for dot in self.dots:
            dot.update()

    def is_alive(self):
        """判断点击特效是否还存在。"""
        return self.life > 0

    def draw(self, screen):
        """绘制点击特效。"""
        alpha = max(0, int(170 * self.life / self.max_life))

        if self.weather_type == "rainy":
            self._draw_ripple(screen, alpha)
            return
        if self.weather_type == "storm":
            self._draw_lightning(screen, alpha)
            return

        for dot in self.dots:
            dot.draw(screen, alpha)

    def _draw_ripple(self, screen, alpha):
        """雨天：绘制地面水波纹。"""
        ripple_width = int(self.radius * 2.5)
        ripple_height = int(self.radius * 0.7)
        surface_width = ripple_width + 12
        surface_height = ripple_height + 12
        ripple_surface = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA)
        rect = pygame.Rect(6, 6, ripple_width, ripple_height)

        pygame.draw.ellipse(ripple_surface, (190, 226, 245, alpha), rect, 2)
        inner_rect = rect.inflate(-int(ripple_width * 0.35), -int(ripple_height * 0.35))
        if inner_rect.width > 2 and inner_rect.height > 2:
            pygame.draw.ellipse(ripple_surface, (210, 235, 248, alpha // 2), inner_rect, 1)

        screen.blit(ripple_surface, (self.x - surface_width // 2, self.y - surface_height // 2))

    def _draw_lightning(self, screen, alpha):
        """绘制闪电和短暂天空亮光。"""
        flash = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        flash_alpha = max(0, min(70, alpha // 2))
        flash.fill((230, 220, 255, flash_alpha))
        screen.blit(flash, (0, 0))

        if len(self.lightning_points) >= 2:
            pygame.draw.lines(screen, (246, 239, 255), False, self.lightning_points, 5)
            pygame.draw.lines(screen, (190, 185, 255), False, self.lightning_points, 2)

            # 画一个小分叉，让闪电更有二次元效果
            middle = self.lightning_points[len(self.lightning_points) // 2]
            branch_end = (middle[0] + random.choice([-55, 55]), middle[1] + 65)
            pygame.draw.line(screen, (238, 230, 255), middle, branch_end, 2)


class ParticleSystem:
    """粒子系统管理器。"""

    def __init__(self, weather_type, screen_width, screen_height):
        """根据天气类型创建对应粒子。"""
        self.weather_type = weather_type
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.particles = []
        self.mouse_trails = []
        self.click_effects = []
        self._storm_timer = 0
        self._create_particles()

    def _create_particles(self):
        """按照天气类型生成粒子列表。"""
        if self.weather_type == "sunny":
            self.particles = [GlowParticle(self.screen_width, self.screen_height, "down") for _ in range(28)]
        elif self.weather_type == "rainy":
            self.particles = [RainParticle(self.screen_width, self.screen_height) for _ in range(95)]
        elif self.weather_type == "foggy":
            self.particles = [FogParticle(self.screen_width, self.screen_height) for _ in range(16)]
        elif self.weather_type == "storm":
            self.particles = [StormRainParticle(self.screen_width, self.screen_height) for _ in range(130)]
        elif self.weather_type == "starry_night":
            self.particles = [StarParticle(self.screen_width, self.screen_height) for _ in range(70)]
        elif self.weather_type == "snowy_night":
            self.particles = [SnowParticle(self.screen_width, self.screen_height) for _ in range(95)]
        elif self.weather_type == "sunrise":
            self.particles = [GlowParticle(self.screen_width, self.screen_height, "up") for _ in range(36)]
        else:
            self.particles = [GlowParticle(self.screen_width, self.screen_height, "up") for _ in range(30)]

    def add_mouse_trail(self, x, y):
        """在鼠标位置添加一个光轨粒子。"""
        color = self._get_mouse_trail_color()
        self.mouse_trails.append(MouseTrailParticle(x, y, color))

        if len(self.mouse_trails) > 90:
            self.mouse_trails = self.mouse_trails[-90:]

    def add_click_effect(self, x, y):
        """在鼠标点击位置添加特殊效果。"""
        if self.weather_type == "rainy" and y < self.screen_height * 0.62:
            return

        self.click_effects.append(ClickEffect(self.weather_type, x, y, self.screen_width, self.screen_height))

        if len(self.click_effects) > 12:
            self.click_effects = self.click_effects[-12:]

    def update(self):
        """更新所有粒子。"""
        for particle in self.particles:
            particle.update()

        for trail in self.mouse_trails:
            trail.update()

        for effect in self.click_effects:
            effect.update()

        # 暴风雨偶尔自动闪电，间隔用计时器控制，避免频繁闪烁
        if self.weather_type == "storm":
            self._storm_timer += 1
            if self._storm_timer > 90 and random.random() < 0.018:
                x = random.randint(160, self.screen_width - 160)
                y = random.randint(220, 430)
                self.click_effects.append(ClickEffect("storm", x, y, self.screen_width, self.screen_height))
                self._storm_timer = 0

        self.mouse_trails = [trail for trail in self.mouse_trails if trail.is_alive()]
        self.click_effects = [effect for effect in self.click_effects if effect.is_alive()]

    def draw(self, screen):
        """绘制所有粒子。"""
        for particle in self.particles:
            particle.draw(screen)

        for trail in self.mouse_trails:
            trail.draw(screen)

        for effect in self.click_effects:
            effect.draw(screen)

    def _get_mouse_trail_color(self):
        """根据天气类型选择鼠标光轨颜色。"""
        if self.weather_type == "sunny":
            return 255, 222, 105
        if self.weather_type == "rainy":
            return 176, 222, 245
        if self.weather_type == "foggy":
            return 213, 220, 240
        if self.weather_type == "storm":
            return 215, 196, 255
        if self.weather_type == "starry_night":
            return 230, 218, 255
        if self.weather_type == "snowy_night":
            return 220, 238, 255
        if self.weather_type == "sunrise":
            return 255, 174, 139

        return 255, 220, 170