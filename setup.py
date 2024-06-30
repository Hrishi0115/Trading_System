from setuptools import setup, find_packages

# Function to read the requirements.txt file
def parse_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Filter out comments and empty lines
        requirements = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
        return requirements

setup(
    name='trading_system',
    version='0.1',
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    # entry_points={
    #     'console_scripts': [
    #         # if you have any scripts to run
    #     ],
    # },
)

# Setting `PYTHONPATH` for the project

# 1. Create and activate venv
# 2. In cmd: `set PYTHONPATH=C:\Users\hrish\trading_system`
# 3. Make `PYTHONPATH` persistent in the virtual environment:
# echo set PYTHONPATH=C:\Users\hrish\AlgoTradingPlatform\backtesting-engine >> venv\Scripts\activate.bat
# Verify PYTHONPATH
# python -c "import sys; print(sys.path)"