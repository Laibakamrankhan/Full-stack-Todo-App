import sys
import os
# Add the src directory to the Python path so imports work correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Now import the app from the src module
from src.main import app

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)