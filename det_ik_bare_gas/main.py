import pygame
import pandas as pd
import pygame_widgets
from altair import value
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.toggle import Toggle
import asyncio

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (56, 117, 215)
YELLOW = (255, 255, 0)
GREY = (100, 100, 100)
GREY1 = (200, 200, 200)
GAME_STATE = 0

df = pd.read_csv("df.csv", delimiter=",")
df = df.sample(n=500, random_state=40)

# Get the min and max emission values from the DataFrame
min_emission = df["emission"].min()
max_emission = df["emission"].max()

# Data ranges
lon_unit = (600 - 16) / 42
lat_unit = (600 - 25) / 37

pygame.font.init()


bg = pygame.image.load("image.jpg")
bg = pygame.transform.smoothscale(bg, (1200, 600))

bg1 = pygame.image.load("image2.jpg")
bg1 = pygame.transform.smoothscale(bg1, (1200, 600))

title = pygame.image.load("title.png")
title = pygame.transform.smoothscale(title, (400, 100))

methan = pygame.image.load("methan.png")
methan = pygame.transform.smoothscale(methan, (120, 50))

kuldioxid = pygame.image.load("Kuldioxid.png")
kuldioxid = pygame.transform.smoothscale(kuldioxid, (150, 50))


eu_map = pygame.image.load("test.png")
eu_map = pygame.transform.scale(eu_map, (600, 600))


# Function to interpolate color based on emission values
def interpolate_color(emission, min_emission, max_emission, alpha=7):
    # Map emission values to a range between 0 and 1
    normalized_emission = (emission - min_emission) / (max_emission - min_emission)

    # Define colors for low and high emissions
    low_color = (34, 139, 34)
    high_color = (255, 69, 0)  # Dark Red

    # Interpolate color based on emission value
    interpolated_color = tuple(
        int(c1 * (1 - normalized_emission) + c2 * normalized_emission) for c1, c2 in zip(low_color, high_color)
    )

    # Ensure color components are within the valid range (0 to 255)
    interpolated_color = tuple(max(0, min(255, value)) for value in interpolated_color)

    # Include alpha value for transparency
    interpolated_color = interpolated_color + (alpha,)

    return interpolated_color


def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)


def draw_rect_alpha(surface, color, rect):
    target_rect = pygame.Rect(rect)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, target_rect)


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1200, 600

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption('Det Ik Bare Gas')
        font = pygame.font.Font(None, 24)

        # Create a slider with a range between 90 and 110 at position (300, 300)
        self.slider_0 = Slider(
            self._display_surf, 120, 160 + 50 + 100 + 50, 300, 10, min=0, max=20, handleColour=BLUE, colour=WHITE, handleRadius=10
        )
        # Create a text box (acting as a label) at position (475, 200)
        self.output_0 = TextBox(self._display_surf, 440, 145 + 50 + 100 + 50 - 10, 60, 50)
        self.output_0.disable()  # Disable editing, act as a label

        # Create a slider with a range between 90 and 110 at position (300, 300)
        self.slider_1 = Slider(
            self._display_surf, 120, 160 + 100 + 50 + 100 + 50, 300, 10, min=0, max=20, handleColour=BLUE, colour=WHITE, handleRadius=10
        )
        # Create a text box (acting as a label) at position (475, 200)
        self.output_1 = TextBox(self._display_surf, 440, 145 + 100 + 50 + 100 + 50 - 10, 60, 50)
        self.output_1.disable()  # Disable editing, act as a label

        # Create a slider with a range between 90 and 110 at position (300, 300)
        self.slider_2 = Slider(
            self._display_surf, 120, 160 + 200 + 50 + 100 + 50, 300, 10, min=0, max=20, handleColour=BLUE, colour=WHITE, handleRadius=10
        )
        # Create a text box (acting as a label) at position (475, 200)
        self.output_2 = TextBox(self._display_surf, 440, 145 + 200 + 50 + 100 + 50 - 10, 60, 50)
        self.output_2.disable()  # Disable editing, act as a label

        self.toggle = Toggle(self._display_surf, 255, 170, 80, 20, onColour=(150,150,150), handleOnColour=(200, 200, 200))

        self._running = True

    def on_event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self._running = False
        else:
            # Set the label text to the current value of the slider
            pygame_widgets.update(events)
            self.output_0.setText(str(self.slider_0.getValue() + 90) + "%")
            self.output_1.setText(str(self.slider_1.getValue() + 90) + "%")
            self.output_2.setText(str(self.slider_2.getValue() + 90) + "%")

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.blit(bg1, (0, 0))
        self._display_surf.blit(eu_map, (600, 0))
        self._display_surf.blit(title, (80, 20))
        self._display_surf.blit(kuldioxid, (60, 150))
        self._display_surf.blit(methan, (400, 150))
        # Draw a black rectangle (200x400) with 50% transparency at (50, 200)
        rect_color = (0, 0, 0, 128)  # Black with alpha (128 for 50% transparency)
        rect_size = (500, 425)
        rect_position = (50, 100 + 120)
        draw_rect_alpha(self._display_surf, rect_color, (*rect_position, *rect_size))
        if GAME_STATE == 0:
            label_title = pygame.font.Font(None, 64).render("Parametre", True, WHITE)
            label_text = pygame.font.Font(None, 24).render("Temperatur", True, GREY1)
            label_text_1 = pygame.font.Font(None, 24).render("Vandindhold", True, GREY1)
            label_text_2 = pygame.font.Font(None, 24).render("Permafrost", True, GREY1)
            self._display_surf.blit(label_title, (100, 180 + 70))
            self._display_surf.blit(label_text, (100, 180 + 100 + 50))
            self._display_surf.blit(label_text_1, (100, 280 + 100 + 50))
            self._display_surf.blit(label_text_2, (100, 380 + 100 + 50))
            for index, row in df.iterrows():
                lon = row["lon"]*0.7 + 30
                lat = (row["lat"]*1.2 - 50)
                emission = row["emission"]
                # Calculate Pygame coordinates
                pygame_x = 600 + 8 + int(lon * lon_unit)
                pygame_y = 600 - 4 - int(lat * lat_unit)

                # Interpolate the color based on emission value
                circle_color = interpolate_color(
                    emission + self.slider_0.getValue() * 600 + self.slider_1.getValue() * 300 - self.slider_2.getValue() * 600,
                    min_emission,
                    max_emission,
                )

                draw_circle_alpha(self._display_surf, circle_color, (pygame_x, pygame_y), 80)

                # Draw a circle on the Pygame surface
                # Use 'ordered_clustering' to determine the color
                # cluster_label = row['cluster_ordered']
                # color = color_mapping.get(cluster_label, (255, 255, 255))  # Default to white if label not in mapping
                # draw_circle_alpha(self._display_surf, color, (pygame_x, pygame_y), 10)
        else:
            return 0

    def on_cleanup(self):
        pygame.quit()

    async def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            events = pygame.event.get()
            self.on_render()
            self.on_event(events)
            self.on_loop()
            pygame.display.update()
            await asyncio.sleep(0)

        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    asyncio.run(theApp.on_execute())
