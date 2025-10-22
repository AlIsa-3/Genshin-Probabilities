# Imports
import random
import argparse
import math


class Simulation:
    """
    Class For the Monte-Carlo Simulation of Genshin Impact Wishes


    Attributes:
        * wish_count: An integer number of wishes to simulate
        * target_5_star_count: An integer representing the target number of limited 5-stars to obtain
        * current_pity: An integer representing the current pity on the banner
        * banner_pity: An integer representing the hard-pity value on the banner
        * isGuaranteed: A boolean, True if the next 5-star is guaranteed to be limited, False otherwise
        * CR_score: An integer representing the "counter" for Capturing Radiance described in
            * https://www.reddit.com/r/Genshin_Impact/comments/1hd1sqa/understanding_genshin_impacts_capturing_radiance/
            * Default = 1
        * simulation_count The integer number of trials to simulate
            * Default = 10000
        * verbose Whether to display more details about the simulation
            * Default = False

        * current_limited_count: An integer representing the current number of limited 5-stars obtained on a given run
        * success_trials: An integer number of trials where the number of limited 5-stars obtained was at least the target
        * success_probability: A float equal to the computed approximate probability of obtaining at least the target number
          of limited 5-stars

        * wishes_taken_single_round_first is an integer representing the number of wishes taken to get the first limited 5-star on one round
        * average_wishes_taken_first is the ceiling of the average value of wishes_taken_single_round_first across all simulations

        * wishes_taken_single_round is an integer representing the number of wishes taken to achieve the target in a single simulation
        * average_wishes_taken is the ceiling of the average value of wishes_taken_single_round across all simulations


    """

    def __init__(
        self,
        wish_count: int,
        target_5_star_count: int,
        current_pity: int,
        banner_pity: int,
        isGuaranteed: bool,
        CR_score: int = 1,
        simulation_count: int = 10000,
        verbose: bool = False,
    ) -> None:
        self.wish_count = wish_count
        self.target_5_star_count = target_5_star_count
        self.current_pity = current_pity
        self.banner_pity = banner_pity
        self.isGuaranteed = isGuaranteed
        self.CR_score = CR_score
        self.simulation_count = simulation_count
        self.verbose = verbose

        self.current_limited_count: int = 0
        # Number of runs where obtained limited 5-stars is at least the target
        self.success_trials: int = 0

        self.success_probability: float = 0

        # Number of wishes taken to achieve target
        self.wishes_taken_single_round: int = 0
        self.average_wishes_taken: float = 0

        # Number of wishes to obtain the first limited 5-star
        self.wishes_taken_single_round_first: int = 0
        self.average_wishes_taken_first: int = 0

    def _account_for_soft_pity(self) -> bool:
        """
        Determines whether a 5-star is rolled naturally, accounting for soft-pity.

        Returns:
        * A boolean True or False whether a 5-star was rolled naturally

        Raises:
        None
        """
        # Soft pity starts ~16 away from hard pity
        soft_pity_value: int = self.banner_pity - self.current_pity

        # The chance of getting a 5 star increases by about 6% for every 1 increase in current pity up to banner pity
        weight_True: float = 0.06 * (1 + 16 - soft_pity_value)
        # Normalization Condition
        weight_False: float = 1 - weight_True

        if soft_pity_value <= 16:
            return random.choices(
                population=[True, False], weights=[weight_True, weight_False]
            )[0]
        else:
            # 1000 represents 100%
            random_number: int = random.randint(1, 1000)
            # If the random integer from 1-1000 is a specific number, that represents obtaining a 5-star
            return random_number == 6

    def _account_for_capturing_radiance(self) -> bool:
        """
        Accounts for the new Capturing Radiance system based on data found here:
        https://www.reddit.com/r/Genshin_Impact/comments/1hd1sqa/understanding_genshin_impacts_capturing_radiance/

        Returns:
        * A boolean representing whether Capturing Radiance has activated or not

        Raises:
        None

        """

        if self.CR_score == 3:
            self.CR_score = 1
            return True
        else:
            self.CR_score += 1
            return False

    def _one_wish(
        self,
    ) -> bool:
        """
        Simulates a single wish

        Returns:
        * A boolean representing whether a limited five star is obtained
        Raises:
        * None
        """

        # Boolean value representing whether a 5-star was obtained on this current wish initialized to False
        isLimited_5_star: bool = False

        # If reached hard pity, force obtaining a 5-star
        # Or if a 5-star is obtained naturally, accounting for soft-pity
        if (self.current_pity == self.banner_pity) or self._account_for_soft_pity():
            return self._five_star()

        # If no 5-star obtained, pity increases by 1 while the other values remain unchanged
        else:
            self.current_pity += 1

            return isLimited_5_star

    def _five_star(
        self,
    ) -> bool:
        """
        Determines the logic for checking if a 5-star that is obtained is limited

        Returns:
        * A boolean True if limited 5-star, False otherwise

        Raises:
        * None
        """
        # Reset current pity
        self.current_pity = 0

        # Now check whether it is the limited 5-star or not:
        # If guaranteed then it is always the limited
        if self.isGuaranteed:
            # Next 5-star is no longer guaranteed to be limited
            self.isGuaranteed = False
            # Limited was obtained so update flag
            isLimited_5_star = True

            return isLimited_5_star

        # Otherwise have to determine outcome with 50/50 probability
        else:
            # Find result of the 50/50 either True or False
            isLimited_5_star = self._fifty_fifty()

            # If hit became True, no longer guaranteed. Otherwise if hit is False, the next 5-star is guaranteed to be limited
            self.isGuaranteed = not isLimited_5_star

            return isLimited_5_star

    def _fifty_fifty(self) -> bool:
        """
        Randomly Selects a choice of either True or False.
        * True represents getting a limited 5-star
        * False represents not getting a limited 5-star


        Returns:
        * bool containing a bool either True or False

        Raises:
        None
        """

        isSuccess: bool = random.choice([True, False])

        # If False is chosen try Capturing Radiance
        if not isSuccess:
            isSuccess = self._account_for_capturing_radiance()

        return isSuccess

    def _one_run(self) -> bool:
        """
        Simulates one run of wishes.

        Returns:
            * A boolean value, True if the number of limited 5-stars obtained was at least target_limited_5_stars.

        Raises:
            * None
        """

        # So that only the first limited 5-star is counted for the number of wishes taken
        isFirstLimited: bool = True

        # So that only the first time the target is reached is counted
        isFirstTargetReached: bool = True

        # Simulate each wish
        for wish_number in range(self.wish_count):
            # Obtain the results of the wish
            isLimited5Star: bool = self._one_wish()

            # Record the wish number at which the first limited 5-star is obtained
            if isLimited5Star and isFirstLimited:
                isFirstLimited = False
                self.wishes_taken_single_round_first = wish_number + 1

            # Update Current Run Limited 5-star count
            self.current_limited_count += int(isLimited5Star)

            # Record the wish number at which the target limited 5-star count is reached
            if (
                self.current_limited_count == self.target_5_star_count
                and isFirstTargetReached
            ):
                isFirstTargetReached = False
                self.wishes_taken_single_round = wish_number + 1

        # If the target was not reached then update wishes taken to be the total number of wishes
        if isFirstTargetReached:
            self.wishes_taken_single_round = self.wish_count


        # After Running simulation of wishes, return a boolean.
        # True if at least the target number of limited 5-stars was obtained,
        # False otherwise
        return self.current_limited_count >= self.target_5_star_count

    def _simulation(
        self,
    ) -> None:
        """
        Monte-Carlo probability approximation for the probability of getting at least a specified number of limited 5-stars
        within a certain amount of wishes.

        Returns:
        * None
        - Updates the value of the success_probability with the probability of getting a specified number of limited 5-stars
          within a certain amount of wishes

        - Updates the value for the average_wishes_taken to achieve the target in

        Raises:
        None
        """

        # Original Values to reset after each run
        original_CR_score = self.CR_score
        original_current_pity = self.current_pity
        original_isGuaranteed = self.isGuaranteed

        for _ in range(self.simulation_count):
            # Since _one_run() returns a boolean value, True if the target was achieved and False otherwise,
            # Cast its return to an int and add it to the running total of successful runs.
            # This means that if the target was met, int(_one_run()) will == 1, otherwise it will == 0
            self.success_trials += int(self._one_run())

            # Add total number of wishes taken for first limited 5-star
            self.average_wishes_taken_first += self.wishes_taken_single_round_first

            # Add total number of wishes for target 5-star count
            self.average_wishes_taken += self.wishes_taken_single_round

            # Reset values after run
            self.CR_score = original_CR_score
            self.current_limited_count = 0
            self.current_pity = original_current_pity
            self.isGuaranteed = original_isGuaranteed

        # After performing the simulation:
        # Divide the number of outcomes where the target was met by the number of simulations
        # This will give the probability of achieving the target number of limited 5-stars within a given number of wishes
        self.success_probability = self.success_trials / self.simulation_count

        # Find out average number of wishes taken
        # Divide by number of simulations
        # We want an integer value so we will calculate the ceiling of the resulting division to obtain a value
        # Average number of wishes to obtain first limited 5-star
        self.average_wishes_taken_first = math.ceil(
            self.average_wishes_taken_first / self.simulation_count
        )

        # Average number of wishes to obtain the target count of limited 5-stars
        self.average_wishes_taken = math.ceil(
            self.average_wishes_taken / self.simulation_count
        )
        # If the average number of wishes to obtain the target is 0 --> it means the target was never reached
        # So update value as infinite
        if self.average_wishes_taken == 0:
            self.average_wishes_taken = float("inf")

    def _display(
        self,
    ) -> None:
        """
        Display the output of the simulation

        If verbose then displays more details about the simulation

        Returns:
        None

        Raises:
        None
        """
        output_string: str = (
            f"The probability of getting {self.target_5_star_count} limited 5-stars in {self.wish_count} "
            f"wishes is approximately {self.success_probability:.2%}\n"
        ) 


        # If the average number of wishes taken to reach the target is the wish count
        #  --> likely that the target is usually not reached
        # Update average value to infinite
        if self.average_wishes_taken == self.wish_count:
            self.average_wishes_taken = float("inf")
        if self.verbose:
            output_string += str(
                f"Calculated using {self.simulation_count} simulations\n"
                f"Took on average {self.average_wishes_taken} wishes to reach the target\n"
                f"Took on average {self.average_wishes_taken_first} to obtain the first limited 5-star"
            )

        print(output_string)
        return None

    def run_simulation(self) -> None:
        """
        Runs the Monte-Carlo simulation of the Probability of getting a Specific Number of Limited 5-Stars in Genshin Impact
        within a specific number of wishes.

        Returns:
        * None

        Raises:
        * None
        """
        self._simulation()
        self._display()

        return None


