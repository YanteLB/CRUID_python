
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"name":"Task API", "version":"1", "endpoints": ["/tasks"]}

@app.get("/health")
def health():
    return {"status": "OK"}


#def main():
 #   print("Hello from cruid-python!")


#if __name__ == "__main__":
#    main()
