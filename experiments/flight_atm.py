from math import sqrt, pi


g = 9.81
p = 1.25

g = 0


def simulate_one_stage(mv, mf, u, h0, v0, isp, dm, dt, r):
    """

    :param mv: Vehicle mass
    :param mf: Fuel mass
    :param u: Drag coefficient
    :param h0: Start height
    :param v0: Start velocity
    :param isp: ISP in m/s
    :param dm: Engine dm / 1 second
    :param dt: Simulation accuracy
    :param r: Rocket radius
    :return:
    """

    print('')
    print('############################################')

    velocity = v0
    height = h0
    time = 0

    p_rp1 = 1000
    p_h2 = 250

    h_rp1 = mf / (p_rp1 * pi * r * r)
    h_h2 = mf / (p_h2 * pi * r * r)
    print('HEIGHT IF FUEL IS RP1: {}'.format(h_rp1))
    print('HEIGHT IF FUEL IS H2: {}'.format(h_h2))

    while True:
        if mf >= dm * dt:
            dmp = dm * dt
        else:
            dmp = mf

        mf -= dmp
        f = isp * dmp / dt

        a = f / (mv + mf)
        a -= g * dt

        a_aero = u * p * pi * r * r * velocity * velocity / 2 / (mv + mf)
        if velocity > 0:
            a_aero = -a_aero
        a += a_aero * dt

        height += velocity * dt
        velocity += a * dt

        time += dt

        if a <= 0:
            break

    return height, velocity, time


if __name__ == '__main__':
    print(simulate_one_stage(5, 100, 0.5, 0, 0, 4800, 0.5, 0.01, 0.15))
