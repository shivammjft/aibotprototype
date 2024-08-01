from concurrent.futures import ThreadPoolExecutor
from langchain_community.document_loaders import WebBaseLoader
from requests.exceptions import RequestException, SSLError
import threading


lock = threading.Lock()

def process_batch(links):
    processed_count = 0
    results = []
    
    for link in links:
        try:
            loader = WebBaseLoader([link])
            result = loader.load()
            results.extend(result)
        except (RequestException, SSLError) as e:
            print(f"Error processing link {link}: {e}")
        except Exception as e:
            print(f"Unexpected error processing link {link}: {e}")
        finally:
            with lock:
                processed_count += 1
                print(f"Processed {processed_count} / {len(links)} links")

    return results

def parallel_load(links, num_threads):

    batch_size = 10
    all_docs = []

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_batch, links[i:i + batch_size]) for i in range(0, len(links), batch_size)]
        
        for future in futures:
            try:
                result = future.result()
                if result:
                    all_docs.extend(result)
            except Exception as e:
                print(f"Error in future result: {e}")

    return all_docs
