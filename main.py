
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


#def main():
 #   print("Hello from cruid-python!")


#if __name__ == "__main__":
#    main()
