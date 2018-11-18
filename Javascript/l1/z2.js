function is_divisible_by_digits_sum(n){
    return n % (n.toString().split("").reduce((a, b) => +a + +b, 0)) == 0
}

function is_divisible_by_all_digits(n){
    return n.toString().split("").every((a) => n % (+a) == 0)
}

function get_good_numbers(n){
    return new Set([...Array(n+1).keys()].filter((n) => is_divisible_by_all_digits(n) && is_divisible_by_digits_sum(n)))
}

console.log(get_good_numbers(1000000))
//ctrl alt n gives output
