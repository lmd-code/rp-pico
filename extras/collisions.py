"""
Collision Detection Functions
"""

def get_bounds(obj):
    """
    Get object bounding box (left/right/top/bottom edges)
    
    Parameters
    ----------
    
    obj: dict
        Dictionary object containing the x/y coordinates and width/height of object
    """
    return  {
        'l': obj['x'],
        'r': obj['x'] + obj['w'] - 1,
        't': obj['y'],
        'b': obj['y'] + obj['h'] - 1
    }


def edge_collision(player, target):
    """
    Detect when player collides with the outer edge of the playing area
    """
    pb = get_bounds(player)
    tb = get_bounds(target)

    if pb['l'] < tb['l'] or pb['r'] > tb['r'] or pb['t'] < tb['t'] or pb['b'] > tb['b']:
        return True # Collision detected

    return False


def box_collision(player, target):
    """
    Detect when player collides with another object 
    """
    pb = get_bounds(player)
    tb = get_bounds(target)

    if pb['l'] <= tb['r'] and pb['r'] >= tb['l'] and pb['t'] <= tb['b'] and pb['b'] >= tb['t']:
        return True # Collision detected

    return False
