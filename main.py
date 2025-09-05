import os
import random
import statistics
from collections import Counter
import psycopg2
from dotenv import load_dotenv
from bs4 import BeautifulSoup

#Part 1: Data Extraction and Analysis

def parse_colors_from_html(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        return None

    with open(file_path, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')

    all_colors = []
    for row in soup.select('tbody tr'):
        color_data = row.find_all('td')[1].text
        colors = [color.strip().upper() for color in color_data.split(',')]
        all_colors.extend(colors)

    # Clean the data: Corrected a common typo 'BLEW' -> 'BLUE'
    cleaned_colors = ['BLUE' if color == 'BLEW' else color for color in all_colors]
    
    print(" Data Extraction Complete ")
    print(f"Total colors recorded: {len(cleaned_colors)}")
    return cleaned_colors

def analyze_colors(colors):
    if not colors:
        print("No colors to analyze.")
        return

    # Calculate frequency of each color
    color_counts = Counter(colors)
    print("\n Color Frequencies")
    for color, count in color_counts.items():
        print(f"{color}: {count}")

    # 1. Mean Color (Interpreted as color with frequency closest to the mean frequency)
    frequencies = list(color_counts.values())
    mean_freq = statistics.mean(frequencies)
    closest_color = min(color_counts.keys(), key=lambda color: abs(color_counts[color] - mean_freq))
    print(f"\n Analysis Results")
    print(f"1. Mean Color (by frequency): {closest_color}")
    
    # 2. Most Worn Color (Mode)
    most_common_color = color_counts.most_common(1)[0][0]
    print(f"2. Most Worn Color (Mode): {most_common_color}")

    # 3. Median Color (The middle element after sorting all colors alphabetically)
    sorted_colors = sorted(colors)
    median_index = len(sorted_colors) // 2
    median_color = sorted_colors[median_index]
    print(f"3. Median Color (Alphabetical): {median_color}")
    
    # 4. Variance of the colors (based on their frequencies)
    variance = statistics.variance(frequencies) if len(frequencies) > 1 else 0
    print(f"4. Variance of Frequencies: {variance:.2f}")

    # 5. Probability of choosing RED
    total_colors = len(colors)
    red_count = color_counts.get('RED', 0)
    probability_red = (red_count / total_colors) * 100 if total_colors > 0 else 0
    print(f"5. Probability of choosing Red: {probability_red:.2f}%")
    
    return color_counts

#Part 2: Database Integration with PostgreSQL

load_dotenv()  # Load environment variables from .env file

def save_to_postgres(color_counts):
    print("\n PostgreSQL Integration ")
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()
        # Insert or update data
        for color, freq in color_counts.items():
            upsert_query = """
            INSERT INTO color_frequencies (color_name, frequency)
            VALUES (%s, %s)
            ON CONFLICT (color_name)
            DO UPDATE SET frequency = EXCLUDED.frequency;
            """
            cursor.execute(upsert_query, (color, freq))
        conn.commit()
        print("Successfully saved color frequencies to the database.")

    except psycopg2.OperationalError as e:
        print(f"Database connection failed: {e}")
        print("Please ensure PostgreSQL is running and your credentials are correct.")
    except Exception as e:
        print(f"An error occurred: {e}")

#Part 3: Bonus Algorithmic Questions 
def recursive_binary_search(data, target, low, high):
    if low > high:
        return -1  # Target not found
    mid = (low + high) // 2
    if data[mid] == target:
        return mid  # Target found at index mid
    elif data[mid] < target:
        return recursive_binary_search(data, target, mid + 1, high)
    else:
        return recursive_binary_search(data, target, low, mid - 1)

def generate_binary_and_convert():
    # Generate 4 random bits (0 or 1) and join them into a string
    binary_string = "".join(random.choice(['0', '1']) for _ in range(4))
    
    # Convert the binary string to a decimal integer
    decimal_value = int(binary_string, 2)
    
    print("\n Random Binary to Decimal Conversion")
    print(f"Random 4-digit binary number: {binary_string}")
    print(f"Decimal equivalent: {decimal_value}")

def sum_fibonacci(n):
    a, b = 0, 1
    total_sum = 0
    for _ in range(n):
        total_sum += a
        a, b = b, a + b
    
    print("\n Sum of First 50 Fibonacci Numbers")
    print(f"The sum is: {total_sum}")


# 7. Recursive search example
    print("\n Recursive Search Example ")
    sample_list = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91] 
    search_target = 23
    result_index = recursive_binary_search(sample_list, search_target, 0, len(sample_list) - 1)
    print(f"Searching for {search_target} in {sample_list}")
    if result_index != -1:
        print(f"Found at index: {result_index}")
    else:
        print("Target not found in the list.")


file_path = "python_class_question.html"
def main():
    # Part 1: Extract and analyze colors
    colors = parse_colors_from_html(file_path)
    color_counts = analyze_colors(colors)

    # Part 2: Save results to PostgreSQL
    if color_counts:
        save_to_postgres(color_counts)

    # Part 3: Algorithmic exercises
    print("\n Algorithmic Demonstrations")
    # Recursive search demo
    sample_list = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    search_target = 23
    result_index = recursive_binary_search(sample_list, search_target, 0, len(sample_list) - 1)
    print(f"Searching for {search_target} in {sample_list}")
    if result_index != -1:
        print(f"Found at index: {result_index}")
    else:
        print("Target not found in the list.")

    # Binary conversion demo
    generate_binary_and_convert()

    # Fibonacci sum demo
    sum_fibonacci(50)


if __name__ == "__main__":
    main()
