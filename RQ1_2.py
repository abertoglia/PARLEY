import os

import create_maps
import prism_model_generator
import umc_synthesis
import prism_caller
import run_evochecker
import evaluation
import plot_fronts

max_replications = 10
max_maps = 12

def maps():
    create_maps.create_90_maps()


def models(i):
    print("Start models")
    prism_model_generator.generate_model(i)
    infile = f'Applications/EvoChecker-master/models/model_{i}.prism'
    outfile = f'Applications/EvoChecker-master/models/model_{i}_umc.prism'
    # TODO umc_synthesis.manipulate_prism_model is currently broken
    umc_synthesis.manipulate_prism_model(infile, outfile, before_actions=['east', 'west', 'north', 'south'],
                                         after_actions=['check'])
    print("Finish models")


def baseline(i):
    baseline_file = f'Applications/EvoChecker-master/data/ROBOT{i}_BASELINE/Front'
    infile = f'Applications/EvoChecker-master/models/model_{i}.prism'
    os.makedirs(f'Applications/EvoChecker-master/data/ROBOT{i}_BASELINE', exist_ok=True)
    with open(baseline_file, 'w') as b_file:
        for period in range(1, 11):
            b_file.write(prism_caller.compute_baseline(infile, period))
            if period < 10:
                b_file.write('\n')
            print('finished baseline map {0}, value {1}'.format(str(i), str(period)))


def evo_checker(i):
    # invoke EvoChecker
    print("Start EvoChecker")
    run_evochecker.run(i, max_replications)
    print("Finish EvoChecker")


def fronts(i):
    print("Start fronts")
    for period in range(max_replications):
        plot_fronts.plot_pareto_front(i, period)
    print("Finish fronts")


def main():
    print("Start main")
    # maps()
    for i in range(10, max_maps):
        # models(i)
        # baseline(i)
        evo_checker(i)
        fronts(i)
        print(f'Finished map {i}')
    
    # evaluation
    evaluation.main(max_replications, max_maps)
    
    print("Finish main")


if __name__ == '__main__':
    os.makedirs('plots/fronts', exist_ok=True)
    os.makedirs('plots/box-plots', exist_ok=True)
    main()
