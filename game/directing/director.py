import random

from game.shared.point import Point
from game.rock import Rock
from game.gems import Gems
from game.shared.color import Color

MAX_GEMS = 15
MAX_ROCKS = 20

class Director:
    """Director - A class that directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
        _score holds the player score
    """
   
    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._score = 0
        
    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
        self._video_service.close_window()

    def _add_score(self, points):
        """
            Adds points to score
            Args: self - an instance of director,
                points to add
        """
        self._score += points

    def _get_score(self):
        """
          Returns current score
          Args: self - an instance of director
        """
        return self._score   

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the player.
        
        Args:
            cast (Cast): The cast of actors.
        """

        player = cast.get_first_actor("players")
        velocity = self._keyboard_service.get_direction()
        #constrain velocity to x axis
        velocity._y = 0
        player.set_velocity(velocity)

    def _do_updates(self, cast):
        """Updates the player's position and adds or subtracts any points with falling objects.
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor('banners')
        player = cast.get_first_actor('players')
        rocks = cast.get_actors("rocks")
        gems = cast.get_actors("gems")

        # get screen dimensions: max_x and max_y 
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        player.move_next(max_x, max_y)
        cell_size = self._video_service.get_cell_size()

        # Random chance to spawn rocks and gems if fewer than MAX
        if len(rocks) < MAX_ROCKS:
            if random.randrange(0,10) == 8:
                new_rock = Rock()
                
                column = int(max_x / cell_size)
                location = Point(random.randrange(column)*cell_size,0)
                new_rock.set_position(location)
                cast.add_actor("rocks",new_rock)

        if len(gems) < MAX_GEMS:
            if random.randrange(0,20) == 8:
                new_gem = Gems()
                
                column = int(max_x / cell_size)
                location = Point(random.randrange(column)*cell_size,0)
                new_gem.set_position(location)
                cast.add_actor("gems",new_gem)
        
        for rock in rocks:
            rock.move_next(max_x, max_y)
            y = rock.get_position().get_y()

            # Check for collision with player
            if player.get_position().close_enough(rock.get_position(), cell_size):
                self._add_score(rock.get_points())
                cast.remove_actor("rocks",rock)
            #remove the rock when it reaches the bottom of the screen
            elif y > max_y - cell_size:
                cast.remove_actor("rocks",rock)
        
        for gem in gems:

            #move the gem
            gem.move_next(max_x, max_y)
            y = gem.get_position().get_y()

            #Make the gem sparkle!
            r = y%128 + 128
            g = int(y*3)%128 + 128
            b = int(y*5)%128 + 128
            color = Color(r,g,b)
            gem.set_color(color)

            #Check for collision or reaching the bottom of the screen
            if player.get_position().close_enough(gem.get_position(), cell_size):
                self._add_score(gem.get_points())
                cast.remove_actor("gems",gem)
            #remove the rock when it reaches the bottom of the screen
            elif y > max_y - cell_size:
                cast.remove_actor("gems",gem) 
            
        # Update banner with score
        banner.set_text(f"Score: {self._get_score()}")

    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()