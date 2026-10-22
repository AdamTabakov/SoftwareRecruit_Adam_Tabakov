import math

# constants
TIME_STEP = 0.1
MAX_TURN_RATE = 90.0
MAX_SPEED = 2.0
WAYPOINT_TOL = 0.5

# settings
TURN_ANGLE = 30
HEADING_TOL = 3.0
SLOWDOWN_DIST = 2.0

# restrict value to range
def clamp(val, lower, upper):
    return max(lower, min(val, upper))

# calc distance
def distance_waypoint(x, y, target_x, target_y):
    return math.hypot(target_x - x, target_y - y)

# calc target heading
def target_heading(x, y, target_x, target_y):
    dx = target_x - x
    dy = target_y - y
    angle = math.degrees(math.atan2(dy, dx))
    return angle % 360.0

# calc heading diff
def heading_diff(target, current):
    return (target - current + 180.0) % 360.0 - 180.0

# navigation
def navigation(x, y, heading, target_x, target_y):
    distance = distance_waypoint(x, y, target_x, target_y)
    des_heading = target_heading(x, y, target_x, target_y)
    # shortest angle between current and desired heading
    error = heading_diff(des_heading, heading)

    # check if waypoint is reached
    if distance <= WAYPOINT_TOL:
        return 0.0, 0.0

    # calculate turn command
    if abs(error) <= HEADING_TOL:
        turn_cmd = 0.0
    else:
        turn_cmd = clamp(error / 45.0, -1.0, 1.0)

    # no need to turn if heading error is small
    if abs(error) > TURN_ANGLE:
        drive_cmd = 0.0
    else:
        # calculate drive command and alignment
        drive_cmd = clamp(distance / SLOWDOWN_DIST, 0.0, 1.0)
        alignment = max(0.0, math.cos(math.radians(error)))
        drive_cmd *= alignment
    # clamp turn and drive commands to [-1.0, 1.0]
    return (
        clamp(turn_cmd, -1.0, 1.0),
        clamp(drive_cmd, -1.0, 1.0)
    )
# apply turn and drive commands to the robot
def update(x, y, heading, turn_cmd, drive_cmd):
    ang_vel = turn_cmd * MAX_TURN_RATE
    lin_vel = drive_cmd * MAX_SPEED

    mid_heading = math.radians(
        heading + ang_vel * TIME_STEP / 2.0
    )

    x += lin_vel * math.cos(mid_heading) * TIME_STEP
    y += lin_vel * math.sin(mid_heading) * TIME_STEP
    heading = (heading + ang_vel * TIME_STEP) % 360.0

    return x, y, heading
# run the simulation
def run_sim():
    x = float(input("X: "))
    y = float(input("Y: "))
    heading = float(input("Heading: "))% 360.0

    num_waypoints = int(input("Number of waypoints: "))
    waypoints = []
    # get waypoint coordinates from user
    for i in range(num_waypoints):
        print(f"waypoint {i}")
        target_x = float(input(f"Target X {i}: "))
        target_y = float(input(f"Target Y {i}: "))
        waypoints.append((target_x, target_y))
    # if there are no waypoints, exit
    if num_waypoints == 0:
        print("no waypoints")
        return

    active = 0
    elapsed = 0.0

    max_steps = 10000
    # run the simulation
    for step in range(max_steps):
        target_x, target_y = waypoints[active]
        distance = distance_waypoint(x, y, target_x, target_y)
        if distance <= WAYPOINT_TOL:
            active += 1
            if active == num_waypoints:
                turn_cmd = 0.0
                drive_cmd = 0.0
                print("Done")
                return
            continue
        # run navigation and return turn and drive commands
        turn_cmd, drive_cmd = navigation(x, y, heading, target_x, target_y)
        # apply turn and drive commands to the robot
        x, y, heading = update(x, y, heading, turn_cmd, drive_cmd)
        elapsed += TIME_STEP

        if step % 10 == 0:
            print(f"step {step}, elapsed {elapsed:.2f}s")
    print(f"Max steps reached. Done in {elapsed:.2f}s")

def main():
    while True:
        run_sim()

        again = input("Again (y/n)? ")
        if again.lower() != "y":
            break

if __name__ == "__main__":
    main()
