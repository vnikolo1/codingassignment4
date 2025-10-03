# import modal

# app = modal.App("f1-streamlit-dashboard")

# image = (
#     modal.Image.debian_slim().pip_install("streamlit", "supabase", "pandas").add_local_dir(".", remote_path="/root")
# )

# @app.function(image=image, secrets=[modal.Secret.from_name("supabase-secrets")], min_containers=1)
# @modal.web_server(8000)
# def run_streamlit():
#     import subprocess
#     subprocess.run([
#         "streamlit", "run", "/root/app.py",
#         "--server.port", "8000", "--server.address", "0.0.0.0"
#     ])

import shlex
import subprocess
from pathlib import Path
import os
from dotenv import load_dotenv

import modal

# Load environment variables from .env file
load_dotenv()

streamlit_script_local_path = Path(__file__).parent / "app.py"
streamlit_script_remote_path = "/root/app.py"
image = (
    modal.Image.debian_slim(python_version="3.9")
    .uv_pip_install("streamlit", "supabase", "pandas", "plotly", "python-dotenv")
    .env({"FORCE_REBUILD": "true"})  # 🚨 Add this line to force a rebuild
    .add_local_file(streamlit_script_local_path, streamlit_script_remote_path)
)
app = modal.App(name="usage-dashboard", image=image)

if not streamlit_script_local_path.exists():
    raise RuntimeError(
        "Hey your starter streamlit isnt working"
    )

@app.function(secrets=[modal.Secret.from_name("supabase-secrets")], allow_concurrent_inputs=100)
@modal.web_server(8000)
def run():
    target = shlex.quote(streamlit_script_remote_path)
    cmd = f"streamlit run {target} --server.port 8000 --server.enableCORS=false --server.enableXsrfProtection=false"
    # Build environment variables, filtering out None values
    env_vars = {}
    if os.getenv("SUPABASE_KEY"):
        env_vars["SUPABASE_KEY"] = os.getenv("SUPABASE_KEY")
    if os.getenv("SUPABASE_URL"):
        env_vars["SUPABASE_URL"] = os.getenv("SUPABASE_URL")
    
    # Include current environment to ensure PATH and other essential vars are available
    env_vars.update(os.environ)
        
    subprocess.Popen(cmd, shell=True, env=env_vars)