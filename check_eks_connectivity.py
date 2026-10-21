
import subprocess

command = ["kubectl", "get", "nodes", "-o", "wide"]

try:
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=30
    )

    if result.returncode == 0:
        print("Successfully connected to Kubernetes!")
        print(result.stdout)
    else:
        print("Kubernetes command failed:")
        print(result.stderr)

except FileNotFoundError:
    print("kubectl was not found. Check its installation and PATH.")

except subprocess.TimeoutExpired:
    print("Connection timed out. Check your EKS cluster and network.")
