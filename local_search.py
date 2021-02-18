from typing import Dict, FrozenSet, Optional, Tuple


def calculate_cost(facilities, curr_set):
    try:
        length = len(facilities[next(iter(curr_set))])
        cost: int = sum(facilities[facility][length - 1] for facility in curr_set)
        for i in range(length - 1):
            cost += min([facilities[facility][i] for facility in curr_set])
        return cost
    except StopIteration:
        # for empty sets
        return float('inf')


def analyze_set(facilities, curr_set, cache, step, print_output):
    if curr_set not in cache:
        cost = calculate_cost(facilities, curr_set)
        cache[curr_set] = {'cost': cost, 'step': step}
        if print_output:
            print("%s: cost = %f" % (set(curr_set), cost))
    else:
        cost = cache[curr_set]['cost']
        if print_output:
            print("%s: refer to step %i" % (set(curr_set), cache[curr_set]['step']))
    return cost, cache


def remove_options(facilities, curr_set, cache, step, print_output):
    optimal_solution = cache[curr_set]
    removed_facility = None
    if print_output:
        print("Removal:")
    for facility in curr_set:
        if print_output:
            print("%s:" % facility)
        cost, cache = analyze_set(facilities, curr_set - {facility}, cache, step, print_output)
        if cost < optimal_solution['cost']:
            optimal_solution = cache[curr_set - {facility}]
            removed_facility = facility
    return optimal_solution, cache, removed_facility


def add_options(facilities, curr_set, cache, step, print_output):
    optimal_solution = cache[curr_set]
    added_facility = None
    if print_output:
        print("Addition:")
    for facility in set(facilities.keys()) - curr_set:
        if print_output:
            print("%s:" % facility)
        cost, cache = analyze_set(facilities, curr_set | {facility}, cache, step, print_output)
        if cost < optimal_solution['cost']:
            optimal_solution = cache[curr_set | {facility}]
            added_facility = facility
    return optimal_solution, cache, added_facility


def replace_options(facilities, curr_set, cache, step, print_output):
    optimal_solution = cache[curr_set]
    replacing_facility = None
    if print_output:
        print("Replacement:")
    for facility_rm in curr_set:
        for facility_add in set(facilities.keys()) - curr_set:
            if print_output:
                print("%s replaced by %s:" % (facility_rm, facility_add))
            cost, cache = analyze_set(facilities, (curr_set - {facility_rm}) | {facility_add}, cache, step, print_output)
            if cost < optimal_solution['cost']:
                optimal_solution = cache[(curr_set-{facility_rm}) | {facility_add}]
                replacing_facility = (facility_rm, facility_add)
    return optimal_solution, cache, replacing_facility


f = [lambda x, y: x - {y}, lambda x, y: x | {y}, lambda x, y: (x - {y[0]}) | {y[1]}]


def print_best_option(operated_facility, best_option):
    print("What we do now:")
    if best_option == 0:
        print("We remove %s" % operated_facility)
    elif best_option == 1:
        print("We add %s" % operated_facility)
    else:
        print("We replace %s with %s" % operated_facility)


def local_search(facilities, starting_set: FrozenSet[any], print_output=True):
    step: int = 0
    cache: Dict[any, any] = {starting_set: {'cost': calculate_cost(facilities, starting_set), 'step': step}}
    curr_set = starting_set
    optimal_solution = cache[starting_set]
    if print_output:
        print("%s: cost = %f" % (set(curr_set), optimal_solution['cost']))
    while True:
        step += 1
        if print_output:
            print("Step %i:" % step)
        # Removal
        optimal_solution_removal, cache, removed_facility = remove_options(facilities, curr_set, cache, step, print_output)
        # Addition
        optimal_solution_addition, cache, added_facility = add_options(facilities, curr_set, cache, step, print_output)
        # Replacement
        optimal_solution_replacement, cache, replacing_facility = replace_options(facilities, curr_set, cache, step, print_output)
        if removed_facility is None and added_facility is None and replacing_facility is None:
            break
        options = [optimal_solution_removal, optimal_solution_addition, optimal_solution_replacement]
        facility_operator = [removed_facility, added_facility, replacing_facility]
        best_option: int = min_index([option['cost'] for option in options])
        if print_output:
            print_best_option(facility_operator[best_option], best_option)
        optimal_solution = options[best_option]
        curr_set = f[best_option](curr_set, facility_operator[best_option])
        if print_output:
            print()

    if print_output:
        print("The best local maximum is %s with a cost of %i" % (set(curr_set), optimal_solution['cost']))
    return optimal_solution


def min_index(a):
    return a.index(min(a))
