import json
from transformers import pipeline
import torch

class NlpProcessor:
    """
    A class to handle loading the NLP model and processing meeting transcripts.
    It uses the Hugging Face pipeline for easy model inference.
    """
    def __init__(self, model_name="meta-llama/Llama-3-8B-Instruct"):
        """
        Initializes the processor with a specific model name.

        Args:
            model_name (str): The identifier of the Hugging Face model to use.
        """
        self.model_name = model_name
        self.pipe = None

    def load_model(self):
        """
        Downloads and loads the pre-trained model and tokenizer into a pipeline.
        """
        try:
            print(f"Loading model: {self.model_name}...")
            self.pipe = pipeline(
                "text-generation",
                model=self.model_name,
                model_kwargs={"torch_dtype": torch.bfloat16},
                device_map="auto"
            )
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def process_transcript(self, transcript_text: str) -> dict:
        """
        Takes a raw meeting transcript and uses the loaded LLM to extract a
        summary and blockers in a structured JSON format.

        Args:
            transcript_text (str): The full text of the meeting transcript.

        Returns:
            dict: A dictionary containing the summary, blockers, and action items.
                  Returns a default error structure if processing fails.
        """
        if not self.pipe:
            print("Error: Model is not loaded. Please call load_model() first.")
            return self._get_error_structure("Model not loaded")

        prompt = f"""
        You are an expert AI assistant specializing in analyzing Scrum meeting transcripts.
        Your task is to process the following meeting transcript and extract key information.

        Please provide the output in a clean, valid JSON format with the following keys:
        - "summary": A concise, one-paragraph summary of the meeting.
        - "blockers": A list of strings, where each string is a potential blocker or impediment mentioned. If none, provide an empty list.
    

        Here is an example of the desired JSON output structure:
        ```json
        {{
            "summary": "The team discussed progress on the user authentication feature. Alice is nearly done with the front-end, but Bob is blocked on the database migration. An action item was created for Carol to grant Bob the necessary permissions.",
            "blockers": [
                "Bob is blocked on the database migration due to lack of permissions."
            ]
        }}
        ```

        Here is the transcript to analyze:
        ---
        {transcript_text}
        ---

        Now, provide the structured JSON output for the transcript above:
        """

        messages = [
            {"role": "system", "content": "You are a helpful assistant that provides structured JSON output."},
            {"role": "user", "content": prompt},
        ]
        
        generated_text = ""
        try:
            print("Generating analysis from transcript...")
            outputs = self.pipe(
                messages,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.6,
                top_p=0.9,
            )
            generated_text = outputs[0]["generated_text"][-1]['content']

            print("Parsing model output...")
            # Find the start and end of the JSON block to be safe
            json_start = generated_text.find('{')
            json_end = generated_text.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_string = generated_text[json_start:json_end]
                parsed_output = json.loads(json_string)
                
                # Basic validation to ensure the keys we need are present
                if all(key in parsed_output for key in ["summary", "blockers", "action_items"]):
                    return parsed_output
                else:
                    print("Error: Model output was missing required keys.")
                    return self._get_error_structure("Model output missing keys", generated_text)
            else:
                print("Error: Could not find a valid JSON object in the model's response.")
                return self._get_error_structure("Invalid JSON in response", generated_text)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from model output: {e}")
            return self._get_error_structure("JSON Decode Error", generated_text)
        except Exception as e:
            print(f"An unexpected error occurred during NLP processing: {e}")
            return self._get_error_structure(str(e))

    def _get_error_structure(self, error_message: str, raw_output: str = "") -> dict:
        """A helper function to return a standardized error dictionary."""
        return {
            "summary": f"Error: Could not process transcript. Reason: {error_message}",
            "blockers": [],
            "action_items": [],
            "raw_model_output": raw_output
        }
