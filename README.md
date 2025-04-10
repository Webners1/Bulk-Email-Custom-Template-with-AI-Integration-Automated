# Bulk-Email-Custom-Template-with-AI-Integration-Automated

An advanced Python-based email marketing solution with AI-powered personalization, intelligent scheduling, and automated campaign management.

## Features

- **AI-Powered Personalization**: Integrates with OpenAI to generate highly personalized email content
- **Beautiful HTML Templates**: Ready-to-use responsive email templates with customizable sections
- **Smart Scheduling**: Optimized sending times based on recipient timezone and day of week
- **Campaign Automation**: Set up recurring campaigns with intelligent scheduling
- **CSV Integration**: Import recipient data from standard CSV files
- **Delivery Management**: Controls for email velocity and daily sending limits
- **Detailed Analytics**: Track sent emails and campaign performance
- **Multi-timezone Support**: Optimized sending for global recipient lists

## IMPORTANT LEGAL DISCLAIMER

This tool is provided for educational purposes only. Before using this software for sending emails, please ensure you comply with all applicable laws and regulations regarding electronic communications, including but not limited to:

1. **CAN-SPAM Act (US)**: Requires commercial emails to include opt-out mechanisms, valid physical address, and prohibits deceptive headers/subject lines.

2. **GDPR (EU)**: Requires explicit consent before sending marketing emails to EU residents, and includes rights to access, rectify, and erase personal data.

3. **CASL (Canada)**: Requires express or implied consent, identification information, and unsubscribe mechanisms.

4. **Local anti-spam laws**: Many countries have their own regulations governing commercial electronic messages.

By using this software, you acknowledge that:
- You have obtained proper consent from recipients or have a lawful basis for contact
- You will provide clear identification of yourself/organization in all messages
- You will honor opt-out requests promptly
- You will maintain proper records of consent as required by applicable laws

The author of this software accepts no responsibility for misuse or any legal consequences resulting from the use of this tool. Always consult with a legal professional before implementing any email marketing campaign.

## Setup Instructions

### Prerequisites

- Python 3.7+
- SMTP server access
- CSV file with recipient data
- OpenAI API key (optional, for AI-enhanced content)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/Bulk-Email-Custom-Template-with-AI-Integration-Automated.git
   cd Bulk-Email-Custom-Template-with-AI-Integration-Automated
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a configuration file:
   ```
   cp config-example.json config.json
   ```

4. Edit the configuration file with your SMTP settings and preferences

### CSV Format

Prepare your CSV file with recipient data in the following format:

| Email | First Name | Last Name | Company | Industry | Title | Company City |
|-------|------------|-----------|---------|----------|-------|--------------|
| john@example.com | John | Doe | Acme Inc | Technology | CTO | New York |

The more data fields you include, the more personalized the AI-generated content will be.

## Usage

### Interactive Mode

Run the script in interactive mode to set up your campaign:

```
python index.py
```

You'll be prompted to enter your SMTP configuration, email settings, and scheduling preferences.

### Command Line Options

```
python index.py --reset      # Reset sent email records
python index.py --show       # Display sent email statistics
python index.py --now        # Send emails immediately
python index.py --limit 50   # Set custom daily sending limit
```

### Scheduling

The script can automatically determine optimal sending times based on recipient timezones. To use the scheduling feature:

```
python index.py
```

Then select "y" when asked if you want to set up a schedule.

## Configuration Options

The `config.json` file supports the following options:

```json
{
    "smtp_server": "smtp.example.com",
    "smtp_port": "587",
    "smtp_user": "your-email@example.com",
    "smtp_pass": "your-password",
    "letter_subject": "Subject line with {company} placeholder",
    "letter_from": "Your Name",
    "letter_signature": "Your Name\nYour Position",
    "use_ai": true,
    "openai_api_key": "your-openai-api-key",
    "delay_between_emails": 5,
    "daily_limit": 100,
    "csv_path": "./recipients.csv",
    "schedule_time": "09:00",
    "schedule_days": ["monday", "wednesday", "friday"]
}
```

## Advanced Features

### AI Content Generation

When enabled, the system uses advanced AI to generate custom email content for each recipient based on their profile data. This creates highly personalized messages that significantly improve engagement rates.

### Timezone Optimization

The scheduler automatically detects optimal sending times based on day of week and recipient timezone, increasing the likelihood of email opens and responses.

### HTML Template Customization

You can customize the HTML email templates by editing the templates in the code. The system supports placeholders for dynamic content insertion.

## Security Notes

- Store your `config.json` file securely and never commit it to public repositories
- Consider using app-specific passwords for email accounts when possible
- Use strong passwords and encryption for all configuration files
- Regularly rotate API keys and credentials

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to all contributors who have helped improve this tool
- Special thanks to the open source community for their invaluable resources

---

Created by [StackUss](https://www.stackuss.com) - Your trusted partner in high-tech transformation.