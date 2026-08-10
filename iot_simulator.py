
import random
import time
import requests


# Flask API URL
FLASK_API_URL = "http://127.0.0.1:5000/api/sensor-data"


def generate_sensor_data():
    """Generate simulated health sensor readings."""

    heart_rate = random.randint(65, 95)
    spo2 = round(random.uniform(96.0, 99.0), 1)
    temperature = round(random.uniform(36.3, 37.2), 1)

    return {
        "heart_rate": heart_rate,
        "spo2": spo2,
        "temperature": temperature
    }


def send_sensor_data(data):
    """Send sensor readings to the Silent Health AI Flask API."""

    try:
        response = requests.post(
            FLASK_API_URL,
            json=data,
            timeout=5
        )

        if response.status_code == 200:
            print("✓ Data sent successfully")
            return True

        print(f"✗ Failed to send data. HTTP Status: {response.status_code}")
        print(f"  Response: {response.text}")
        return False

    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to Flask.")
        print("  Make sure app.py is running on port 5000.")
        return False

    except requests.exceptions.Timeout:
        print("✗ Flask API request timed out.")
        return False

    except requests.exceptions.RequestException as e:
        print(f"✗ Error sending sensor data: {e}")
        return False


if __name__ == "__main__":

    print("=" * 45)
    print("      SILENT HEALTH AI - IoT SIMULATOR")
    print("=" * 45)
    print("Virtual device started...")
    print("Connecting to Flask API...")
    print(f"API: {FLASK_API_URL}")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:

            # Generate virtual sensor readings
            data = generate_sensor_data()

            # Display readings
            print(
                f"❤️ Heart Rate : {data['heart_rate']} BPM"
            )
            print(
                f"🫁 SpO₂       : {data['spo2']} %"
            )
            print(
                f"🌡 Temperature: {data['temperature']} °C"
            )

            print("-" * 45)

            # Send readings to Flask
            print("Sending data to Silent Health AI...")
            send_sensor_data(data)

            print("-" * 45)
            print()

            # Wait before generating the next reading
            time.sleep(3)

    except KeyboardInterrupt:
        print("\nVirtual device stopped.")

