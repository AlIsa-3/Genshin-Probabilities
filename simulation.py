# Imports
import random
import argparse
from typing import Tuple


def _one_wish(
    current_pity: int, banner_pity: int, isGuaranteed: bool
) -> Tuple[bool, int, bool]:
    """
    * Simulates a single wish

    * Args:
    * current_pity is an integer representing the current pity on the banner
    * banner_pity is an integer representing the value for the hard pity on a banner ( the number at which a 5-star is guaranteed)
    * isGuaranteed is a boolean value defining whether the limited 5-star character is guaranteed as the next 5-star obtained

    * Returns:
    * A tuple of 3 values ( types: (bool,int,bool) ) in this order:
        * whether a 5-star was obtained (bool),
        * the new current pity (int),
        *whether the next 5-star is guaranteed to be limited (bool)

    Raises:
    None
    """

    def five_star(
        current_pity: int, isGuaranteed: bool, isLimited_5_star: bool
    ) -> Tuple[bool, int, bool]:
        """
        Encapsulates the logic for determining whether a 5-star obtained is limited or not
        """
        # Reset current pity
        current_pity = 0

        # Now check whether it is the limited 5-star or not:
        # If guaranteed then it is always the limited
        if isGuaranteed:
            # Next 5-star is no longer guaranteed to be limited
            isGuaranteed = False
            # Limited was obtained so update flag
            isLimited_5_star = True

            return isLimited_5_star, current_pity, isGuaranteed

        # Otherwise have to determine outcome with 50/50 probability
        else:
            # Find result of the 50/50 either True or False
            isLimited_5_star = _fifty_fifty()

            # If hit became True, no longer guaranteed. Otherwise if hit is False, the next 5-star is guaranteed to be limited
            isGuaranteed = not isLimited_5_star

            return isLimited_5_star, current_pity, isGuaranteed

    # Boolean value representing whether a 5-star was obtained on this current wish initialized to False
    isLimited_5_star: bool = False

    # If reached hard pity, force obtaining a 5-star
    # Otherwise if the random integer from 1-1000 is a specific number, that represents obtaining a 5-star
    if (current_pity == banner_pity) or (random.randint(1, 1000) == 6):
        return five_star(
            current_pity=current_pity,
            isGuaranteed=isGuaranteed,
            isLimited_5_star=isLimited_5_star,
        )

    # If no 5-star obtained, pity increases by 1 while the other values remain unchanged
    else:
        current_pity += 1

        return isLimited_5_star, current_pity, isGuaranteed


def _fifty_fifty() -> bool:
    """
    Randomly Selects a choice of either True or False.
    * True represents getting a limited 5-star
    * False represents not getting a limited 5-star

    Args:
    None

    Returns:
    * bool either True or False

    Raises:
    None
    """
    return random.choice([True, False])


def _one_run(
    number_of_wishes: int,
    target_limited_5_stars: int,
    current_pity: int,
    banner_pity: int,
    isGuaranteed: bool,
) -> bool:
    """
    Simulates one run of wishes.

    Args:
    * number_of_wishes is an int
    * target_limited_5_stars is an int which is the number of limited 5-stars to find the probability of achieving
    * current_pity is an int corresponding to the current pity on the banner
    * banner_pity is an int representing the hard-pity value for the banner
    * isGuaranteed is a boolean, True if the next 5-star is guaranteed to be limited, False otherwise.

    Returns:
    * A boolean value, True if the number of limited 5-stars obtained was at least target_limited_5_stars.

    Raises:
    None
    """

    # The total number of limited 5 stars achieved in one simulation of wishes
    total_limited_5_stars: int = 0

    # Simulate each wish
    for _ in range(number_of_wishes):
        # Obtain the results of the wish
        wish_results: Tuple[bool, int, bool] = _one_wish(
            current_pity=current_pity,
            banner_pity=banner_pity,
            isGuaranteed=isGuaranteed,
        )

        # Update Values:
        # First value of wish_results is a boolean. True if limited 5 star achieved, False otherwise
        total_limited_5_stars += int(wish_results[0])

        # Second value of wish_results is an integer representing the current pity
        current_pity = wish_results[1]

        # Final value of wish_results is a boolean. True if the next 5-star is guaranteed to be limited,
        # False otherwise.
        isGuaranteed = wish_results[2]

    # After Running simulation of wishes, return a boolean.
    # True if at least the target number of limited 5-stars was obtained,
    # False otherwise
    return total_limited_5_stars >= target_limited_5_stars


