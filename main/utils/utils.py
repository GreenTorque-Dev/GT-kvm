import os
import time
from datetime import timedelta
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from django.core.mail import EmailMessage
from django.conf import settings
import psutil


def convert_to_gb(memory_bytes):
    # Convert bytes to gigabytes if the value is greater than 1 GB
    return round(memory_bytes / (1024 ** 3), 2)

def get_memory_usage():
    # Get the total virtual memory
    total_memory = psutil.virtual_memory().total

    # Get the current process ID
    current_pid = os.getpid()

    # Initialize variables for current and other processes' memory usage
    current_python_memory = 0
    other_processes_memory = 0

    # Iterate over all running processes
    for process in psutil.process_iter(['pid', 'name', 'memory_info']):
        process_info = process.info
        process_pid = process_info['pid']
        if not process_info['memory_info']:
            continue
        process_memory = process_info['memory_info'].rss



        # Check if the current process is the Python script
        if process_pid == current_pid:
            current_python_memory = float(process_memory)
        else:
            other_processes_memory += float(process_memory)

    # Convert total memory to gigabytes
    total_memory_gb = convert_to_gb(total_memory)

    # Create the result dictionary
    result_dict = {
        'total_memory': convert_to_gb(total_memory),
        'current_python_memory': convert_to_gb(current_python_memory),
        'current_python_percentage': round((current_python_memory / total_memory) , 2) * 100,
        'other_processes_memory': convert_to_gb(other_processes_memory),
        'other_processes_percentage': (other_processes_memory/ total_memory) * 100
    }

    return result_dict

def get_cpu_usage():
    # Get the current process ID
    current_pid = os.getpid()

    # Get CPU usage for the entire system
    total_cpu_percent = psutil.cpu_percent(interval=1.0)

    # Get CPU usage for the current process
    current_python_cpu = psutil.Process(current_pid).cpu_percent(interval=1.0)

    # Calculate CPU usage for other processes
    other_processes_cpu = total_cpu_percent - current_python_cpu

    # Create the result dictionary
    result_dict = {
        'current_python_cpu': current_python_cpu,
        'other_processes_cpu': other_processes_cpu,
        'total_used': total_cpu_percent,
    }

    return result_dict


def get_system_uptime():
    try:
        boot_time = psutil.boot_time()
        uptime_seconds = int(time.time() - boot_time)
        uptime_str = str(timedelta(seconds=uptime_seconds))
        return uptime_str
    except Exception as e:
        return f""


def send_email(subject, message, recipient_list, from_email=None):
    """
    Send an email and save it as a file.

    :param subject: Subject of the email
    :param message: Body of the email
    :param recipient_list: List of recipient email addresses
    :param from_email: Sender email address (optional, defaults to DEFAULT_FROM_EMAIL)
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    email = EmailMessage(
        subject,
        message,
        from_email,
        recipient_list
    )
    email.send(fail_silently=False)


def add_query_params(url, params):
    # Parse the URL into components
    url_parts = urlparse(url)
    query_params = parse_qs(url_parts.query)

    # Update the query parameters with the new ones
    query_params.update(params)
    query_params_flat = {k: v[0] if isinstance(v, list) else v for k, v in query_params.items()}

    # Rebuild the query string
    new_query_string = urlencode(query_params_flat)
    new_url = urlunparse(url_parts._replace(query=new_query_string))

    return new_url




def get_labels_data():
    return {
        'us-southeast': 'Atlanta, GA (us-southeast)',
        'us-ord': 'Chicago, IL (us-ord)',
        'us-central': 'Dallas, TX (us-central)',
        'us-west': 'Fremont, CA (us-west)',
        'us-lax': 'Los Angeles, CA (us-lax)',
        'us-mia': 'Miami, FL (us-mia)',
        'us-east': 'Newark, NJ (us-east)',
        'us-sea': 'Seattle, WA (us-sea)',
        'us-iad': 'Washington, DC (us-iad)',
        'ca-central': 'Toronto, CA (ca-central)',
        'ap-south': 'Singapore, SG (ap-south)',
        'jp-osa': 'Osaka, JP (jp-osa)',
        'ap-northeast': 'Tokyo, JP (ap-northeast)',
        'in-maa': 'Chennai, IN (in-maa)',
        'ap-west': 'Mumbai, IN (ap-west)',
        'id-cgk': 'Jakarta, ID (id-cgk)',
        'se-sto': 'Stockholm, SE (se-sto)',
        'nl-ams': 'Amsterdam, NL (nl-ams)',
        'it-mil': 'Milan, IT (it-mil)',
        'uk-lon': 'London, UK (uk-lon)',
        'fr-par': 'Paris, FR (fr-par)',
        'es-mad': 'Madrid, ES (es-mad)',
        'eu-central': 'Frankfurt, DE (eu-central)',
        'eu-west': 'Dublin, IE (eu-west)',
        'ap-southeast': 'Sydney, AU (ap-southeast)',
        'br-gru': 'Sao Paulo, BR (br-gru)'
    }

