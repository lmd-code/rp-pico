"""
Object Movement Functions

For moving objects around a screen in games etc
"""

# Assign directions to angles/degrees of circle (can be assigned to 'dpad' buttons)
DIRECTIONS = {
    'up': 0,     # north/forward
    'right': 90, # east/clockwise
    'down': 180, # south/backward
    'left': 270  # west/counter-clockwise
}


def move(x: int, y: int, direction: int, speed: int) -> tuple[int, int]:
    """
    Move object
    
    Move the object x/y coordinate position in the given direction at the given speed.

    Parameters
    ----------
    x: int
        Current x coordinate in pixels
    y: int
        Current y coordinate in pixels
    direction: int
        Direction to move object in degrees
    speed: int
        Speed to move object in pixels (more pixels = faster)

    Returns
    -------
    x: int
        New x coordinate in pixels
    y: int
        New y coordinate in pixels
    """
    if direction == DIRECTIONS['up']:
        y -= speed
    elif direction == DIRECTIONS['down']:
        y += speed
    elif direction == DIRECTIONS['left']:
        x -= speed
    elif direction == DIRECTIONS['right']:
        x += speed

    return x, y


def flip(current_direction) -> int:
    """
    Flip direction
    
    Reverse the current direction (rotate by 180 degrees) of object
    
    Parameters
    ----------    
    current_direction: int
        Current direction in degrees

    Returns
    -------
    int
        New direction in degrees
    """
    return rotate(current_direction, 180)


def turn_right(current_direction) -> int:
    """
    Turn right

    Change direction by 90 degrees clockwise
    
    Parameters
    ----------
    current_direction: int
        Current direction in degrees

    Returns
    -------
    int
        New direction in degrees
    """
    return rotate(current_direction, 90)


def turn_left(current_direction) -> int:
    """
    Turn left

    Change direction by 90 degrees counter-clockwise
    
    Parameters
    ----------
    current_direction: int
        Current direction in degrees

    Returns
    -------
    int
        New direction in degrees
    """
    return rotate(current_direction, 90, True)


def rotate(current_position, rotate_by, ccw = False) -> int:
    """
    Rotate object a specified number of degrees clockwise or counter-clockwise.
    
    Paramters:
    ----------
    current_position: int
        Current position in degrees
    rotate_by: int
        Number of degrees to rotate (will wrap around 360 back to 0)
    ccw: bool, default False
        Rotate counter-clockwise (default is clockwise)

    Returns
    -------
    int
        New position in degrees
    """
    if ccw:
        return (current_position - rotate_by) % 360 # counter-clockwise
        
    return (current_position + rotate_by) % 360 # clockwise
