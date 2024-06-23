import sys

import modal

app = modal.App("example-hello-world")


@app.function()
def f(i):
    if i % 2 == 0:
        print("hello", i)
    else:
        print("world", i, file=sys.stderr)

    return i * i


@app.local_entrypoint()
def main():
    # run the function locally
    print(f.local(1000))
