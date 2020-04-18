import pygame
import random
import pickle
import constants


class World:
    def __init__(self, bg_colour):
        self.bg_colour = bg_colour
        self.sprite_list = []
        self.car_sprite = ""
        self.road_sprite = ""
        self.ended = False
        self.end_world_crashed = ""
        self.end_world_emoji = ""

    def update(self, event):
        if not self.ended:
            for s in self.sprite_list:
                s.update(event)
            self.road_sprite.update(event)
            self.car_sprite.update(event)
        else:
            self.end_world_crashed.visible = True
            self.end_world_emoji.visible = True

    def add_sprite(self, s):
        if s.type == "car":
            self.car_sprite = s
        elif s.type == "road":
            self.road_sprite = s
        elif s.type == "end_world_crashed":
            self.end_world_crashed = s
        elif s.type == "end_world_emoji":
            self.end_world_emoji = s
        else:
            self.sprite_list.append(s)

    def draw(self, target_surface):
        target_surface.fill(self.bg_colour)
        for s in self.sprite_list:
            if s.visible:
                s.draw(target_surface)
        if type(self.road_sprite) == Road_sprite:
            if self.road_sprite.visible:
                self.road_sprite.draw(target_surface)
        if type(self.car_sprite) == Car_sprite:
            if self.car_sprite.visible:
                self.car_sprite.draw(target_surface)
        if type(self.end_world_crashed) == Text_sprite:
            if self.end_world_crashed.visible:
                self.end_world_crashed.draw(target_surface)
        if type(self.end_world_emoji) == Text_sprite:
            if self.end_world_emoji.visible:
                self.end_world_emoji.draw(target_surface)

    def detect_collision(self):
        if type(self.road_sprite) == Road_sprite and type(self.car_sprite) == Car_sprite:
            self.car_sprite.set_crashed(self.road_sprite.detect_collision(self.car_sprite))
            return self.car_sprite.crashed
        else:
            return False


class Intro_world(World):
    def __init__(self, bg_colour):
        super(Intro_world, self).__init__(bg_colour)
        self.sequence_sprite = []

    def add_sequence_sprite(self, s):
        if len(self.sequence_sprite) == 0:
            s[0].visible = True
        else:
            s[0].visible = False
        # print("Added "+str(s.text)+str(s.visible))
        self.sequence_sprite.append(s)

    def update(self, event):
        i = 0
        active_sprite_index = 0
        if type(event) != int:
            if event.type == pygame.USEREVENT + 2:
                while i < (len(self.sequence_sprite) - 1):
                    if self.sequence_sprite[i][0].visible:
                        self.sequence_sprite[i][0].visible = False
                        self.sequence_sprite[i + 1][0].visible = True
                        active_sprite_index = i + 1
                        i += 2
                    else:
                        i += 1
                pygame.time.set_timer(
                    pygame.USEREVENT + 2, self.sequence_sprite[active_sprite_index][0].time, True
                )
            if active_sprite_index == 2:
                pygame.mixer.music.load(constants.getFilePath("321GO.ogg"))
                pygame.mixer.music.play(0)
            if active_sprite_index == len(self.sequence_sprite) - 1:
                pygame.time.set_timer(
                    pygame.USEREVENT + 1,
                    self.sequence_sprite[active_sprite_index][0].time + 1,
                    True,
                )

    def draw(self, target_surface):
        super(Intro_world, self).draw(target_surface)
        for sprite_list in self.sequence_sprite:
            if sprite_list[0].visible:
                for sprite in sprite_list:
                    sprite.draw(target_surface)


class Sprite:
    def __init__(self):
        self.visible = True

    def draw(self, target_surface):
        pass

    def update(self, event):
        pass


class Divider_sprite(Sprite):
    def __init__(self, startx, starty, width, height, colour):
        super(Divider_sprite, self).__init__()
        self.startx = startx
        self.starty = starty
        self.width = width
        self.height = height
        self.colour = colour
        self.type = "divider"

    def update(self, new_y):
        self.starty = new_y
        return self

    def draw(self, target_surface):
        pygame.draw.rect(
            target_surface, self.colour, (self.startx, self.starty, self.width, self.height), 0,
        )


