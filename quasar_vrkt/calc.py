import math

G = 6.6743 * 10**(-11)
M = 0.0289
R = 8.31

def calculate_gravity_acceleration(planet_mass, planet_radius, altitude):
    return (G * planet_mass) / ((planet_radius + altitude)**2)

def calculate_planet_gravity(planet_mass, object_mass, distance):
    return (G * planet_mass * object_mass) / (distance**2)

def calculate_aerodynamic_force(coefficient, density, velocity, area):
    return (coefficient * density * velocity**2 * area) / 2

def calculate_air_temperature(T0, altitude):
    if altitude <= 11000:
        return T0 - 6 * (altitude / 1000)
    elif (altitude > 11000) and (altitude <= 25000):
        return -56.5 + 273
    elif (altitude > 25000) and (altitude <= 50000):
        return 273 - 56.5 + (56.5 * (altitude - 25000) / 25000)
    elif (altitude > 50000) and (altitude <= 100000):
        return 273 - 90 * (altitude - 50000) / 50000
    else:
        return 183

def calculate_air_pressure(P0, T0, altitude, planet_mass, planet_radius):
    g = calculate_gravity_acceleration(planet_mass, planet_radius, altitude)
    t = calculate_air_temperature(T0, altitude)
    return P0 * math.exp((-M * g * altitude) / (R * t))

def calculate_air_density(P0, T0, altitude, planet_mass, planet_radius):
    if(altitude <= 100000):
        p = calculate_air_pressure(P0, T0, altitude, planet_mass, planet_radius)
        t = calculate_air_temperature(T0, altitude)
        return (M * p) / (R * t)
    else:
        return 0