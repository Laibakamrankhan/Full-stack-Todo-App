import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

print("Python path:", sys.path[:3])  # Show first few paths
print("Current working directory:", os.getcwd())

# Try importing the app with error handling
try:
    from src.main import app
    print("Successfully imported app from src.main")

    # Now try to run with uvicorn
    import uvicorn
    print("Successfully imported uvicorn")

    print("Starting server on port 8007...")
    uvicorn.run(app, host="0.0.0.0", port=8007, log_level="info")

except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"Runtime error: {e}")
    import traceback
    traceback.print_exc()