import unittest
import os
import sys
import tkinter as tk
from gui import create_gui

class TestGuiSmoke(unittest.TestCase):
    def test_gui_launch(self):
        # This is a smoke test: it checks that the GUI window can be created and destroyed without error.
        # Full GUI automation is not possible in headless/dev containers, but this ensures no import/runtime errors.
        try:
            root = tk.Tk()
            root.withdraw()  # Hide main window
            # Try to create the GUI (should not raise)
            create_gui()
        except Exception as e:
            self.fail(f"GUI failed to launch: {e}")
        finally:
            try:
                root.destroy()
            except Exception:
                pass

if __name__ == "__main__":
    unittest.main()
