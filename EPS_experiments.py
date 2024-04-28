import stormpy
import sys
import time
import matplotlib.pyplot as plt


def update_mdp_file(file_name, p, gamma, beta):
    with open(file_name) as f:
        lines = f.readlines()
        lines[0] = f"mdp\n"
        lines[1] = f"const double x = {p};\n"
        lines[2] = f"const double y = {gamma};\n"
        lines[3] = f"const double cq = {beta};\n"
        with open(file_name, "w") as f:
            f.writelines(lines)

def update_mc_file(file_name, p, gamma):
    with open(file_name + '_adv.pm') as f:
        lines = f.readlines()
        lines[0] = f"dtmc\n"
        lines[1] = f"const double x = {p};\n"
        lines[2] = f"const double y = {gamma};\n"
        with open(file_name + '_adv.pm', "w") as f:
            f.writelines(lines)
    with open(file_name + '_total.pm') as f:
        lines = f.readlines()
        lines[0] = f"dtmc\n"
        lines[1] = f"const double x = {p};\n"
        lines[2] = f"const double y = {gamma};\n"
        with open(file_name + '_total.pm', "w") as f:
            f.writelines(lines)

def update_mc_file_beta(file_name, p, gamma, beta):
    with open(file_name + '.pm') as f:
        lines = f.readlines()
        lines[0] = f"dtmc\n"
        lines[1] = f"const double x = {p};\n"
        lines[2] = f"const double y = {gamma};\n"
        lines[3] = f"const double cq = {beta};\n"
        with open(file_name + '.pm', "w") as f:
            f.writelines(lines)

def run_mdp(file_name, formula_str):
    prism_program = stormpy.parse_prism_program(file_name)
    properties = stormpy.parse_properties(formula_str, prism_program)
    model = stormpy.build_model(prism_program, properties)
    result = stormpy.model_checking(model, properties[0])
    initial_state = model.initial_states[0]
    return float(result.at(initial_state))

def binary_serach(file_name, p, gamma, formula_str, error=0.001):
    beta_low = 0
    beta_high = 1
    while beta_high - beta_low >= error:
        beta = (beta_high + beta_low) / 2
        update_mdp_file(file_name, p, gamma, beta)
        MP_star = run_mdp(file_name, formula_str)
        if MP_star < 0:
            beta_high = beta
        else:
            beta_low = beta
    return beta_low

def mc_binary_serach(file_name, p, gamma, formula_str, error=0.001):
    beta_low = 0
    beta_high = 1
    while beta_high - beta_low >= error:
        beta = (beta_high + beta_low) / 2
        update_mc_file_beta(file_name, p, gamma, beta)
        MP_star = run_mdp(file_name + '.pm', formula_str)
        if MP_star < 0:
            beta_high = beta
        else:
            beta_low = beta
    return beta_low

def mdp_extract_data(file_name, gamma, ps):
    res = []
    print(f"start extracting data for gamma = {gamma}, and file = {file_name}")
    for p in ps:
        print("p =", p)
        tmp = binary_serach(file_name, p, gamma, "Rmax=? [S]")
        res.append(tmp)
        print('ERRev =', tmp)
    return res

def mc_extract_data(file_name, gamma, ps):
    res = []
    print(f"start extracting data for MC")
    for p in ps:
        print("p =", p)
        # update_mc_file(file_name, p, gamma)
        # adv_blocks = run_mdp(file_name + '_adv.pm', "R=? [S]")
        # total_blocks = run_mdp(file_name + '_total.pm', "R=? [S]")
        # res.append(adv_blocks / total_blocks)
        tmp = mc_binary_serach(file_name, p, gamma, "R=? [S]")
        res.append(tmp)
        print('ERRev =', tmp)
    return res

def produce_results(mdp_file_names, mc_file_names, gamma, from_p, to_p, p_step):
    step_count = int((to_p - from_p) / p_step)
    ps = [from_p + i * p_step for i in range(step_count)]

    fig, ax = plt.subplots()
    times = {}

    for label in mdp_file_names:
        file_name = mdp_file_names[label]
        start_time = time.time()
        res = mdp_extract_data(file_name, gamma, ps)
        times[label] = time.time() - start_time
        print('time spent on ' + file_name + ' =', time.time() - start_time)
        ax.plot(ps, res, label=label)

    for label in mc_file_names:
        file_name = mc_file_names[label]
        start_time = time.time()
        res = mc_extract_data(file_name, gamma, ps)
        times[label] = time.time() - start_time
        print('time spent on ' + file_name + ' =', time.time() - start_time)
        ax.plot(ps, res, label=label)

    ax.plot(ps, ps, label='honest mining')


    plt.xlabel('Fraction of adversarial resources(p)')
    plt.ylabel('ERRev')
    plt.legend()
    plt.grid()
    plt.savefig('./results/MDP_gamma=' + str(gamma) + '.png', dpi=300)

    keys = list(times.keys())
    lines = ['' for _ in range(len(keys))]
    for i in range(len(keys)):
        k = keys[i]
        lines[i] = str(k) + ': ' + str(times[k]) + ' seconds\n'
    with open('./results/time_log_gamma=' + str(gamma) + '.txt', "w") as f:
        f.writelines(lines)

    plt.show()


path_to_d1f1 = './storm_models/mdp_d1f1.pm'
path_to_d2f1 = './storm_models/mdp_d2f1.pm'
path_to_d2f2 = './storm_models/mdp_d2f2.pm'
path_to_d3f2 = './storm_models/mdp_d3f2.pm'
path_to_d4f2 = './storm_models/mdp_d4f2.pm'

path_to_mc_f5 = './storm_models/MC_ver2'

if __name__ == '__main__':
    gamma = float(sys.argv[1])
    mdp_paths = {'MDP, d=1, f=1': path_to_d1f1, 'MDP, d=2, f=1': path_to_d2f1, 'MDP, d=2, f=2': path_to_d2f2, 'MDP, d=3, f=2': path_to_d3f2, 'MDP, d=4, f=2': path_to_d4f2}
    mc_paths = {'Single-tree attack, f=5': path_to_mc_f5}
    # mdp_paths = {'MDP, d=4, f=2': path_to_d4f2, 'MDP, d=2, f=1': path_to_d2f1}
    # mc_paths = {'Single-tree attack, f=5': path_to_mc_f5}
    produce_results(mdp_paths, mc_paths, gamma=gamma, from_p=0, to_p=0.31, p_step=0.01)
