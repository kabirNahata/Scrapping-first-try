import requests
from pyquery import PyQuery as pq
import json
import time
import re
import random
import os
import datetime

current_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H")
OUTPUT_FILENAME = f"extracted_dataset_{current_timestamp}.json"

# User agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183"
]

# Base URL for colleges
BASE_URL = "https://collegedunia.com/"

URL = "https://collegedunia.com/university/25740-iim-shillong-indian-institute-of-management-shillong"

# Final extracted data dictionary
ALL_EXTRACTED_DATA = {}

def extract_data_from_html(html_text):
    """Extract college data from HTML content"""
    src = pq(html_text)
    jsonData = src.find('script:last')
    final = pq(jsonData).text()
    
    try:
        data_dict = json.loads(final)
    except json.JSONDecodeError:
        return None
    
    # with open("newfile.json", "w", encoding='utf-8') as f:
    #     json.dump(data_dict, f, ensure_ascii=False, indent=4)
    # exit()
    # Extract required parameters
    extracted_data = {}
    
    # Extract college name
    try:
        college_name = data_dict['props']['initialProps']['pageProps']['data']['college_name']
        extracted_data['college_name'] = college_name
    except (KeyError, IndexError, TypeError):
        extracted_data['college_name'] = None
    
    # Extract stream details
    streams_info = []
    try:
        streams = data_dict['props']['initialProps']['pageProps']['data']['streamGoalData']['streams']
        for stream in streams:
            stream_name = stream.get('stream', '')
            slugs = stream.get('slugs', [])
            slug = slugs[0].get('slug', '') if slugs else ''
            streams_info.append({
                'stream_name': stream_name,
                'slug': slug
            })
    except (KeyError, TypeError):
        pass
    extracted_data['streams'] = streams_info
    
    # Extract website, phone, college_type
    try:
        basic_info = data_dict['props']['initialProps']['pageProps']['data']['basic_info']
        website = basic_info.get('website', '')
        phone = basic_info.get('mobile', [])
        college_type = basic_info.get('type_of_college', '')
        extracted_data['website'] = website
        extracted_data['phone'] = phone
        extracted_data['college_type'] = college_type
    except (KeyError, TypeError):
        extracted_data['website'] = ''
        extracted_data['phone'] = []
        extracted_data['college_type'] = ''
    
    # Initialize rating fields
    extracted_data['email'] = ''
    extracted_data['rating_value'] = ''
    extracted_data['review_count'] = ''
    extracted_data['worst_rating'] = ''
    extracted_data['best_rating'] = ''
    extracted_data['positive_notes'] = ''
    
    # Extract email and rating details from schema
    try:
        schema_json_str = data_dict['props']['initialProps']['pageProps']['data']['schemaJsonLd']['2']
        schema_json_str3 = data_dict['props']['initialProps']['pageProps']['data']['schemaJsonLd']['3']
        try:
            # print(schema_json_str)
            # Try to parse the JSON string
            schema_data = json.loads(schema_json_str)
            schema_data3 = json.loads(schema_json_str3)

            # print(schema_data)
            # print(extracted_data["phone"])

            # print(extracted_data)
            # Extract email
            if "email" in schema_data.keys():
                extracted_data['email'] = schema_data.get('email', '')
            else:
                schema_data3 = json.loads(schema_json_str3)
                extracted_data['email'] = schema_data3.get('email', '')


            # Extract positive notes
                extracted_data['positive_notes'] = schema_data.get('positiveNotes', '')
            
            # Extract rating details
            if "aggregateRating" in schema_data.keys():
                aggregate_rating = schema_data.get('aggregateRating', {})
                if isinstance(aggregate_rating, dict):
                    extracted_data['rating_value'] = aggregate_rating.get('ratingValue', '')
                    extracted_data['review_count'] = aggregate_rating.get('reviewCount', '')
                    extracted_data['worst_rating'] = aggregate_rating.get('worstRating', '')
                    extracted_data['best_rating'] = aggregate_rating.get('bestRating', '')
                if len(extracted_data['phone'])==0:
                    extracted_data["phone"]= schema_data.get('telephone', '')
            else:
                aggregate_rating = schema_data3.get('aggregateRating', {})
                if isinstance(aggregate_rating, dict):
                    extracted_data['rating_value'] = aggregate_rating.get('ratingValue', '')
                    extracted_data['review_count'] = aggregate_rating.get('reviewCount', '')
                    extracted_data['worst_rating'] = aggregate_rating.get('worstRating', '')
                    extracted_data['best_rating'] = aggregate_rating.get('bestRating', '') 
                if len(extracted_data['phone']) == 0:
                        extracted_data["phone"]= schema_data3.get('telephone', '')
            # print(extracted_data)
                       

        
        except json.JSONDecodeError:
            # Fallback to regex if JSON parsing fails
            
            # Email regex
            email_match = re.search(r'"email":"([^"]+)"', schema_json_str)
            if email_match:
                extracted_data['email'] = email_match.group(1)
            
            # Positive notes regex
            positive_notes_match = re.search(r'"positiveNotes":"([^"]+)"', schema_json_str)
            if positive_notes_match:
                extracted_data['positive_notes'] = positive_notes_match.group(1)
            
            # Rating regexes
            rating_value_match = re.search(r'"ratingValue":\s*"?([0-9.]+)"?', schema_json_str)
            if rating_value_match:
                extracted_data['rating_value'] = rating_value_match.group(1)
            
            review_count_match = re.search(r'"reviewCount":\s*"?([0-9]+)"?', schema_json_str)
            if review_count_match:
                extracted_data['review_count'] = review_count_match.group(1)
            
            worst_rating_match = re.search(r'"worstRating":\s*"?([0-9.]+)"?', schema_json_str)
            if worst_rating_match:
                extracted_data['worst_rating'] = worst_rating_match.group(1)
            
            best_rating_match = re.search(r'"bestRating":\s*"?([0-9.]+)"?', schema_json_str)
            if best_rating_match:
                extracted_data['best_rating'] = best_rating_match.group(1)
    
    except (KeyError, TypeError):
        pass
    
    # Extract course fees
    # print("cccccc"*10)
    courses_info = []
    try:
        full_time_courses = data_dict['props']['initialProps']['pageProps']['data']['new_compare_courses']['full_time']
        # print(full_time_courses)
        for course in full_time_courses:
            stream_list = course.get('stream', [])

            if len(stream_list) > 0:
            
                for stream_item in stream_list:
                    course_name = stream_item.get('name', '')
                    if isinstance(stream_item.get('total_current_fee'), dict):
                        fee_amount = stream_item.get('total_current_fee', {}).get('general', {}).get('amount', '')
                    
                    courses_info.append({
                        'course_name': course_name,
                        'fee_amount': fee_amount
                    })
            else:
                print("Stream not found")
    except (KeyError, TypeError):
        pass
    
    extracted_data['courses'] = courses_info
    # print(courses_info)
    # print("......"*10)
    # print(f"Course info {extracted_data}")

    # Extract cutoff details
    cutoffs_info = []
    try:
        course_data = data_dict['props']['initialProps']['pageProps']['data']['course_data']
        
        courses_list = course_data['courses']
        if isinstance(course_data['cutoff'], dict):
            cutoff_dict = course_data['cutoff']
        
        # Create course ID to name mapping
        id_to_name = {}
        for course in courses_list:
            # print(course)
            try:
                id_to_name[course['id']] = course['name']
            except (KeyError, TypeError):
                continue
        
        if isinstance(course_data['cutoff'], dict):
            for course_id, cutoff_list in cutoff_dict.items():
                try:
                    course_name = id_to_name.get(int(course_id), 'Unknown Course')
                    for cutoff in cutoff_list:
                        cutoffs_info.append({
                            'course_name': course_name,
                            'cutoff': cutoff.get('cutoff', ''),
                            'cutoff_type': cutoff.get('cutoff_type', ''),
                            'exam': cutoff.get('exam', '')
                        })
                except (ValueError, TypeError):
                    continue
        
        # Fallback to stream cutoffs if needed
        if not cutoffs_info:
            try:
                full_time_courses = data_dict['props']['initialProps']['pageProps']['data']['new_compare_courses']['full_time']
                if isinstance(full_time_courses, list):
                    for course in full_time_courses:
                        stream_list = course.get('stream', [])
                        for stream_item in stream_list:
                            cutoff_data = stream_item.get('cutoff', [])
                            if cutoff_data and isinstance(cutoff_data, dict):
                                course_name = stream_item.get('name', '')
                                cutoffs_info.append({
                                    'course_name': course_name,
                                    'cutoff': cutoff_data.get('cutoff', ''),
                                    'cutoff_type': cutoff_data.get('cutoff_type', ''),
                                    'exam': cutoff_data.get('exam', '')
                                })
            except (KeyError, TypeError):
                pass
    except (KeyError, TypeError):
        pass
    extracted_data['cutoffs'] = cutoffs_info
    
    return extracted_data

def main():
    user_agent = random.choice(USER_AGENTS)
    time.sleep(5)  # Sleep before making next batch of requests

    # Configure headers
    HEADERS = {
            "User-Agent": user_agent,
            "Accept": "application/json"
            }

    response = requests.get(URL, headers=HEADERS, timeout=30)

    if response.status_code == 200:
        extracted_data = extract_data_from_html(response.text)

    print(extracted_data)

        
if __name__ == "__main__":
    main()
    