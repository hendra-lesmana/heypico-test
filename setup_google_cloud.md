# Setting Up Google Cloud and Maps API

This guide will walk you through the process of creating a Google Cloud account and setting up the necessary APIs for the LLM with Google Maps Integration project.

## 1. Create a Google Cloud Account

1. Go to [Google Cloud](https://cloud.google.com/) and click on "Get Started for Free" or "Sign in" if you already have a Google account.
2. Follow the prompts to create a new Google Cloud account.
3. You'll need to provide credit card information for verification, but you'll be using the free tier credits for this project.

## 2. Create a New Project

1. Once logged in to the Google Cloud Console, click on the project dropdown at the top of the page.
2. Click on "New Project".
3. Enter a project name (e.g., "LLM Maps Integration") and click "Create".

## 3. Enable the Required APIs

1. In the Google Cloud Console, navigate to "APIs & Services" > "Library".
2. Search for and enable the following APIs:
   - **Maps JavaScript API**: For embedding maps in your web application
   - **Places API**: For searching locations and getting place details
   - **Directions API**: For getting directions between locations

## 4. Create an API Key

1. In the Google Cloud Console, navigate to "APIs & Services" > "Credentials".
2. Click on "Create Credentials" and select "API Key".
3. Your new API key will be displayed. Copy this key as you'll need it for your application.

## 5. Secure Your API Key

It's important to restrict your API key to prevent unauthorized use:

1. In the credentials page, find your API key and click on it to edit.
2. Under "Application restrictions", you can restrict the key to specific websites (HTTP referrers) or IP addresses.
3. Under "API restrictions", restrict the key to only the APIs you're using (Maps JavaScript API, Places API, and Directions API).

## 6. Set Up Billing Alerts (Optional but Recommended)

1. Go to "Billing" in the Google Cloud Console.
2. Select your billing account.
3. Click on "Budgets & alerts".
4. Click "Create Budget" and follow the prompts to set up alerts when your usage approaches certain thresholds.

## 7. Add Your API Key to the Project

1. Copy your API key.
2. Open the `.env` file in your project directory.
3. Replace `your_api_key_here` with your actual API key:

```
GOOGLE_MAPS_API_KEY=your_actual_api_key_here
```

## Free Tier Usage Limits

Google Cloud offers a free tier for Maps API usage. As of the creation of this guide, the limits include:

- Maps JavaScript API: $200 of free usage per month (approximately 28,000 map loads)
- Places API: $200 of free usage per month
- Directions API: $200 of free usage per month

These limits should be more than sufficient for development and personal use. The application includes rate limiting to help prevent exceeding these limits.

## Monitoring Usage

1. In the Google Cloud Console, go to "APIs & Services" > "Dashboard".
2. Here you can monitor your API usage and ensure you stay within the free tier limits.

## Troubleshooting

If you see errors related to the Google Maps API, check the following:

1. Ensure your API key is correctly added to the `.env` file.
2. Verify that you've enabled all the required APIs.
3. Check if your API key has the correct restrictions that still allow your application to use it.
4. Look at the Google Cloud Console "APIs & Services" > "Dashboard" for any error messages or quota issues.