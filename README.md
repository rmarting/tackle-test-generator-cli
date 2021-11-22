# Tackle-Test CLI

This repository contains a Python-based Command-line interface (CLI), `tkltest`, for the Tackle-Test
tooling for performing automated test generation and differential testing on two application versions
(in the context of application modernization). Currently, `tlktest` provides this capability for Java unit
testing, where unit test cases can be automatically generated on a given application version (the _base_ version)
and executed against a modified version to detect differences.

The core test generator that the CLI invokes resides in the related
[tackle-test-generator-core](https://github.com/konveyor/tackle-test-generator-core) repository.

The tool is integrated with two automated unit test-generation tools for Java: 
[Randoop](https://randoop.github.io/randoop/) and [EvoSuite](https://www.evosuite.org/). So tests can be
generated using either of these tools standalone or in combination with CTD modeling, which generates
test cases guided by a different coverage criterion that exercises methods based on combinations of different
types of method parameters. The goal of CTD-guided test generation is to exercise a method with different
combinations of subtypes of the declared types of the method parameters. To do this, the test generator creates
a CTD model for each method by identifying  possible subtypes of each method parameter type using class-hierarchy
analysis and rapid type analysis. From this  model, a CTD test plan is generated for a given interaction level;
the rows in the test plan become  coverage goals for the test generator. This type of test generation puts
emphasis on type interactions (or type-based testing), and applying CTD modeling enables the interaction levels
to be controlled as well  as optimizes the number of coverage goals (and resulting test cases) at an interaction level.

`tkltest` also lets tests to be generated with or without assertions. In the case of EvoSuite and Randoop,
the assertions are generated by those tools. In the case of CTD amplification, differential assertions are
added by the test generator on states of objects observed during in-memory execution of test sequences.
Addition of assertions to tests makes the tests stronger in detecting behavioral differences between
two application versions, but it can also result in some false failures when expected differences in program state
occur between the versions. If assertions are not added, the only differences detected by the test cases
are those that cause the application to fail with runtime exceptions.

## Installing and Running the CLI

The CLI command can be installed locally to be run, or it can be run in a Docker container, in which case
the various dependencies (Java, Ant, and Maven) need not be installed locally.

### Prerequisite

To run the CLI in either way, a few jar files need to be downloaded from Maven repositories hosted on GitHub, which
requires authentication. To enable authentication, create a [GitHub personal access token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token),
with the permission `read:packages`. Note that using your GitHub password will not work for downloading one
of the jar files; a personal access token must be used.

### Running the CLI via Docker or Docker Compose

Set the environment variables `GITHUB_USERNAME` to your GitHub username and `GITHUB_TOKEN` to the
personal access token that you created.

To run the CLI using `docker-compose` (to print the CLI `help` message), run the following command in the CLI directory,
which builds the docker image for the CLI (called `tkltest-cli`) and then runs the CLI command; the docker
container is removed upon completion of the CLI command.

```buildoutcfg
docker-compose run --rm tkltest-cli --help
```

Alternatively, to build and run the CLI using `docker` instead of `docker-compose`, run the commands in the CLI
directory:

```buildoutcfg
docker build --build-arg GITHUB_TOKEN=$GITHUB_TOKEN --build-arg GITHUB_USERNAME=$GITHUB_USERNAME --tag tkltest-cli .
```
```buildoutcfg
docker run --rm -it -v /path-to-the-cli-directory:/app/tackle-test-cli tkltest-cli --help
```

Note that the CLI directory is mounted onto the container in both cases, so that the results of test generation or
execution in the container are available in the CLI directory on the host machine. This also requires that the
classes, the library dependencies, and the configuration file for the app under test be placed in a directory
under the CLI directory, so that they are available in the container.

For convenience in running the CLI via `docker-compose` or `docker`, you can create an alias, such as
one of the following:

```buildoutcfg
alias tkltest='docker-compose run --rm tkltest-cli'
```
```buildoutcfg
alias tkltest='docker run --rm -it -v /path-to-the-cli-directory:/app/tackle-test-cli tkltest-cli'
```

### Running the CLI from local installation

To run the CLI from local installation, JDK and one or more of Ant, Maven, and Gradle need to be installed. Additionally, Java library dependencies have to be downloaded.

1. Install Python 3.8

2. Install JDK 8. The JDK home directory has to be specified as a configuration option;
   see the section [Configuration Options](#configuration-options).
   
3. Install one or more of the required build systems depending on the Tackle-Test features used: Ant, Maven, Gradle. Of these systems, Maven is required for installing the CLI; the others are optional and are required only if the respective tool features are used. Tackle-Test uses these build systems are used in two ways:

   - To run the generated tests: Along with generating JUnit test cases, the CLI generates an Ant `build.xml`, a Maven `pom.xml` or a Gradle `build.gradle`, which can be used for building and running the generated tests. The build system to use can be configured using the `execute` command option `-bt/--build-type` (see [Configuration Options](#configuration-options)). Install the build system that you prefer for running the tests.
   
   - To collect library dependencies of the application under test (AUT): The CLI can use the AUT's build file to collect the AUT's library dependencies automatically. Alternatively, the user has to specify the dependencies manually in a text file (see [Specifying the app under test](doc/user_guide.md#specifying-the-app-under-test)). Currently, this feature is supported for Gradle only; Ant and Maven support will be added. Install Gradle if you plan to use the dependency computation feature.

5. Download Java libraries using the script [lib/download_lib_jars.sh](lib/download_lib_jars.sh). The jar
for the test-generator core is downloaded from the Maven registry on GitHub Packages
([tackle-test-generator-core packages](https://github.com/konveyor/tackle-test-generator-core/packages/)) and
specific builds of EvoSuite jars that are downloaded from another
[Maven registry on GitHub Packages](https://github.com/sinha108/maven-packages/packages);
both of these require authentication. To do this, before running the download script, update
[lib/settings.xml](lib/settings.xml) to replace `GITHUB_USERNAME` with your GitHub username and
`GITHUB_TOKEN` with the personal access token that you created.
   
   Alternatively, you can download the test-generator-core jar
   [here](https://github.com/konveyor/tackle-test-generator-core/packages) and the EvoSuite
   jars [here](https://github.com/sinha108/maven-packages/packages),
   and add them to the `lib/download` directory.
   
   The remaining Java libraries can be downloaded using the script:
   
    ```buildoutcfg
    cd lib; ./download_lib_jars.sh
    ```
    
    Windows users should run:
    
      ```buildoutcfg
    cd lib; download_lib_jars.sh 
    ```
   
   This downloads the Java libraries required by the CLI into the `lib/download` directory.

   CTD modeling and test-plan generation is done using the [NIST Automated Combinatorial Testing for Software](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software) tool, which is packaged with the CLI (in the `lib` directory).

6. Finally, to install the CLI command `tkltest` in a virtual environment, follow these steps:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install --editable .
   ```

   Windows users should run:

   ```
   python3 -m venv venv
   venv\Scripts\activate.bat
   pip install --editable .
   ```

To install the CLI for development, set the editable mode: `pip install --editable`.
You can then continue to develop it and make changes and simply run the command without having to package
and re-install it.

## Usage

`tkltest` provides different commands, along with options, for generating and running test cases.
`tkltest --help` shows the available commands and options.

```
usage: tkltest [-h] [-cf CONFIG_FILE] [-l {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
               [-td TEST_DIRECTORY] [-rp REPORTS_PATH] [-vb] [-v]
               {config,generate,execute} ...

Command-line interface for generating and executing test cases on two
application versions and performing differential testing (currently supporting
Java unit testing)

positional arguments:
  {config,generate,execute}
    config              Initialize configuration file or list configuration
                        options
    generate            Generate test cases on the application under test
    execute             Execute generated tests on the application version
                        under test

optional arguments:
  -h, --help            show this help message and exit
  -cf CONFIG_FILE, --config-file CONFIG_FILE
                        path to TOML file containing configuration options
  -l {CRITICAL,ERROR,WARNING,INFO,DEBUG}, --log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}
                        logging level for printing diagnostic messages
  -td TEST_DIRECTORY, --test-directory TEST_DIRECTORY
                        name of root test directory containing the generated
                        JUnit test classes
  -rp REPORTS_PATH, --reports-path REPORTS_PATH
                        path to the reports directory
  -vb, --verbose        run in verbose mode printing detailed status messages
  -v, --version         print CLI version number
```

To see the CLI in action on a sample Java application, set JAVA_HOME to the JDK installation
and run the command
```
tkltest --config-file ./test/data/irs/tkltest_config.toml --verbose generate ctd-amplified
```

Note that this command may take a few minutes to complete. The `verbose` option allows to view its progress in the standard output. 
Note that during test sequence initialization phase, the output is not printed to the standard output but rather to logs files.
You can open those logs to view the progress during this phase.

## Quick Start Guide

We list the minimal steps required to use the tool for its two main functions: generating unit tests
and executing them. More detailed description is available in the [CLI user guide](doc/user_guide.md).

1. Created an empty configuration file, named `tkltest_config.toml`, by running the command
   ```
   tkltest config init --file tkltest_config.toml
   ````
   `tkltest_config.toml` will be created in the working directory.

2. Assign values to the following configuration options in the configuration file
   (details on all configuration options are available [here](#configuration-options)):
   
   - `app_name`: name of the app under test (this name is used as prefix of file/directories created
     during test generation)
   
   - `app_classpath_file`: relative or absolute path to a text file containing library 
     dependencies of the app under test. For example, see [irs classpath file](test/data/irs/irsMonoClasspath.txt)
     
   - `monolith_app_path`: a list of paths (relative or absolute) to directories containing 
     app classes (jar files cannot be specified here). For example, see
     [daytrader toml spec](test/data/daytrader7/tkltest_config.toml#L6)
     
   - `app_packages`: a list of app package prefixes, with wildcards at the end. For example, see
     [daytrader toml spec](test/data/daytrader7/tkltest_config.toml#L63)

3. To generate test cases, run the command
   ```
   tkltest --verbose generate ctd-amplified
   ```
   The unit test cases will be generated in a folder named `tkltest-output-<app-name>/<app-name>-ctd-amplified-tests/monolith`.
   A CTD coverage report will be created as well  in a folder named `tkltest-output-<app-name>/<app-name>-tkltest-reports`, showing
   the CTD test plan row coverage achieved by the generated tests.

4. To execute the generated unit tests on the legacy app, run the command
   ```
   tkltest --verbose --test-directory tkltest-output-<app-name>/<app-name>-ctd-amplified-tests execute
   ```
   JUnit reports and Jacoco code coverage reports will be created in  `tkltest-output-<app-name>/<app-name>-tkltest-reports`.
 
Note that, if the `--config-file` option is not specified on the command line (as in the commands above),
the CLI uses by default `./tkltest_config.toml` as the configuration file.

## Generate Command

Generates JUnit test cases on the application. Currently, the supported sub-command of `generate`
is `ctd-amplified`, which performs CTD modeling and optimization over application classes to
compute coverage goals, and generates test cases to cover those  goals. CTD-guided test
generation can leverage either Randoop or EvoSuite for generating  initial or building-block
test sequences that are then extended for covering rows in the  CTD test plan.

By default, this sub-command generates diff assertions and adds them to the generated test cases.
To avoid adding assertions, use the `-nda/--no-diff-assertions` option.

``` 
usage: tkltest generate [-h] [-nda] [-pf PARTITIONS_FILE]
                        {ctd-amplified,evosuite,randoop} ...

positional arguments:
  {ctd-amplified,evosuite,randoop}
    ctd-amplified       Use CTD for computing coverage goals
    evosuite            Use EvoSuite for generating a test suite
    randoop             Use Randoop for generating a test suite

optional arguments:
  -h, --help            show this help message and exit
  -nda, --no-diff-assertions
                        do not add assertions for differential testing to the
                        generated tests
  -pf PARTITIONS_FILE, --partitions-file PARTITIONS_FILE
                        path to file containing specification of partitions
```

## Execute Command

Executes generated JUnit test cases on the application under test. The application version
(legacy or modernized) to run the tests on can specified in the toml file, via the general
options `monolith_app_path` (list of paths to application classes) and `app_classpath_file`
(file containing paths to jar files that  represent the library dependencies of app).

```
usage: tkltest execute [-h] [-bt {ant,maven,gradle}] [-nbf] [-cc] [-onli]
                       [-tc TEST_CLASS]

optional arguments:
  -h, --help            show this help message and exit
  -bt {ant,maven,gradle}, --build-type {ant,maven,gradle}
                        build file type for compiling and running the tests -
                        either ant, maven or gradle
  -nbf, --no-build-file-creation
                        Whether to generate build files. If set to false, a
                        build file (of type set in build_type option) should
                        already exist and will be used
  -cc, --code-coverage  generate code coverage report with JaCoCo agent
  -onli, --online-instrumentation
                        perform online instrumentation of app classes for
                        measuring code coverage (default: app classes are
                        instrumented offline)
  -tc TEST_CLASS, --test-class TEST_CLASS
                        path to a test class file (.java) to compile and run
```

For details on the `execute` command options, see the section [Configuration Options](#configuration-options).

## Known Tool Issues

1. On apps with native UI (e.g., swing), the tool can sometimes get stuck during sequence execution
   (even though it uses a Java agent for replacing calls to GUI components); as a workaround,
   users can exclude UI-related classes from the set of test targets.

2. Coverage in JEE apps could be low because of limited JEE mocking support.

3. A known issue on Windows OS is that Tackle-test might exceed Windows limit of 260 characters for a file system folder path name length. 
 Tackle-test mimics the structure of the application under its output directory, to enable generating 
tests in the same package as the class under test, and gaining access to all its non-private members and methods. 
If your application has a deep package hierarchy, these paths might exceed the 260 characters length limit. For Windows 10,
there are online instructions available on how to enable long paths and avoid this limitation.

## Configuration Options

All configuration options for `tkltest` commands  can be specified in a [toml](https://toml.io/en/)
file, containing sections for different commands and subcommands.

A subset of the configuration options can also be specified on the command line, as the
examples above illustrate. If an option is specified both on the command line
and in the configuration file, the command-line value overrides the configuration-file value.

The configuration file can be initialized via `tkltest config init`. `tkltest config list` lists
all available configuration options with information about each option: the option's TOML name,
the option's command-line short/long names (if it supported in the CLI), whether the option is
required, and the option description).

| TOML name ("*"=req, "^"=CLI-only)   | CLI name                       | Description                                                                                                                             |
|-------------------------------------|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| general                             |                                |                                                                                                                                         |
| app_name*                           |                                | name of the application being tested                                                                                                    |
| app_classpath_file*                 |                                | file containing paths to jar files that represent the library dependencies of app                                                       |
| config_file^                        | -cf/--config-file              | path to TOML file containing configuration options                                                                                      |
| log_level^                          | -l/--log-level                 | logging level for printing diagnostic messages                                                                                          |
| monolith_app_path*                  |                                | list of paths to application classes                                                                                                    |
| java_jdk_home*                      |                                | root directory for JDK installation (must be JDK; JRE will not suffice); can be set as environment variable JAVA_HOME                   |
| test_directory                      | -td/--test-directory           | name of root test directory containing the generated JUnit test classes                                                                 |
| reports_path                        | -rp/--reports-path             | path to the reports directory                                                                                                           |
| verbose                             | -vb/--verbose                  | run in verbose mode printing detailed status messages                                                                                   |
| version^                            | -v/--version                   | print CLI version number                                                                                                                |
|                                     |                                |                                                                                                                                         |
| config                              |                                | Initialize configuration file or list configuration options                                                                             |
|                                     |                                |                                                                                                                                         |
| config.init                         |                                | Initialize configuration options and print (in TOML format) to file or stdout                                                           |
| file^                               | -f/--file                      | name of TOML file to create with initialized configuration options                                                                      |
|                                     |                                |                                                                                                                                         |
| config.list                         |                                | List all configuration options with description                                                                                         |
|                                     |                                |                                                                                                                                         |
| generate                            |                                | Generate test cases on the application under test                                                                                       |
| jee_support                         |                                | add support JEE mocking in generated tests cases                                                                                        |
| no_diff_assertions                  | -nda/--no-diff-assertions      | do not add assertions for differential testing to the generated tests                                                                   |
| partitions_file                     | -pf/--partitions-file          | path to file containing specification of partitions                                                                                     |
| target_class_list                   |                                | list of target classes to perform test generation on                                                                                    |
| excluded_class_list                 |                                | list of classes or packages to exclude from test generation. Packages must end with a wildcard.                                         |
| time_limit                          |                                | time limit (in seconds) for evosuite/randoop test generation                                                                            |
| app_build_type*                     |                                | build type for collecting app dependencies: gradle (support for maven and ant to be added)                                              |
| app_build_config_file*              |                                | path to app build file for the specified app build type                                                                                 |
| app_build_settings_file             |                                | path to app build settings file for the specified app build type                                                                        |
|                                     |                                |                                                                                                                                         |
| generate.ctd_amplified              |                                | Use CTD for computing coverage goals                                                                                                    |
| base_test_generator                 | -btg/--base-test-generator     | base test generator to use for creating building-block test sequences                                                                   |
| augment_coverage                    | -ac/--augment-coverage         | augment CTD-guided tests with coverage-increasing base tests                                                                            |
| no_ctd_coverage                     | -nctd/--no-ctd-coverage        | generate CTD coverage report                                                                                                            |
| interaction_level                   |                                | CTD interaction level (strength) for test-plan generation                                                                               |
| num_seq_executions                  |                                | number of executions to perform to determine pass/fail status of generated sequences                                                    |
| refactored_app_path_prefix*         |                                | path prefix to root directory of refactored app version                                                                                 |
| refactored_app_path_suffix*         |                                | list of paths to refactored app classes                                                                                                 |
| reuse_base_tests                    | -rbt/--reuse-base-tests        | reuse existing base test cases                                                                                                          |
|                                     |                                |                                                                                                                                         |
| generate.evosuite                   |                                | Use EvoSuite for generating a test suite                                                                                                |
| criterion                           |                                | coverage criterion for evosuite                                                                                                         |
|                                     |                                |                                                                                                                                         |
| generate.randoop                    |                                | Use Randoop for generating a test suite                                                                                                 |
| no_error_revealing_tests            |                                | do not generate error-revealing tests with randoop                                                                                      |
|                                     |                                |                                                                                                                                         |
| execute                             |                                | Execute generated tests on the application version under test                                                                           |
| app_packages*                       |                                | list of app packages. Must end with a wildcard                                                                                          |
| build_type                          | -bt/--build-type               | build file type for compiling and running the tests - either ant, maven or gradle                                                       |
| create_build_file                   | -nbf/--no-build-file-creation  | Whether to generate build files. If set to false, a build file (of type set in build_type option) should already exist and will be used |
| code_coverage                       | -cc/--code-coverage            | generate code coverage report with JaCoCo agent                                                                                         |
| online_instrumentation              | -onli/--online-instrumentation | perform online instrumentation of app classes for measuring code coverage (default: app classes are instrumented offline)               |
| test_class                          | -tc/--test-class               | path to a test class file (.java) to compile and run                                                                                    |
