import math
from matplotlib import pyplot as plt

import objects.stage
import objects.parachute
import objects.engine

import calc
import utilities

# Program entry point
if __name__ == '__main__':
    print("Loading configuration...")
    config = utilities.load_simulation_config("config.json")

    M1 = config["planet_1_mass"]
    M2 = config["planet_2_mass"]

    R1 = config["planet_1_radius"]
    R2 = config["planet_2_radius"]

    x0 = config["x0"]
    y0 = config["y0"]
    m0 = 0
    dt = config["delta_time"]

    T0 = config["T0"]
    P0 = config["P0"]

    # Stage info reader
    stages = []
    for stage_info in config["stages"]:
        em = stage_info["empty_mass"]
        fm = stage_info["fuel_mass"]
        at = stage_info["active_time"]
        dc = stage_info["drag_coefficient"]
        sa = stage_info["surface_area"]

        th = stage_info["thrust"]
        fc = stage_info["fuel_consumption"]
        engine = objects.engine.Engine(th, fc)

        pd = stage_info["parachute_deploy"]
        pa = stage_info["parachute_area"]
        parachute = objects.parachute.Parachute(pa, pd)

        stages.append(objects.stage.Stage(em, fm, at, dc, sa, engine, parachute))
        m0 += (em + fm)
    
    print("=== INITIAL DATA ===")
    print(f"Start X: {x0} m")
    print(f"Start Y: {y0} m")
    print(f"Simulation timestep: {dt} s")
    print(f"Rocket stages count: {len(stages)}\n")

    # Simulation cycle
    print("=== SIMULATION ===")
    eps = 10**(-30)

    # Initializing simulation variables
    x = x0 + eps
    y = y0 + eps
    ax = eps
    ay = eps
    overall_time = 0
    vx = 0
    vy = 0
    m = m0

    xm = 12*10**6
    ym = 0
    Tm = 139000

    # Simulation data recordings
    X_ARRAY = []
    XM_ARRAY = []
    YM_ARRAY = []
    RM_ARRAY = []
    Y_ARRAY = []
    V_ARRAY = []
    T_ARRAY = []
    R_ARRAY = []

    for stage in stages:
        print("--> Starting new stage")

        C = stage.drag_coefficient
        S = stage.surface_area
        Ft = stage.engine.thrust
        k = stage.engine.consumption
        fuel = stage.fuel_mass
        has_fuel = True

        for t in range(overall_time, stage.active_time + overall_time, dt):
            # Applying current velocity and coordinates
            vx = vx + ax * dt
            vy = vy + ay * dt
            x = x + vx * dt + 0.5 * ax * dt**2
            y = y + vy * dt + 0.5 * ay * dt**2
            
            # Computing new Muna coordinates
            xm = 12*10**6 * math.cos(2 * math.pi * t / Tm)
            ym = 12*10**6 * math.sin(2 * math.pi * t / Tm)

            # Computing current scalar parameters
            r = math.sqrt(x**2 + y**2)
            rm = math.sqrt((xm - x)**2 + (ym - y)**2)
            v = math.sqrt(vx**2 + vy**2)
            d = calc.calculate_air_density(P0, T0, r - R1, M1, R1)

            # Save new plot data
            if overall_time % 60 == 0:
                XM_ARRAY.append(xm / 1000)
                YM_ARRAY.append(ym / 1000)
                RM_ARRAY.append(rm / 1000)
                X_ARRAY.append(x / 1000)
                Y_ARRAY.append(y / 1000)
                V_ARRAY.append(v)
                T_ARRAY.append(t / 60)
                R_ARRAY.append((r - R1) / 1000)

            if r - R1 < 0:
                print("CRASH!")
                utilities.draw_graph(X_ARRAY, Y_ARRAY, "km", "km", "Motion trajectory")
                utilities.draw_graph(T_ARRAY, RM_ARRAY, "t, min", "km", "Muna distance")
                utilities.draw_graph(XM_ARRAY, YM_ARRAY, "km", "km", "Muna trajectory")
                utilities.draw_graph(T_ARRAY, V_ARRAY, "t, min", "m/s", "Velocity - V(t)")
                utilities.draw_graph(T_ARRAY, R_ARRAY, "t, min", "km", "h(t)")
                exit()

            # Computing new gravity forces and their projection angles
            Fe = calc.calculate_planet_gravity(M1, m, r)
            alpha = math.atan2(y, x) - math.pi
            Fm = calc.calculate_planet_gravity(M2, m, rm)
            gamma = math.pi + math.atan2(ym - y, xm - x)

            # Simplest thrust direction control
            if t <= 60:
                theta = math.pi / 13
            elif (t > 60) and (t < 500):
                theta = math.pi / 14
            elif (t > 1200) and (t <= 1480):
                theta = math.pi + math.pi / 14
            else:
                theta = 0

            br = (t > 1200) and (t <= 1480)
            # Computing new accelerations
            ax = (Fe * math.cos(alpha) + (has_fuel or br) * Ft * math.cos(theta) + Fm * math.cos(gamma)) / m
            ay = (Fe * math.sin(alpha) + (has_fuel or br) * Ft * math.sin(theta) + Fm * math.sin(gamma)) / m

            # Output logging
            if overall_time % 60 == 0:
                print(f"t = {int(t / 60)} min ; V ~ {v:.3} m/s ; ax ~ {ax:.1} ; ay ~ {ay:.1}")

            # Mass update
            fuel = fuel - k * dt
            if fuel <= 0:
                has_fuel = False
            else:
                m -= k * dt
            
            overall_time += dt

        m -= (stage.empty_mass + fuel)
    
    utilities.draw_graph(X_ARRAY, Y_ARRAY, "km", "km", "Motion trajectory")
    utilities.draw_graph(T_ARRAY, RM_ARRAY, "t, min", "km", "Muna distance")
    utilities.draw_graph(XM_ARRAY, YM_ARRAY, "km", "km", "Muna trajectory")
    utilities.draw_graph(T_ARRAY, V_ARRAY, "t, min", "m/s", "Velocity - V(t)")
    utilities.draw_graph(T_ARRAY, R_ARRAY, "t, min", "km", "h(t)")