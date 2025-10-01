import modal

app = modal.App("f1-streamlit-dashboard")

image = (
    modal.Image.debian_slim().pip_install("streamlit", "supabase", "pandas").add_local_dir(".", remote_path="/root")
)

@app.function(image=image, secrets=[modal.Secret.from_name("supabase-secrets")], min_containers=1)
@modal.web_server(8000)
def run_streamlit():
    import subprocess
    subprocess.run([
        "streamlit", "run", "/root/app.py",
        "--server.port", "8000", "--server.address", "0.0.0.0"
    ])