import cv2
import numpy as np
def canny(img,par1=200,par2=400):
    l = cv2.cvtColor(img,cv2.COLOR_BGR2HLS)[:, :, 1]
    blur = cv2.bilateralFilter(l, 7, 10, 20)
    edge = cv2.Canny(blur, par1, par2)
    return edge

def gridFront(img, cols=7, rows=3, update_img=False):
    points,img2 = findGrid(img,img,cols,rows)
    return points,img2

def drawGrid(img2, v_bounds, u_bounds, u_max, v_max, c_v, c_u, color):
    #cv2.line(img2, (c_u, max(c_v - 50, 0)), (c_u, v_max), (0, 0, 255), 2)
    for v_bound in v_bounds:
        cv2.line(img2, (0, v_bound), (u_max, v_bound), color, 2)
    for u_bound in u_bounds:
        cv2.line(img2, (u_bound, c_v), (u_bound, v_max), color, 2)
    return img2

def findGrid(img, img2, cols, rows,grid_line_color=(39, 157, 47),v_point_color=(221, 0, 255),u_point_color=(18, 246, 255)):
    V, L, R = [], [], []
    edge = canny(img)
    u_max, v_max = 639, 479
    c_v, c_u = 309,320
    v_bounds = [int(c_v + (v_max - c_v) * i / (rows + 1)) for i in range(1, rows + 1)]
    u_bounds = [int(u_max * i / (cols + 1)) for i in range(1, cols + 1)]
    
    img2 = drawGrid(img2, v_bounds, u_bounds, u_max, v_max, c_v, c_u, grid_line_color)
    
    for u_bound in u_bounds:
        vertical_slice = edge[:, u_bound]
        y, = np.nonzero(vertical_slice)
        y = y[y >= c_v]
        if len(y):
            y_max = np.max(y)
            V.append(v_max - y_max)
            cv2.circle(img2, (u_bound, y_max), 5, v_point_color, -1)
        else:
            V.append(v_max - c_v + 1)
    for v_bound in v_bounds:
        horizontal_slice = edge[v_bound, :]
        x, = np.nonzero(horizontal_slice)
        left = x[x <= c_u]
        if len(left):
            left_max = np.max(left)
            L.append(c_u - left_max)
            cv2.circle(img2, (left_max, v_bound), 5, u_point_color, -1)
        else:
            L.append(c_u + 1)
        right = x[x >= c_u]
        if len(right):
            right_min = np.min(right)
            R.append(right_min - c_u)
            cv2.circle(img2, (right_min, v_bound), 5, u_point_color, -1)
        else:
            R.append(u_max - c_u + 1)
    return (V, L, R), img2