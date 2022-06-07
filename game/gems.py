import random
from game.actor import Actor;
from game.shared.color import Color;
from game.shared.point import Point;

class Gems(Actor):

    """
        A Gems. This class inherits from Actor.        
    """

    def __init__(self):

        """
            Args: self - an instance of Gems.
            Calls the init for the parent class (Actor)
            Sets the appearance of Gems, its score,
            and its initial velocity.            
        """

        #Call the parent init
        super().__init__()

        #set the look of the gems
        super().set_text("*")

        #set the points for gems, adding a point for each gem hit.
        super().set_points(+1)

        #Set Velocity with parent set_text method
        speed = random.randrange(1,16)
        super().set_velocity(Point(0,speed))

        #Choose a random brilliant color for the rock
        r = random.randrange(5,232)
        g = random.randrange(20,35)
        b = random.randrange(5,173) 
        color = Color(r,g,b)       
        super().set_color(color)

        