# Arcadify by Alexander Cleary
from os import path


class Arcadify:
    def __init__(self, screen, pygame):
        self.screen = screen
        self.path = path.dirname(path.realpath(__file__))
        self.pygame = pygame

        def fetch(filename):
            return path.join(self.path, filename)

        self.special_chars = {
            '?': 'question_mark',
            '!': 'exclamation',
            '.': 'decimal_point',
            '%': 'decimal_point',
            ':': 'colon',
            '-': 'hyphen',
            '_': 'underscore',
            ',': 'comma',
        }
        self.fontKey = (['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                         'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                         '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                        + list(self.special_chars.values()) + ['unknown'])

        self.font = {
            'white': [pygame.image.load(fetch(f'font/white/{i}.png')) for i in self.fontKey],
            'yellow': [pygame.image.load(fetch(f'font/yellow/{i}.png')) for i in self.fontKey],
            'blue': [pygame.image.load(fetch(f'font/blue/{i}.png')) for i in self.fontKey],
            'red': [pygame.image.load(fetch(f'font/red/{i}.png')) for i in self.fontKey],
            'black': [pygame.image.load(fetch(f'font/black/{i}.png')) for i in self.fontKey],
        }

    def render(self, text, x_coord, y_coord, colour="white", size=1):
        if colour not in self.font.keys():
            raise RuntimeError("Colour is not in list of accepted colours.")
        text = str(text)

        for i, digit in enumerate(text):
            if digit.isdigit():
                self.screen.blit(self.pygame.transform.scale(self.font[colour][int(digit) + 26],
                                                             (7 * size, 7 * size)), (x_coord + i * 8 * size, y_coord))
            elif digit in self.special_chars.keys():
                self.screen.blit(
                    self.pygame.transform.scale(self.font[colour][36 + list(self.special_chars.keys()).index(digit)],
                                                (7 * size, 7 * size)), (x_coord + i * 8 * size, y_coord))
            elif digit.isalpha():
                if digit.islower():
                    digit = ord(digit) - ord('a')
                else:
                    digit = ord(digit) - ord('A')
                self.screen.blit(self.pygame.transform.scale(self.font[colour][int(digit)],
                                                             (7 * size, 7 * size)), (x_coord + i * 8 * size, y_coord))
            elif digit == " ":
                pass
            else:
                self.screen.blit(self.pygame.transform.scale(self.font[colour][-1],
                                                             (7 * size, 7 * size)), (x_coord + i * 8 * size, y_coord))
