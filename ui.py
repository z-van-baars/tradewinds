import pygame
import utilities
import assets
import spice


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
    def __init__(self, screen, player):
        self.open = True
        self.screen = screen
        self.player = player
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

    def render_buttons(self, mouse_pos):
        for button in self.buttons:
            if utilities.check_if_inside(button.sprite.rect.x,
                                         button.sprite.rect.right,
                                         button.sprite.rect.y,
                                         button.sprite.rect.bottom,
                                         mouse_pos):
                button.sprite.image = button.hover
            else:
                button.sprite.image = button.regular
            self.screen.blit(button.sprite.image, [button.sprite.rect.x, button.sprite.rect.y])

    def keydown_handler(self, key):
        pass

    def keyup_handler(self, key):
        pass

    def render_decals(self, screen):
        pass

    def mouse_click_handler(self, mouse_pos):
        pass

    def menu_onscreen(self):
        while self.open:
            click = False
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_click_handler(mouse_pos)
                    click = True
                elif event.type == pygame.KEYDOWN:
                    self.keydown_handler(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup_handler(event.key)

            self.render_buttons(mouse_pos)

            for button in self.buttons:
                if utilities.check_if_inside(button.sprite.rect.x,
                                             button.sprite.rect.right,
                                             button.sprite.rect.y,
                                             button.sprite.rect.bottom,
                                             mouse_pos):
                    if click:
                        button.click()

            self.screen.blit(self.background_pane.image, [self.background_pane.rect.left, self.background_pane.rect.top])
            for button in self.buttons:
                self.screen.blit(button.sprite.image, [button.sprite.rect.x, button.sprite.rect.y])
            self.render_decals(self.screen)

            pygame.display.flip()


class PortPopup(Menu):
    def __init__(self, screen, player, port):
        super().__init__(screen, player)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = assets.port_screen
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = screen.get_width() / 2 - 150
        self.background_pane.rect.y = (screen.get_height() / 2) - 50

        self.port = port
        header_font = pygame.font.SysFont('Calibri', 18, True, False)
        self.name_stamp = header_font.render(port.name, True, (255, 255, 255))
        self.goto = False

        def x_click():
            self.open = False

        def goto_click():
            self.goto = True
            self.open = False

        x_button = Button(assets.x_regular,
                          assets.x_hover,
                          x_click,
                          self.background_pane.rect.right - 23,
                          self.background_pane.rect.top + 3)

        goto_button = Button(assets.goto_regular,
                             assets.goto_hover,
                             goto_click,
                             self.background_pane.rect.x + 3,
                             self.background_pane.rect.y + 30)

        self.buttons = [x_button, goto_button]

    def render_decals(self, screen):
        screen.blit(self.name_stamp, [self.background_pane.rect.x + 100,
                                      self.background_pane.rect.top + 2])

    def menu_onscreen(self):
        while self.open:
            click = False
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_click_handler(mouse_pos)
                    click = True
                elif event.type == pygame.KEYDOWN:
                    self.keydown_handler(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup_handler(event.key)

            self.render_buttons(mouse_pos)

            for button in self.buttons:
                if utilities.check_if_inside(button.sprite.rect.x,
                                             button.sprite.rect.right,
                                             button.sprite.rect.y,
                                             button.sprite.rect.bottom,
                                             mouse_pos):
                    if click:
                        button.click()

            self.screen.blit(self.background_pane.image, [self.background_pane.rect.left, self.background_pane.rect.top])
            for button in self.buttons:
                self.screen.blit(button.sprite.image, [button.sprite.rect.x, button.sprite.rect.y])
            self.render_decals(self.screen)

            pygame.display.flip()
        return self.goto


class PortMenu(Menu):
    def __init__(self, screen, player, port):
        super().__init__(screen, player)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = assets.port_screen
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = screen.get_width() / 2 - 150
        self.background_pane.rect.y = (screen.get_height() / 2) - 50

        self.port = port
        header_font = pygame.font.SysFont('Calibri', 18, True, False)
        self.name_stamp = header_font.render(port.name, True, (255, 255, 255))

        def market_click():
            # open a new market window
            new_market_window = MarketMenu(screen, player, port)
            new_market_window.menu_onscreen()
            self.open = False

        def x_click():
            self.open = False

        def view_port_click():
            # open display window for port data
            pass

        def repair_click():
            # open repair screen window
            pass

        x_button = Button(assets.x_regular,
                          assets.x_hover,
                          x_click,
                          self.background_pane.rect.right - 23,
                          self.background_pane.rect.top + 3)

        market_button = Button(assets.market_regular,
                               assets.market_hover,
                               market_click,
                               self.background_pane.rect.x + 3,
                               self.background_pane.rect.y + 30)

        view_port_button = Button(assets.view_port_regular,
                                  assets.view_port_hover,
                                  view_port_click,
                                  self.background_pane.rect.x + 180,
                                  self.background_pane.rect.y + 30)

        repair_button = Button(assets.repair_regular,
                               assets.repair_hover,
                               repair_click,
                               self.background_pane.rect.x + 86,
                               self.background_pane.rect.y + 30)

        self.buttons = [market_button, x_button, view_port_button, repair_button]

    def render_decals(self, screen):
        screen.blit(self.name_stamp, [self.background_pane.rect.x + 100,
                                      self.background_pane.rect.top + 2])


class MarketMenu(Menu):
    def __init__(self, screen, player, port):
        super().__init__(screen, player)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = assets.market_screen
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = screen.get_width() / 2 - 250
        self.background_pane.rect.y = (screen.get_height() / 2) - 250

        self.port = port
        header_font = pygame.font.SysFont('Calibri', 18, True, False)
        self.name_stamp = header_font.render("{0} Market".format(port.name), True, (255, 255, 255))

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

        def view_port_click():
            self.update_display_cache()
            # open display window for port data

        def sell_click():
            spice_name = self.display_cache["cargo visible items"][self.display_cache["cargo selected"]]
            spice_quantity = self.player.ship.cargo[spice_name]
            new_quantity_popup = QuantityMenu(screen, player, port, spice_name, spice_quantity, "sale")
            amount_to_sell = new_quantity_popup.menu_onscreen()
            if amount_to_sell != 0:
                print(self.player.ship.cargo[spice_name], amount_to_sell)
                self.player.ship.cargo[spice_name] -= amount_to_sell
                self.player.silver += amount_to_sell * self.port.sell_price[spice_name]
                self.port.supply[spice_name] += amount_to_sell
            self.update_display_cache()

        def buy_click():
            spice_name = self.display_cache["market visible items"][self.display_cache["market selected"]]
            spice_quantity = self.port.supply[spice_name]
            new_quantity_popup = QuantityMenu(screen, player, port, spice_name, spice_quantity, "purchase")
            amount_to_buy = new_quantity_popup.menu_onscreen()
            current_cargo = 0
            for commodity_name, commodity_quantity in self.player.ship.cargo.items():
                current_cargo += commodity_quantity
            if amount_to_buy != 0 and current_cargo + amount_to_buy <= self.player.ship.cargo_cap and amount_to_buy <= self.player.silver:
                self.port.supply[spice_name] -= amount_to_buy
                self.player.silver -= amount_to_buy * self.port.purchase_price[spice_name]
                if spice_name in self.player.ship.cargo:
                    self.player.ship.cargo[spice_name] += amount_to_buy
                else:
                    self.player.ship.cargo[spice_name] = amount_to_buy
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
            if self.display_cachce["cargo list top"] > 0:
                self.display_cache["cargo list top"] -= 1
                self.update_display_cache()

        def cargo_down_click():
            if self.display_cache["cargo list top"] < len(self.display_cache["cargo commodities list"]) - 1:
                self.display_cache["cargo list top"] += 1
                self.update_display_cache()

        x_button = Button(assets.x_regular,
                          assets.x_hover,
                          x_click,
                          self.background_pane.rect.right - 23,
                          self.background_pane.rect.top + 3)

        view_port_button = Button(assets.view_port_regular,
                                  assets.view_port_hover,
                                  view_port_click,
                                  self.background_pane.rect.x + 36,
                                  self.background_pane.rect.y + 440)

        sell_button = Button(assets.sell_regular,
                             assets.sell_hover,
                             sell_click,
                             self.background_pane.rect.right - 64,
                             self.background_pane.rect.bottom - 100)

        buy_button = Button(assets.buy_regular,
                            assets.buy_hover,
                            buy_click,
                            self.background_pane.rect.x + 14,
                            self.background_pane.rect.bottom - 100)

        market_up_arrow = Button(assets.arrow_up_regular,
                                 assets.arrow_up_hover,
                                 market_up_click,
                                 self.background_pane.rect.x + 14,
                                 self.background_pane.rect.y + 48)

        market_down_arrow = Button(assets.arrow_down_regular,
                                   assets.arrow_down_hover,
                                   market_down_click,
                                   self.background_pane.rect.left + 14,
                                   self.background_pane.rect.bottom - 125)

        cargo_up_arrow = Button(assets.arrow_up_regular,
                                assets.arrow_up_hover,
                                cargo_up_click,
                                self.background_pane.rect.right - 34,
                                self.background_pane.rect.y + 48)

        cargo_down_arrow = Button(assets.arrow_down_regular,
                                  assets.arrow_down_hover,
                                  cargo_down_click,
                                  self.background_pane.rect.right - 34,
                                  self.background_pane.rect.bottom - 125)

        self.buttons = [x_button,
                        view_port_button,
                        sell_button,
                        buy_button,
                        market_up_arrow,
                        market_down_arrow,
                        cargo_up_arrow,
                        cargo_down_arrow]

    def update_display_cache(self):
        self.display_cache["silver"] = self.player.silver
        current_cargo = 0
        for commodity_name, commodity_quantity in self.player.ship.cargo.items():
            current_cargo += commodity_quantity
        self.display_cache["cargo cap"] = "{0} / {1}".format(str(current_cargo), str(self.player.ship.cargo_cap))
        self.display_cache["market commodities list"] = []
        for commodity_name, commodity_quantity, in self.port.supply.items():
            if commodity_quantity > 0:
                self.display_cache["market commodities list"].append(commodity_name)
        self.display_cache["cargo commodities list"] = []
        for commodity_name, commodity_quantity, in self.player.ship.cargo.items():
            if commodity_quantity > 0:
                self.display_cache["cargo commodities list"].append(commodity_name)

        if self.display_cache["market selected"] > len(self.display_cache["market commodities list"]) - 1:
            self.display_cache["market selected"] -= 1
        if self.display_cache["cargo selected"] > len(self.display_cache["cargo commodities list"]) - 1:
            self.display_cache["cargo selected"] -= 1
        market_list = self.display_cache["market commodities list"]
        self.display_cache["market visible items"] = market_list[self.display_cache["market list top"]:self.display_cache["market list top"] + 20]
        cargo_list = self.display_cache["cargo commodities list"]
        self.display_cache["cargo visible items"] = cargo_list[self.display_cache["cargo list top"]:self.display_cache["cargo list top"] + 20]
        self.update_selection_boxes()

    def update_selection_boxes(self):
        x = self.background_pane.rect.left
        y = self.background_pane.rect.top
        box_y = y + 48 + ((self.display_cache["market selected"] - self.display_cache["market list top"]) * 14)
        self.display_cache["market selection box"].image = pygame.Rect(x + 37,
                                                                       box_y,
                                                                       208,
                                                                       15)
        box_y = y + 48 + ((self.display_cache["cargo selected"] - self.display_cache["cargo list top"]) * 14)
        self.display_cache["cargo selection box"].image = pygame.Rect(x + 252,
                                                                      box_y,
                                                                      208,
                                                                      15)

    def mouse_click_handler(self, mouse_pos):
        x = self.background_pane.rect.left
        y = self.background_pane.rect.top
        count = 0
        spacer = 14
        for each in self.display_cache["market visible items"]:
            x1 = x + 37
            x2 = x1 + 170
            y1 = (y + 48 + (count * spacer))
            y2 = y1 + 15
            if utilities.check_if_inside(x1, x2, y1, y2, mouse_pos):
                self.display_cache["market selected"] = count + self.display_cache["market list top"]
                self.update_display_cache()
            count += 1

        count = 0
        for each in self.display_cache["cargo visible items"]:
            x1 = x + 252
            x2 = x1 + 170
            y1 = (y + 48 + (count * spacer))
            y2 = y1 + 15
            if utilities.check_if_inside(x1, x2, y1, y2, mouse_pos):
                self.display_cache["cargo selected"] = count + self.display_cache["cargo list top"]
                self.update_display_cache()
            count += 1

    def draw_selection_boxes(self):
        if self.display_cache["market list top"] <= self.display_cache["market selected"] <= self.display_cache["market list top"] + 21:
            pygame.draw.rect(self.screen, (255, 198, 13), self.display_cache["market selection box"].image, 1)
        if self.display_cache["cargo list top"] <= self.display_cache["cargo selected"] <= self.display_cache["cargo list top"] + 21:
            pygame.draw.rect(self.screen, (255, 198, 13), self.display_cache["cargo selection box"].image, 1)

    def render_decals(self, screen):
        x = self.background_pane.rect.x
        y = self.background_pane.rect.y
        left_margin = (self.background_pane.image.get_width() / 2) - (self.name_stamp.get_width() / 2)
        screen.blit(self.name_stamp, [x + left_margin,
                                      y + 2])
        small_font = pygame.font.SysFont("Calibri", 14, True, False)
        silver_stamp = small_font.render("Silver: {0}".format(str(self.display_cache["silver"])),
                                         True,
                                         (255, 255, 255))
        screen.blit(silver_stamp, [x + 3, y + 3])
        count = 0
        spacer = 14
        for spice_name in self.display_cache["market visible items"]:
            spice_name_stamp = small_font.render(spice_name, True, (255, 255, 255))
            spice_quantity_stamp = small_font.render(str(self.port.supply[spice_name]), True, (255, 255, 255))
            spice_price_stamp = small_font.render(str(self.port.purchase_price[spice_name]), True, (200, 0, 0))

            screen.blit(spice_quantity_stamp, [x + 37,
                                               y + 50 + count * spacer])
            screen.blit(spice_name_stamp, [x + 90,
                                           y + 50 + count * spacer])
            screen.blit(spice_price_stamp, [x + 210,
                                            y + 50 + count * spacer])
            count += 1

        count = 0
        spacer = 14
        for spice_name in self.display_cache["cargo visible items"]:
            if self.player.ship.cargo[spice_name] > 0:
                spice_name_stamp = small_font.render(spice_name, True, (255, 255, 255))
                spice_quantity_stamp = small_font.render(str(self.player.ship.cargo[spice_name]), True, (255, 255, 255))
                spice_price_stamp = small_font.render(str(self.port.sell_price[spice_name]), True, (0, 210, 0))
                screen.blit(spice_quantity_stamp, [x + 252,
                                                   y + 50 + count * spacer])
                screen.blit(spice_name_stamp, [x + 305,
                                               y + 50 + count * spacer])
                screen.blit(spice_price_stamp, [x + 440,
                                                y + 50 + count * spacer])
                count += 1
        cargo_stamp = small_font.render(self.display_cache["cargo cap"], True, (255, 255, 255))
        screen.blit(cargo_stamp, [x + 314, y + 438])
        self.draw_selection_boxes()


class QuantityMenu(Menu):
    def __init__(self, screen, player, port, commodity, commodity_max, transaction_type):
        super().__init__(screen, player)
        self.background_pane = pygame.sprite.Sprite()
        self.background_pane.image = assets.quantity_popup
        self.background_pane.rect = self.background_pane.image.get_rect()
        self.background_pane.rect.x = screen.get_width() / 2 - 90
        self.background_pane.rect.y = (screen.get_height() / 2) - 70
        self.commodity_quantity = 0
        self.port = port
        self.step = 1
        self.transaction_type = transaction_type
        self.transaction_modifiers = {"purchase": self.port.purchase_price[commodity],
                                      "sale": self.port.sell_price[commodity]}
        self.transaction_colors = {"purchase": (200, 0, 0),
                                   "sale": (0, 210, 0)}
        header_font = pygame.font.SysFont("Calibri", 18, True, False)

        self.display_cache = {"commodity quantity": self.commodity_quantity,
                              "commodity max": commodity_max,
                              "commodity name": header_font.render(commodity, True, (255, 255, 255))}

        self.update_display_cache()

        def quantity_up_click():
            cargo_margin = 0
            cargo_margin += self.player.ship.cargo_cap
            loaded_cargo = 0
            for commodity_name, commodity_quantity in self.player.ship.cargo.items():
                loaded_cargo += commodity_quantity
            cargo_margin -= loaded_cargo
            if self.commodity_quantity < commodity_max:
                self.commodity_quantity = min(self.commodity_quantity + self.step,
                                              commodity_max,
                                              cargo_margin)
            self.update_display_cache()

        def quantity_down_click():
            if self.commodity_quantity > 0:
                self.commodity_quantity = max(self.commodity_quantity - self.step,
                                              0)
            self.update_display_cache()

        def done_click():
            self.open = False
            if self.transaction_type == "purchase":
                if self.player.silver < int(self.display_cache["transaction cost"]):
                    self.open = True

        def cancel_click():
            self.open = False
            self.commodity_quantity = 0

        cancel_button = Button(assets.cancel_regular,
                               assets.cancel_hover,
                               cancel_click,
                               self.background_pane.rect.left + 6,
                               self.background_pane.rect.top + 90)

        done_button = Button(assets.done_regular,
                             assets.done_hover,
                             done_click,
                             self.background_pane.rect.x + 90,
                             self.background_pane.rect.y + 90)

        quantity_up_button = Button(assets.arrow_right_regular,
                                    assets.arrow_right_hover,
                                    quantity_up_click,
                                    self.background_pane.rect.right - 23,
                                    self.background_pane.rect.top + 48)

        quantity_down_button = Button(assets.arrow_left_regular,
                                      assets.arrow_left_hover,
                                      quantity_down_click,
                                      self.background_pane.rect.left + 3,
                                      self.background_pane.rect.top + 48)

        self.buttons = [done_button,
                        cancel_button,
                        quantity_up_button,
                        quantity_down_button]

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
        self.display_cache["commodity quantity"] = str(self.commodity_quantity)
        cost = self.commodity_quantity * self.transaction_modifiers[self.transaction_type]
        self.display_cache["transaction cost"] = str(cost)

    def render_decals(self, screen):
        x = self.background_pane.rect.x
        y = self.background_pane.rect.y
        small_font = pygame.font.SysFont("Calibri", 14, True, False)
        left_margin = (self.background_pane.image.get_width() / 2) - (self.display_cache["commodity name"].get_width() / 2)
        screen.blit(self.display_cache["commodity name"], [x + left_margin, y + 3])
        screen.blit(small_font.render("0", True, (255, 255, 255)), [x + 6, y + 70])
        screen.blit(small_font.render(str(self.display_cache["commodity max"]), True, (255, 255, 255)),
                    [x + 150, y + 70])

        quantity_stamp = small_font.render(self.display_cache["commodity quantity"], True, (255, 255, 255))
        cost_string = self.display_cache["transaction cost"]
        cost_stamp = small_font.render("$ {0} ".format(str(cost_string)), True, self.transaction_colors[self.transaction_type])
        quantity_margin = (self.background_pane.image.get_width() / 2) - (quantity_stamp.get_width() / 2)
        cost_margin = (self.background_pane.image.get_width() / 2) - (cost_stamp.get_width() / 2)
        screen.blit(quantity_stamp, [x + quantity_margin, y + 70])
        screen.blit(cost_stamp, [x + cost_margin, y + 50])

    def menu_onscreen(self):
        while self.open:
            click = False
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_click_handler(mouse_pos)
                    click = True
                elif event.type == pygame.KEYDOWN:
                    self.keydown_handler(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup_handler(event.key)

            self.render_buttons(mouse_pos)

            for button in self.buttons:
                if utilities.check_if_inside(button.sprite.rect.x,
                                             button.sprite.rect.right,
                                             button.sprite.rect.y,
                                             button.sprite.rect.bottom,
                                             mouse_pos):
                    if click:
                        button.click()

            self.screen.blit(self.background_pane.image, [self.background_pane.rect.left, self.background_pane.rect.top])
            for button in self.buttons:
                self.screen.blit(button.sprite.image, [button.sprite.rect.x, button.sprite.rect.y])
            self.render_decals(self.screen)

            pygame.display.flip()
        return self.commodity_quantity
