import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import asyncio
from typing import Dict, Any
import re
import json
import os

class GraniteModel:
    """IBM Granite 3.3 2B Instruct model for citizen engagement"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = "ibm-granite/granite-3.3-2b-instruct"
        self.fallback_responses = self._load_fallback_responses()
    async def load_model(self):
        """Safely load the IBM Granite model and use fallback on failure."""
        try:
            print("Loading IBM Granite model...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )

            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )

            if self.device == "cpu":
                self.model = self.model.to(self.device)

            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            print(f"✅ Model loaded successfully on {self.device}")

        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None
            self.tokenizer = None

        
    def _load_fallback_responses(self) -> Dict[str, str]:
        """Load fallback responses from JSON file or use built-in responses"""
        try:
            # Try to load from external JSON file
            if os.path.exists("fallback_responses.json"):
                with open("fallback_responses.json", "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Could not load external fallback responses: {e}")
        
        # Return built-in fallback responses
        return self._get_builtin_fallback_responses()
    
    def _get_builtin_fallback_responses(self) -> Dict[str, str]:
        """Built-in comprehensive fallback responses for government services"""
        return {
            "aadhaar": """Aadhaar Card Application Process:

SUMMARY: Aadhaar is a 12-digit unique identification number issued by UIDAI to Indian residents based on biometric and demographic data.

STEP-BY-STEP PROCEDURE:
1. Locate nearest Aadhaar Enrollment Center using UIDAI website
2. Fill enrollment form with accurate details
3. Submit required documents (POI, POA, DOB proof)
4. Provide biometric data (10 fingerprints, iris scan, photograph)
5. Verify details and submit application
6. Collect enrollment slip with EID number
7. Track status online after 60 days

REQUIRED DOCUMENTS:
- Proof of Identity:Passport, PAN card, Voter ID, Driving License, Birth Certificate
- Proof of Address: Passport, Bank statement, Utility bills, Ration card, Property documents
- Date of Birth: Birth certificate, 10th marksheet, Passport, PAN card

PROCESSING TIME & FEES:
- Processing: 60-90 days
- Enrollment: FREE for first time
- Updates: ₹50 (demographic), ₹100 (biometric)

CONTACT INFORMATION:
- Website: uidai.gov.in
- Helpline: 1947
- Email: help@uidai.gov.in""",

            "pan_card": """PAN Card Application Process:

SUMMARY: Permanent Account Number (PAN) is a 10-character alphanumeric identifier issued by Income Tax Department for tax-related transactions.

STEP-BY-STEP PROCEDURE:
1. Visit NSDL/UTIITSL website or authorized centers
2. Fill Form 49A (Indian citizens) or 49AA (foreign citizens)
3. Attach required documents and photographs
4. Pay application fee
5. Submit application online or offline
6. Track application status using acknowledgment number
7. Receive PAN card by post within 15-20 days

REQUIRED DOCUMENTS:
- Identity Proof: Aadhaar, Passport, Voter ID, Driving License
- Address Proof: Aadhaar, Passport, Bank statement, Utility bills
- Date of Birth: Birth certificate, 10th marksheet, Passport
- Photographs: 2 recent passport-size photos

PROCESSING TIME & FEES:
- Processing: 15-20 days
- Normal: ₹107 (online), ₹114 (offline)
- Tatkal: ₹1,020 (online), ₹1,028 (offline)

CONTACT INFORMATION:
- Website: incometaxindia.gov.in
- NSDL: tin-nsdl.com
- UTIITSL: utiitsl.com
- Helpline: 020-27218080""",

            "voter_id": """Voter ID Card Application Process:

SUMMARY: Voter ID (EPIC) is an identity document issued by Election Commission of India to eligible citizens for voting in elections.

