import asyncio
from Client.client import Client
import time

async def test_client_performance(num_requests):
    client = Client()
    tasks = []
    for _ in range(num_requests):
        # Choose the type of message to send (bytes, json, xml)
        message = client._create_dictionary_bytes()  # Example for bytes
        task = asyncio.ensure_future(client._send(message))
        tasks.append(task)
    # Measure time
    start_time = time.perf_counter()
    await asyncio.gather(*tasks)
    end_time = time.perf_counter()
    print(f"Sent {num_requests} messages in {end_time - start_time} seconds")

if __name__ == "__main__":
    number_of_requests = 100  # Change this to how many requests you want to send
    asyncio.run(test_client_performance(number_of_requests))
