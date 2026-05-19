'''
Simple GUI Module containing ```TextButton``` and ```IconButton``` classes used
in the simulation developed by Rhylan M.

'''

# import externals
import pygame
from typing import override

# import locals
from src.constants import TOOLTIP_LENGTHS

# used for typehinting
class function:
    '''
    Simple empty class used for indicating a parameter should be set as a function.
    Used for typehinting in function/method params.

    Usage:
    ```
        def execute_function(func:function):
            func()
            print('Function executed successfully!')

        def print_text():
            print('Hello World!')
    ```

    >>> execute_function(print_text)
    Hello World!
    Function executed successfully!

    '''
    ...

# parent button class
class Button:
    '''
    The parent class with basic ```check_click()``` method.
    Pygame GUI button used for inheritence.
    
    '''
    # init method
    def __init__(self, rect:pygame.Rect, method:function) -> None:
        # store params
        self.rect = rect
        self.method = method

        # font for writing text
        self.font = pygame.font.SysFont(None, 24)

    # override the __str__ method
    @override
    def __str__(self) -> None: ...

    # method returns true if clicked else returns false
    def check_click(self, mouse_pos:list[float, float]) -> bool:
        '''
        Runs the Button's ```self.method()``` value. Returns ```True``` if 
        clicked; else returns ```False```.

        >>> Button.check_click(pos)
        False

        '''
        # check touch mouse
        if self.rect.collidepoint(mouse_pos):
            self.method()
            return True
        return False

# TextButton class : inherits from Button
class TextButton(Button):
    '''
    Child class inheriting from ```Button``` class.
    Has a new ```draw()``` method to draw self on pygame window
    with text on top.

    Colors can be specified however default to dark gray for normal
    and deep red for hover.

    '''
    # init method containing super
    def __init__(self, rect:pygame.Rect, text:str, method:function, color:tuple[int, int, int]=(50, 50, 50), selected_color:tuple[int, int, int]=(100, 0, 0)) -> None:
        super().__init__(rect, method)
        # store text param
        self.text = text

        self.base_y = self.rect.y

        self.color = color
        self.selected_color = selected_color

    # draw method
    def draw(self, screen:pygame.Surface, selected_bool:bool, y_scroll:int=0) -> None:
        '''
        Draw self on surface specified by ```screen``` param. Use the
        ```self.selected_color``` if ```selected_bool``` is True else use 
        ```self.color```. Set y value based on how far scrolled inset
        window is (default 0). Blits text as well.
        
        '''
        # conditional colour if selected
        color = self.selected_color if selected_bool else self.color

        # set y
        self.rect.y = self.base_y + y_scroll

        # draw rect then draw text
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        text = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.rect.x + 10, self.rect.y + 15))

# IconButton class : inherits from Button
class IconButton(Button):
    '''
    Child class inheriting from ```Button``` class.
    Has a new ```draw()``` method to draw self on pygame window
    with an image on top (thus the name IconButton).

    Also has a new method to show tooltip if the button
    is hovered.

    '''
    # init method containing super
    def __init__(self, rect:pygame.Rect, img:pygame.image, tooltip:str, method:function) -> None:
        super().__init__(rect, method)

        # store params as self variables
        self.tooltip = tooltip
        self.icon = img

    # draw method
    def draw(self, screen:pygame.Surface) -> None:
        '''
        Draw self on surface specified by ```screen``` param. Draw in a
        different color if the button is hovered.

        Blits an image on top of button as well.
        
        '''
        # draw circle
        pos = pygame.mouse.get_pos()
        color = (100, 100, 100) if self.rect.collidepoint(pos) else (50, 50, 50)
        pygame.draw.circle(screen, color, self.rect.center, self.rect.width // 2)
        
        # blit image on circle
        img_rect = self.icon.get_rect(center=self.rect.center)
        screen.blit(self.icon, img_rect)
    
    # show tooltip if button hovered
    def check_hover(self, mouse_pos:list[float, float], screen:pygame.Surface) -> None:
        '''
        Displays a tooltip when hovered for usability. Tooltip
        describes the function of the button.

        '''
        # check mouse collision
        if self.rect.collidepoint(mouse_pos):
            # create a translucent surface
            info_bg = pygame.Surface((TOOLTIP_LENGTHS[self.tooltip], 28))
            info_bg.set_alpha(180)
            info_bg.fill((30, 30, 30))
            screen.blit(info_bg, (mouse_pos[0] + 10, mouse_pos[1] + 10))

            # blit text onto surface
            text = self.font.render(self.tooltip, True, (255, 255, 255))
            screen.blit(text, (mouse_pos[0] + 15, mouse_pos[1] + 15))
        