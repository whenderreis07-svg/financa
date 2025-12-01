from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"ok": True, "msg": "Assistente Financeiro rodando"}

@app.get("/healthz")
def healthz():
    return {"status": "healthy"}