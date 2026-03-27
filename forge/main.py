import sys

def app():
    """The main entry point for the forge CLI."""
    # We will import the Textual App here later
    print("Welcome to Forge. The swarm is initializing...")
    
    # If the user passes arguments like `forge status`
    if len(sys.argv) > 1:
        command = sys.argv[1]
        print(f"Executing command: {command}")
    else:
        # Launch the TUI by default
        print("Launching TUI...")

if __name__ == "__main__":
    app()