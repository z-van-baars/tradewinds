import utilities as util
import pygame
import art
import math


context_menu = pygame.image.load('art/menus/context_menu.png')
tile_info_pane = pygame.image.load('art/menus/tile_info_pane.png')
impassable_popup_pane = pygame.image.load('art/menus/impassable_popup_pane.png')
city_menu_pane = pygame.image.load('art/menus/city_menu_pane.png')
market_menu_pane = pygame.image.load('art/menus/market_screen.png')
quantity_popup = pygame.image.load('art/menus/quantity_popup.png')

leave_r_img = pygame.image.load('art/buttons/leave_regular.png')
leave_h_img = pygame.image.load('art/buttons/leave_hover.png')

market_r_img = pygame.image.load('art/buttons/market_regular.png')
market_h_img = pygame.image.load('art/buttons/market_hover.png')

cancel_r_img = pygame.image.load('art/buttons/cancel_regular.png')
cancel_h_img = pygame.image.load('art/buttons/cancel_hover.png')

done_r_img = pygame.image.load('art/buttons/done_regular.png')
done_h_img = pygame.image.load('art/buttons/done_hover.png')

move_r_img = pygame.image.load('art/buttons/move_here_regular.png')
move_h_img = pygame.image.load('art/buttons/move_here_hover.png')

enter_city_r_img = pygame.image.load('art/buttons/enter_city_regular.png')
enter_city_h_img = pygame.image.load('art/buttons/enter_city_hover.png')

tile_info_r_img = pygame.image.load('art/buttons/tile_info_regular.png')
tile_info_h_img = pygame.image.load('art/buttons/tile_info_hover.png')

ok_r_img = pygame.image.load('art/buttons/ok_button_regular.png')
ok_h_img = pygame.image.load('art/buttons/ok_button_hover.png')

# Market Screen Buttons
x_button_r_img = pygame.image.load('art/buttons/x_regular.png')
x_button_h_img = pygame.image.load('art/buttons/x_hover.png')

arrow_u_r_img = pygame.image.load('art/buttons/arrow_up_regular.png')
arrow_u_h_img = pygame.image.load('art/buttons/arrow_up_hover.png')
arrow_d_r_img = pygame.image.load('art/buttons/arrow_down_regular.png')
arrow_d_h_img = pygame.image.load('art/buttons/arrow_down_hover.png')
arrow_r_r_img = pygame.image.load('art/buttons/arrow_right_regular.png')
arrow_r_h_img = pygame.image.load('art/buttons/arrow_right_hover.png')
arrow_l_r_img = pygame.image.load('art/buttons/arrow_left_regular.png')
arrow_l_h_img = pygame.image.load('art/buttons/arrow_left_hover.png')

buy_r_img = pygame.image.load('art/buttons/buy_regular.png')
buy_h_img = pygame.image.load('art/buttons/buy_hover.png')

sell_r_img = pygame.image.load('art/buttons/sell_regular.png')
sell_h_img = pygame.image.load('art/buttons/sell_hover.png')

max_r_img = pygame.image.load('art/buttons/max_regular.png')
max_h_img = pygame.image.load('art/buttons/max_hover.png')

min_r_img = pygame.image.load('art/buttons/min_regular.png')
min_h_img = pygame.image.load('art/buttons/min_hover.png')

button_images = [leave_r_img,
                 leave_h_img,
                 market_r_img,
                 market_h_img,
                 cancel_r_img,
                 cancel_h_img,
                 done_r_img,
                 done_h_img,
                 move_r_img,
                 move_h_img,
                 enter_city_r_img,
                 enter_city_h_img,
                 tile_info_r_img,
                 tile_info_h_img,
                 x_button_r_img,
                 x_button_h_img,
                 arrow_u_r_img,
                 arrow_u_h_img,
                 arrow_d_r_img,
                 arrow_d_h_img,
                 arrow_r_r_img,
                 arrow_r_h_img,
                 arrow_l_r_img,
                 arrow_l_h_img,
                 buy_r_img,
                 buy_h_img,
                 sell_r_img,
                 sell_h_img,
                 max_r_img,
                 max_h_img,
                 min_r_img,
                 min_h_img]

