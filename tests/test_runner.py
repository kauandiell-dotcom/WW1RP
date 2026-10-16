"""Master Test Runner for Baianagem-WW1-ROLEPLAY.
Discovers and executes all test suites in tests/ with strict exit code reporting.
"""
import os, sys, unittest

def run_all_tests():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_dir, pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_all_tests())
