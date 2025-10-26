# CF-bot

A bot of discord to get daily problems of Codeforces, and soon more functions.

## 🎯 Available Full Commands

| Command        | Description                  | Example                |
|----------------|------------------------------|------------------------|
| `!testdaily`   | Sends a daily test problem.   | `!testdaily`           |
| `!problem`     | Sends a problem with a custom range. | `!problem 1000 1500` |
| `!showrange`   | Shows the current problem range. | `!showrange`         |
| `!setrange`    | Changes the problem range.    | `!setrange 800 1200`  |
| `!setchannel`  | Sets the channel for problem posts. | `!setchannel #channel` |
| `!showchannel` | Shows the currently configured channel. | `!showchannel` |
| `!config`      | Displays the full configuration. | `!config`           |


## Key Features & Benefits

*   **Daily Codeforces Problems:** Automatically posts daily Codeforces problems to a designated Discord channel.
*   **Customizable:**  Configuration options for channel selection and problem difficulty (future implementation).
*   **Extensible:** Designed with future functionality in mind.

## Prerequisites & Dependencies

Before you begin, ensure you have the following installed:

*   **Python:** Version 3.7 or higher.
*   **pip:** Python package installer (usually included with Python).
*   **Discord Account & Server:** You'll need a Discord account and a server where you want to deploy the bot.
*   **Discord Bot Token:** You'll need to create a Discord bot in the Discord Developer Portal and obtain its token.

The following Python packages are required:

*   `discord.py>=2.3.0`
*   `python-dotenv>=1.0.0`
*   `requests>=2.31.0`
*   `apscheduler>=3.10.0`

## Installation & Setup Instructions

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/fabricioarce/CF-bot.git
    cd CF-bot
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**

    *   Create a `.env` file in the project's root directory.
    *   Add the following variables to the `.env` file, replacing the placeholders with your actual values:

        ```
        TOKEN=YOUR_DISCORD_BOT_TOKEN
        CHANNEL_ID=YOUR_DISCORD_CHANNEL_ID
        ```

        *   `TOKEN`: Your Discord bot token. Obtain this from the Discord Developer Portal.
        *   `CHANNEL_ID`: The ID of the Discord channel where the bot should post problems.  To get this, enable Developer Mode in Discord (Settings -> Advanced) and then right-click on the channel and select "Copy ID".

5.  **Run the Bot:**

    ```bash
    python main.py
    ```

## Usage Examples & API Documentation

The bot automatically posts a daily Codeforces problem to the configured channel.  Further customization and command examples will be added in future versions.

*   `codeforces_api.py` contains the `CodeForcesAPI` class which handles interaction with the Codeforces API.
*   `commands.py` contains the `CodeForcesCog` which handles Discord bot commands (currently none implemented).
*   `main.py` is the main entry point for the bot.

## Configuration Options

The bot is configured via environment variables in the `.env` file. The following variables are used:

*   **`TOKEN`**: Your Discord bot token (required).
*   **`CHANNEL_ID`**: The Discord channel ID where the bot will send messages (required).

Future versions will include configuration options for problem difficulty, time of day for posting, etc.

## Contributing Guidelines

Contributions are welcome!  Please follow these guidelines:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Write clear, concise code with proper comments.
4.  Submit a pull request with a detailed description of your changes.

## License Information

No license is specified for this project.  All rights are reserved by the owner.

## Acknowledgments

*   [discord.py](https://discordpy.readthedocs.io/en/stable/)
*   [Codeforces API](https://codeforces.com/api/help)