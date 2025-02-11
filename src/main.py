import os
import uvicorn

if __name__ == "__main__":
    env = os.getenv("ENV", "dev")
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True, env_file=str(f"env/.env.{env}"))
