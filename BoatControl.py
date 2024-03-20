import pygame
import math
import ydlidar

pygame.init()

# Initialize YDLIDAR
ydlidar.os_init()
ports = ydlidar.lidarPortList()
port = "/dev/ydlidar"
for key, value in ports.items():
    port = value

laser = ydlidar.CYdLidar()
laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 230400)
laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
laser.setlidaropt(ydlidar.LidarPropScanFrequency, 10.0)
laser.setlidaropt(ydlidar.LidarPropSampleRate, 9)
laser.setlidaropt(ydlidar.LidarPropSingleChannel, False)

ret = laser.initialize()

# Constants
LIDAR_RESOLUTION = 360
VISUALIZATION_RESOLUTION = 360

# Function to generate line positions based on the number of lines
def generate_line_positions(number_of_lines):
    angle = 360 / number_of_lines
    lines = []
    for x in range(number_of_lines):
        lines.append([300 * math.cos((x + 1) * angle / 180 * math.pi), 300 * math.sin((x + 1) * angle / 180 * math.pi)])
    return lines

line_positions = generate_line_positions(VISUALIZATION_RESOLUTION)

# Set up the drawing window
screen = pygame.display.set_mode([800, 800])

try:
    running = True
    # Main loop
    while running:
        # Check if the user clicked the window close button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        # Fill the background with white
        screen.fill((250, 250, 250))

        # Get YDLidar data
        scan = ydlidar.LaserScan()
        r = laser.doProcessSimple(scan)
        if r:
            for point in scan.points:
                # Convert angle to degrees
                angle_degrees = math.degrees(point.angle)
                # Append angle and range to lidar data list
                if angle_degrees < VISUALIZATION_RESOLUTION:
                    # Calculate the position based on polar to Cartesian coordinates
                    x = point.range * math.cos(math.radians(angle_degrees))
                    y = point.range * math.sin(math.radians(angle_degrees))
                    # Scale the position for visualization
                    x_visual = int(x * 100)  # Adjust scale for visualization
                    y_visual = int(y * 100)  # Adjust scale for visualization
                    # Draw the point at the calculated position
                    pygame.draw.circle(screen, (255, 0, 0), (400 + x_visual, 400 + y_visual), 2)
        else:
            print("Failed to get Lidar Data")

        # Draw lidar center point
        pygame.draw.circle(screen, (0, 0, 0), (400, 400), 12)

        # Flip the display
        pygame.display.flip()

finally:
    # Turn off YDLidar and quit Pygame
    laser.turnOff()
    laser.disconnecting()
    pygame.quit()
