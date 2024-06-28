from pyray import Vector2, Vector3
import numpy as np
from math import factorial

class BezierCurve:
    def __init__(self, start_point: np.ndarray, end_point: np.ndarray, control_points: list[np.ndarray]):
        self._sp = start_point
        self._ep = end_point
        self._cp = control_points
        self._p = [start_point, *control_points, end_point]

    def calc(self, t):
        n = len(self._p)
        a = np.zeros(self._sp.shape)
        # print(n)
        for i, p in enumerate(self._p):
            bc = factorial(n)/(factorial(i)*factorial(n-i))
            a = a + bc*((1 - t)**(n - i))*(t**i)*p
        a = a + (t**n)*self._p[-1]
        return a

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    bc = BezierCurve(
        np.array([0.0,0.0]),
        np.array([5.0,5.0,]),
        [np.array([1.0,1.5]), np.array([2.0,1.2]), np.array([0.5, 0.5]), np.array([3.7, 0.1]), np.array([4.2, 6.7])]
    )
    inp = np.linspace(0, 1, 50)
    s = [bc.calc(v) for v in inp]
    s_ = np.array(s)
    x = s_[:,0]
    y = s_[:,1]
    points = np.array(bc._p)
    # fig, ax = plt.subplots()
    # ax.plot(x, y)
    # ax.scatter(points[:,0], points[:,1])
    # plt.show()
    coord = 10.0
    bc = BezierCurve(
        np.array([18.0,16.0,18.0]),
        np.array([0.0,5.5,0.0]),
        [
            np.array([20.0, 4.0, 0.0]),
        ]
        # [np.array([0.0,5.0,0.0])]
    )
    pillers = np.array([
        [ coord, 0,  coord],
        [-coord, 0,  coord],
        [ coord, 0, -coord],
        [-coord, 0, -coord],
    ])
    bc2 = BezierCurve(
        np.array([0.0,5.5,0.0]),
        np.array([-18.0,5.5,-18.0]),
        [
            np.array([-20.0, 4.0, 0.0]),
        ]
        # [np.array([0.0,5.0,0.0])]
    )
    bc3 = BezierCurve(
        np.array([18.0,10.5,18.0]),
        np.array([-18.0,5.5,-18.0]),
        [
            np.array([18.0, 2.5, -20.0]),
            np.array([-18.0, 2.5, 20.0]),

        ]
        # [np.array([0.0,5.0,0.0])]
    )
    bc3 = BezierCurve(
        np.array([18.0,10.5,18.0]),
        np.array([-0.0,2.5,18.0]),
        [
            np.array([18.0, 3.5, -10.0]),
            np.array([-25.0, 3.5, -40.0]),
            np.array([-8.0, 3.5, -60.0]),
            np.array([-45.0, 2.5, 55.0]),
        ]
        # [np.array([0.0,5.0,0.0])]
    )
    s = np.array([bc.calc(v) for v in inp])
    s2 = np.array([bc2.calc(v) for v in inp])
    s3 = np.array([bc3.calc(v) for v in inp])
    print(s[-1])
    p3d = np.array(bc._p)
    p3d3 = np.array(bc3._p)
    ax = plt.figure().add_subplot(projection='3d')
    ax.scatter(pillers[:,0], pillers[:,2], pillers[:,1])
    # ax.plot(s[:,0], s[:,2], s[:,1])
    # ax.scatter(p3d[:,0], p3d[:,2], p3d[:,1])
    # ax.plot(s2[:,0], s2[:,2], s2[:,1])
    ax.plot(s3[:,0], s3[:,2], s3[:,1])
    ax.scatter(p3d3[:,0], p3d3[:,2], p3d3[:,1])
    plt.show()