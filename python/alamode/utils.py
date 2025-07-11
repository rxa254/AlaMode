import matplotlib.pyplot as plt

def dsxy2figxy(ax, dsxy):
    bbox = ax.get_position()
    if len(dsxy) == 2:
        return (bbox.x0 + dsxy[0]*bbox.width, bbox.y0 + dsxy[1]*bbox.height)
    x0 = bbox.x0 + dsxy[0]*bbox.width
    y0 = bbox.y0 + dsxy[1]*bbox.height
    w = dsxy[2]*bbox.width
    h = dsxy[3]*bbox.height
    return (x0, y0, w, h)
