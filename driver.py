"""
Job driver for distributed workloads.
Written by Gautam Mittal.
"""
import subprocess
import pandas as pd

def update_all():
    for server in get_ips():
        subprocess.run(["ssh", server, "tmux kill-server; cd ~/cs170; rm -rf ~/cs170/outputs; git reset --hard HEAD; git pull; source venv/bin/activate; pip install -r requirements.txt"])

def get_ips():
    with open('ips.txt', 'r') as f:
        content = f.readlines()
    return [x.strip() for x in content]

def reset_ssh():
    for server in get_ips():
        subprocess.run(["ssh-keygen", "-R", "{}".format(server)])

def start_job():
    servers = get_ips()

    inputs = pd.read_csv('leaderboard.csv')
    inputs = inputs.loc[inputs['rank'] > 20]
    inputs = inputs['input'].values
    inputs_per_box = len(inputs) // len(servers)

    total = 0

    for i in range(len(servers)):
        server = servers[i]
        if i == len(servers) - 1:
            workload = inputs[i*inputs_per_box:]
        else:
            workload = inputs[i*inputs_per_box:(i+1)*inputs_per_box]

        total += len(workload)

        workload_str = ' '.join(["inputs/{}.in".format(w) for w in workload])

        script = """cd ~/cs170; tmux new -d -s 0; tmux send-keys -t 0 "source venv/bin/activate; python solver.py {}" ENTER;""".format(workload_str)
        subprocess.run(["ssh", server, script])

    print("Total inputs deployed: {}".format(total))
    assert total == len(inputs)

if __name__ == "__main__":
    update_all()
    start_job()