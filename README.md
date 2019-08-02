# Multi-Pendulum Project
This build supports both simple and complex/compound pendulum (assuming no friction at the pivot or air resistance). 5 formulas of equations of motion for the multi-simple pendulum are derived via MatLab and the repository contains an example file for deriving complex pendulum equations of motion. This project allows for a fully customizable/interactive pendulum simulation with 3 methods for PDE-s and an ability to use none of them, comes with a GUI, is easily generalizable.  This project is to simply show that it is possible to create a simulation of N number of pendulums at once given the computational resources.

## Accession
To run this project simply clone the repository and run "py_pend_run.bat". Keep in mind to install the dependency:
```bash
pip install pygame
```

## Demo
Demonstration of the project:

<a href="https://www.youtube.com"><img src="https://s3.gifyu.com/images/123123bbb36354161fd2cc.gif" alt="123123bbb36354161fd2cc.gif" border="0" /></a>

For a better demo/explanation, visit [Youtube](https://www.youtube.com)

## Methods for Solving Partial Differential Equations (PDE-s)
The script currently contains 3 types of methods for solving PDE-s
1) Euler's Method with time complexity of O(n^2)
2) Runge-Kutta Method (II-order, I-derivative) with time complexity of O(n^3)
3) Runge-Kutta Method (IV-order, I-derivative) with time complexity of O(n^5)

It is important to note that different methods of solving equations greatly affect the overall motion of the pendula system. Currently (at least in this project), the RK-IV-I method can be used for closest approximation - keeping in mind that the RK-IV-I is the slowest of the 4.

The 4-th method simply implies not using any of the aforementioned methods to solve for velocity. Instead, we directly solve with respect to acceleration and change velocity FPS times per second, where FPS is a constant. Moreover, by the equations of motion it is implied that each pendulum has its own equation for the second order derivative of the angle with respect to time. since the length of the pendulum is constant, we can use polar coordinates and portray its position by a single variable - angle (fi), instead of 2 variables (x,y) on the cartesian plane. giving a single simple pendulum only 1 degree of freedom. which is great news.

The second order derivative of the angle with respect to time is acceleration. However our functions (Eqs of motion) do not have time as a variable implicitly, so we have to define them explicitly, such that dw(fi)/dt=C ==> w = C * t where w is velocity, Thus getting the desired result.


## Contributing
I welcome any pull requests. Keep in mind that the "my_gui.py" file requires optimization and reading it in its current state may be hard, focus on the main python script. Any questions regarding how it works can be directly sent to me at: aleksandrekhorbaladze@gmail.com

## License
[MIT](https://choosealicense.com/licenses/mit/)
