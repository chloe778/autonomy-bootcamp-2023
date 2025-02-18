"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
"""

from .. import commands
from .. import drone_report
from .. import drone_status
from .. import location
from ..private.decision import base_decision


class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
    """
    def __init__(self, waypoint: location.Location, acceptance_radius: float):
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print("Waypoint: " + str(waypoint))

        self.acceptance_radius = acceptance_radius

        self.at_waypoint = False
        self.closest_landing_pad = None

    def distance_sqr (self, p1: location.Location, p2: location.Location):
        return ((p1.location_x - p2.location_x) ** 2 + (p1.location_y - p2.location_y) ** 2)
    
    def find_closest_pad (self, p1: location.Location, landing_pad_locations: "list[location.Location]"):
        min_dist = float("inf")
        best_location = None
        for pad in landing_pad_locations:
            distance = self.distance_sqr(p1, pad)
            if distance < min_dist:
                min_dist = distance
                best_location = pad
        return best_location

    def run(self,
            report: drone_report.DroneReport,
            landing_pad_locations: "list[location.Location]") -> commands.Command:
        """
        Make the drone fly to the waypoint and then land at the nearest landing pad.

        You are allowed to create as many helper methods as you want,
        as long as you do not change the __init__() and run() signatures.

        This method will be called in an infinite loop, something like this:

        ```py
        while True:
            report, landing_pad_locations = get_input()
            command = Decision.run(report, landing_pad_locations)
            put_output(command)
        ```
        """
        command = commands.Command.create_null_command()

        if report.status == drone_status.DroneStatus.HALTED:
            if not self.at_waypoint:
                target = self.waypoint
            else:
                target = self.find_closest_pad(report.position, landing_pad_locations)
            distance_to_target_sqr = self.distance_sqr(target,report.position)
            if distance_to_target_sqr <= self.acceptance_radius * self.acceptance_radius:
                if not self.at_waypoint:
                    self.at_waypoint = True
                else:
                    command = commands.Command.create_land_command()
            else:
                command = commands.Command.create_set_relative_destination_command(target.location_x - report.position.location_x, target.location_y - report.position.location_y)



        return command
