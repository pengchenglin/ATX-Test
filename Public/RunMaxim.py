#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest


class RunMaxim:
    def __init__(self, device):
        self.test_report_root = './MaximReport'
        self.device = device

        if not os.path.exists(self.test_report_root):
            os.mkdir(self.test_report_root)

        self.test_report_path = os.path.join(self.test_report_root, self.device['model'].replace(':', '_').replace(' ', '')+'_'+self.device['serial'])

        if not os.path.exists(self.test_report_path):
            os.mkdir(self.test_report_path)

    def get_path(self):
        return self.test_report_path

    def get_device(self):
        return self.device

    def run_cases(self, cases):
        runner = unittest.TextTestRunner()
        runner.run(cases)