class Block_sprite(Sprite):
    def __init__(self, colour, x_max, y_max):
        super(Block_sprite, self).__init__()
        self.width = random.randint(40, 250)
        self.height = random.randint(30, 200)
        self.x_max = x_max
        self.y_max = y_max
        self.x = random.randint(int(0 - self.width / 2), int(self.x_max - self.width / 2))
        self.y = -self.height
        self.colour = colour
        self.type = "block"
        self.increase_amount = 7

    def update(self, event):
        if type(event) == int:
            self.y += self.increase_amount
            self.increase_amount += 0.1

    def draw(self, target_surface):
        pygame.draw.rect(
            target_surface, self.colour, (self.x, self.y, self.width, self.height), 0,
        )

    def detect_collision(self, car):
        block_start_x = self.x
        block_start_y = self.y
        block_end_x = self.x + self.width
        block_end_y = self.y + self.height
        car_start_x = car.x
        car_start_y = car.y
        car_end_x = car.x + car.width
        car_end_y = car.y + car.height

        return (
                (
                        car_start_x <= block_end_x
                        and car_start_x >= block_start_x
                        and car_start_y <= block_end_y
                        and car_start_y >= block_start_y
                )
                or (
                        car_end_x >= block_start_x
                        and car_end_x <= block_end_x
                        and car_start_y <= block_end_y
                        and car_start_y >= block_start_y
                )
                or (
                        car_end_y <= block_end_y
                        and car_end_y >= block_start_y
                        and car_end_x >= block_start_x
                        and car_end_x <= block_end_x
                )
                or (
                        car_end_y <= block_end_y
                        and car_end_y >= block_start_y
                        and car_start_x >= block_start_x
                        and car_start_x <= block_end_x
                )
        )


