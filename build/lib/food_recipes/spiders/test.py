import time

def convert_to_minutes(time_string):
    try:
        # Use strptime to parse the time string
        time_obj = time.strptime(time_string, "%Hhrs %Mmins")
        
        # Convert hours and minutes to minutes and return the result
        minutes = time_obj.tm_hour * 60 + time_obj.tm_min
        return minutes
    except ValueError:
        # Handle invalid time string
        print("Invalid time string format")
        return None

# Example usage
time_string = "2hrs 5mins"
minutes = convert_to_minutes(time_string)

if minutes is not None:
    print(f"{time_string} is equivalent to {minutes} minutes.")