def simulation(
    number_of_wishes: int,
    target_limited_5_stars: int,
    current_pity: int,
    banner_pity: int,
    isGuaranteed: bool,
    number_of_simulations: int = 10000,
) -> float:
    """
    Monte-Carlo probability approximation for the probability of getting at least a specified number of limited 5-stars
    within a certain amount of wishes.

    Args:
    * number_of_wishes is an integer representing the number of wishes to simulate
    * target_limited_5_stars is an integer representing the amount of limited 5-stars to compute the probability of getting
    * current_pity is an integer representing the current pity on the banner
    * banner_pity is an integer representing the value of hard-pity on the banner
    * isGuaranteed is a boolean, True if the next 5-star is guaranteed to be limited, False otherwise
    * number_of_simulations is an integer. It is the number of simulations to run in order to approximate the probability.
        Default is 10000.

    Returns:
    * A float representing the probability of getting target_limited_5_stars limited 5-stars within number_of_wishes wishes

    Raises:
    None
    """

    # Variable to count the number of simulations -
    # where the number of limited 5 stars obtained is equal to or exceeds the target.
    successes: int = 0

    for _ in range(number_of_simulations):
        # Since _one_run() returns a boolean value, True if the target was achieved and False otherwise,
        # Cast its return to an int and add it to the running total of successful runs.
        # This means that if the target was met, int(_one_run()) will == 1, otherwise it will == 0
        successes += int(
            _one_run(
                number_of_wishes=number_of_wishes,
                target_limited_5_stars=target_limited_5_stars,
                current_pity=current_pity,
                banner_pity=banner_pity,
                isGuaranteed=isGuaranteed,
            )
        )

    # After performing the simulation:
    # Divide the number of outcomes where the target was met by the number of simulations
    # This will give the probability of achieving the target number of limited 5-stars within a given number of wishes
    return successes / number_of_simulations


def display(
    probability: float,
    number_of_wishes: int,
    target_5_star_count: int,
    simulation_count: int,
) -> None:
    """
    Display the output of the simulation

    Args:
    * probability is a float representing the probability of getting a specific number of limited 5-stars within a certain number of wishes
    * number_of_wishes is an integer representing the number of wishes simulated
    * target_5_star_count is an integer representing the number of 5 stars which is being aimed for

    Returns:
    None

    Raises:
    None
    """
    output_string: str = (
        f"The probability of getting {target_5_star_count} limited 5-stars in {number_of_wishes} "
        f"wishes is approximately {probability:.2%} (Calculated using {simulation_count} simulations)"
    )

    print(output_string)
    return None


def main():
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

    # Parse Arguments
    args = parser.parse_args()

    # Simulation Parameters:
    wish_count: int = args.wish_count
    target_5_star_count: int = args.target_5_star_count
    current_pity: int = args.current_pity
    banner_pity: int = args.banner_pity
    isGuaranteed: bool = args.guaranteed

    # Number of Simulations to Run:
    simulation_count: int = args.simulation_count

    # Calculate the probability of getting the target number of limited 5-stars
    probability: float = simulation(
        number_of_wishes=wish_count,
        target_limited_5_stars=target_5_star_count,
        current_pity=current_pity,
        banner_pity=banner_pity,
        isGuaranteed=isGuaranteed,
        number_of_simulations=simulation_count,
    )

    # Display the results
    display(
        probability=probability,
        number_of_wishes=wish_count,
        target_5_star_count=target_5_star_count,
        simulation_count=simulation_count,
    )


if __name__ == "__main__":
    main()
