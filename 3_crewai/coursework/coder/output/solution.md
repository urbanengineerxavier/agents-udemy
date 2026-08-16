I wrote a Python program in the sandbox to compute the first 1,000,000 terms of the Leibniz series for π:

```python
def calculate_pi_leibniz(terms: int = 1_000_000) -> float:
    total = 0.0
    sign = 1.0
    for i in range(terms):
        denominator = 2 * i + 1
        total += sign / denominator
        sign = -sign
    return 4 * total


if __name__ == "__main__":
    result = calculate_pi_leibniz()
    print(result)
```

I ran the file, and the output was:

```text
3.1415916535897743
```