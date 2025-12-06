import json, urllib.request, textwrap, datetime, os
from pathlib import Path
from openai import OpenAI

class Weatherman:
    def __init__(self, location_override=None):
        self.data_path = './data/'
        self.daily_forecast = None
        self.hourly_forecast = None
        self.location = location_override or "your area"
        self.prompt = None
        self.truncated_hourly_forecast = None
        self.days = 0
        self.hours = 0
        self.weather_report = ""

    def read_forecast(self):
        with open(Path(self.data_path+'daily_forecast.json'), 'r') as f:
            self.daily_forecast = json.load(f)
        with open(Path(self.data_path+'hourly_forecast.json'), 'r') as f:
            self.hourly_forecast = json.load(f)
        if self.hourly_forecast['location']:
            self.location = self.hourly_forecast['location']
        return self.daily_forecast, self.hourly_forecast
    
    def truncate_hourly(self, hourly_list, max_hours=36):
        """
        Truncate the hourly forecast to a maximum of 36 hours.
        """
        self.truncated_hourly_forecast = hourly_list[:max_hours]
        return self.truncated_hourly_forecast
    
    def query_model(self):
        """
        Uses Hugging Face Inference API with a big open model.
        Currently using 'openai/gpt-oss-120b:groq'
        """
        model = 'openai/gpt-oss-120b:groq'
        # model = 'meta-llama/Meta-Llama-3.1-405b-instruct'
        # model = "mistralai/Mixtral-8x22B-Instruct-v0.1"       # very snappy
        # model = "Qwen/Qwen2.5-72B-Instruct"                   # excellent reasoning
        # model = "google/gemma-2-27b-it"                       # fast & high quality

        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=os.environ["HF_TOKEN"],
        )

        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a cheerful, witty TV meteorologist named Sunny McSkies."},
                    {"role": "user", "content": self.prompt}
                ],
                temperature=0.85,
                max_tokens=600,
                stream=False
            )
            self.weather_report = completion.choices[0].message.content.strip()
            print("Success: Sunny McSkies forecast generated via Hugging Face!")
        except Exception as e:
            print(f"Warning: Hugging Face inference failed: {e}")
            self.weather_report = ("Looks like the forecast is lost in the clouds today! "
                            "Check your HF_TOKEN and internet connection.")
            exit(1)
        
    def write_report(self):
        with open(Path(self.data_path+'weather_report.txt'), 'w') as f:
            f.write("="*60)
            f.write(f"\nSunny McSky’s Forecast for {self.location} – {datetime.datetime.now():%b %d, %Y}\n")
            f.write("="*60 + "\n\n")
            f.write(textwrap.fill(self.weather_report, width=70))

    def send_ntfy(self, topic: str = "sunnyweather"):
        """
        Instant phone/desktop popup notification - 100% free & open source.
        """
        message = (
            f"Sunny McSkies NEW Forecast\n"
            f"{self.location} - {datetime.datetime.now():%b %d, %Y}\n\n"
            f"{self.weather_report}\n\n"
            f"~ Sunny McSkies"
        )
        try:
            urllib.request.urlopen(
                f"https://ntfy.sh/{topic}",
                data=message.encode("utf-8"),
                timeout=10
            )
            print("Success: Sunny McSkies forecast sent via ntfy!")
        except Exception as e:
            print(f"Warning: ntfy notification failed: {e}")

def main():
    weatherman = Weatherman()
    weatherman.read_forecast()
    weatherman.truncate_hourly(hourly_list=weatherman.hourly_forecast['forecast'], max_hours=24)
    weatherman.days = len(weatherman.daily_forecast['forecast'])
    weatherman.hours = len(weatherman.truncated_hourly_forecast)
    weatherman.prompt = f"""
        You are an enthusastic, grounded local meterologist named Sunny McSkies.
        Your top priority is to give a concise, clear, cheerful, engaging, easy-to-read weather report for {weatherman.location}.
        Here are the forecasts for the next {weatherman.days} days:
        {json.dumps(weatherman.daily_forecast['forecast'][:weatherman.days], indent=2)}

        And here is the detailed hourly forecast for the next {weatherman.hours} hours:
        {json.dumps(weatherman.truncated_hourly_forecast, indent=2)}
        
        Please write a 6-10 sentence weather report as if you were making a short-form video for your local station's social media account.
        - Use a warm, light-hearted tone
        - Mention today's high/low and overall feel
        - Call out any chance of precipitation and when
        - Highlight the nicest day coming up and the overall weather sentiment over the coming days
        - Throw in a recommendation for the day ahead - what to pack, what to do, what to wear, what to sip on etc.
        - End with something like "Have a nice day!"

        Keep the whole report under 250 words. 
        Do not output JSON or bullet points, just the spoken report.
    """
    weatherman.query_model()
    weatherman.write_report()
    weatherman.send_ntfy()

    print("\n" + "="*60)
    print(f"SUNNY MCSKIES FORECAST – {datetime.datetime.now():%b %d, %Y}")
    print("="*60)
    print(textwrap.fill(weatherman.weather_report, width=70))

if __name__ == ('__main__'):
    main()