"""
Job driver for distributed workloads.
Written by Gautam Mittal.
"""
import subprocess

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
    inputs = inputs['input'].values
    


    for server in servers:
        script = """cd ~/cs170; tmux new -d -s 0; tmux send-keys -t 0 "source venv/bin/activate; echo 'Hello world'" ENTER;"""
        subprocess.run(["ssh", server, script])