import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(to_email, subject, html_content, from_email='pablosilvasena@gmail.com'):
    """
    Envia um email usando SendGrid
    
    Args:
        to_email (str): Email do destinatário
        subject (str): Assunto do email
        html_content (str): Conteúdo HTML do email
        from_email (str): Email do remetente
    
    Returns:
        bool: True se enviado com sucesso, False caso contrário
    """
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f"Email enviado com sucesso! Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {str(e)}")
        return False

if __name__ == "__main__":
    send_email(
        to_email='pablosilvasena@gmail.com',
        subject='Teste de Email',
        html_content='<strong>Email de teste</strong>'
    )