STEP-BY-STEP PROCEDURE:
1. Visit National Voters' Service Portal (nvsp.in)
2. Fill online Form 6 for new registration
3. Upload required documents and photograph
4. Submit application online
5. Print acknowledgment receipt
6. Booth Level Officer (BLO) verification
7. Receive Voter ID card within 30 days

REQUIRED DOCUMENTS:
- Age Proof: Birth certificate, 10th marksheet, Passport, Driving License
- Address Proof: Aadhaar, Passport, Bank statement, Utility bills, Ration card
- Photograph: Recent passport-size photo

PROCESSING TIME & FEES:
- Processing: 30 days
- Fees: FREE
- Duplicate card: ₹25

CONTACT INFORMATION:
- Website: nvsp.in
- Helpline: 1950
- Email: complaints@eci.gov.in""",

            "ayushman_bharat": """Ayushman Bharat Pradhan Mantri Jan Arogya Yojana (PM-JAY):

SUMMARY: World's largest health insurance scheme providing ₹5 lakh annual coverage to over 10 crore poor and vulnerable families.

STEP-BY-STEP PROCEDURE:
1. Check eligibility using SECC 2011 database
2. Visit nearest Common Service Center (CSC)
3. Provide Aadhaar number and family details
4. Biometric authentication
5. Generate Ayushman card instantly
6. Use card at empaneled hospitals for cashless treatment

REQUIRED DOCUMENTS:
- Aadhaar Card: Mandatory for all family members
- Ration Card: For family verification
- Mobile Number: For OTP verification

PROCESSING TIME & FEES:
- Card Generation: Instant at CSC
- Fees: Completely FREE
- Coverage: ₹5 lakh per family per year

CONTACT INFORMATION:
- Website: pmjay.gov.in
- Helpline: 14555
- Email: info@nha.gov.in""",

            "grievance_redressal": """Public Grievance Redressal System:

SUMMARY: Centralized platform for citizens to lodge complaints against government departments and track resolution status.

STEP-BY-STEP PROCEDURE:
1. Visit CPGRAMS portal (pgportal.gov.in)
2. Register with mobile number and email
3. Login and click 'Lodge Grievance'
4. Select ministry/department
5. Provide detailed complaint with supporting documents
6. Submit and note registration number
7. Track status regularly using registration number

REQUIRED DOCUMENTS:
- Supporting Evidence: Photos, documents related to grievance
- Identity Proof: Any government ID for verification
- Contact Details: Valid mobile and email

PROCESSING TIME & FEES:
- Processing: 30 days maximum
- Fees: Completely FREE
- Appeal: 30 days if not satisfied

CONTACT INFORMATION:
- Website: pgportal.gov.in
- Helpline: 1100
- Email: grievances@gov.in""",

            "health_schemes": """Major Government Health Schemes:

SUMMARY: Comprehensive healthcare coverage through various government schemes for different categories of citizens.

MAJOR SCHEMES:
1. Ayushman Bharat PM-JAY: ₹5 lakh coverage for poor families
2. CGHS: Central Government Health Scheme for employees
3. ESIC: Employees' State Insurance for organized sector workers
4. PMSBY: Pradhan Mantri Suraksha Bima Yojana - ₹2 lakh accident insurance
5. State Health Schemes: Various state-specific programs

STEP-BY-STEP PROCEDURE:
1. Identify applicable scheme based on eligibility
2. Visit nearest enrollment center
3. Submit required documents
4. Complete registration process
5. Receive health card/policy document
6. Use benefits at empaneled hospitals

REQUIRED DOCUMENTS:
- Aadhaar Card: Mandatory for most schemes
- Income Certificate: For means-tested schemes
- Bank Account: For premium payments
- Employment Proof: For employment-based schemes

PROCESSING TIME & FEES:
- Processing: 7-30 days
- Fees: Varies by scheme (many are free)
- Premium: ₹12-₹330 per year for insurance schemes

CONTACT INFORMATION:
- Ayushman Bharat: 14555
- CGHS: cghs.gov.in
- ESIC: esic.nic.in""",

            "default": """Welcome to Citizen Services Assistant

