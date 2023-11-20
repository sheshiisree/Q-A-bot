import traceback
import fitz
import os
from transformers import BertTokenizer, BertForQuestionAnswering
import torch
from models import Chat
from database import session
from sqlalchemy import desc

model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
model = BertForQuestionAnswering.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

class BotService:
    def __init__(self):
        pass

    def obj_to_dict(self, data):
        response = {}
        if data is None:
            return {}
        for c in data.__table__.columns:
            if c.name not in ["created_date", "updated_date"]:
                response[c.name] = getattr(data, c.name)
            else:
                response[c.name] = str(getattr(data, c.name))
        return response

    def obj_to_list(self, data):
        list_dicts = []
        if data is None:
            return []
        for obj in data:
            list_dicts.append(self.obj_to_dict(obj))        
        return list_dicts

    
    
    def append_to_context(self, new_data):
        with open('context.txt', 'a') as file:
            file.write("\n\n\n\n\n" + new_data)

    def get_context_from_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def find_relevant_context(self, question, full_context, num_sentences=5):
        keywords = question.split()
        sentences = full_context.split('.')
        relevant_sentences = [sentence for sentence in sentences if any(keyword.lower() in sentence.lower() for keyword in keywords)]
        return ' '.join(relevant_sentences[:num_sentences])

    def extract_text_from_pdf(self, pdf_path, start_page = None, end_page = None, skip_lines = 0):
        doc = fitz.open(pdf_path)
        extracted_text = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()

            lines = text.split('\n')
            if skip_lines:
                lines = lines[1:]
            cleaned_text = '\n'.join(lines)
            extracted_text.append(cleaned_text)
        doc.close()
        extracted_text = list(map(str.strip, extracted_text))
        if start_page and end_page:
            return extracted_text[start_page:end_page]
        elif start_page:
            return extracted_text[start_page:]
        elif end_page:
            return extracted_text[:end_page]
        else:
            return extracted_text

    def preload_data(self):
        file_path = 'context.txt'

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted.")
        else:
            print(f"File '{file_path}' does not exist.")
        
        
        file_name = '1.pdf'
        text_by_pages = self.extract_text_from_pdf(file_name, 4)
        full_document = '\n\n'.join(text_by_pages)
        self.append_to_context(full_document)

        file_name = '2.pdf'
        text_by_pages = self.extract_text_from_pdf(file_name, 18, -27, 1)
        full_document = '\n\n'.join(text_by_pages)
        self.append_to_context(full_document)

        file_name = '3.pdf'
        text_by_pages = self.extract_text_from_pdf(file_name, 11, -75, 1)
        full_document = '\n\n'.join(text_by_pages)
        self.append_to_context(full_document)

        file_name = '4.pdf'
        text_by_pages = self.extract_text_from_pdf(file_name)
        full_document = '\n\n'.join(text_by_pages)
        self.append_to_context(full_document)

    def answer_question_model(self, question, context):
        inputs = tokenizer.encode_plus(question, context, return_tensors='pt', add_special_tokens=True)
        input_ids = inputs["input_ids"]

        # Get model output
        model_output = model(**inputs)

        # Extract scores
        answer_start_scores = model_output.start_logits
        answer_end_scores = model_output.end_logits

        answer_start = torch.argmax(answer_start_scores)
        answer_end = torch.argmax(answer_end_scores) + 1

        # Convert tokens to string
        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[0][answer_start:answer_end]))
        
        new_conversation = Chat(
            question = question,
            answer = answer
        )
        session.add(new_conversation)
        session.commit()
            
        return answer

    def answer_question(self, question):
        full_context = self.get_context_from_file('context.txt')
        relevant_context = self.find_relevant_context(question, full_context)
        print("------------------------------------------------")
        print("relevant_context:", relevant_context)
        print("------------------------------------------------")

        answer = self.answer_question_model(question, relevant_context)
        return {"status": True, "answer": answer}
    
    def load_conversation(self, start_index = 1, stop_index = 10):
        # Offset by 9 to start at the 10th record
        # Limit to 11 records (10 to 20 inclusive)
        print("start_index", start_index)
        print("stop_index", stop_index)

        latest_records = session.query(Chat).order_by(desc(Chat.created_date)).offset(start_index).limit(stop_index).all()
        print("latest_records", latest_records)
        return {"status": True, "data": self.obj_to_list(latest_records)}




