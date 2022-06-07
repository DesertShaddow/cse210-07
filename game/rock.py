import random
from game.actor import Actor;
from game.shared.point import Point;
from game.shared.color import Color;

class Rock(Actor):
    """
        A Rock. This class inherits from Actor.        
    """

    def __init__(self):
        """
            Args: self - an instance of Rock
            Calls the init for the parent class (Actor)
            Sets the appearance of the rock, its score,
            and its initial velocity            
        """

        #Call parent init()
        super().__init__()

        #Set Appearance with parent set_text method
        super().set_text("0")

        #Set Points value with parent set_text method
        super().set_points(-1)

        #Set Velocity with parent set_text method
        speed = random.randrange(1,16)
        super().set_velocity(Point(0,speed))

        #Choose a random reddish to gray color for the rock
        r = random.randrange(200,255)
        g = random.randrange(128,175) 
        color = Color(r,g,g)       
        super().set_color(color)

     

        