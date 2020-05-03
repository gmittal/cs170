"""
Job driver for distributed workloads.
Written by Gautam Mittal.
"""
import subprocess
import pandas as pd

def update_all():
    for server in get_ips():
        subprocess.run(["ssh", server, "cd ~/cs170; git pull"])

def get_ips():
    with open('ips.txt', 'r') as f:
        content = f.readlines()
    return [x.strip() for x in content]

def start_job():
    servers = get_ips()

    inputs = pd.read_csv('leaderboard.csv')
    # inputs = inputs.loc[inputs['rank'] > 1]
    inputs = inputs['input'].values[:4]
    inputs_per_box = len(inputs) // len(servers)

    for i in range(len(servers)):
        server = servers[i]
        if i == len(servers) - 1:
            workload = inputs[i*inputs_per_box:]
        else:
            workload = inputs[i*inputs_per_box:(i+1)*inputs_per_box]

        workload_str = ' '.join(["inputs/{}".format(w) for w in workload])

        import pdb; pdb.set_trace()

        script = """cd ~/cs170; tmux new -d -s 0; tmux send-keys -t 0 "source venv/bin/activate; python solver.py {}" ENTER;""".format(workload_str)
        subprocess.run(["ssh", server, script])

if __name__ == "__main__":
    update_all()
    start_job()