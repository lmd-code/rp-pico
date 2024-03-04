"""
DPAD (4 button) - Direction and Rotation Functions
"""

# Assign directions to angles/degrees of circle (0-359) - these are assigned to buttons
DIRECTIONS = {
    'up': 0,
    'right': 90,
    'down': 180,
    'left': 270
}

def flip(direction):
    """
    Flip direction (turn 180 degrees) - useful for bouncing off wall. Shortcut for rotate function.
    
    Parameters
    ----------
    
    direction: int
        Current direction
    """
    
    return rotate(direction, 180)


def turn(direction, ccw = False):
    """
        Rotate direction 90 degrees clockwise (default) or counter-clockwise. Shortcut for rotate function.
        
        Parameters
        ----------
        
        direction: int
            Current direction
            
        ccw: bool
            Rotate counter-clockwise (default: False, rotate clockwise)
    """

    return rotate(direction, 90, ccw)


def rotate(direction, degrees, ccw = False):
    """
    Rotate from current position a specified number of degrees clockwise or counter-clockwise.
    
    Paramters:
    ----------
    
    direction: int
        Current direction
    
    degrees: int
        Number of degrees to rotate (will rotate around 360 back to 0)

    ccw: bool
        Rotate counter-clockwise (default: False, rotate clockwise)
    """
    
    if ccw:
        return (direction - degrees) % 360 # counter-clockwise
        
    return (direction + degrees) % 360 # clockwise
