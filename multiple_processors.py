import multiprocessing
import random
import time
from typing import Dict


def random_task(task_id: int) -> Dict[str, object]:
    """Perform a random CPU-bound task and return the result metadata."""
    # Choose a random workload size and operation type
    workload = random.randint(5_000_000, 12_000_000)
    operation = random.choice(["sum", "prime_check", "square_sum"])
    start_time = time.perf_counter()

    if operation == "sum":
        result_value = sum(range(workload))
    elif operation == "prime_check":
        result_value = is_prime(workload)
    else:
        result_value = sum(i * i for i in range(workload // 1000))

    elapsed = time.perf_counter() - start_time
    return {
        "task_id": task_id,
        "operation": operation,
        "workload": workload,
        "result": result_value,
        "duration_seconds": round(elapsed, 3),
    }


def is_prime(n: int) -> bool:
    """Return True if n is prime, else False."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    limit = int(n**0.5) + 1
    for i in range(3, limit, 2):
        if n % i == 0:
            return False
    return True


def build_tasks(total_tasks: int) -> list[int]:
    """Build a list of task IDs for distributed execution."""
    return list(range(1, total_tasks + 1))


def main() -> None:
    total_tasks = 8
    workers = multiprocessing.cpu_count()

    print("Starting multiprocessing sample application")
    print(f"Detected CPU cores: {workers}")
    print(f"Dispatching {total_tasks} random tasks across {workers} workers...\n")

    tasks = build_tasks(total_tasks)

    with multiprocessing.Pool(processes=workers) as pool:
        for result in pool.imap_unordered(random_task, tasks):
            print(
                f"Task {result['task_id']:2d}: "
                f"{result['operation']:11s} "
                f"workload={result['workload']:10d} "
                f"duration={result['duration_seconds']:5.3f}s"
            )

    print("\nAll tasks completed.")


if __name__ == "__main__":
    for _ in range(100):
        main()
