### AI Instagram Greeting Parser

This application scrapes Instagram profiles, extracts profile picture details using OpenAI's Vision model, and generates personalized greetings to send as direct messages based on the user's profile content (for example, noticing a pet in the picture and mentioning it in the greeting).

---

### Installation and Setup

#### 1. Clone the repository:
```bash
git clone <repository_url>
cd ai_insta_greeting
```

#### 2. Set up a virtual environment:
Create a virtual environment to isolate dependencies.

```bash
python3 -m venv venv
```

Activate the virtual environment:

- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  venv\Scripts\activate
  ```

#### 3. Install dependencies:
Install the required Python libraries using `requirements.txt`:
or for Windows:
Install the required Python libraries using `requirements_for_windows.txt`:

```bash
pip install -r requirements.txt
```
or for Windows:
```bash
pip install -r requirements_for_windows.txt
```


#### 4. Set up environment variables:
Create a `.env` file in the project root directory. You need to provide:

- Your OpenAI API key for vision-based processing.
- Proxy settings (if applicable).

Example `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
current_proxy=your_proxy_settings_here
```

#### 5. Adding accounts to send greetings:
Add accounts you want to sent greetings to to the `instagram_accounts.txt` file.


#### 6. Instagram login setup:
The first time you run the script, you'll be prompted to log into Instagram manually. After the login, cookies will be saved to the database for future logins, so you won't need to log in again.

### Running the Application

Once all dependencies are installed and environment variables are set up, you can run the script:

```bash
python main.py
```

- The script will load the list of Instagram usernames from the `instagram_accounts.txt` file and iterate over each username.
- For each profile, it will:
  1. Extract the profile picture.
  2. Use the OpenAI Vision model to describe the image.
  3. Generate a greeting message based on the image description.
  4. Send the greeting as a direct message to the Instagram user.

### Important Notes

1. **Instagram Login:**
   - When running the script for the first time, Instagram might prompt you to log in manually. Follow the on-screen instructions to log in, and the cookies will be saved for future sessions.
   
2. **Cookies Storage:**
   - The login cookies are saved in a local SQLite database (`accounts.db`), so future sessions won’t require manual login again.

3. **Proxies:**
   - If your connection requires proxies, make sure to add proxy details in the `.env` file under the `current_proxy` variable.

4. **OpenAI Vision API:**
   - This script uses the OpenAI API for analyzing profile pictures. Make sure your API key is valid and you have enough credits for usage.

### File Structure

```
ai_insta_greeting/
│
├── src/
│   ├── AI/
│   │   ├── __init__.py
│   │   ├── get_AI_greeting_handler.py
│   │   └── get_image_description.py
│   ├── algorithms/
│   ├── database/
│   ├── driver/
│   ├── proxy/
│   ├── ui/
│   └── utils/
│
├── venv/
├── .env
├── .gitignore
├── accounts.db
├── instagram_accounts.txt
├── main.py
├── requirements.txt
└── README.md
```

### Usage Example

If you want to add Instagram accounts for the script to process, add them in `instagram_accounts.txt`, one username per line.

Example:
```
instagram_user_1/
instagram_user_2/
```

---

### Contributing
Feel free to open issues or submit pull requests to contribute to the project.

### License
This project is licensed under the [MIT License](LICENSE).

---

By following these steps, you can set up the environment and run the script to automatically generate and send personalized greetings to Instagram users based on their profile pictures.
