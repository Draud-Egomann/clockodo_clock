# ClockoDoClock

## Overview

This application integrates with the Clockodo API to to automatically clock in / out at certain times. It requires a correctly set up `.env` file to function properly.

## Requirements

- Python 3.x
- Pip for installing dependencies

## Setup

### Environment Variables

To run the application, you need to configure the following environment variables in a `.env` file located at the `root` of the project directory:

```plaintext
API_KEY = your_api_key_here
EMAIL = your_email_here
SUBDOMAIN = your_subdomain_here (default: my)
SERVICES_ID = your_services_id_here (set to 0 if unknown)
CUSTOMERS_ID = your_customers_id_here (set to 0 if unknown)
RANDOM_CLOCKING_IN = True or False
WORKING_DAYS = ["Monday", "Tuesday", ..., "Sunday"]
START_STOP_TIMES = [("08:00:00", "12:00:00"), ("13:00:00", "17:00:00")]
```

Alternatively, you can run the `src/create_env.py` script to generate a `.env` file with the necessary variables. The script will prompt you to fill in the missing values.

```bash
cd ./src
python ./create_env.py
```

### Installing Dependencies

To install the necessary Python libraries, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

Once the environment and dependencies are set up, you can run the application with:

```bash
cd ./src
python ./main.py
```

The program will check the correctness of the `.env` variables and prompt you to fill in missing service and customer IDs via the Clockodo API if they are set to 0.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your enhancements.

## License

The project is licensed under the MIT License. For more information, see the [LICENSE](LICENSE) file.