def main() -> None:
    # CLI Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "wish_count",
        type=int,
        help="The number of wishes to simulate",
    )
    parser.add_argument(
        "target_5_star_count",
        type=int,
        help="The target number of limited 5-stars to obtain",
    )
    parser.add_argument(
        "current_pity",
        type=int,
        help="The current pity on the banner",
    )
    parser.add_argument(
        "banner_pity",
        type=int,
        help="The value for hard-pity on the banner",
    )
    parser.add_argument(
        "--simulation-count",
        "-c",
        type=int,
        default=10000,
        help="The number of simulations to run",
    )
    parser.add_argument(
        "--guaranteed",
        "-g",
        action="store_true",
        help="The next 5-star is guaranteed to be limited",
    )
    parser.add_argument(
        "--capturing-radiance",
        "-cr",
        type=int,
        default=1,
        help="Number of 50/50s lost in a row excluding guarantees",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Whether to display more details about the simulation",
    )

    # Parse Arguments
    args = parser.parse_args()

    # Simulation Parameters:
    wish_count: int = args.wish_count
    target_5_star_count: int = args.target_5_star_count
    current_pity: int = args.current_pity
    banner_pity: int = args.banner_pity
    isGuaranteed: bool = args.guaranteed

    # Capturing Radiance
    CR_score: int = args.capturing_radiance

    # Number of Simulations to Run:
    simulation_count: int = args.simulation_count

    # Initialize Object
    sim = Simulation(
        wish_count=wish_count,
        target_5_star_count=target_5_star_count,
        current_pity=current_pity,
        banner_pity=banner_pity,
        isGuaranteed=isGuaranteed,
        CR_score=CR_score,
        simulation_count=simulation_count,
        verbose=args.verbose,
    )

    # Run Simulation and Display Results
    sim.run_simulation()

    return None


if __name__ == "__main__":
    main()