class Road_sprite(Sprite):
    def __init__(self, divider_width, divider_height, colour, target_surface):
        super(Road_sprite, self).__init__()
        self.dividers = []
        self.divider_width = divider_width
        self.divider_height = divider_height
        self.spacing = int(divider_height / 4)
        self.colour = colour
        self.x_max = target_surface.get_size()[0]
        self.y_max = target_surface.get_size()[1]
        self.blocks = []
        self.type = "road"
        self.dodged_count = 0
        self.dodged = Text_sprite(
            "Dodged: " + str(0),
            constants.getFilePath("FasterOne.ttf"),
            constants.corner_small_text_size,
            0,
            25,
            constants.BLACK,
            0,
        )
        try:
            with open("highscores.dat", "rb") as file:
                self.highscore = pickle.load(file)
        except FileNotFoundError:
            self.highscore = 0
        self.global_highscore = Text_sprite(
            "Highscore: " + str(self.highscore),
            constants.getFilePath("FasterOne.ttf"),
            constants.corner_small_text_size,
            0,
            0,
            constants.BLACK,
            0,
        )
        self.DodgeCar_corner = Text_sprite(
            "DodgeCar",
            constants.getFilePath("EndeavourForever.ttf"),
            constants.corner_small_text_size,
            constants.display_width - 140,
            10,
            constants.BLACK,
            2500,
        )
        self.spacebar_again = Text_sprite(
            "Press space to restart.", constants.FasterOneFontPath, 25, 250, 0, constants.GREEN, 0,
        )

    def initialise_road(self):
        divider_x = self.x_max / 2 - self.divider_width / 2
        divider_y = 0
        while divider_y < self.y_max:
            d1 = Divider_sprite(
                divider_x, divider_y, self.divider_width, self.divider_height, self.colour,
            )
            self.dividers.append(d1)
            divider_y += self.divider_height + self.spacing
        self.blocks.append(Block_sprite(constants.BLUE, self.x_max, self.y_max))

    def update(self, event):
        if type(event) == int:
            increase_amount = int(self.divider_height / 20)
            dividers2 = []
            divider_1 = self.dividers[0]
            if divider_1.starty + increase_amount >= 0:
                dividers2.append(
                    Divider_sprite(
                        divider_1.startx,
                        -1 * (self.divider_height + self.spacing),
                        self.divider_width,
                        self.divider_height,
                        self.colour,
                    )
                )
            for d in self.dividers:
                new_y_pos = d.starty + increase_amount
                if new_y_pos < self.y_max:
                    dividers2.append(d.update(new_y_pos))
            self.dividers = dividers2

            b2 = []
            for b in self.blocks:
                b.update(event)
                if b.y < self.y_max:
                    b2.append(b)
                else:
                    self.dodged_count += 1
                    self.dodged.text = "Dodged: " + str(self.dodged_count)

            max_blocks = random.randint(3, 7)

            if len(b2) < max_blocks and b2[len(b2) - 1].y > self.y_max / max_blocks:
                b2.append(Block_sprite(constants.BLUE, self.x_max, self.y_max))
            self.blocks = b2

    def draw(self, target_surface):
        for d in self.dividers:
            d.draw(target_surface)
        for b in self.blocks:
            b.draw(target_surface)
        self.dodged.draw(target_surface)
        self.global_highscore.draw(target_surface)
        self.DodgeCar_corner.draw(target_surface)
        self.spacebar_again.draw(target_surface)

    def detect_collision(self, car):
        for b in self.blocks:
            if b.detect_collision(car):
                self.crashed = True
                # print(
                #     "collided: {0},{1}-{2},{3} car:{4},{5}-{6}{7} SCORE: {8}"
                #       .format(
                #         b.x,
                #         b.y,
                #         b.x + b.width,
                #         b.y + b.height,
                #         car.x,
                #         car.y,
                #         car.x + car.width,
                #         car.y + car.height,
                #         self.dodged_count,
                #     )
                # )
                if self.dodged_count > self.highscore:
                    with open("highscores.dat", "wb") as file:
                        pickle.dump(self.dodged_count, file)
                return self.crashed
        self.crashed = False
        return self.crashed


class Car_sprite(Sprite):
    def __init__(self, img_path, crashed_img_path, target_surface):
        super(Car_sprite, self).__init__()
        self.target_surface = target_surface
        self.image = pygame.image.load(img_path)
        self.crashed_image = pygame.image.load(crashed_img_path)
        self.width = self.image.get_size()[0]
        self.height = self.image.get_size()[1]
        self.x_max = target_surface.get_size()[0]
        self.y_max = target_surface.get_size()[1]
        self.x = self.x_max / 2 - self.width / 2
        self.y = self.y_max - int(self.height * 1.1)
        self.go_left = False
        self.go_right = False
        self.type = "car"
        self.crashed = False

    def move_left(self):
        if self.x > 0:
            self.x -= self.width / 5

    def move_right(self):
        if self.x < self.x_max - self.width:
            self.x += self.width / 5

    def update(self, event):
        if type(event) != int:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.go_left = True
                elif event.key == pygame.K_RIGHT:
                    self.go_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.go_left = False
                elif event.key == pygame.K_RIGHT:
                    self.go_right = False
        if self.go_right:
            self.move_right()
        if self.go_left:
            self.move_left()

    def set_crashed(self, is_crashed):
        self.crashed = is_crashed
        if is_crashed:
            self.image = self.crashed_image

    def draw(self, target_surface):
        target_surface.blit(self.image, (self.x, self.y))


class Text_sprite(Sprite):
    def __init__(self, text, font, size, x, y, colour, time):
        super(Text_sprite, self).__init__()
        self.colour = colour
        self.text = text
        self.size = size
        print(font)
        print(type(font))
        self.font = pygame.font.Font(font, size)
        self.x = x
        self.y = y
        self.type = "text"
        self.time = time

    def draw(self, target_surface):
        font_surface = self.font.render(str(self.text), True, self.colour)
        target_surface.blit(font_surface, (self.x, self.y))
