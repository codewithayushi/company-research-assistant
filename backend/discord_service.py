import requests

def send_report_to_discord(bot_token: str, channel_id: str, applicant_name: str, applicant_email: str, company_name: str, company_website: str, pdf_path: str):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {bot_token}"
    }
    
    message_content = (
        f"🚨 **New Company Research Report Submitted**\n\n"
        f"👤 **Applicant Name:** {applicant_name}\n"
        f"📧 **Applicant Email:** {applicant_email}\n"
        f"🏢 **Company Name:** {company_name}\n"
        f"🌐 **Company Website:** {company_website}"
    )
    
    try:
        with open(pdf_path, "rb") as f:
            files = {
                "file": (pdf_path, f, "application/pdf")
            }
            data = {
                "content": message_content
            }
            response = requests.post(url, headers=headers, data=data, files=files)
            response.raise_for_status()
            return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}