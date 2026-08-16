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
