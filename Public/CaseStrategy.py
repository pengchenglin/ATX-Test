import os
import unittest


class CaseStrategy:
    def __init__(self):
        self.suite_path = 'TestSuite_'
        self.case_path = 'TestCase'
        self.case_pattern = 'test*.py'

    def _collect_cases(self, cases, top_dir=None):
        suites = unittest.defaultTestLoader.discover(self.case_path,
                                                     pattern=self.case_pattern, top_level_dir=top_dir)
        for suite in suites:
            for case in suite:
                cases.addTest(case)

    def collect_cases(self, suite=False):
        """collect cases

        collect cases from the giving path by case_path via the giving pattern by case_pattern

        return: all cases that collected by the giving path and pattern, it is a unittest.TestSuite()

        """
        cases = unittest.TestSuite()

        if suite:
            test_suites = []
            for file in os.listdir('.'):
                if self.suite_path in file:
                    if os.path.isdir(file):
                        test_suites.append(file)

            for test_suite in test_suites:
                self._collect_cases(cases, top_dir=test_suite)
        else:
            self._collect_cases(cases, top_dir=None)

        return cases
