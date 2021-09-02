# ***************************************************************************
# Copyright IBM Corporation 2021
#
# Licensed under the Eclipse Public License 2.0, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ***************************************************************************

import os

# name of default config file
TKLTEST_DEFAULT_CONFIG_FILE='tkltest_config.toml'

# name of (hidden) config file created by generate command (to be used by the execute command)
TKLTEST_GENERATE_CONFIG_FILE='.tkltest_generate.toml'

TKLTEST_CLI_RELATIVE_DIR = '..'

# lib download dir
TKLTEST_LIB_DIR = os.path.join(TKLTEST_CLI_RELATIVE_DIR, 'lib')
TKLTEST_LIB_DOWNLOAD_DIR = os.path.join(TKLTEST_LIB_DIR, 'download')

# version of testgen core
TKLTEST_TESTGEN_CORE_VERSION = '1.0.0'
TKLTEST_TESTGEN_CORE_JAR = os.path.join(TKLTEST_LIB_DOWNLOAD_DIR,
                                        'tackle-test-generator-core-{}-SNAPSHOT.jar'.format(TKLTEST_TESTGEN_CORE_VERSION))

# suffix for the default test directory name (used if test directory is unspecified)
# CTD amplified tests
TKLTEST_DEFAULT_CTDAMPLIFIED_TEST_DIR_SUFFIX = "-ctd-amplified-tests"
# Randoop standalone tests
TKLTEST_DEFAULT_RANDOOP_TEST_DIR_SUFFIX = "-randoop-standalone-tests"
# EvoSuite standalone tests
TKLTEST_DEFAULT_EVOSUITE_TEST_DIR_SUFFIX = "-evosuite-standalone-tests"

# suffix for the directory containing test reports (CTD, junit, jacoco); names of the 
# sub-directories for different reports
TKLTEST_MAIN_REPORT_DIR_SUFFIX = '-tkltest-reports'
TKL_CTD_REPORT_DIR = 'ctd-report'
TKL_JUNIT_REPORT_DIR = 'junit-reports'
TKL_CODE_COVERAGE_REPORT_DIR = 'jacoco-reports'

# suffix for the file containing the CTD model and test plan
TKL_CTD_TEST_PLAN_FILE_SUFFIX = '_ctd_models_and_test_plans.json'

# suffix for the file containing the building-block test sequences
TKL_BB_SEQ_FILE_SUFFIX = '_bb_test_sequences.json'

# suffix of the folder where evosuite tests are generated as part of sequence initialization

TKL_EVOSUITE_OUTDIR_SUFFIX = "-evosuite-tests"

# name of the CTD coverage file generated by the test sequence extender
TKL_EXTENDER_COVERAGE_FILE_SUFFIX = '_coverage_report.json'

# suffix of name of summary file created by the sequence extender
TKL_EXTENDER_SUMMARY_FILE_SUFFIX = '_test_generation_summary.json'

# name of test generator indicating use of all existing test generators in concert
COMBINED_TEST_GENERATOR_NAME = 'CombinedTestGenerator'

# mapping of base test generator names specified in CLI option to the internal name
# or name of the corresponding code component
BASE_TEST_GENERATORS = {
    'combined': COMBINED_TEST_GENERATOR_NAME,
    'evosuite': 'EvoSuiteTestGenerator',
    'randoop': 'RandoopTestGenerator'
}

# suffix for the file containing the CTD model and test plan
ERROR_PATTERNS_FILE = 'errorPatterns.json'

# randoop used version
RANDOOP_VERSION = "4.2.6"

# evosuite used version
EVOSUITE_VERSION = "1.0.7"

# soot used version
SOOT_VERSION = "4.1.0"

# ACTS version
ACTS_VERSION = '3.2'

# maven version used for creating maven build file
MAVEN_VERSION = "4.0.0"

# Jacoco for maven used version

JACOCO_MAVEN_VERSION = "0.8.7"

# maven site plugin version used

MAVEN_SITE_PLUGIN_VERSION = "3.7.1"

# maven reports plugin version used

MAVEN_REPORTS_PLUGIN_VERSION = "3.0.0"

# maven surfire plugin version used

MAVEN_SURFIRE_VERSION = "3.0.0-M5"

# Initial timeout for extender to complete before starting to check if it terminated

EXTENDER_INITIAL_TIMEOUT = 300

# Repeated timeout for extender completion after initial timeout is reached

EXTENDER_REPEATED_TIMEOUT = 60