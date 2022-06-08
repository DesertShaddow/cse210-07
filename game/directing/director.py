from game.gems import Gems
from game.rock import Rock

class Director:
    '''
    '''
    
    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service

        self.gems = Gems()
        self.rocks = Rock()
        
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

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the player.
        
        Args:
            cast (Cast): The cast of actors.
        """

        player = cast.get_first_actor("players")
        velocity = self._keyboard_service.get_direction()
        player.set_velocity(velocity)

    def _do_updates(self, cast):
        """Updates the player's position and adds or subtracts any points with falling objects.
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor('banner')
        player = cast.get_first_actor("players")

        # banner.set_text("")
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        player.move_next(max_x, max_y)
        
        for rock in self.rocks:
            if player.get_position().close_enough():
                points = rock.get_points()
                banner.set_text(points)
        
        for gem in self.gems:
            if player.get_position().close_enough():
                points = gem.get_points()
                banner.set_text(f'Score: {points}')    
        
    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()