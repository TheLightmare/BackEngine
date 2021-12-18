import pygame


class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, game, action, text, pos, font, feedback=""):
        self.screen = game.screen
        self.text = text
        self.action = action
        self.x, self.y = pos
        self.font = font
        self.game = game
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(self.text, "black")

    def change_text(self, text, bg="black"):
        """Change the text when you click"""
        self.textsurface = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.textsurface.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.textsurface, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self):
        self.screen.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    run = True
                    while run :
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONUP :
                                run = False
                    self.game.do_action(self.action)