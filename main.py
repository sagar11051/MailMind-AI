import sys
import os
from dotenv import load_dotenv
from agents.classifier_agent import ClassifierAgent
from agents.json_agent import JSONAgent
from agents.email_agent import EmailAgent
from memory.shared_memory import SharedMemory
from utils.logger import setup_logger
from utils.pdf_parser import extract_text_from_pdf
from utils.email_parser import parse_email

load_dotenv()
HF_TOKEN = os.getenv('HF_TOKEN')

def process_input(input_path):
    logger = setup_logger()
    shared_memory = SharedMemory()
    classifier = ClassifierAgent(HF_TOKEN)
    json_agent = JSONAgent(HF_TOKEN)
    email_agent = EmailAgent(HF_TOKEN)

    # Load input
    if input_path.endswith('.pdf'):
        input_data = extract_text_from_pdf(input_path)
    elif input_path.endswith('.json'):
        import json
        with open(input_path) as f:
            input_data = json.load(f)
    elif input_path.endswith('.txt'):
        with open(input_path) as f:
            input_data = f.read()
    else:
        logger.error('Unsupported file type')
        return {'error': 'Unsupported file type'}

    # Classify and route
    result = classifier.classify_and_route(input_data)
    logger.info(f'Classification result: {result}')
    shared_memory.set('last_classification', str(result))

    if result['route_to'] == 'json_agent':
        output = json_agent.process_json(input_data)
    elif result['route_to'] == 'email_agent':
        output = email_agent.process_email(input_data)
    else:
        output = {'error': 'No valid route'}
    logger.info(f'Agent output: {output}')
    shared_memory.set('last_output', str(output))
    return {'classification': result, 'output': output}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python main.py --input <input_file>')
        sys.exit(1)
    input_path = sys.argv[2]
    process_input(input_path) 