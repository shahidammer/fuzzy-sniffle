# ============================================================================
# FILE 5: main.py (Runner)
# ============================================================================
"""
Main entry point for the application.
"""

from gr_interface import FlightBookingApp


def main():
    """Main function to run the application."""
    print("🚀 Starting Flight Booking Assistant...")
    
    # Create and launch application
    app = FlightBookingApp()
    app.launch(share=False)


if __name__ == "__main__":
    main()