for img in button_images:
    img.set_colorkey(util.colors.key)
    img = img.convert_alpha()


class Button(object):
    def __init__(self, regular_image, hover_image, on_click, x=0, y=0):

        self.regular = regular_image
        self.hover = hover_image
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.regular
        self.sprite.rect = self.sprite.image.get_rect()
        self.click = on_click
        self.sprite.rect.x = x
        self.sprite.rect.y = y


class Menu(object):
    def __init__(self, game_state):
        self.open = True
        self.dragging = False
        self.drag_offset = None
        self.player = game_state.player
        self.screen = game_state.screen
        self.active_map = game_state.active_map
        self.screen_width = game_state.screen_width
        self.screen_height = game_state.screen_height
        self.game_state = game_state
        self.cached_image = pygame.Surface([0, 0])

    def render_buttons(self, pos):
        mouse_pos = (pos[0] - self.background_pane.rect.x,
                     pos[1] - self.background_pane.rect.y)
        for button in self.buttons:
            if util.check_if_inside(button.sprite.rect.x,
                                    button.sprite.rect.right,
                                    button.sprite.rect.y,
                                    button.sprite.rect.bottom,
                                    mouse_pos):
                button.sprite.image = button.hover
            else:
                button.sprite.image = button.regular
            self.screen.blit(button.sprite.image,
                             [button.sprite.rect.x, button.sprite.rect.y])

    def drag(self, pos):
        if not self.dragging:
            return

        if not self.drag_offset:
            x = self.background_pane.rect.x - pos[0]
            y = self.background_pane.rect.y - pos[1]
            self.drag_offset = (x, y)
        self.background_pane.rect.x = pos[0] + self.drag_offset[0]
        self.background_pane.rect.y = pos[1] + self.drag_offset[1]

    def update_last_pos(self):
        pass

    def keydown_handler(self, key):
        pass

    def keyup_handler(self, key):
        pass

    def render_decals(self, pos):
        pass

    def get_interaction(self, event, pos):
        if util.check_if_inside(self.background_pane.rect.left,
                                self.background_pane.rect.right,
                                self.background_pane.rect.top,
                                self.background_pane.rect.bottom,
                                pos):
            return True
        return False

    def mouse_release_handler(self, event, pos):
        self.dragging = False
        self.drag_offset = None

    def mouse_click_handler(self, event, pos):
        mouse_pos = (pos[0] - self.background_pane.rect.x,
                     pos[1] - self.background_pane.rect.y)
        for button in self.buttons:
            if util.check_if_inside(button.sprite.rect.x,
                                    button.sprite.rect.right,
                                    button.sprite.rect.y,
                                    button.sprite.rect.bottom,
                                    mouse_pos):
                button.click()

    def event_handler(self, event, pos):
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_click_handler(event, pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_release_handler(event, pos)
        elif event.type == pygame.KEYDOWN:
            self.keydown_handler(event.key)
        elif event.type == pygame.KEYUP:
            self.keyup_handler(event.key)

    def render_onscreen_cache(self, pos):
        self.cached_image = pygame.Surface([self.background_pane.image.get_width(),
                                            self.background_pane.image.get_height()])
        self.render_buttons(pos)
        self.cached_image.blit(self.background_pane.image, [0, 0])
        for button in self.buttons:
            self.cached_image.blit(button.sprite.image,
                                   [button.sprite.rect.x, button.sprite.rect.y])
        self.render_decals(pos)


class ContextMenu(Menu):
    def __init__(self, game_state, pos, tile):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = context_menu
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = pos[0]
        self.background_pane.rect.y = pos[1]
        self.tile = tile

        def move_click():
            if tile.biome in ["ocean", "sea", "shallows", "river"]:
                game_state.player.column = tile.column
                game_state.player.row = tile.row
                self.open = False
            else:
                cannot_move_popup = ImpassablePopup(game_state)
                game_state.active_menus = [cannot_move_popup] + game_state.active_menus

        def enter_city_click():
            new_city_menu = CityMenu(game_state, self.tile.city)
            game_state.active_menus = [new_city_menu] + game_state.active_menus
            self.open = False

        def tile_info_click():
            new_tile_info_pane = TileInfoPane(game_state, pos, tile)
            game_state.active_menus = [new_tile_info_pane] + game_state.active_menus
            self.open = False

        def cancel_click():
            self.open = False

        move_button = Button(move_r_img,
                             move_h_img,
                             move_click,
                             5,
                             25)

        enter_city_button = Button(enter_city_r_img,
                                   enter_city_h_img,
                                   enter_city_click,
                                   5,
                                   25)

        tile_info_button = Button(tile_info_r_img,
                                  tile_info_h_img,
                                  tile_info_click,
                                  100,
                                  25)

        cancel_button = Button(cancel_r_img,
                               cancel_h_img,
                               cancel_click,
                               180,
                               25)
        self.buttons = [move_button, tile_info_button, cancel_button]
        player_neighbors = util.get_adjacent_tiles(game_state.active_map.game_tile_rows[game_state.player.row][game_state.player.column],
                                                   game_state.active_map)
        if self.tile.city and self.tile in player_neighbors:
            self.buttons = [enter_city_button, tile_info_button, cancel_button]

    def render_decals(self, pos):
        header_font = pygame.font.SysFont('Calibri', 18, True, False)
        header_text = "{0} {1}".format(self.tile.biome, self.tile.terrain)
        if self.tile.city:
            header_text = "{0}".format(self.tile.city.name)
        header_stamp = header_font.render(header_text, True, util.colors.white)
        self.cached_image.blit(header_stamp, [5, 5])


class ImpassablePopup(Menu):
    def __init__(self, game_state):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = impassable_popup_pane
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = (self.game_state.screen.get_width() / 2) - (self.background_pane.image.get_width() / 2)
        self.background_pane.rect.y = (self.game_state.screen.get_height() / 2) - (self.background_pane.image.get_height() / 2)

        def ok_click():
            self.open = False

        def dragbar_click():
            self.dragging = True

        ok_button = Button(ok_r_img,
                           ok_h_img,
                           ok_click,
                           self.background_pane.image.get_width() / 2 - 28,
                           56)

        dragbar_r_img = pygame.Surface([self.background_pane.image.get_width() - 2, 9])
        dragbar_r_img.fill(util.colors.dragbar)

        dragbar = Button(dragbar_r_img,
                         dragbar_r_img,
                         dragbar_click,
                         1,
                         1)

        self.buttons = [ok_button, dragbar]


class TileInfoPane(Menu):
    def __init__(self, game_state, pos, tile):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = tile_info_pane
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = pos[0]
        self.background_pane.rect.y = pos[1]
        self.tile = tile

        def ok_click():
            self.open = False

        def dragbar_click():
            self.dragging = True

        ok_button = Button(ok_r_img,
                           ok_h_img,
                           ok_click,
                           10,
                           270)

        dragbar_r_img = pygame.Surface([self.background_pane.image.get_width() - 2, 9])
        dragbar_r_img.fill(util.colors.dragbar)

        dragbar = Button(dragbar_r_img,
                         dragbar_r_img,
                         dragbar_click,
                         1,
                         1)

        self.buttons = [ok_button, dragbar]

    def render_decals(self, pos):
        header_font = pygame.font.SysFont('Calibri', 18, True, False)
        coordinates_text = "{0}, {1}".format(self.tile.column, self.tile.row)
        biome_text = self.tile.biome
        terrain_text = self.tile.terrain
        resource_text = "None"
        if self.tile.resource:
            resource_text = self.tile.resource
        city_text = "None"
        if self.tile.city:
            city_text = self.tile.city.name
        coordinates_stamp = header_font.render(coordinates_text, True, util.colors.white)
        biome_stamp = header_font.render(biome_text, True, util.colors.white)
        terrain_stamp = header_font.render(terrain_text, True, util.colors.white)
        resource_stamp = header_font.render(resource_text, True, util.colors.white)
        city_stamp = header_font.render(city_text, True, util.colors.white)
        water_flux_stamp = header_font.render("{0}, {1}, {2}".format(self.tile.water_source[0], self.tile.water_source[1], self.tile.water_flux[2]),
                                              True,
                                              util.colors.white)

        self.cached_image.blit(coordinates_stamp, [8, 73])
        self.cached_image.blit(biome_stamp, [8, 115])
        self.cached_image.blit(water_flux_stamp, [100, 115])
        self.cached_image.blit(terrain_stamp, [8, 156])
        if self.tile.resource:
            self.cached_image.blit(art.resource_images[self.tile.resource][0], [5 + resource_stamp.get_width(), 200 - 20])
        self.cached_image.blit(resource_stamp, [8, 200])
        self.cached_image.blit(city_stamp, [8, 245])


class CityMenu(Menu):
    def __init__(self, game_state, city):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = city_menu_pane
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = (self.game_state.screen.get_width() / 2) - (self.background_pane.image.get_width() / 2)
        self.background_pane.rect.y = (self.game_state.screen.get_height() / 2) - (self.background_pane.image.get_height() / 2)
        self.city = city

        def leave_click():
            self.open = False

        def market_click():
            new_market_menu = MarketMenu(game_state, city)
            game_state.clear_menutype([MarketMenu])
            game_state.active_menus = [new_market_menu] + game_state.active_menus
            self.open = False

        def dragbar_click():
            self.dragging = True

        dragbar_r_img = pygame.Surface([self.background_pane.image.get_width() - 2, 9])
        dragbar_r_img.fill(util.colors.dragbar)

        dragbar = Button(dragbar_r_img,
                         dragbar_r_img,
                         dragbar_click,
                         1,
                         1)

        market_button = Button(market_r_img,
                               market_h_img,
                               market_click,
                               5,
                               35)

        leave_button = Button(leave_r_img,
                              leave_h_img,
                              leave_click,
                              5,
                              65)

        self.buttons = [leave_button, market_button,
                        dragbar]

    def render_decals(self, pos):
        header_font = pygame.font.SysFont('Calibri', 18, True, False)
        city_name_text = "{0}".format(self.city.name)
        city_name_stamp = header_font.render(city_name_text, True, util.colors.white)
        self.cached_image.blit(city_name_stamp, [self.background_pane.image.get_width() / 2 - city_name_stamp.get_width() / 2,
                                                 15])


class MarketMenu(Menu):
    def __init__(self, game_state, city):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = market_menu_pane
        self.background_pane.rect = self.background_pane.image.get_rect()
        x_origin = (self.screen.get_width() / 2 -
                    self.background_pane.image.get_width() / 2)
        y_origin = (self.screen.get_height() / 2 -
                    self.background_pane.image.get_height() / 2)
        self.background_pane.rect.x = x_origin
        self.background_pane.rect.y = y_origin

        self.city = city
        header_font = pygame.font.SysFont('Calibri', 18, True, False)
        self.name_stamp = header_font.render("{0} Market".format(city.name),
                                             True,
                                             (255, 255, 255))

        self.display_cache = {"market commodities list": [],
                              "cargo commodities list": [],
                              "market list top": 0,
                              "cargo list top": 0,
                              "market visible items": [],
                              "cargo visible items": [],
                              "market selected": 0,
                              "cargo selected": 0,
                              "market selection box": pygame.sprite.Sprite(),
                              "cargo selection box": pygame.sprite.Sprite(),
                              "cargo cap": "0 / 0"}

        self.update_display_cache()

        def x_click():
            self.open = False

        def sell_click():
            artikel_name = self.display_cache["cargo visible items"][self.display_cache["cargo selected"]]
            sell_quantity_popup = QuantityMenu(self.game_state, self.player, self.city, artikel_name, "sale")
            game_state.active_menus = [sell_quantity_popup] + game_state.active_menus

            self.update_display_cache()

        def buy_click():
            artikel_name = self.display_cache["market visible items"][self.display_cache["market selected"]]
            buy_quantity_popup = QuantityMenu(self.game_state, self.player, self.city, artikel_name, "purchase")
            game_state.clear_menutype([QuantityMenu])
            game_state.active_menus = [buy_quantity_popup] + game_state.active_menus

            self.update_display_cache()

        def market_up_click():
            if self.display_cache["market list top"] > 0:
                self.display_cache["market list top"] -= 1
                self.update_display_cache()

        def market_down_click():
            if self.display_cache["market list top"] < len(self.display_cache["market commodities list"]) - 1:
                self.display_cache["market list top"] += 1
                self.update_display_cache()

        def cargo_up_click():
            if self.display_cache["cargo list top"] > 0:
                self.display_cache["cargo list top"] -= 1
                self.update_display_cache()

        def cargo_down_click():
            if self.display_cache["cargo list top"] < len(self.display_cache["cargo commodities list"]) - 1:
                self.display_cache["cargo list top"] += 1
                self.update_display_cache()

        def dragbar_click():
            self.dragging = True

        dragbar_r_img = pygame.Surface([self.background_pane.image.get_width() - 2, 9])
        dragbar_r_img.fill(util.colors.dragbar)

        dragbar = Button(dragbar_r_img,
                         dragbar_r_img,
                         dragbar_click,
                         1,
                         1)

        x_button = Button(x_button_r_img,
                          x_button_h_img,
                          x_click,
                          477,
                          13)

        sell_button = Button(sell_r_img,
                             sell_h_img,
                             sell_click,
                             432,
                             410)

        buy_button = Button(buy_r_img,
                            buy_h_img,
                            buy_click,
                            14,
                            410)

        market_up_arrow = Button(arrow_u_r_img,
                                 arrow_u_h_img,
                                 market_up_click,
                                 14,
                                 58)

        market_down_arrow = Button(arrow_d_r_img,
                                   arrow_d_h_img,
                                   market_down_click,
                                   14,
                                   385)

        cargo_up_arrow = Button(arrow_u_r_img,
                                arrow_u_h_img,
                                cargo_up_click,
                                466,
                                58)

        cargo_down_arrow = Button(arrow_d_r_img,
                                  arrow_d_h_img,
                                  cargo_down_click,
                                  466,
                                  385)

        self.buttons = [x_button,
                        sell_button,
                        buy_button,
                        market_up_arrow,
                        market_down_arrow,
                        cargo_up_arrow,
                        cargo_down_arrow,
                        dragbar]

    def update_display_cache(self):
        self.display_cache["silver"] = self.player.silver
        current_cargo = 0
        for artikel_name, artikel_quantity in self.player.ship.cargo.items():
            current_cargo += artikel_quantity
        self.display_cache["cargo cap"] = "{0} / {1}".format(str(current_cargo), str(self.player.ship.cargo_cap))
        self.display_cache["market artikels list"] = []
        for artikel_name, artikel_quantity, in self.city.supply.items():
            if artikel_quantity > 0:
                self.display_cache["market artikels list"].append(artikel_name)
        self.display_cache["cargo artikels list"] = []
        for artikel_name, artikel_quantity, in self.player.ship.cargo.items():
            if artikel_quantity > 0:
                self.display_cache["cargo artikels list"].append(artikel_name)

        if self.display_cache["market selected"] > len(self.display_cache["market artikels list"]) - 1:
            self.display_cache["market selected"] -= 1
        if self.display_cache["cargo selected"] > len(self.display_cache["cargo artikels list"]) - 1:
            self.display_cache["cargo selected"] -= 1
        market_list = self.display_cache["market artikels list"]
        self.display_cache["market visible items"] = market_list[self.display_cache["market list top"]:self.display_cache["market list top"] + 20]
        cargo_list = self.display_cache["cargo artikels list"]
        self.display_cache["cargo visible items"] = cargo_list[self.display_cache["cargo list top"]:self.display_cache["cargo list top"] + 20]
        self.update_selection_boxes()

    def update_selection_boxes(self):
        box_y = 58 + ((self.display_cache["market selected"] - self.display_cache["market list top"]) * 14)
        self.display_cache["market selection box"].image = pygame.Rect(37,
                                                                       box_y,
                                                                       208,
                                                                       15)
        box_y = 58 + ((self.display_cache["cargo selected"] - self.display_cache["cargo list top"]) * 14)
        self.display_cache["cargo selection box"].image = pygame.Rect(252,
                                                                      box_y,
                                                                      208,
                                                                      15)

    def mouse_click_handler(self, event, pos):
        mouse_pos = (pos[0] - self.background_pane.rect.x, pos[1] - self.background_pane.rect.y)
        for button in self.buttons:
            if util.check_if_inside(button.sprite.rect.x,
                                    button.sprite.rect.right,
                                    button.sprite.rect.y,
                                    button.sprite.rect.bottom,
                                    mouse_pos):
                button.click()
        count = 0
        spacer = 14
        for each in self.display_cache["market visible items"]:
            x1 = 37
            x2 = x1 + 170
            y1 = (58 + (count * spacer))
            y2 = y1 + 15
            if util.check_if_inside(x1, x2, y1, y2, mouse_pos):
                self.display_cache["market selected"] = count + self.display_cache["market list top"]
                self.update_display_cache()
            count += 1

        count = 0
        for each in self.display_cache["cargo visible items"]:
            x1 = 252
            x2 = x1 + 170
            y1 = (58 + (count * spacer))
            y2 = y1 + 15
            if util.check_if_inside(x1, x2, y1, y2, mouse_pos):
                self.display_cache["cargo selected"] = count + self.display_cache["cargo list top"]
                self.update_display_cache()
            count += 1

    def draw_selection_boxes(self):
        if self.display_cache["market list top"] <= self.display_cache["market selected"] <= self.display_cache["market list top"] + 21:
            pygame.draw.rect(self.cached_image, (255, 198, 13), self.display_cache["market selection box"].image, 1)
        if self.display_cache["cargo list top"] <= self.display_cache["cargo selected"] <= self.display_cache["cargo list top"] + 21:
            pygame.draw.rect(self.cached_image, (255, 198, 13), self.display_cache["cargo selection box"].image, 1)

    def render_decals(self, pos):
        left_margin = (self.background_pane.image.get_width() / 2) - (self.name_stamp.get_width() / 2)
        self.update_display_cache()
        self.cached_image.blit(self.name_stamp, [left_margin, 12])
        small_font = pygame.font.SysFont("Calibri", 14, True, False)
        silver_stamp = small_font.render("Silver: {0}".format(str(self.display_cache["silver"])),
                                         True,
                                         (255, 255, 255))
        self.cached_image.blit(silver_stamp, [3, 13])
        count = 0
        spacer = 14
        for artikel_name in self.display_cache["market visible items"]:
            artikel_name_stamp = small_font.render(artikel_name, True, (255, 255, 255))
            artikel_quantity_stamp = small_font.render(str(self.city.supply[artikel_name]), True, (255, 255, 255))
            artikel_price_stamp = small_font.render(str(self.city.purchase_price[artikel_name]), True, (200, 0, 0))

            self.cached_image.blit(artikel_quantity_stamp, [37,
                                                            60 + count * spacer])
            self.cached_image.blit(artikel_name_stamp, [90,
                                                        60 + count * spacer])
            self.cached_image.blit(artikel_price_stamp, [210,
                                                         60 + count * spacer])
            count += 1

        count = 0
        spacer = 14
        for artikel_name in self.display_cache["cargo visible items"]:
            if self.player.ship.cargo[artikel_name] > 0:
                artikel_name_stamp = small_font.render(artikel_name, True, (255, 255, 255))
                artikel_quantity_stamp = small_font.render(str(self.player.ship.cargo[artikel_name]), True, (255, 255, 255))
                artikel_price_stamp = small_font.render(str(self.city.sell_price[artikel_name]), True, (0, 210, 0))
                self.cached_image.blit(artikel_quantity_stamp, [252,
                                                                60 + count * spacer])
                self.cached_image.blit(artikel_name_stamp, [305,
                                                            60 + count * spacer])
                self.cached_image.blit(artikel_price_stamp, [440,
                                                             60 + count * spacer])
                count += 1
        cargo_stamp = small_font.render(self.display_cache["cargo cap"], True, (255, 255, 255))
        self.cached_image.blit(cargo_stamp, [314, 448])
        self.draw_selection_boxes()


class QuantityMenu(Menu):
    def __init__(self, game_state, player, city, artikel_name, transaction_type):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = quantity_popup
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = self.screen.get_width() / 2 - self.background_pane.image.get_width() / 2
        self.background_pane.rect.y = (self.screen.get_height() / 2) - self.background_pane.image.get_height() / 2
        self.artikel_name = artikel_name
        self.artikel_quantity = 0
        self.max_quantity = 0
        self.transaction_type = transaction_type
        self.city = city
        if self.transaction_type == "sale":
            self.max_quantity = self.player.ship.cargo[self.artikel_name]
        else:
            self.max_quantity = self.city.supply[self.artikel_name]
        self.step = 1

        self.transaction_modifiers = {"purchase": self.city.purchase_price[self.artikel_name],
                                      "sale": self.city.sell_price[self.artikel_name]}
        self.transaction_colors = {"purchase": (200, 0, 0),
                                   "sale": (0, 210, 0)}
        header_font = pygame.font.SysFont("Calibri", 18, True, False)

        self.display_cache = {"artikel quantity": self.artikel_quantity,
                              "artikel max": self.max_quantity,
                              "artikel name": header_font.render(self.artikel_name, True, (255, 255, 255))}

        self.update_display_cache()

        def quantity_up_click():
            cargo_margin = 0  # remaining empty space in the player's ship
            cargo_margin += self.player.ship.cargo_cap
            loaded_cargo = 0
            for artikel_name, quantity in self.player.ship.cargo.items():
                loaded_cargo += quantity
            cargo_margin -= loaded_cargo
            if self.artikel_quantity < self.max_quantity:
                self.artikel_quantity = min(self.artikel_quantity + self.step,
                                            self.max_quantity)
            self.update_display_cache()

        def quantity_down_click():
            if self.artikel_quantity > 0:
                self.artikel_quantity = max(self.artikel_quantity - self.step,
                                            0)
            self.update_display_cache()

        def max_click():
            self.artikel_quantity = self.max_quantity
            self.update_display_cache()

        def min_click():
            self.artikel_quantity = 0
            self.update_display_cache()

        def done_click():
            tcost = self.artikel_quantity * self.transaction_modifiers[self.transaction_type]
            if self.transaction_type == "purchase":
                if self.player.silver >= tcost:
                    current_cargo = 0
                    for artikel_id, quantity in self.player.ship.cargo.items():
                        current_cargo += quantity
                    if current_cargo + self.artikel_quantity <= self.player.ship.cargo_cap:
                        self.city.increment_supply(artikel_name, -self.artikel_quantity)
                        self.player.silver -= self.artikel_quantity * self.city.purchase_price[artikel_name]
                        if artikel_name in self.player.ship.cargo:
                            self.player.ship.cargo[artikel_name] += self.artikel_quantity
                        else:
                            self.player.ship.cargo[artikel_name] = self.artikel_quantity
                        self.open = False
            elif self.transaction_type == "sale":
                self.player.ship.cargo[self.artikel_name] -= self.artikel_quantity
                self.player.silver += self.artikel_quantity * self.city.sell_price[self.artikel_name]
                self.city.increment_supply(self.artikel_name, self.artikel_quantity)
                self.open = False

        def cancel_click():
            self.open = False
            self.artikel_quantity = 0

        def dragbar_click():
            self.dragging = True

        dragbar_r_img = pygame.Surface([self.background_pane.image.get_width() - 2, 9])
        dragbar_r_img.fill(util.colors.dragbar)

        dragbar = Button(dragbar_r_img,
                         dragbar_r_img,
                         dragbar_click,
                         1,
                         1)

        cancel_button = Button(cancel_r_img,
                               cancel_h_img,
                               cancel_click,
                               6,
                               130)

        done_button = Button(done_r_img,
                             done_h_img,
                             done_click,
                             90,
                             130)

        quantity_up_button = Button(arrow_r_r_img,
                                    arrow_r_h_img,
                                    quantity_up_click,
                                    157,
                                    58)

        quantity_down_button = Button(arrow_l_r_img,
                                      arrow_l_h_img,
                                      quantity_down_click,
                                      3,
                                      58)

        max_button = Button(max_r_img,
                            max_h_img,
                            max_click,
                            137,
                            96)

        min_button = Button(min_r_img,
                            min_h_img,
                            min_click,
                            3,
                            96)

        self.buttons = [done_button,
                        cancel_button,
                        quantity_up_button,
                        quantity_down_button,
                        max_button,
                        min_button,
                        dragbar]

    def keydown_handler(self, key):
        if key == pygame.K_LSHIFT or key == pygame.K_RSHIFT:
            self.step = 10
        elif key == pygame.K_LCTRL or key == pygame.K_RCTRL:
            self.step = 100

    def keyup_handler(self, key):
        if key == pygame.K_LSHIFT or key == pygame.K_RSHIFT:
            self.step = 1
        elif key == pygame.K_LCTRL or key == pygame.K_RCTRL:
            self.step = 1

    def update_display_cache(self):
        self.display_cache["artikel quantity"] = str(self.artikel_quantity)
        cost = self.artikel_quantity * self.transaction_modifiers[self.transaction_type]
        self.display_cache["transaction cost"] = str(cost)

    def render_decals(self, pos):
        small_font = pygame.font.SysFont("Calibri", 14, True, False)
        left_margin = (self.background_pane.image.get_width() / 2) - (self.display_cache["artikel name"].get_width() / 2)
        self.cached_image.blit(self.display_cache["artikel name"], [left_margin, 13])
        self.cached_image.blit(small_font.render("0",
                                                 True,
                                                 (255, 255, 255)),
                               [6, 80])
        self.cached_image.blit(small_font.render(str(self.display_cache["artikel max"]),
                                                 True,
                                                 (255, 255, 255)),
                               [150, 80])

        quantity_stamp = small_font.render(self.display_cache["artikel quantity"],
                                           True,
                                           (255, 255, 255))
        cost_string = self.display_cache["transaction cost"]
        cost_stamp = small_font.render("$ {0} ".format(str(cost_string)), True, self.transaction_colors[self.transaction_type])
        quantity_margin = (self.background_pane.image.get_width() / 2) - (quantity_stamp.get_width() / 2)
        cost_margin = (self.background_pane.image.get_width() / 2) - (cost_stamp.get_width() / 2)
        self.cached_image.blit(quantity_stamp, [quantity_margin, 80])
        self.cached_image.blit(cost_stamp, [cost_margin, 60])


class MiniMap(Menu):
    def __init__(self, game_state):
        super().__init__(game_state)
        self.background_pane = pygame.sprite.Sprite()
        map_image = game_state.active_map.biome_map_preview
        self.background_pane.image = art.mini_map_preview
        self.background_pane.image.blit(pygame.transform.rotate(map_image, -45),
                                        [2, 2])
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = game_state.screen_width - 200
        self.background_pane.rect.y = 0

        self.buttons = []

    def mouse_click_handler(self, event, pos):
        mouse_pos = (pos[0] - self.background_pane.rect.x,
                     pos[1] - self.background_pane.rect.y)

        if util.check_if_inside(0, self.background_pane.rect.width,
                                0, self.background_pane.rect.height,
                                mouse_pos):
            x_new, y_new = util.get_map_coords(mouse_pos, 0, 0, 102)
            x_pixel_new, y_pixel_new = util.get_screen_coords(x_new, y_new)
            x_shift = x_pixel_new - self.game_state.screen_width / 2
            self.game_state.active_map.x_shift = x_shift
            y_shift = y_pixel_new - self.game_state.screen_height / 2
            self.game_state.active_map.y_shift = y_shift

        for button in self.buttons:
            if util.check_if_inside(button.sprite.rect.x,
                                    button.sprite.rect.right,
                                    button.sprite.rect.y,
                                    button.sprite.rect.bottom,
                                    mouse_pos):
                button.click()

    def render_decals(self, pos):
        def get_visible_tile_square(x_shift, y_shift, background_x_middle, width, height):
            xw = math.floor(width / 40)
            yh = math.floor(height / 15)
            x = width - 198
            y = 2
            x2 = x - (x_shift / 40)
            y2 = y - (y_shift / 15)
            tile_square = pygame.Rect(x2, y2, xw, yh)
            # tile_square = tile_square.move(0, 0)
            return tile_square, x2, y2

        background_left, background_top, background_right, background_bottom, background_x_middle = self.game_state.display_parameters
        visible_tile_square, x, y = get_visible_tile_square(background_left,
                                                            background_top,
                                                            background_x_middle,
                                                            self.game_state.screen.get_width(),
                                                            self.game_state.screen.get_height())
        visible_tile_square.x -= self.background_pane.rect.x
        visible_tile_square.y -= self.background_pane.rect.y
        pygame.draw.rect(self.cached_image, util.colors.red, visible_tile_square, 1)
