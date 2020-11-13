class SocialDistancingRulesetsRequest:

    def __init__(self, rulesets):
        self.socialDistancingRulesets = {k: self.to_json(v) for k, v in rulesets.items()}

    def to_json(self, ruleset):
        return {
            "name": ruleset.name,
            "numberOfDisabledSeatsToTheSides": ruleset.number_of_disabled_seats_to_the_sides,
            "disableSeatsInFrontAndBehind": ruleset.disable_seats_in_front_and_behind,
            "disableDiagonalSeatsInFrontAndBehind": ruleset.disable_diagonal_seats_in_front_and_behind,
            "numberOfDisabledAisleSeats": ruleset.number_of_disabled_aisle_seats,
            "maxGroupSize": ruleset.max_group_size,
            "maxOccupancyAbsolute": ruleset.max_occupancy_absolute,
            "maxOccupancyPercentage": ruleset.max_occupancy_percentage,
            "oneGroupPerTable": ruleset.one_group_per_table,
            "fixedGroupLayout": ruleset.fixed_group_layout,
            "disabledSeats": ruleset.disabled_seats,
            "enabledSeats": ruleset.enabled_seats,
            "index": ruleset.index,
        }
