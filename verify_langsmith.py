import os
from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

def verify_langsmith_config():
    # 1. Check Variable Presence
    keys = ["LANGCHAIN_TRACING_V2", "LANGCHAIN_API_KEY", "LANGCHAIN_ENDPOINT"]
    print(f"--- Environment Check (Python 3.11) ---")
    
    for key in keys:
        val = os.getenv(key)
        status = "✅" if val else "❌ MISSING"
        # Mask the API key for safety in logs
        display_val = f"{val[:8]}..." if val and "API_KEY" in key else val
        print(f"{key:22}: {status} ({display_val})")

    # 2. Test Connectivity
    print("\n--- Connectivity Test ---")
    try:
        # The Client will automatically look for LANGCHAIN_API_KEY and LANGCHAIN_ENDPOINT
        client = Client()
        
        # This actual API call verifies if the key is valid and the endpoint is reachable
        projects = list(client.list_projects(limit=1))
        print("✅ Connection Successful!")
        print(f"Verified against: {os.getenv('LANGCHAIN_ENDPOINT', 'https://api.smith.langchain.com')}")
        
    except Exception as e:
        print(f"❌ Connection Failed!")
        print(f"Error Detail: {e}")
        
        if "401" in str(e) or "Unauthorized" in str(e):
            print("\n💡 Hint: Your API Key might be invalid or using the old 'LANGSMITH_' prefix in your .env.")
        elif "Connection" in str(e) or "Timeout" in str(e):
            print("\n💡 Hint: Check your NGINX proxy or local firewall. It can't reach the LangSmith servers.")

if __name__ == "__main__":
    verify_langsmith_config()