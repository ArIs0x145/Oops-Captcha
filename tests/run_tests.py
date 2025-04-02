import unittest
import os
import sys

if __name__ == '__main__':
    # Load all test files starting with 'test_'
    test_suite = unittest.defaultTestLoader.discover(
        start_dir=os.path.dirname(__file__), 
        pattern='test_*.py'
    )
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Output result summary
    print(f"Total tests: {result.testsRun}")
    print(f"Errors: {len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    
    # Exit with non-zero code if there are errors or failures
    if result.errors or result.failures:
        sys.exit(1)
    sys.exit(0) 