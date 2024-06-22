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
    bc = BezierCurve(
        np.array([0.0,0.0,0.0]),
        np.array([5.0,5.0,5.0]),
        [np.array([1.0,1.5,4.0]), np.array([2.0,1.2,-3.0]), np.array([0.5, 0.5,0.5]), np.array([3.7, 0.1, 4.2]), np.array([4.2, 6.7, 3.1])]
        # [np.array([0.0,5.0,0.0])]
    )
    s = np.array([bc.calc(v) for v in inp])
    p3d = np.array(bc._p)
    ax = plt.figure().add_subplot(projection='3d')
    ax.plot(s[:,0], s[:,1], s[:,2])
    ax.scatter(p3d[:,0], p3d[:,1], p3d[:,2])
    plt.show()