I can help you with information about various government services and procedures:

POPULAR SERVICES:
• Aadhaar Card (enrollment, updates, corrections)
• PAN Card (new application, corrections, duplicate)
• Voter ID (registration, address change, corrections)
• Driving License (learner's, permanent, renewal)
• Passport (new, renewal, tatkal services)
• Ration Card (new application, additions, corrections)
• Income Tax (ITR filing, TDS, refunds)
• Pension Schemes (old age, widow, disability)
• Birth/Death Certificates
• Marriage Registration

HEALTH & WELFARE:
• Ayushman Bharat (PM-JAY health insurance)
• Government Health Schemes
• Disability Certificates
• Scholarship Applications
• Grievance Redressal System

HOW TO GET HELP:
1. Ask specific questions about any government service
2. I'll provide step-by-step procedures
3. Required documents and eligibility criteria
4. Processing time, fees, and contact information
5. Official websites and helpline numbers

EXAMPLES:

• "How to apply for PAN card?"
• "Documents needed for Ayushman Bharat?"
• "Voter ID address change process"
• "File grievance against government department"

For urgent matters, contact the relevant department directly."""
        }
        
    async def load_model(self):
        """Load the IBM Granite model and tokenizer"""
        try:
            print("Loading IBM Granite model...")
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            # Load model with optimizations
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            
            if self.device == "cpu":
                self.model = self.model.to(self.device)
                
            # Set pad token if not available
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            print(f"Model loaded successfully on {self.device}")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            # Fallback to a simple response system for demo
            self.model = None
            self.tokenizer = None
    
    def create_citizen_prompt(self, user_query: str) -> str:
        """Create an enhanced specialized prompt for citizen engagement"""
        prompt = f"""You are an expert government service assistant with comprehensive knowledge of Indian government procedures, schemes, and services. Provide detailed, accurate, and helpful information to citizens.

Question: {user_query}

Please provide a comprehensive response that includes:

SUMMARY: Brief overview of the service/procedure

STEP-BY-STEP PROCEDURE:
1. Detailed sequential steps
2. Where to go/apply
3. What to do at each stage

REQUIRED DOCUMENTS:
- List all necessary documents
- Mention acceptable alternatives
- Specify original vs photocopy requirements

PROCESSING TIME & FEES:
- Expected processing duration
- Government fees (if applicable)
- Additional charges to consider

CONTACT INFORMATION:
- Official website links
- Helpline numbers
- Email addresses
- Physical office locations (if relevant)

IMPORTANT NOTES:
- Eligibility criteria
- Common mistakes to avoid
- Deadlines or time limits
- Additional tips for smooth processing

Provide specific, actionable information that citizens can immediately use. Be comprehensive but clear.

Response:"""
        return prompt
    
    def create_sentiment_prompt(self, text: str) -> str:
        """Create a prompt for sentiment analysis with enhanced accuracy"""
        prompt = f"""You are an expert sentiment analyzer. Analyze the following text and determine if it expresses a Positive, Negative, or Neutral sentiment.

Rules:
- Positive: satisfaction, praise, gratitude, happiness, approval, success
- Negative: complaints, anger, frustration, disappointment, criticism, failure
- Neutral: factual information, questions, balanced opinions

Text: "{text}"

Think step by step:
1. What emotions does this text express?
2. Are there positive or negative words?
3. What is the overall tone?

Classification (respond with only one word):"""
        return prompt
    
    def _is_response_adequate(self, response: str, user_query: str) -> bool:
        """Check if model response is adequate or needs fallback"""
        if not response:
            return False
            
        response_clean = response.strip()
        
        # Check for minimum length (less than 5 words)
        word_count = len(response_clean.split())
        if word_count < 5:
            return False
            
        # Check for inadequate responses
        inadequate_phrases = [
            "i don't know",
            "i'm not sure",
            "i cannot help",
            "i don't have information",
            "sorry, i can't",
            "i'm unable to",
            "i don't understand",
            "please contact",
            "visit the website",
            "call the helpline"
        ]
        
        response_lower = response_clean.lower()
        for phrase in inadequate_phrases:
            if phrase in response_lower and len(response_clean) < 100:
                return False
                
        # Check for generic/irrelevant responses
        generic_indicators = [
            "as an ai",
            "as a language model",
            "i'm a bot",
            "i'm an assistant",
            "i cannot provide",
            "please consult"
        ]
        
        for indicator in generic_indicators:
            if indicator in response_lower:
                return False
                
        # Check if response contains useful information
        useful_indicators = [
            "step", "procedure", "document", "form", "apply", "visit",
            "required", "process", "fee", "time", "website", "helpline",
            "eligibility", "criteria", "certificate", "registration"
        ]
        
        useful_count = sum(1 for indicator in useful_indicators if indicator in response_lower)
        
        # Response should have at least 2 useful indicators and reasonable length
        return useful_count >= 2 and len(response_clean) >= 50
    
    def _calculate_response_confidence(self, response: str, user_query: str) -> float:
        """Calculate confidence score for model response (0.0 to 1.0)"""
        if not response:
            return 0.0
            
        response_clean = response.strip().lower()
        query_lower = user_query.lower()
        
        confidence = 0.0
        
        # Length factor (longer responses generally better for government services)
        length_score = min(len(response_clean) / 200, 1.0) * 0.2
        confidence += length_score
        
        # Specific information indicators
        specific_indicators = [
            "₹", "rupees", "days", "months", "form", "documents",
            "procedure", "steps", "website", "helpline", "office"
        ]
        specific_count = sum(1 for indicator in specific_indicators if indicator in response_clean)
        specific_score = min(specific_count / 5, 1.0) * 0.3
        confidence += specific_score
        
        # Query relevance (check if response addresses the query)
        query_words = set(query_lower.split())
        response_words = set(response_clean.split())
        relevance_score = len(query_words & response_words) / max(len(query_words), 1) * 0.3
        confidence += relevance_score
        
        # Structure indicators (well-structured responses)
        structure_indicators = ["summary", "procedure", "documents", "fees", "contact"]
        structure_count = sum(1 for indicator in structure_indicators if indicator in response_clean)
        structure_score = min(structure_count / 3, 1.0) * 0.2
        confidence += structure_score
        
        return min(confidence, 1.0)
    
    async def generate_response(self, prompt: str, max_length: int = 512) -> str:
        """Generate response using the Granite model with fallback logic"""
        if self.model is None or self.tokenizer is None:
            # Use fallback when model isn't loaded
            return self._get_fallback_response(prompt)
        
        try:
            # Tokenize input with better settings for Granite
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=2048,
                padding=False
            ).to(self.device)
            
            # Generate response with optimized parameters for Granite
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_length,
                    temperature=0.2,
                    do_sample=True,
                    top_p=0.85,
                    top_k=40,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.2,
                    no_repeat_ngram_size=3,
                    early_stopping=True
                )
            
            # Decode response and clean it
            response = self.tokenizer.decode(
                outputs[0][inputs["input_ids"].shape[1]:],
                skip_special_tokens=True
            ).strip()
            
            # Clean up the response
            response = self._clean_response(response)
            
            # Extract user query from prompt for validation
            user_query = self._extract_query_from_prompt(prompt)
            
            # Check if response is adequate
            if not self._is_response_adequate(response, user_query):
                print("Model response inadequate, using fallback")
                return self._get_fallback_response(prompt)
            
            # Check confidence score
            confidence = self._calculate_response_confidence(response, user_query)
            if confidence < 0.4:  # Confidence threshold
                print(f"Low confidence ({confidence:.2f}), using fallback")
                return self._get_fallback_response(prompt)
            
            return response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return self._get_fallback_response(prompt)
    
    def _extract_query_from_prompt(self, prompt: str) -> str:
        """Extract user query from the prompt"""
        # Look for "Question:" pattern
        if "Question:" in prompt:
            start = prompt.find("Question:") + 9
            end = prompt.find("\n", start)
            if end == -1:
                end = len(prompt)
            return prompt[start:end].strip()
        return prompt
    
    def _clean_response(self, response: str) -> str:
        """Clean and format the model response"""
        if not response:
            return response
            
        # Remove common artifacts and clean up
        response = response.strip()
        
        # Remove repeated phrases or incomplete sentences at the end
        lines = response.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('Question:') and not line.startswith('Text:') and not line.startswith('Classification:'):
                cleaned_lines.append(line)
        
        cleaned_response = '\n'.join(cleaned_lines)
        
        # Remove trailing incomplete sentences
        if cleaned_response.endswith('...') or cleaned_response.endswith('-'):
            sentences = cleaned_response.split('.')
            if len(sentences) > 1:
                cleaned_response = '.'.join(sentences[:-1]) + '.'
        
        return cleaned_response
    
    def _get_fallback_response(self, prompt: str) -> str:
        """Get appropriate fallback response based on query"""
        if "sentiment" in prompt.lower() or "classification:" in prompt.lower():
            return self._analyze_sentiment_fallback(prompt)
        
        # Extract user query from prompt
        user_query = self._extract_query_from_prompt(prompt)
        return self._fallback_response(user_query)
    
    def _fallback_response(self, query: str) -> str:
        """Enhanced fallback responses when model is not available or inadequate"""
        query_lower = query.lower()
        
        # Check for specific service keywords and return appropriate response
        service_keywords = {
            "aadhaar": ["aadhar", "aadhaar", "uid", "unique identification"],
            "pan_card": ["pan", "permanent account", "income tax"],
            "voter_id": ["voter", "election", "epic", "voting"],
            "ayushman_bharat": ["ayushman", "pmjay", "health insurance", "medical"],
            "grievance_redressal": ["grievance", "complaint", "redressal", "cpgrams"],
            "health_schemes": ["health scheme", "medical scheme", "insurance"]
        }
        
        # Find matching service
        for service, keywords in service_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return self.fallback_responses.get(service, self.fallback_responses["default"])
        
        # Check for other services
        if any(word in query_lower for word in ["ration", "pds", "subsidy", "food security"]):
            return """Ration Card Application Process:

SUMMARY: Ration card provides access to subsidized food grains through Public Distribution System (PDS).

STEP-BY-STEP PROCEDURE:
1. Visit local Food & Civil Supplies office
2. Collect application form or download online
3. Fill form with family details
4. Attach required documents
5. Submit application with photographs
6. Pay prescribed fee
7. Collect acknowledgment receipt
8. Verification by inspector
9. Receive ration card within 30 days

REQUIRED DOCUMENTS:
- Address proof (Aadhaar, utility bills, rent agreement)
- Identity proof (Aadhaar, voter ID, passport)
- Income certificate
- Family photograph
- Bank account details

PROCESSING TIME & FEES:
- Processing: 15-30 days
- Fees: ₹15-30 (varies by state)
- APL/BPL classification based on income

CONTACT INFORMATION:
- Local Food & Civil Supplies Department
- State government websites
- Helpline: 1967 (varies by state)"""
        
        elif any(word in query_lower for word in ["pension", "retirement", "elderly", "senior", "old age"]):
            return """Pension Schemes for Citizens:

SUMMARY: Various pension schemes available for different categories of citizens including elderly, widows, and disabled persons.

MAJOR SCHEMES:
1. Old Age Pension:For senior citizens (60+)
2. Widow Pension: For widows below poverty line
3. Disability Pension: For disabled persons
4. National Pension System (NPS): For all citizens

STEP-BY-STEP PROCEDURE:
1. Visit local tehsil/block office
2. Fill application form
3. Submit required documents
4. Income and age verification
5. Medical examination (if required)
6. Approval by competent authority
7. Receive pension in bank account

REQUIRED DOCUMENTS:
- Age proof (birth certificate, school certificate)
- Income certificate
- Aadhaar card
- Bank account details
- Photographs
- Medical certificate (for disability pension)

PROCESSING TIME & FEES:
- Processing: 30-60 days
- Fees: Usually FREE
- Pension amount: ₹200-1000 per month (varies by state)

CONTACT INFORMATION:
- Local Tehsil/Block office
- District Collector office
- State social welfare department"""
        
        elif any(word in query_lower for word in ["license", "driving", "dl", "permit", "vehicle"]):
            return """Driving License Application Process:

SUMMARY: Driving License (DL) is mandatory for driving any motor vehicle on Indian roads, issued by Regional Transport Office (RTO).

STEP-BY-STEP PROCEDURE:
1. Apply online at parivahan.gov.in or visit RTO
2. Fill Form 1 (application for learner's license)
3. Submit documents and pay fees
4. Pass written test to get learner's license
5. Practice driving for minimum 30 days
6. Apply for permanent license (Form 2)
7. Pass practical driving test
8. Receive permanent driving license

REQUIRED DOCUMENTS:
- Form 1 and Form 2
- Age proof (birth certificate, 10th marksheet)
- Address proof (Aadhaar, voter ID, passport)
- Medical certificate (for commercial vehicles)
- Passport-size photographs (4 copies)
- Learner's license (for permanent DL)

PROCESSING TIME & FEES:
- Learner's License: ₹150, same day issuance
- Permanent License: ₹200, 7-15 days
- Smart Card: ₹200 additional
- Validity: 20 years (till age 50), 10 years thereafter

CONTACT INFORMATION:
- Website: parivahan.gov.in
- Local RTO office
- Helpline: Varies by state"""
        
        elif any(word in query_lower for word in ["tax", "income", "itr", "filing", "return"]):
            return """Income Tax Return (ITR) Filing:

SUMMARY:Annual declaration of income and tax computation filed with Income Tax Department by eligible taxpayers.

STEP-BY-STEP PROCEDURE:
1. Gather all tax documents
2. Choose correct ITR form (ITR-1 to ITR-7)
3. Login to e-filing portal
4. Fill ITR form online
5. Verify tax computation
6. Submit return electronically
7. Verify using Aadhaar OTP/EVC/DSC
8. Download acknowledgment

REQUIRED DOCUMENTS:
- PAN card
- Aadhaar card
- Form 16/16A (TDS certificates)
- Bank statements
- Investment proofs (80C, 80D, etc.)
- Capital gains statements
- Business income details (if applicable)

PROCESSING TIME & FEES:
- Filing: Free on income tax portal
- Due dates: July 31 (individuals), September 30 (audited)
- Refund processing: 30-45 days
- Late filing penalty: ₹5,000-10,000

CONTACT INFORMATION:
- Website: incometaxindiaefiling.gov.in
- Helpline: 1800-103-0025
- Email: ito.admin@incometax.gov.in"""
        
        elif any(word in query_lower for word in ["passport", "travel", "document"]):
            return """Passport Application Process:

SUMMARY: Passport is an official travel document issued by Government of India for international travel.

STEP-BY-STEP PROCEDURE:
1. Register on passportindia.gov.in
2. Fill online application form
3. Pay fee online
4. Book appointment at PSK/POPSK
5. Visit center with original documents
6. Document verification and biometric capture
7. Police verification (if required)
8. Passport printing and dispatch

REQUIRED DOCUMENTS:
- Online application form
- Birth certificate
- Address proof (Aadhaar, voter ID, utility bills)
- Identity proof (Aadhaar, PAN, voter ID)
- Photographs (2 recent passport-size)
- Annexure H (if applicable)

PROCESSING TIME & FEES:
- Normal: 30-45 days
  - 36 pages: ₹1,500
  - 60 pages: ₹2,000
- Tatkal: 3-7 days
  - Additional ₹2,000 over normal fees

CONTACT INFORMATION:
- Website: passportindia.gov.in
- Helpline: 1800-258-1800
- Email: support@passportindia.gov.in"""
        
        elif any(word in query_lower for word in ["birth", "death", "certificate", "registration"]):
            return """Birth/Death Certificate Process:

SUMMARY: Legal documents proving birth/death, mandatory for various government services and legal purposes.

STEP-BY-STEP PROCEDURE:
1. Visit Registrar office or apply online
2. Fill registration form
3. Submit required documents
4. Pay prescribed fee
5. Collect receipt/acknowledgment
6. Receive certificate after verification

REQUIRED DOCUMENTS:
For Birth Certificate:
- Hospital discharge summary
- Parents' identity and address proofs
- Marriage certificate of parents

For Death Certificate:
- Medical certificate/Post-mortem report
- Identity proof of deceased
- Affidavit by relative

PROCESSING TIME & FEES:
- Registration: Within 21 days (birth), 24 hours (death)
- Late registration: Additional fees apply
- Certificate fees: ₹10-50
- Processing: Same day to 7 days

CONTACT INFORMATION:
- Local Registrar office
- Online: crsorgi.gov.in
- Municipal corporation offices"""
        
        # Return default response if no specific service matches
        return self.fallback_responses["default"]
    
    def _analyze_sentiment_fallback(self, prompt: str) -> str:
        """Enhanced sentiment analysis fallback with better accuracy"""
        # Extract the text being analyzed
        text = ""
        if 'text: "' in prompt.lower():
            start = prompt.lower().find('text: "') + 7
            end = prompt.find('"', start)
            if end > start:
                text = prompt[start:end]
        
        if not text:
            return "Neutral"
        
        return self._enhanced_keyword_sentiment(text)
    
    def _enhanced_keyword_sentiment(self, text: str) -> str:
        """Enhanced keyword-based sentiment analysis"""
        text_lower = text.lower()
        
        # Strong positive indicators
        strong_positive = [
            "excellent", "outstanding", "fantastic", "amazing", "wonderful", 
            "brilliant", "superb", "perfect", "love", "great job", "well done",
            "highly satisfied", "extremely happy", "very good", "impressed"
        ]
        
        # Positive indicators
        positive_words = [
            "good", "great", "nice", "satisfied", "happy", "pleased", 
            "thank", "grateful", "appreciate", "helpful", "efficient", 
            "quick", "easy", "smooth", "useful", "working", "solved"
        ]
        
        # Strong negative indicators
        strong_negative = [
            "terrible", "horrible", "awful", "disgusting", "pathetic",
            "worst", "hate", "extremely bad", "very poor", "completely useless",
            "totally disappointed", "absolutely terrible", "unacceptable"
        ]
        
        # Negative indicators
        negative_words = [
            "bad", "poor", "disappointed", "frustrated", "angry", "upset",
            "difficult", "slow", "complicated", "confusing", "problem",
            "issue", "error", "failed", "broken", "not working", "useless"
        ]
        
        # Neutral indicators
        neutral_words = [
            "okay", "fine", "average", "normal", "standard", "regular",
            "question", "how", "what", "when", "where", "information"
        ]
        
        # Count occurrences
        strong_pos_count = sum(1 for word in strong_positive if word in text_lower)
        pos_count = sum(1 for word in positive_words if word in text_lower)
        strong_neg_count = sum(1 for word in strong_negative if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        neutral_count = sum(1 for word in neutral_words if word in text_lower)
        
        # Weight the scores
        positive_score = (strong_pos_count * 3) + (pos_count * 1)
        negative_score = (strong_neg_count * 3) + (neg_count * 1)
        
        # Determine sentiment with better logic
        if positive_score > negative_score and positive_score > 0:
            return "Positive"
        elif negative_score > positive_score and negative_score > 0:
            return "Negative"
        elif neutral_count > 0 and positive_score == negative_score:
            return "Neutral"
        else:
            # Check for question patterns
            if any(word in text_lower for word in ["?", "how", "what", "when", "where", "why"]):
                return "Neutral"
            # Default to neutral for ambiguous cases
            return "Neutral"
    
    async def analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of given text with improved accuracy"""
        prompt = self.create_sentiment_prompt(text)
        response = await self.generate_response(prompt, max_length=30)
        
        # Extract and validate sentiment from response
        sentiment = self._extract_sentiment(response, text)
        return sentiment
    
    def _extract_sentiment(self, model_response: str, original_text: str) -> str:
        """Extract sentiment from model response with improved accuracy"""
        # Clean the response
        response = model_response.strip().upper()
        
        # Look for sentiment keywords in the response
        if "POSITIVE" in response:
            return "Positive"
        elif "NEGATIVE" in response:
            return "Negative"
        elif "NEUTRAL" in response:
            return "Neutral"
        
        # Use enhanced keyword-based analysis as fallback
        return self._enhanced_keyword_sentiment(original_text)
    
    async def chat_response(self, user_query: str) -> str:
        """Generate chat response for citizen queries with enhanced fallback logic"""
        prompt = self.create_citizen_prompt(user_query)
        response = await self.generate_response(prompt, max_length=400)
        
        # Additional validation for chat responses
        if not self._is_response_adequate(response, user_query):
            print("Chat response inadequate, using enhanced fallback")
            response = self._fallback_response(user_query)
        
        return response
    
    def save_fallback_responses_template(self):
        """Save fallback responses to JSON file for easy editing"""
        try:
            with open("fallback_responses.json", "w", encoding="utf-8") as f:
                json.dump(self.fallback_responses, f, indent=2, ensure_ascii=False)
            print("Fallback responses saved to fallback_responses.json")
        except Exception as e:
            print(f"Error saving fallback responses: {e}")
    
    def get_service_categories(self) -> Dict[str, list]:
        """Get available service categories for UI/frontend"""
        return {
            "Identity Documents": [
                "Aadhaar Card", "PAN Card", "Voter ID", "Passport", "Driving License"
            ],
            "Certificates": [
                "Birth Certificate", "Death Certificate", "Income Certificate", "Caste Certificate"
            ],
            "Social Welfare": [
                "Ration Card", "Pension Schemes", "Scholarship", "Disability Certificate"
            ],
            "Health Services": [
                "Ayushman Bharat", "Health Insurance", "Medical Certificate"
            ],
            "Tax Services": [
                "Income Tax Filing", "GST Registration", "TDS Services"
            ],
            "Grievance & Support": [
                "Public Grievance", "RTI Application", "Consumer Complaints"
            ]
        }
    
    def get_quick_help(self, category: str = None) -> str:
        """Get quick help text for specific category or general help"""
        if category and category.lower() in self.fallback_responses:
            return self.fallback_responses[category.lower()]
        
        return """Quick Help - Popular Services:

🔸 "How to apply for Aadhaar card?"
🔸 "PAN card application process"
🔸 "Voter ID registration steps"
🔸 "Ayushman Bharat eligibility"
🔸 "Driving license requirements"
🔸 "File income tax return"
🔸 "Grievance redressal process"

Tips for Better Responses:
• Be specific about the service you need
• Mention if you need documents, fees, or timelines
• Ask about eligibility criteria if unsure
• Request step-by-step procedures for complex processes

Emergency Contacts:
• Police: 100 • Fire: 101 • Ambulance: 108
• Women Helpline: 1091 • Child Helpline: 1098"""