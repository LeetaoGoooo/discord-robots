# Discord Gemini Robot

This project sets up a Discord bot using Python that utilizes the Gemini API to answer questions and recognize image . Additionally, it integrates with Bing Create to create images and enhances the creation process using Gemini.

## Features

- Question Answering: The bot can answer questions using the Gemini API.
- Image Recognize: The bot can recognize the content of the image.
- Bing Create Integration: The bot can create images using Bing Create and enhance the creation process using Gemini.

## Installation

1. Clone the repository:

    ```shell

    git clone https://github.com/LeetaoGoooo/discord-robots.git
    ```

2. Install the required dependencies:

    ```shell
    pip install -r requirements.txt
    ```

3. Set up the Discord bot token:

    ```shell
    export DISCORD_TOKEN=DISCORD_TOKEN
    export BING_TOKEN=BING_TOKEN
    export GUILD=GUILD
    export GEMINI_KEY=GEMINI_KEY
    ```
    [👉How to get your own guild](https://support.discord.com/hc/en-us/articles/206346498)

4. Run the bot:

    ```shell
    python bot.py
    ```

or use Dockerfile

```shell
docker build -t discord-robots .
docker run  --name name -d  -e DISCORD_TOKEN=DISCORD_TOKEN -e GEMINI_KEY=GEMINI_KEY -e BING_TOKEN=BING_TOKEN discord-robots 
```

## Usage

Once the bot is running, you can invite it to your Discord server and interact with it using various commands. Here are some examples:

<image src="./screens/answer-question.png" width="300"/><image src="./screens/image-recognize.png" width="300"/><image src="./screens/bing-create.png" width="300"/>

Please refer to the documentation for more details on available commands and their usage.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow the guidelines outlined in the CONTRIBUTING.md file.

## License

This project is licensed under the [MIT License](LICENSE).
