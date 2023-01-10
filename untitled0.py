import math

def calc_beam_angle(altitude):
  # Earth's radius in meters
  earth_radius = 6371e3

  # Calculate the distance from the Earth's surface to the satellite
  distance = earth_radius + altitude

  # Calculate the beam angle in radians
  beam_angle = math.atan(earth_radius / distance)

  # Convert the beam angle to degrees
  beam_angle_degrees = beam_angle * 180 / math.pi

  return beam_angle_degrees

def calc_radius_of_coverage(altitude, elevation_mask):
  # Calculate the beam angle in degrees
  beam_angle_degrees = calc_beam_angle(altitude)

  # Calculate the elevation angle in degrees
  elevation_angle_degrees = beam_angle_degrees - elevation_mask

  # Calculate the radius of coverage using the elevation angle
  radius_of_coverage = altitude * math.tan(elevation_angle_degrees * math.pi / 180)

  return radius_of_coverage

# Test the function with an altitude of 400 km and an elevation mask of 20 degrees
print(calc_radius_of_coverage(500e3, 20))
