# Deploying Paperplane to Render

This guide will help you deploy the Paperplane userbot to Render instead of Heroku.

## Prerequisites

1. A Render account (sign up at https://render.com)
2. A GitHub account with this repository
3. Telegram API credentials (API_ID and API_HASH from https://my.telegram.org)
4. A MongoDB Atlas database (free tier available at https://cloud.mongodb.com)
5. A generated string session

## Step 1: Generate String Session

1. Install Python dependencies locally:
   ```bash
   pip install telethon
   ```

2. Run the string session generator:
   ```bash
   python generate_string_session.py
   ```

3. Enter your API_ID and API_HASH when prompted
4. Follow the authentication process
5. Copy the generated string session

## Step 2: Set up MongoDB

1. Go to https://cloud.mongodb.com and create a free account
2. Create a new cluster (free tier is sufficient)
3. Create a database user with read/write permissions
4. Get the connection string (MongoDB URI)
5. Replace `<password>` in the URI with your database user password

## Step 3: Deploy to Render

### Option 1: Using render.yaml (Recommended)

1. Fork this repository to your GitHub account
2. Go to https://render.com and sign in
3. Click "New" → "Blueprint"
4. Connect your GitHub account and select this repository
5. Render will automatically detect the `render.yaml` file
6. Set the required environment variables:
   - `API_KEY`: Your Telegram API ID
   - `API_HASH`: Your Telegram API Hash
   - `STRING_SESSION`: The generated string session
   - `MONGO_DB_URI`: Your MongoDB connection string
7. Click "Apply" to deploy

### Option 2: Manual Service Creation

1. Go to https://render.com and sign in
2. Click "New" → "Background Worker"
3. Connect your GitHub account and select this repository
4. Configure the service:
   - **Name**: paperplane-userbot
   - **Environment**: Docker
   - **Dockerfile Path**: ./Dockerfile
   - **Plan**: Starter (or higher based on your needs)
5. Add environment variables (same as Option 1)
6. Click "Create Background Worker"

## Step 4: Configure Environment Variables

Set the following environment variables in Render:

### Required Variables:
- `API_KEY`: Your Telegram API ID (e.g., 20587910)
- `API_HASH`: Your Telegram API Hash
- `STRING_SESSION`: Generated string session
- `MONGO_DB_URI`: MongoDB connection string

### Optional Variables:
- `BOTLOG`: Set to "True" to enable logging (default: False)
- `BOTLOG_CHATID`: Chat ID for bot logs (if BOTLOG is True)
- `PM_AUTO_BAN`: Set to "True" to enable PM auto-ban (default: False)
- `WELCOME_MUTE`: Set to "True" to enable welcome mute (default: False)
- `SCREENSHOT_LAYER_ACCESS_KEY`: For screenshot functionality
- `OPEN_WEATHER_MAP_APPID`: For weather commands
- `WOLFRAM_ID`: For Wolfram Alpha integration
- `SPOTIPY_CLIENT_ID`: Spotify Client ID
- `SPOTIPY_CLIENT_SECRET`: Spotify Client Secret
- `LASTFM_API`: Last.fm API key
- `LASTFM_SECRET`: Last.fm secret
- `LASTFM_USERNAME`: Last.fm username
- `LASTFM_PASSWORD`: Last.fm password
- `GDRIVE_FOLDER`: Google Drive folder ID

## Step 5: Monitor Deployment

1. Go to your service dashboard in Render
2. Check the "Logs" tab to monitor the deployment
3. Once deployed, your userbot should be running and responsive to commands

## Differences from Heroku

1. **No Dynos**: Render uses "Services" instead of Heroku's dynos
2. **Always On**: Background workers on Render don't sleep like Heroku's free dynos
3. **Docker Native**: Render has better Docker support
4. **Environment Variables**: Similar to Heroku but managed through Render's dashboard
5. **Logs**: Real-time logs available in the Render dashboard

## Troubleshooting

### Common Issues:

1. **Build Failures**: Check the build logs in Render dashboard
2. **Environment Variables**: Ensure all required variables are set correctly
3. **MongoDB Connection**: Verify your MongoDB URI is correct and accessible
4. **String Session**: Make sure the string session is valid and not expired

### Getting Help:

1. Check the logs in Render dashboard
2. Verify all environment variables are set
3. Ensure your MongoDB cluster is running and accessible
4. Test your string session locally before deploying

## Cost Considerations

- Render's Starter plan for background workers costs $7/month
- MongoDB Atlas free tier provides 512MB storage
- Consider upgrading plans based on your usage requirements

## Security Notes

1. Never share your string session with anyone
2. Keep your API credentials secure
3. Use environment variables for all sensitive data
4. Regularly rotate your API keys and sessions