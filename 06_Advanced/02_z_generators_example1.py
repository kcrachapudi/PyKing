import time

# --- PIPELINE STAGE 1: The Source ---
def data_source(file_path):
    """
    Simulates reading a massive file line-by-line.
    Instead of loading the whole file into RAM, we 'yield' one line at a time.
    """
    print(f"[Source] Opening connection to {file_path}...")
    # In a real scenario, this would be: with open(file_path) as f: for line in f:
    raw_data = [
        "22.5", "23.1", "ERROR", "24.5", "999.9", "22.8", "missing", "25.2"
    ]
    
    for item in raw_data:
        print(f"\n[Source] Fetching raw reading: {item}")
        time.sleep(0.5)  # Simulate small I/O delay
        yield item

# --- PIPELINE STAGE 2: The Filter ---
def data_cleaner(source):
    """
    Takes an existing generator (source) and filters out the 'trash'.
    It acts like a sieve in the pipeline.
    """
    for reading in source:
        # Check if the data is a valid number and within a sane range
        try:
            val = float(reading)
            if 0 <= val <= 100:  # Ignore extreme outliers like 999.9
                yield val
            else:
                print(f"  [Filter] Dropping outlier: {val}")
        except ValueError:
            print(f"  [Filter] Dropping non-numeric junk: '{reading}'")

# --- PIPELINE STAGE 3: The Transformer ---
def unit_converter(clean_source):
    """
    Takes the cleaned numbers and performs a calculation.
    Data is still flowing through the pipe one-by-one.
    """
    for celsius in clean_source:
        fahrenheit = (celsius * 9/5) + 32
        print(f"    [Transformer] Converting {celsius}C to {fahrenheit:.1f}F")
        yield round(fahrenheit, 2)

# --- THE ASSEMBLY LINE ---
def run_pipeline():
    print("--- Pipeline Started ---")
    
    # 1. We connect the pipes together. 
    # NOTE: NO CODE RUNS YET. We are just building the plumbing.
    source = data_source("sensors.log")
    cleaned = data_cleaner(source)
    final_stream = unit_converter(cleaned)
    
    print("Plumbing finished. Starting the 'For Loop' pump...")
    
    # 2. The 'for' loop acts as the pump at the very end of the pipe.
    # It pulls the FIRST item through all three stages before asking for the SECOND.
    for result in final_stream:
        print(f"      [Sink] Success! Final Output: {result}")

    print("\n--- Pipeline Empty ---")

if __name__ == "__main__":
    run_pipeline()
