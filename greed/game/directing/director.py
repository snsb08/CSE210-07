from game.shared.point import Point


class Director:
    """A person who directs the game. 

    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _display_service (DisplayService): For providing display output.
    """

    def __init__(self, keyboard_service, display_service):
        self._SCORE = 600
        self.__game_over = False
        """Constructs a new Director using the specified keyboard and display services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            display_service (DisplayService): An instance of DisplayService.
        """
        self._keyboard_service = keyboard_service
        self._display_service = display_service

    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._display_service.open_window()
        while self._display_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
            if self._is_over():
                self.__game_over = False
                self._display_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.

        Args:
            cast (Cast): The cast of actors.
        """
        robot = cast.get_first_actor("robots")
        velocity = self._keyboard_service.get_direction()
        robot.set_velocity(velocity)

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with artifacts.

        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("banners")
        robot = cast.get_first_actor("robots")
        artifacts = cast.get_actors("artifacts")
        rocks = cast.get_actors("rocks")

        banner.set_text("Score: " + str(self._SCORE))
        max_x = self._display_service.get_width()
        max_y = self._display_service.get_height()
        robot.move_next(max_x, max_y)

        for artifact in artifacts:
            artifact.set_velocity(Point(0, 5))
            artifact.move_next(max_x, max_y)

            if robot.get_position().equals(artifact.get_position()):
                message = self._SCORE
                banner.set_text(message)
                cast.remove_actor("artifacts", artifact)
                self._SCORE += 1

        for rock in rocks:
            rock.set_velocity(Point(0, 5))
            rock.move_next(max_x, max_y)
            if robot.get_position().equals(rock.get_position()):
                message = self._SCORE
                banner.set_text(message)
                cast.remove_actor("rocks", rock)
                self._SCORE -= 1
                if self._SCORE == 0:
                    self.__game_over = True

        banner.set_text("Score: " + str(self._SCORE))

    # The game over

    def _is_over(self):
        return self.__game_over

    def _do_outputs(self, cast):
        """Draws the actors on the screen.

        Args:
            cast (Cast): The cast of actors.
        """
        self._display_service.clear_buffer()
        actors = cast.get_all_actors()
        self._display_service.draw_actors(actors)
        self._display_service.flush_buffer()
